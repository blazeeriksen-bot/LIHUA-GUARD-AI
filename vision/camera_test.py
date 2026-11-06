"""
LIHUA GUARD AI
Camera Test

Version: 0.4
"""

import cv2

from vision.camera import CameraSystem


camera = CameraSystem()

if not camera.start_camera():

    print("❌ Camera test failed")

    raise SystemExit


print("")

print("🌸 Camera test started")
print("Tekan Q untuk keluar")


while camera.is_online():

    frame = camera.capture_frame()

    if frame is None:

        break


    cv2.imshow(
        "LIHUA GUARD AI - Camera Test",
        frame
    )


    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


camera.release_camera()

cv2.destroyAllWindows()

print("🌸 Camera test finished")