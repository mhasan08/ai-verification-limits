from __future__ import annotations

from typing import Any, Dict, Tuple

from .policy import check_policy

MAX_COMPLEXITY_BYTES = 170  # simulate verifier limitation


def verify_without_certificate(instance: Dict[str, Any], complexity_estimate: Dict[str, int]) -> Tuple[bool, str]:
    """
    Simulates a limited verifier that cannot certify high-complexity instances.
    """
    if complexity_estimate["zlib_bytes"] > MAX_COMPLEXITY_BYTES:
        return False, "Verifier unable to certify: instance too complex"

    compliant, reason = check_policy(instance)
    return compliant, reason
