"""
LIHUA GUARD AI
Threat Tracker Test

Version: 0.8.1
"""

from core.threat_tracker import ThreatTracker


tracker = ThreatTracker(
    confirmation_frames=3
)


print("🌸 THREAT TRACKER v0.8.1 TEST")
print("")


# FRAME 1

tracker.update([
    {
        "id": 7,
        "object": "knife",
        "confidence": 51.0
    }
])

tracker.mark_threat(7, 21)

print("Frame 1:")
print(tracker.get_history())
print("")


# FRAME 2

tracker.update([
    {
        "id": 7,
        "object": "knife",
        "confidence": 57.0
    }
])

tracker.mark_threat(7, 23)

print("Frame 2:")
print(tracker.get_history())
print("")


# FRAME 3
# Threat becomes confirmed here.

tracker.update([
    {
        "id": 7,
        "object": "knife",
        "confidence": 56.0
    }
])

tracker.mark_threat(7, 22)

print("Frame 3:")
print(tracker.get_history())
print("")


# FRAME 4
# Confidence changes dramatically.
# Score must remain locked at 22.

tracker.update([
    {
        "id": 7,
        "object": "knife",
        "confidence": 80.0
    }
])

tracker.mark_threat(7, 40)

print("Frame 4:")
print(tracker.get_history())
print("")


# FRAME 5
# Score must still remain 22.

tracker.update([
    {
        "id": 7,
        "object": "knife",
        "confidence": 50.0
    }
])

tracker.mark_threat(7, 20)

print("Frame 5:")
print(tracker.get_history())
print("")


# MISSING FRAME TEST

print("🌸 MISSING FRAME TEST")
print("")


# FRAME 6

tracker.update([])

track = tracker.get_track(7)

print("Frame 6 - knife missing:")
print(
    f"missing_frames={track['missing_frames']} | "
    f"active={track['active']} | "
    f"confirmed={track['confirmed']} | "
    f"score={track['threat_score']}"
)
print("")


# FRAME 7

tracker.update([])

track = tracker.get_track(7)

print("Frame 7 - knife missing:")
print(
    f"missing_frames={track['missing_frames']} | "
    f"active={track['active']} | "
    f"confirmed={track['confirmed']} | "
    f"score={track['threat_score']}"
)
print("")


# FRAME 8

tracker.update([
    {
        "id": 7,
        "object": "knife",
        "confidence": 62.0
    }
])

track = tracker.get_track(7)

print("Frame 8 - knife returned:")
print(
    f"missing_frames={track['missing_frames']} | "
    f"active={track['active']} | "
    f"confirmed={track['confirmed']} | "
    f"score={track['threat_score']}"
)
print("")


# LONG MISSING TEST

print("🌸 LONG MISSING TEST")
print("")


for i in range(1, 12):

    tracker.update([])

    track = tracker.get_track(7)

    print(
        f"Missing Frame {i}: "
        f"missing_frames={track['missing_frames']} | "
        f"active={track['active']} | "
        f"confirmed={track['confirmed']} | "
        f"score={track['threat_score']}"
    )


print("")


# FINAL STATE

print("Confirmed:")
print(
    tracker.is_confirmed(7)
)

print("")


print("Locked Threat Score:")
print(
    tracker.get_threat_score(7)
)

print("")


print("Total Threat Score:")
print(
    tracker.get_total_threat_score()
)
