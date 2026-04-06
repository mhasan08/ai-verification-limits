from __future__ import annotations

import argparse
import json
from pathlib import Path

from .encoding import build_instance
from .policy import check_policy
from .certificate import generate_certificate, verify_certificate
from .complexity import estimate_complexity
from .verifier import verify_without_certificate


def load_instance(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Toy demo for policy verification vs proof-carrying verification."
    )
    parser.add_argument(
        "--example",
        type=str,
        required=True,
        help="Path to example JSON file containing z, y, and Pi.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="certificate",
        choices=["certificate", "no_certificate"],
        help="Verification mode: certificate-based or direct verification.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print encoded instance JSON.",
    )
    args = parser.parse_args()

    example_path = Path(args.example)
    if not example_path.exists():
        raise FileNotFoundError(f"Example file not found: {example_path}")

    instance = load_instance(str(example_path))

    instance_obj = build_instance(
        z=instance["z"],
        y=instance["y"],
        policy=instance["Pi"],
    )
    encoded = instance_obj.to_canonical_json()
    complexity = estimate_complexity(encoded)

    compliant, reason = check_policy(instance)

    certificate = None
    if compliant and args.mode == "certificate":
        certificate = generate_certificate(instance, reason=reason)

    print("=== Encoded Instance ===")
    if args.pretty:
        parsed = json.loads(encoded)
        print(json.dumps(parsed, indent=2, sort_keys=True))
    else:
        print(encoded)

    print("\n=== Policy Check ===")
    print(f"Compliant: {compliant}")
    print(f"Reason:    {reason}")

    print("\n=== Complexity Estimate (compression proxy) ===")
    print(f"raw_bytes:  {complexity['raw_bytes']}")
    print(f"zlib_bytes: {complexity['zlib_bytes']}")
    print(f"gzip_bytes: {complexity['gzip_bytes']}")
    print(f"lzma_bytes: {complexity['lzma_bytes']}")

    if certificate is not None:
        print("\n=== Certificate ===")
        print(json.dumps(certificate, indent=2, sort_keys=True))

    print("\n=== Formal Verifier Outcome ===")
    if args.mode == "certificate":
        if certificate is None:
            print("Accepted: False")
            print("Mode:     certificate")
            print("Reason:   No certificate provided")
        else:
            valid = verify_certificate(instance, certificate)
            print(f"Accepted: {valid}")
            print("Mode:     certificate")
            if valid:
                print("Reason:   Certificate validated successfully")
            else:
                print("Reason:   Invalid certificate")
    else:
        accepted, verifier_reason = verify_without_certificate(instance, complexity)
        print(f"Accepted: {accepted}")
        print("Mode:     direct verification")
        print(f"Reason:   {verifier_reason}")


if __name__ == "__main__":
    main()
