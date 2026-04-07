# AI Policy Verification: Limits and Proof-Carrying Demo

## 📄 Paper
Paper Title: Incompleteness of AI Safety Verification via Kolmogorov Complexity

Paper Link: https://arxiv.org/abs/2604.04876

This repository provides a minimal, executable demonstration of the distinction between:

- **Truth**: whether a policy-compliance predicate $(P(x))$ actually holds, and  
- **Certifiability**: whether a fixed verifier can certify that fact.

---

## 🧠 Core Idea
AI interaction is modeled as: \[$x$ = $\langle$ $z$, $y$, $\Pi$ $\rangle$\] 

- $z$: environment (sensor inputs, scene context)  
- $y$: system output (action, trajectory)  
- $\Pi$: policy (e.g., collision avoidance, stopping constraints)

The predicate $P(x)$ checks whether the output satisfies the policy.

---

## 📊 Behavior Summary

| Scenario | Description | Truth \(P(x)\) | Certificate | Verifier Outcome |
|----------|------------|----------------|------------|------------------|
| Simple safe | Low-complexity compliant instance | ✅ True | ✅ Present | ✅ Accepted |
| Unsafe | Policy violation | ❌ False | ❌ None | ❌ Rejected |
| Complex safe (no certificate) | High-complexity compliant instance | ✅ True | ❌ None | ❌ Not certified |
| Complex safe (with certificate) | Same instance with proof | ✅ True | ✅ Present | ✅ Accepted |

---

## ⚠️ Key Insight
> **Truth ≠ Verifiability**

---

## ▶️ How to Run
```bash
python -m src.demo --example examples/scene_safe.json --mode certificate
```
Output
```bash
=== Encoded Instance ===
{"Pi":{"min_stopping_margin_m":10.0,"require_no_collision":true},"y":{"action":"maintain","trajectory_id":"traj_safe_01"},"z":{"collision_risk":false,"object_distance_m":45.0,"sensor_mode":"camera+radar","stopping_distance_m":28.5}}

=== Policy Check ===
Compliant: True
Reason:    Policy satisfied with margin 16.50m

=== Complexity Estimate (compression proxy) ===
raw_bytes:  232
zlib_bytes: 168
gzip_bytes: 180
lzma_bytes: 240

=== Certificate ===
{
  "claim": "P(x)=1",
  "instance_digest": "ae28817c18bb5520369c3120d5a24f20643d2243537848703ccf0448473c008f",
  "metadata": {
    "reason": "Policy satisfied with margin 16.50m"
  },
  "signature": "f9a04f6803b60f71578d41d82c311bd5eef945bc890559d527c147c2790b099c"
}

=== Formal Verifier Outcome ===
Accepted: True
Mode:     certificate
Reason:   Certificate validated successfully
```

```bash
python -m src.demo --example examples/scene_unsafe.json --mode certificate
```
Output
```bash
=== Encoded Instance ===
{"Pi":{"min_stopping_margin_m":8.0,"require_no_collision":true},"y":{"action":"maintain","trajectory_id":"traj_unsafe_01"},"z":{"collision_risk":true,"object_distance_m":18.0,"sensor_mode":"camera+radar","stopping_distance_m":20.0}}

=== Policy Check ===
Compliant: False
Reason:    Collision risk present but action is maintain

=== Complexity Estimate (compression proxy) ===
raw_bytes:  232
zlib_bytes: 164
gzip_bytes: 176
lzma_bytes: 236

=== Formal Verifier Outcome ===
Accepted: False
Mode:     certificate
Reason:   No certificate provided
```

```bash
python -m src.demo --example examples/scene_complex_safe.json --mode no_certificate
```
Output
```bash
=== Encoded Instance ===
{"Pi":{"min_stopping_margin_m":10.0,"require_no_collision":true},"y":{"action":"maintain","trajectory_id":"traj_complex_safe_01"},"z":{"collision_risk":false,"object_distance_m":60.0,"sensor_mode":"camera+radar+lidar+fusion+temporal+history+contextual+semantic+occupancy+tracking","stopping_distance_m":30.0}}

=== Policy Check ===
Compliant: True
Reason:    Policy satisfied with margin 30.00m

=== Complexity Estimate (compression proxy) ===
raw_bytes:  309
zlib_bytes: 212
gzip_bytes: 224
lzma_bytes: 296

=== Formal Verifier Outcome ===
Accepted: False
Mode:     direct verification
Reason:   Verifier unable to certify: instance too complex
```

```bash
python -m src.demo --example examples/scene_complex_safe.json --mode certificate
```
Output
```bash
=== Encoded Instance ===
{"Pi":{"min_stopping_margin_m":10.0,"require_no_collision":true},"y":{"action":"maintain","trajectory_id":"traj_complex_safe_01"},"z":{"collision_risk":false,"object_distance_m":60.0,"sensor_mode":"camera+radar+lidar+fusion+temporal+history+contextual+semantic+occupancy+tracking","stopping_distance_m":30.0}}

=== Policy Check ===
Compliant: True
Reason:    Policy satisfied with margin 30.00m

=== Complexity Estimate (compression proxy) ===
raw_bytes:  309
zlib_bytes: 212
gzip_bytes: 224
lzma_bytes: 296

=== Certificate ===
{
  "claim": "P(x)=1",
  "instance_digest": "5b381385172a6baf8005b03e42b2d8ad5137311a4fa01e1d81e7474c3dd50ae2",
  "metadata": {
    "reason": "Policy satisfied with margin 30.00m"
  },
  "signature": "5b378d3541e4d42b901c9c23a5ea276daec30f9f9574f3a49279f8c6e8ab6bbe"
}

=== Formal Verifier Outcome ===
Accepted: True
Mode:     certificate
Reason:   Certificate validated successfully
```

---

## ⚠️ Disclamer
This is a conceptual demonstration, not a full formal system:
- Compression is used as a proxy for Kolmogorov complexity
- Certificates are simplified (not cryptographic proofs)
- The verifier models a bounded system, not a full theorem prover