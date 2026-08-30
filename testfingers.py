import cv2

from hand_detector import HandDetector


cap = cv2.VideoCapture(0)

detector = HandDetector(
    model_path="hand_landmarker.task",
    max_num_hands=1
)


while True:

    success, frame = cap.read()

    if not success:
        print("Could not open camera.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Detect hand
    frame = detector.find_hands(
        frame,
        draw=True
    )

    # Get finger states
    fingers = detector.fingers_up()

    # Display on camera
    cv2.putText(
        frame,
        str(fingers),
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Print to terminal
    print(fingers)

    cv2.imshow(
        "Gesture Controlled PC - Finger Test",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
detector.close()
cv2.destroyAllWindows()