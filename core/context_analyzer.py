"""
LIHUA GUARD AI
Context-Aware Threat Analyzer

Version: 0.1

Turns object detections into contextual evidence.
A dangerous object alone is not treated as an attack.
"""

import math


class ContextAnalyzer:

    def __init__(self, history_frames=8):
        self.history_frames = history_frames
        self.positions = {}
        self.distance_history = {}

    def _center(self, bbox):
        if not bbox:
            return None
        return (
            (bbox["x1"] + bbox["x2"]) / 2.0,
            (bbox["y1"] + bbox["y2"]) / 2.0,
        )

    def _person_distance(self, object_bbox, person_bbox):
        """Distance from object center to person rectangle, normalized by person height."""
        center = self._center(object_bbox)
        if center is None or not person_bbox:
            return None

        x, y = center
        px1, py1 = person_bbox["x1"], person_bbox["y1"]
        px2, py2 = person_bbox["x2"], person_bbox["y2"]

        dx = max(px1 - x, 0, x - px2)
        dy = max(py1 - y, 0, y - py2)
        pixel_distance = math.hypot(dx, dy)

        person_height = max(py2 - py1, 1)
        return pixel_distance / person_height

    def _update_position(self, object_id, center):
        if object_id is None or center is None:
            return 0.0

        history = self.positions.setdefault(object_id, [])
        history.append(center)
        if len(history) > self.history_frames:
            history.pop(0)

        if len(history) < 2:
            return 0.0

        x1, y1 = history[-2]
        x2, y2 = history[-1]
        return math.hypot(x2 - x1, y2 - y1)

    def analyze(self, detection, detections):
        """Return contextual evidence for one high-risk object."""
        object_name = detection.get("object", "").lower()
        if object_name not in {"knife", "baseball bat"}:
            return {
                "context_score": 0,
                "relation": "not_applicable",
                "movement": 0.0,
                "persistent": False,
                "approaching": False,
            }

        object_id = detection.get("id")
        object_bbox = detection.get("bbox")
        object_center = self._center(object_bbox)
        movement = self._update_position(object_id, object_center)

        people = [
            item for item in detections
            if item.get("object", "").lower() == "person"
            and item.get("bbox")
            and item.get("id") is not None
        ]

        if not people or object_bbox is None:
            return {
                "context_score": 0,
                "relation": "isolated",
                "movement": round(movement, 2),
                "persistent": False,
                "approaching": False,
            }

        nearest_distance = min(
            self._person_distance(object_bbox, person["bbox"])
            for person in people
        )

        if nearest_distance <= 0.15:
            relation = "overlapping"
        elif nearest_distance <= 0.50:
            relation = "very_near"
        elif nearest_distance <= 1.00:
            relation = "near"
        else:
            relation = "separate"

        # A stationary dangerous object is not enough to create a threat.
        # Movement + proximity are required before this layer contributes risk.
        context_score = 0

        previous_distance = None
        distance_history = self.distance_history.setdefault(object_id, [])
        if distance_history:
            previous_distance = distance_history[-1]
        distance_history.append(nearest_distance)
        if len(distance_history) > self.history_frames:
            distance_history.pop(0)

        approaching = (
            previous_distance is not None
            and nearest_distance < previous_distance - 0.01
        )

        if movement >= 8 and approaching and relation == "overlapping":
            context_score = 40
        elif movement >= 8 and approaching and relation == "very_near":
            context_score = 30
        elif movement >= 8 and approaching and relation == "near":
            context_score = 20

        persistent = len(self.positions.get(object_id, [])) >= 5
        if persistent and approaching and relation in {"overlapping", "very_near"}:
            context_score += 10

        return {
            "context_score": min(context_score, 50),
            "relation": relation,
            "movement": round(movement, 2),
            "persistent": persistent,
            "approaching": approaching,
            "distance_normalized": round(nearest_distance, 3),
        }

    def cleanup(self, active_ids):
        """Forget stale track histories."""
        active_ids = set(active_ids)
        for object_id in list(self.positions):
            if object_id not in active_ids:
                del self.positions[object_id]
                self.distance_history.pop(object_id, None)
