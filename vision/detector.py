"""
LIHUA GUARD AI
YOLO Vision Detector + Object Tracking

Version: 0.6
"""

from ultralytics import YOLO


class VisionDetector:

    def __init__(self):

        self.model = YOLO(
            "yolo11n.pt"
        )


    def track_frame(self, frame):

        if frame is None:

            return None, []


        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )


        detections = []

        annotated_frame = frame


        for result in results:

            if result.boxes is None:

                annotated_frame = result.plot()

                continue


            annotated_frame = result.plot()


            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )


                confidence = float(
                    box.conf[0]
                )


                class_name = (
                    self.model.names[
                        class_id
                    ]
                )


                object_id = None


                if box.id is not None:

                    object_id = int(
                        box.id[0]
                    )


                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                detection = {

                    "id": object_id,

                    "object": class_name,

                    "confidence": round(
                        confidence * 100,
                        2
                    ),

                    "bbox": {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2
                    }

                }


                detections.append(
                    detection
                )


        return (
            annotated_frame,
            detections
        )