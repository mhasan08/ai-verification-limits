from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class EncodedInstance:
    """Represents x = <z, y, Pi> in a simple structured form."""

    z: Dict[str, Any]
    y: Dict[str, Any]
    policy: Dict[str, Any]

    def to_payload(self) -> Dict[str, Any]:
        return {"z": self.z, "y": self.y, "Pi": self.policy}

    def to_canonical_json(self) -> str:
        return json.dumps(self.to_payload(), sort_keys=True, separators=(",", ":"))

    def to_bytes(self) -> bytes:
        return self.to_canonical_json().encode("utf-8")

    def digest(self) -> str:
        return hashlib.sha256(self.to_bytes()).hexdigest()


def build_instance(z: Dict[str, Any], y: Dict[str, Any], policy: Dict[str, Any]) -> EncodedInstance:
    return EncodedInstance(z=z, y=y, policy=policy)
