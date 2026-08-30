import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self, max_hands=1, detection_confidence=0.7):

        self.max_hands = max_hands
        self.detection_confidence = detection_confidence

        # MediaPipe Tasks setup
        base_options = mp.tasks.BaseOptions(
            model_asset_path="hand_landmarker.task"
        )

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=self.max_hands,
            min_hand_detection_confidence=self.detection_confidence,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.detector = mp.tasks.vision.HandLandmarker.create_from_options(
            options
        )

        self.timestamp = 0

    def find_hands(self, frame, draw=True):

        # OpenCV uses BGR, MediaPipe expects RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert OpenCV frame into MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hands
        results = self.detector.detect_for_video(
            mp_image,
            self.timestamp
        )

        self.timestamp += 1

        # Draw landmarks
        if results.hand_landmarks and draw:

            height, width, _ = frame.shape

            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),
                (0, 5), (5, 6), (6, 7), (7, 8),
                (0, 9), (9, 10), (10, 11), (11, 12),
                (0, 13), (13, 14), (14, 15), (15, 16),
                (0, 17), (17, 18), (18, 19), (19, 20),
                (5, 9), (9, 13), (13, 17)
            ]

            for hand_landmarks in results.hand_landmarks:

                # Draw points
                for landmark in hand_landmarks:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                # Draw connections
                for start, end in connections:

                    x1 = int(hand_landmarks[start].x * width)
                    y1 = int(hand_landmarks[start].y * height)

                    x2 = int(hand_landmarks[end].x * width)
                    y2 = int(hand_landmarks[end].y * height)

                    cv2.line(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

        return frame