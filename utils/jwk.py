# แปลง RSA public PEM -> JWK (minimal fields used for RS256 verification)
import base64
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def _b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def public_pem_to_jwk(public_pem: bytes, kid: str = None):
    pub = serialization.load_pem_public_key(public_pem)
    if not isinstance(pub, rsa.RSAPublicKey):
        raise ValueError("Only RSA public keys supported for JWK conversion")
    numbers = pub.public_numbers()
    n = numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")
    e = numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")
    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "n": _b64u(n),
        "e": _b64u(e),
    }
    if kid:
        jwk["kid"] = kid
    else:
        der = pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        jwk["kid"] = hashlib.sha256(der).hexdigest()
    return jwk
