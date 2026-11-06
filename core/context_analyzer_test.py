"""Tests for context-aware threat analysis."""

from core.context_analyzer import ContextAnalyzer
from core.threat_score import ThreatScore


def bbox(x1, y1, x2, y2):
    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}


def main():
    analyzer = ContextAnalyzer(history_frames=8)
    score = ThreatScore()

    person = {
        "id": 1,
        "object": "person",
        "confidence": 90,
        "bbox": bbox(100, 100, 300, 500),
    }

    isolated_knife = {
        "id": 2,
        "object": "knife",
        "confidence": 90,
        "bbox": bbox(800, 100, 840, 160),
    }

    context = analyzer.analyze(isolated_knife, [person, isolated_knife])
    isolated_score = score.calculate_contextual_score(isolated_knife, context)

    assert context["relation"] == "separate"
    assert isolated_score == 0

    near_knife = {
        "id": 3,
        "object": "knife",
        "confidence": 90,
        "bbox": bbox(230, 270, 260, 310),
    }
    context = analyzer.analyze(near_knife, [person, near_knife])
    near_static_score = score.calculate_contextual_score(near_knife, context)

    assert context["relation"] in {"overlapping", "very_near"}
    assert near_static_score == 0

    moving_knife = {
        "id": 4,
        "object": "knife",
        "confidence": 90,
        "bbox": bbox(340, 270, 370, 310),
    }

    # Move the knife toward the person.
    approaching_seen = False
    moving_score = 0
    for x in (340, 330, 320, 310, 300, 290):
        moving_knife["bbox"] = bbox(x, 270, x + 30, 310)
        context = analyzer.analyze(moving_knife, [person, moving_knife])
        moving_score = max(
            moving_score,
            score.calculate_contextual_score(moving_knife, context)
        )
        if context["approaching"]:
            approaching_seen = True

    assert context["movement"] > 0
    assert approaching_seen is True
    assert moving_score > 0

    print("🌸 CONTEXT THREAT TEST")
    print("isolated:", isolated_score, "relation=", context["relation"])
    print("near stationary:", near_static_score)
    print("moving/persistent:", moving_score, context)
    print("PASS")


if __name__ == "__main__":
    main()
