"""
LIHUA GUARD AI
Camera Module

Version: 0.4
"""

import cv2


class CameraSystem:

    def __init__(self, camera_index=0):

        self.camera_index = camera_index
        self.camera = None
        self.status = "OFFLINE"


    def start_camera(self):

        self.camera = cv2.VideoCapture(
            self.camera_index
        )

        if not self.camera.isOpened():

            self.status = "ERROR"

            print("📷 Camera System: FAILED")

            return False

        self.status = "ONLINE"

        print("📷 Camera System:", self.status)

        return True


    def capture_frame(self):

        if self.camera is None:

            return None

        if self.status != "ONLINE":

            return None

        success, frame = self.camera.read()

        if not success:

            print("📷 Camera: Failed to capture frame")

            return None

        return frame


    def release_camera(self):

        if self.camera is not None:

            self.camera.release()

            self.camera = None

            self.status = "OFFLINE"

            print("📷 Camera System: OFFLINE")


    def is_online(self):

        return self.status == "ONLINE"