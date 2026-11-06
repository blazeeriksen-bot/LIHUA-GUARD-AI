"""
LIHUA GUARD AI
Core System Controller

Version: 1.0.1
"""

import cv2

from core.threat_score import ThreatScore
from core.threat_tracker import ThreatTracker
from core.decision_engine import DecisionEngine
from core.context_analyzer import ContextAnalyzer

from security.logger import LihuaLogger
from security.alert import AlertSystem

from vision.camera import CameraSystem
from vision.detector import VisionDetector


class LihuaSystem:

    def __init__(self):

        self.status = "INITIALIZING"

        # ---------------------------------------
        # Core systems
        # ---------------------------------------

        self.threat = ThreatScore()

        self.tracker = ThreatTracker(
            confirmation_frames=3,
            max_missing_frames=10
        )

        self.decision = DecisionEngine()
        self.context = ContextAnalyzer(history_frames=8)

        # ---------------------------------------
        # Security systems
        # ---------------------------------------

        self.logger = LihuaLogger()

        self.alert = AlertSystem()

        # ---------------------------------------
        # Vision systems
        # ---------------------------------------

        self.camera = CameraSystem()

        self.vision = VisionDetector()

        # ---------------------------------------
        # Runtime state
        # ---------------------------------------

        self.last_score = None

        self.last_action = None

        self.confirmed_ids = set()


    def start(self):

        self.status = "RUNNING"

        print("🌸 LIHUA GUARD AI STARTED")

        print(
            "System Status:",
            self.status
        )

        # ---------------------------------------
        # Start camera
        # ---------------------------------------

        camera_started = (
            self.camera.start_camera()
        )

        if not camera_started:

            print(
                "❌ Camera System: Failed"
            )

            self.logger.record(
                "Camera System failed to start"
            )

            self.status = "ERROR"

            return

        print()

        print(
            "🌸 LIHUA REAL-TIME SECURITY"
        )

        print(
            "Press Q to exit"
        )

        try:

            # ===================================
            # MAIN SECURITY LOOP
            # ===================================

            while self.camera.is_online():

                # --------------------------------
                # Capture frame
                # --------------------------------

                frame = (
                    self.camera.capture_frame()
                )

                if frame is None:

                    print(
                        "❌ Camera: "
                        "Failed to capture frame"
                    )

                    break

                # --------------------------------
                # YOLO + ByteTrack
                # --------------------------------

                (
                    annotated_frame,
                    detections
                ) = self.vision.track_frame(
                    frame
                )

                if annotated_frame is None:

                    annotated_frame = frame

                # --------------------------------
                # Update threat tracker
                # --------------------------------

                self.tracker.update(
                    detections
                )

                # --------------------------------
                # Process detections
                # --------------------------------

                for detection in detections:

                    object_id = detection.get(
                        "id"
                    )

                    object_name = detection.get(
                        "object",
                        "unknown"
                    )

                    confidence = detection.get(
                        "confidence",
                        0
                    )

                    # Ignore objects
                    # without tracking ID.

                    if object_id is None:

                        continue

                    # --------------------------------
                    # Calculate threat contribution
                    # --------------------------------

                    # --------------------------------
                    # Context-aware threat analysis
                    # --------------------------------

                    context = self.context.analyze(
                        detection,
                        detections
                    )

                    detection_score = (
                        self.threat
                        .calculate_contextual_score(
                            detection,
                            context
                        )
                    )

                    if (
                        detection.get("object", "").lower()
                        in {"knife", "baseball bat"}
                    ):
                        print(
                            f"🧠 Context | ID {object_id} | "
                            f"{context['relation']} | "
                            f"movement={context['movement']} | "
                            f"context={context['context_score']} | "
                            f"score={detection_score}"
                        )

                    if detection_score <= 0:

                        continue

                    # --------------------------------
                    # Register threat observation
                    # --------------------------------

                    self.tracker.mark_threat(
                        object_id,
                        detection_score
                    )

                    # --------------------------------
                    # Threat confirmation
                    # --------------------------------

                    confirmed = (
                        self.tracker
                        .is_confirmed(
                            object_id
                        )
                    )

                    if confirmed:

                        # Print confirmation
                        # only once per ID.

                        if (
                            object_id
                            not in self.confirmed_ids
                        ):

                            stable_score = (
                                self.tracker
                                .get_threat_score(
                                    object_id
                                )
                            )

                            print(
                                f"🔴 THREAT CONFIRMED | "
                                f"ID {object_id} | "
                                f"{object_name} | "
                                f"{confidence}% "
                                f"→ stable +"
                                f"{stable_score}"
                            )

                            self.confirmed_ids.add(
                                object_id
                            )

                    else:

                        print(
                            f"⚠️ Threat observed | "
                            f"ID {object_id} | "
                            f"{object_name} | "
                            f"{confidence}% "
                            f"→ waiting confirmation"
                        )

                # --------------------------------
                # Cleanup stale context histories
                # --------------------------------

                self.context.cleanup(
                    detection.get("id")
                    for detection in detections
                    if detection.get("id") is not None
                )

                # --------------------------------
                # Get stable threat score
                # --------------------------------

                score = (
                    self.tracker
                    .get_total_threat_score()
                )

                # --------------------------------
                # Analyze decision
                # --------------------------------

                action = (
                    self.decision.analyze(
                        score
                    )
                )

                # --------------------------------
                # Remember previous state
                # --------------------------------

                previous_score = (
                    self.last_score
                )

                previous_action = (
                    self.last_action
                )

                # --------------------------------
                # Display security state
                # --------------------------------

                if (
                    score != previous_score
                    or
                    action != previous_action
                ):

                    print(
                        f"🛡️ Threat Score: {score}"
                    )

                    print(
                        f"🧠 Decision: {action}"
                    )

                # --------------------------------
                # Security state transition
                # --------------------------------

                if (
                    action == "WARNING"
                    and previous_action
                    != "WARNING"
                ):

                    self.alert.send_alert(
                        "Security warning detected"
                    )

                    self.logger.record(
                        f"WARNING | "
                        f"Threat Score: {score}"
                    )

                elif (
                    action == "LOCKDOWN"
                    and previous_action
                    != "LOCKDOWN"
                ):

                    self.alert.send_alert(
                        "Security lockdown activated"
                    )

                    self.logger.record(
                        f"LOCKDOWN | "
                        f"Threat Score: {score}"
                    )

                # --------------------------------
                # Save current state
                # --------------------------------

                self.last_score = score

                self.last_action = action

                # --------------------------------
                # Camera overlay
                # --------------------------------

                cv2.putText(
                    annotated_frame,
                    f"Threat Score: {score}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    annotated_frame,
                    f"Decision: {action}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                # --------------------------------
                # Display tracked objects
                # --------------------------------

                y_position = 120

                for detection in detections:

                    object_id = detection.get(
                        "id"
                    )

                    object_name = detection.get(
                        "object",
                        "unknown"
                    )

                    confidence = detection.get(
                        "confidence",
                        0
                    )

                    confirmed = False

                    if object_id is not None:

                        confirmed = (
                            self.tracker
                            .is_confirmed(
                                object_id
                            )
                        )

                    if confirmed:

                        state = "CONFIRMED"

                    else:

                        state = "OBSERVING"

                    text = (
                        f"ID {object_id}: "
                        f"{object_name} "
                        f"{confidence}% "
                        f"[{state}]"
                    )

                    cv2.putText(
                        annotated_frame,
                        text,
                        (20, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

                    y_position += 25

                # --------------------------------
                # Display camera
                # --------------------------------

                cv2.imshow(
                    "LIHUA GUARD AI - SECURITY",
                    annotated_frame
                )

                # --------------------------------
                # Keyboard control
                # --------------------------------

                key = (
                    cv2.waitKey(1) & 0xFF
                )

                if key == ord("q"):

                    break

        except KeyboardInterrupt:

            print(
                "\n⚠️ LIHUA shutdown requested"
            )

        except Exception as error:

            print(
                f"❌ LIHUA SYSTEM ERROR: {error}"
            )

            self.logger.record(
                f"SYSTEM ERROR: {error}"
            )

            self.status = "ERROR"

        finally:


            self.camera.release_camera()

            cv2.destroyAllWindows()

            self.status = "STOPPED"

            self.logger.record(
                "Lihua real-time security stopped"
            )

            print(
                "🌸 Lihua real-time security finished"
            )