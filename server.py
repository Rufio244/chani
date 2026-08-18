# server.py — FastAPI token issuer + JWKS + protected endpoint + revocation + introspection
from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
import os, time, uuid, hmac, json, hashlib
import jwt  # PyJWT
from jwt import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError
from dotenv import load_dotenv
from db import get_conn, init_db, add_issued_token, revoke_jti, is_revoked, get_issued
from utils.jwk import public_pem_to_jwk

# โหลด environment
load_dotenv()

AUTH_MODE = os.environ.get("AUTH_MODE", "RS256").upper()  # RS256 or HS256
PRIVATE_KEY_PATH = os.environ.get("PRIVATE_KEY_PATH", "private.pem")
PUBLIC_KEY_PATH = os.environ.get("PUBLIC_KEY_PATH", "public.pem")
SECRET_KEY = os.environ.get("SECRET_KEY", "replace-with-a-strong-secret")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "admin-secret-example")
DATABASE_PATH = os.environ.get("DATABASE_PATH", "tokens.db")

# ตัวอย่าง BIO_DATA (นำมาจากของคุณ)
BIO_DATA = {
    "full_name_th": "นายธันวา ภูปิงบุตร",
    "full_name_en": "Thanva Phupingbut",
    "alias": "Rufio Dinoto",
    "national_id": "1529900399939",
    "nationality": "American",
    "linkedin_profile": "https://www.linkedin.com/in/genaithanva?trk=contact-info",
    "founder_of": [
        "GENAI",
        "STW (ETF)",
        "TGN (Startup)",
        "TPS Global",
        "TPS Group"
    ],
    "contact": {
        "email": "Thanva04122532@gmail.com",
        "phone_line_whatsapp": "+66 82 372 7103"
    }
}

# โหลดคีย์สำหรับ RS256 ถ้าตั้งค่าไว้
PRIVATE_KEY_PEM = None
PUBLIC_KEY_PEM = None
JWKS_CACHE = None
JWKS_KID = None

if AUTH_MODE == "RS256":
    try:
        with open(PRIVATE_KEY_PATH, "rb") as f:
            PRIVATE_KEY_PEM = f.read()
        with open(PUBLIC_KEY_PATH, "rb") as f:
            PUBLIC_KEY_PEM = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to load RSA keys: {e}")

    # compute kid and JWKS
    from cryptography.hazmat.primitives import serialization
    pub = serialization.load_pem_public_key(PUBLIC_KEY_PEM)
    der = pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    JWKS_KID = hashlib.sha256(der).hexdigest()
    jwk = public_pem_to_jwk(PUBLIC_KEY_PEM, kid=JWKS_KID)
    JWKS_CACHE = {"keys": [jwk]}

app = FastAPI(title="Token Issuer (RS256/HS256) with JWKS, Revocation & Introspection")

# DB init
conn = get_conn(DATABASE_PATH)
init_db(conn)

class TokenRequest(BaseModel):
    user_id: str = None
    capabilities: list | None = None
    ttl_seconds: int = 3600
    include_bio: bool = True

def is_admin(token_header: str) -> bool:
    if not token_header:
        return False
    return hmac.compare_digest(token_header, ADMIN_TOKEN)

@app.get("/.well-known/jwks.json")
async def jwks():
    if AUTH_MODE != "RS256":
        raise HTTPException(status_code=404, detail="JWKS not available in HS256 mode")
    return JWKS_CACHE

@app.post("/token")
async def issue_token(req: TokenRequest, x_admin_token: str = Header(None)):
    if not is_admin(x_admin_token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin token")
    now = int(time.time())
    jti = str(uuid.uuid4())
    payload = {
        "iss": "https://auth.example.local",
        "sub": req.user_id or BIO_DATA.get("national_id"),
        "capabilities": req.capabilities or ["unlock_feature"],
        "iat": now,
        "exp": now + int(req.ttl_seconds),
        "jti": jti
    }
    # avoid embedding full BIO; include a hash for reference
    if req.include_bio:
        payload["bio_hash"] = hashlib.sha256(json.dumps(BIO_DATA, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    if AUTH_MODE == "RS256":
        headers = {"kid": JWKS_KID}
        token = jwt.encode(payload, PRIVATE_KEY_PEM, algorithm="RS256", headers=headers)
    else:
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    add_issued_token(conn, jti, payload["sub"], payload["iat"], payload["exp"])
    return {"token": token, "payload": payload}

def extract_bearer(auth_header: str):
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None

def decode_token(token: str, verify_exp=True):
    try:
        if AUTH_MODE == "RS256":
            key = PUBLIC_KEY_PEM
            algorithms = ["RS256"]
        else:
            key = SECRET_KEY
            algorithms = ["HS256"]
        claims = jwt.decode(token, key, algorithms=algorithms, options={"require": ["exp", "iat", "sub"], "verify_exp": verify_exp})
        return claims
    except ExpiredSignatureError:
        raise
    except InvalidSignatureError:
        raise
    except InvalidTokenError as e:
        raise

@app.get("/protected")
async def protected_endpoint(request: Request, authorization: str = Header(None), required_capability: str = "unlock_feature"):
    token = extract_bearer(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    try:
        claims = decode_token(token, verify_exp=True)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    jti = claims.get("jti")
    if not jti:
        raise HTTPException(status_code=401, detail="Token missing jti")
    if is_revoked(conn, jti):
        raise HTTPException(status_code=401, detail="Token revoked")
    caps = claims.get("capabilities", [])
    if required_capability not in caps:
        raise HTTPException(status_code=403, detail="Forbidden: capability required")
    return {
        "status": "ok",
        "message": f"Access granted for capability '{required_capability}'",
        "sub": claims.get("sub"),
        "jti": jti,
        "bio_in_claim": bool(claims.get("bio_hash"))
    }

class RevokeRequest(BaseModel):
    jti: str = None
    token: str = None  # ถ้าใส่ token จะดึง jti ออกมาเอง

@app.post("/revoke")
async def revoke_token(req: RevokeRequest, x_admin_token: str = Header(None)):
    if not is_admin(x_admin_token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin token")
    jti = req.jti
    if not jti and req.token:
        try:
            claims = decode_token(req.token, verify_exp=False)
            jti = claims.get("jti")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid token provided")
    if not jti:
        raise HTTPException(status_code=400, detail="jti or token required")
    revoke_jti(conn, jti)
    return {"revoked": jti}

class IntrospectRequest(BaseModel):
    token: str

@app.post("/introspect")
async def introspect(req: IntrospectRequest):
    token = req.token
    try:
        claims = decode_token(token, verify_exp=False)
    except InvalidTokenError:
        return {"active": False}
    jti = claims.get("jti")
    if not jti:
        return {"active": False}
    revoked = is_revoked(conn, jti)
    exp = claims.get("exp", 0)
    now = int(time.time())
    active = (not revoked) and (exp > now)
    return {"active": active, "claims": claims, "revoked": revoked}
