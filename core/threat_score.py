"""
LIHUA GUARD AI
Threat Scoring Module

Version: 0.7
"""


class ThreatScore:

    def __init__(self):
        self.score = 0

    def add_score(self, value):
        self.score += value
        self.score = max(0, min(self.score, 100))

    def get_score(self):
        return self.score

    def reset(self):
        self.score = 0

    def calculate_from_detection(self, detection):
        object_name = detection.get("object", "").lower()
        confidence = float(detection.get("confidence", 0))

        if confidence < 50:
            return 0
        if object_name == "person":
            return 0

        safe_objects = {
            "chair", "bottle", "cup", "book", "laptop",
            "cell phone", "backpack", "handbag",
        }
        if object_name in safe_objects:
            return 0

        risk_objects = {
            "knife": {"50": 30, "60": 45, "70": 60, "80": 75, "90": 90},
            "baseball bat": {"50": 20, "60": 30, "70": 45, "80": 60, "90": 75},
        }
        if object_name not in risk_objects:
            return 0

        score_table = risk_objects[object_name]
        if confidence >= 90:
            return score_table["90"]
        if confidence >= 80:
            return score_table["80"]
        if confidence >= 70:
            return score_table["70"]
        if confidence >= 60:
            return score_table["60"]
        return score_table["50"]

    def calculate_contextual_score(self, detection, context):
        """Combine object confidence with contextual evidence.

        An isolated knife/bat does not produce a threat score. Context must
        provide evidence that the object is interacting with or moving near a person.
        """
        base_score = self.calculate_from_detection(detection)
        if base_score <= 0:
            return 0

        context_score = int(context.get("context_score", 0))
        if context_score <= 0:
            return 0

        # Context is a multiplier rather than a second independent threat.
        # 0..50 contextual evidence maps to 0.20..1.0.
        multiplier = 0.20 + (context_score / 50.0) * 0.80
        return min(round(base_score * multiplier), 100)

    def calculate_from_detections(self, detections):
        highest_confidence = {}
        for detection in detections:
            object_name = detection.get("object", "").lower()
            confidence = float(detection.get("confidence", 0))
            current = highest_confidence.get(object_name)
            if current is None or confidence > float(current.get("confidence", 0)):
                highest_confidence[object_name] = detection

        total_score = 0
        for detection in highest_confidence.values():
            total_score += self.calculate_from_detection(detection)
        return min(total_score, 100)
