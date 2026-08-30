# To run the below code, Run (python main.py) to get the output
import cv2
import pyautogui

from hand_detector import HandDetector
from gesture_recognizer import GestureRecognizer
from collections import Counter


# Start camera
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

if not cap.isOpened():
    print("Could not access the camera.")
    exit()


# Create detector and recognizer
detector = HandDetector()
recognizer = GestureRecognizer()

# Gesture stabilization
gesture_history = []
history_size = 7


while True:

    # Read camera frame
    success, frame = cap.read()

    if not success:
        print("Could not read frame from camera.")
        break

    # Detect hand and get landmarks
    frame, landmarks = detector.find_hands(frame)


    # Check if a hand was detected
    if landmarks:

        # Detect which fingers are up
        fingers = detector.fingers_up(landmarks)

        # Recognize gesture
        gesture = recognizer.recognize(fingers)


        # -------------------------------
        # INDEX FINGER TEST
        # -------------------------------

        if fingers[1] == 1:

            index_x = landmarks[8][1]
            index_y = landmarks[8][2]

            cv2.circle(
                frame,
                (index_x, index_y),
                15,
                (255, 0, 0),
                -1
            )


        # -------------------------------
        # GESTURE STABILIZATION
        # -------------------------------

        gesture_history.append(gesture)

        if len(gesture_history) > history_size:
            gesture_history.pop(0)

        most_common_gesture = Counter(
            gesture_history
        ).most_common(1)[0][0]


        # Display gesture name
        cv2.putText(
            frame,
            most_common_gesture,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )


    # Show camera window
    cv2.imshow("Gesture Controlled PC", frame)


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release camera
cap.release()
cv2.destroyAllWindows()