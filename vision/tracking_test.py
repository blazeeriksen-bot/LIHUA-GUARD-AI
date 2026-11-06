"""
LIHUA GUARD AI
Vision Tracking Test

Test YOLO + ByteTrack object tracking.

Version: 0.6
"""

import cv2

from vision.camera import CameraSystem
from vision.detector import VisionDetector


print("🌸 LIHUA GUARD AI")
print("🌸 VISION TRACKING TEST")
print("")


camera = CameraSystem()
detector = VisionDetector()


if not camera.start_camera():

    print("❌ Camera test failed")

    raise SystemExit


print("")
print("🌸 Vision tracking test started")
print("Tekan Q untuk keluar")
print("")


while camera.is_online():

    frame = camera.capture_frame()

    if frame is None:

        break


    annotated_frame, detections = detector.track_frame(frame)


    for detection in detections:

        object_id = detection.get("id")
        object_name = detection.get("object")
        confidence = detection.get("confidence", 0)

        print(
            f"ID={object_id} | "
            f"Object={object_name} | "
            f"Confidence={confidence:.2f}"
        )


    cv2.imshow(
        "LIHUA GUARD AI - Tracking Test",
        annotated_frame
    )


    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


camera.release_camera()

cv2.destroyAllWindows()

print("")
print("🌸 Vision tracking test finished")
