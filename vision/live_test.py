"""
LIHUA GUARD AI
Real-Time YOLO Vision Test

Version: 0.4
"""

import cv2

from vision.camera import CameraSystem
from vision.detector import VisionDetector


camera = CameraSystem()
detector = VisionDetector()


if not camera.start_camera():

    print("❌ Camera failed to start")

    raise SystemExit


print("")
print("🌸 LIHUA REAL-TIME VISION")
print("Press Q to exit")


while camera.is_online():

    frame = camera.capture_frame()

    if frame is None:

        break


    detections = detector.detect(frame)


    for detection in detections:

        print(
            f"👁️ {detection['object']} "
            f"({detection['confidence']}%)"
        )


    results = detector.model(
        frame,
        verbose=False
    )


    annotated_frame = results[0].plot()


    cv2.imshow(
        "LIHUA GUARD AI - REAL-TIME VISION",
        annotated_frame
    )


    key = cv2.waitKey(1) & 0xFF


    if key == ord("q"):

        break


camera.release_camera()

cv2.destroyAllWindows()

print("🌸 Real-time vision finished")