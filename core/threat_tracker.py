"""
LIHUA GUARD AI
Threat History Tracker

Version: 1.0
"""


class ThreatTracker:

    def __init__(
        self,
        confirmation_frames=3,
        max_missing_frames=10
    ):

        self.history = {}

        self.confirmation_frames = (
            confirmation_frames
        )

        self.max_missing_frames = (
            max_missing_frames
        )


    def update(self, detections):

        current_ids = set()


        # ---------------------------------------
        # Update objects visible this frame
        # ---------------------------------------

        for detection in detections:

            object_id = detection.get(
                "id"
            )


            if object_id is None:

                continue


            current_ids.add(
                object_id
            )


            object_name = detection.get(
                "object",
                "unknown"
            ).lower()


            confidence = detection.get(
                "confidence",
                0
            )


            # New object

            if object_id not in self.history:

                self.history[object_id] = {

                    "object": object_name,

                    "confidence": confidence,

                    "frames": 1,

                    "threat_frames": 0,

                    "confirmed": False,

                    "threat_score": 0,

                    "active": True,

                    "missing_frames": 0

                }


            # Existing object

            else:

                track = self.history[
                    object_id
                ]


                track["object"] = (
                    object_name
                )


                track["confidence"] = (
                    confidence
                )


                track["frames"] += 1


                track["missing_frames"] = 0


                track["active"] = True


        # ---------------------------------------
        # Handle missing objects
        # ---------------------------------------

        for object_id in list(
            self.history.keys()
        ):

            if object_id in current_ids:

                continue


            track = self.history[
                object_id
            ]


            track["missing_frames"] += 1


            # Temporary detection loss.
            #
            # The threat remains active.

            if (
                track["missing_frames"]
                <= self.max_missing_frames
            ):

                track["active"] = True


            else:

                track["active"] = False


    def mark_threat(
        self,
        object_id,
        score
    ):

        if object_id not in self.history:

            return


        track = self.history[
            object_id
        ]


        # Already confirmed.
        #
        # Do NOT change the locked score.

        if track["confirmed"]:

            return


        track["threat_frames"] += 1


        # ---------------------------------------
        # Confirm threat
        # ---------------------------------------

        if (
            track["threat_frames"]
            >= self.confirmation_frames
        ):

            track["confirmed"] = True

            track["threat_score"] = (
                score
            )


    def is_confirmed(
        self,
        object_id
    ):

        track = self.history.get(
            object_id
        )


        if track is None:

            return False


        return track["confirmed"]


    def get_threat_score(
        self,
        object_id
    ):

        track = self.history.get(
            object_id
        )


        if track is None:

            return 0


        if not track["confirmed"]:

            return 0


        return track["threat_score"]


    def get_confirmed_threats(self):

        confirmed = []


        for object_id, track in (
            self.history.items()
        ):

            if not track["confirmed"]:

                continue


            if not track["active"]:

                continue


            confirmed.append(
                track
            )


        return confirmed


    def get_total_threat_score(self):

        total = 0


        for track in (
            self.get_confirmed_threats()
        ):

            total += track[
                "threat_score"
            ]


        return total


    def get_track(
        self,
        object_id
    ):

        return self.history.get(
            object_id
        )


    def get_history(self):

        return self.history


    def remove_track(
        self,
        object_id
    ):

        if object_id in self.history:

            del self.history[
                object_id
            ]


    def reset(self):

        self.history.clear()