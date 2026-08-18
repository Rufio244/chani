# Verifier helper for FastAPI services (uses JWKS)
import json, requests, jwt
from cachetools import TTLCache
from jwt import InvalidTokenError

JWKS_URL = "https://auth.example.local/.well-known/jwks.json"
JWKS_CACHE = TTLCache(maxsize=2, ttl=300)

def fetch_jwks():
    if "jwks" in JWKS_CACHE:
        return JWKS_CACHE["jwks"]
    r = requests.get(JWKS_URL, timeout=5)
    r.raise_for_status()
    jwks = r.json()
    JWKS_CACHE["jwks"] = jwks
    return jwks

def get_public_key_for_kid(kid: str):
    jwks = fetch_jwks()
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            from jwt.algorithms import RSAAlgorithm
            return RSAAlgorithm.from_jwk(json.dumps(key))
    raise ValueError("kid not found")

def verify_token(token, expected_issuer, expected_audience, required_capability=None, introspect_url=None):
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")
    if not kid:
        raise InvalidTokenError("token missing kid")
    key = get_public_key_for_kid(kid)
    claims = jwt.decode(token, key=key, algorithms=["RS256"], audience=expected_audience, issuer=expected_issuer)
    if required_capability:
        caps = claims.get("capabilities", [])
        if required_capability not in caps:
            raise PermissionError("capability required")
    if introspect_url:
        r = requests.post(introspect_url, json={"token": token}, timeout=5)
        if r.status_code != 200 or not r.json().get("active", False):
            raise PermissionError("token inactive or revoked")
    return claims
