from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

SECRET = "toy_demo_secret_key"


def _digest_instance(instance: Dict[str, Any]) -> str:
    payload = json.dumps(instance, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _sign_digest(digest: str) -> str:
    return hashlib.sha256((digest + SECRET).encode("utf-8")).hexdigest()


def generate_certificate(instance: Dict[str, Any], reason: str) -> Dict[str, Any]:
    digest = _digest_instance(instance)
    signature = _sign_digest(digest)
    return {
        "claim": "P(x)=1",
        "instance_digest": digest,
        "metadata": {"reason": reason},
        "signature": signature,
    }


def verify_certificate(instance: Dict[str, Any], certificate: Dict[str, Any]) -> bool:
    digest = _digest_instance(instance)
    expected_signature = _sign_digest(digest)
    return (
        certificate.get("claim") == "P(x)=1"
        and certificate.get("instance_digest") == digest
        and certificate.get("signature") == expected_signature
    )
