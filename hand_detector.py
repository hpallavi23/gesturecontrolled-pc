import cv2
import math
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:

    def __init__(
        self,
        model_path="hand_landmarker.task",
        max_num_hands=1,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.7,
        min_tracking_confidence=0.7
    ):

        # --------------------------------------------------
        # MediaPipe Hand Landmarker
        # --------------------------------------------------

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_num_hands,
            min_hand_detection_confidence=min_hand_detection_confidence,
            min_hand_presence_confidence=min_hand_presence_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        self.detector = vision.HandLandmarker.create_from_options(
            options
        )

        self.result = None
        self.landmarks = []
        self.handedness = None

        self.timestamp_ms = 0

    # ------------------------------------------------------
    # FIND HAND
    # ------------------------------------------------------

    def find_hands(self, frame, draw=True):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp_ms += 1

        self.result = self.detector.detect_for_video(
            mp_image,
            self.timestamp_ms
        )

        self.landmarks = []
        self.handedness = None

        if self.result.hand_landmarks:

            hand = self.result.hand_landmarks[0]

            height, width, _ = frame.shape

            for landmark_id, landmark in enumerate(hand):

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                self.landmarks.append(
                    [landmark_id, x, y, landmark.z]
                )

            # --------------------------------------------------
            # HANDEDNESS
            # --------------------------------------------------

            if self.result.handedness:

                self.handedness = (
                    self.result.handedness[0][0].category_name
                )

            # --------------------------------------------------
            # DRAW
            # --------------------------------------------------

            if draw:

                self._draw_landmarks(
                    frame,
                    hand
                )

        return frame, self.landmarks

    # ------------------------------------------------------
    # DRAW LANDMARKS
    # ------------------------------------------------------

    def _draw_landmarks(self, frame, hand):

        height, width, _ = frame.shape

        points = []

        for landmark in hand:

            x = int(landmark.x * width)
            y = int(landmark.y * height)

            points.append((x, y))

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

        for start, end in connections:

            cv2.line(
                frame,
                points[start],
                points[end],
                (0, 255, 0),
                2
            )

    # ------------------------------------------------------
    # GET LANDMARKS
    # ------------------------------------------------------

    def find_position(self):

        return self.landmarks

    # ------------------------------------------------------
    # GET HANDEDNESS
    # ------------------------------------------------------

    def get_handedness(self):

        return self.handedness

    # ------------------------------------------------------
    # DISTANCE
    # ------------------------------------------------------

    @staticmethod
    def _distance(p1, p2):

        return math.hypot(
            p2[0] - p1[0],
            p2[1] - p1[1]
        )

    # ------------------------------------------------------
    # ANGLE
    # ------------------------------------------------------

    @staticmethod
    def _angle(p1, p2, p3):

        v1 = (
            p1[0] - p2[0],
            p1[1] - p2[1]
        )

        v2 = (
            p3[0] - p2[0],
            p3[1] - p2[1]
        )

        mag1 = math.hypot(
            v1[0],
            v1[1]
        )

        mag2 = math.hypot(
            v2[0],
            v2[1]
        )

        if mag1 == 0 or mag2 == 0:
            return 0

        dot = (
            v1[0] * v2[0]
            + v1[1] * v2[1]
        )

        cosine = dot / (mag1 * mag2)

        cosine = max(
            -1.0,
            min(1.0, cosine)
        )

        return math.degrees(
            math.acos(cosine)
        )

    # ------------------------------------------------------
    # FINGER EXTENSION
    # ------------------------------------------------------

    def _finger_extended(
        self,
        points,
        mcp_id,
        pip_id,
        dip_id,
        tip_id
    ):

        mcp = points[mcp_id]
        pip = points[pip_id]
        dip = points[dip_id]
        tip = points[tip_id]

        # Angle at PIP
        pip_angle = self._angle(
            mcp,
            pip,
            dip
        )

        # Angle at DIP
        dip_angle = self._angle(
            pip,
            dip,
            tip
        )

        # Distance from MCP to TIP
        mcp_tip = self._distance(
            mcp,
            tip
        )

        # Distance from MCP to PIP
        mcp_pip = self._distance(
            mcp,
            pip
        )

        # A finger is extended when:
        #
        # - both joints are relatively straight
        # - tip is sufficiently far from MCP

        return (
            pip_angle > 145
            and dip_angle > 145
            and mcp_tip > mcp_pip * 1.25
        )

    # ------------------------------------------------------
    # THUMB EXTENSION
    # ------------------------------------------------------

    def _thumb_extended(self, points):

        wrist = points[0]
        thumb_cmc = points[1]
        thumb_mcp = points[2]
        thumb_ip = points[3]
        thumb_tip = points[4]

        angle = self._angle(
            thumb_mcp,
            thumb_ip,
            thumb_tip
        )

        wrist_tip = self._distance(
            wrist,
            thumb_tip
        )

        wrist_mcp = self._distance(
            wrist,
            thumb_mcp
        )

        cmc_tip = self._distance(
            thumb_cmc,
            thumb_tip
        )

        cmc_ip = self._distance(
            thumb_cmc,
            thumb_ip
        )

        # Thumb must be relatively straight
        straight = angle > 145

        # Thumb must move sufficiently away from its base
        far_from_base = wrist_tip > wrist_mcp * 1.35

        # Thumb must actually extend outward
        extended_distance = cmc_tip > cmc_ip * 1.05

        return (
            straight
            and far_from_base
            and extended_distance
        )

    # ------------------------------------------------------
    # FINGERS UP
    # ------------------------------------------------------

    def fingers_up(self):

        if len(self.landmarks) != 21:

            return None

        points = {}

        for landmark in self.landmarks:

            landmark_id, x, y, z = landmark

            points[landmark_id] = (x, y)

        # --------------------------------------------------
        # THUMB
        # --------------------------------------------------

        thumb = (
            1
            if self._thumb_extended(points)
            else 0
        )

        # --------------------------------------------------
        # OTHER FOUR FINGERS
        # --------------------------------------------------

        fingers = []

        finger_data = [
            (5, 6, 7, 8),       # Index
            (9, 10, 11, 12),    # Middle
            (13, 14, 15, 16),   # Ring
            (17, 18, 19, 20)    # Pinky
        ]

        for mcp, pip, dip, tip in finger_data:

            extended = self._finger_extended(
                points,
                mcp,
                pip,
                dip,
                tip
            )

            fingers.append(
                1 if extended else 0
            )

        # --------------------------------------------------
        # FINAL RESULT
        # --------------------------------------------------

        return [
            thumb,
            fingers[0],
            fingers[1],
            fingers[2],
            fingers[3]
        ]

    # ------------------------------------------------------
    # CLOSE
    # ------------------------------------------------------

    def close(self):

        self.detector.close()