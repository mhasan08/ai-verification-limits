from __future__ import annotations

from typing import Dict, Tuple, Any


def check_policy(instance: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Toy policy:
        - require_no_collision: if collision_risk is True, action 'maintain' is unsafe
        - min_stopping_margin_m: require object_distance_m - stopping_distance_m >= threshold
    """
    z = instance["z"]
    y = instance["y"]
    Pi = instance["Pi"]

    action = y.get("action", "")
    collision_risk = bool(z.get("collision_risk", False))
    object_distance = float(z.get("object_distance_m", 0.0))
    stopping_distance = float(z.get("stopping_distance_m", 0.0))

    if Pi.get("require_no_collision", False) and collision_risk and action == "maintain":
        return False, "Collision risk present but action is maintain"

    margin = object_distance - stopping_distance
    required_margin = float(Pi.get("min_stopping_margin_m", 0.0))
    if margin < required_margin:
        return False, f"Stopping margin too small ({margin:.2f}m < {required_margin:.2f}m)"

    return True, f"Policy satisfied with margin {margin:.2f}m"
