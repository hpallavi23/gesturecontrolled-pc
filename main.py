# To run the below code, Run (python main.py) to get the output

import cv2
import pyautogui
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

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


# Screen dimensions
screen_width, screen_height = pyautogui.size()

# SYSTEM VOLUME CONTROL

devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

# Volume range in Windows
volume_min, volume_max, _ = volume.GetVolumeRange()

# Mouse smoothing
prev_x = screen_width // 2
prev_y = screen_height // 2
smoothening = 10
dead_zone = 8

# Prevent repeated clicks while holding pinch
previous_click_gesture = False
previous_right_click_gesture = False
right_click_cooldown = 0

previous_scroll_y = None
scroll_threshold = 15

# Volume control
previous_volume_y = None
volume_threshold = 8
volume_step = 2

# Check if a hand was detected
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

        fingers = detector.fingers_up()

        # KEEP THIS FOR TESTING
        print(fingers)


        # Recognize gesture
        gesture = recognizer.recognize(fingers)


        # ==================================================
        # MOUSE CONTROL
        # ==================================================

        # Index finger controls mouse
        # Only when middle finger is NOT up
        if fingers[1] == 1 and fingers[2] == 0:

            index_x = landmarks[8][1]
            index_y = landmarks[8][2]


            # Draw index fingertip
            cv2.circle(
                frame,
                (index_x, index_y),
                15,
                (255, 0, 0),
                -1
            )


            # Camera frame dimensions
            frame_height, frame_width, _ = frame.shape


            # Convert camera coordinates to screen coordinates
            # X is reversed because the camera is mirrored
            mouse_x = int(
                (frame_width - index_x)
                / frame_width
                * screen_width
            )

            mouse_y = int(
                index_y
                / frame_height
                * screen_height
            )


            # Difference from previous mouse position
            diff_x = mouse_x - prev_x
            diff_y = mouse_y - prev_y


            # Dead zone to ignore tiny movements
            if abs(diff_x) > dead_zone or abs(diff_y) > dead_zone:

                current_x = prev_x + diff_x / smoothening
                current_y = prev_y + diff_y / smoothening


                # Move mouse
                pyautogui.moveTo(
                    int(current_x),
                    int(current_y)
                )


                # Update previous position
                prev_x = current_x
                prev_y = current_y


        # ==================================================
        # PINCH → LEFT CLICK
        # ==================================================


        # Thumb tip = landmark 4
        thumb_x = landmarks[4][1]
        thumb_y = landmarks[4][2]

        # Index tip = landmark 8
        index_x = landmarks[8][1]
        index_y = landmarks[8][2]


        # Calculate distance between thumb and index
        distance = math.hypot(
            index_x - thumb_x,
            index_y - thumb_y
        )


        # Pinch threshold
        pinch_threshold = 35


        # Pinch detected
        click_gesture = (
            fingers == [1, 1, 0, 0, 0]
        )

        # Click only when pinch first appears
        if click_gesture and not previous_click_gesture:

            pyautogui.click()

            print("Left Click")


        # Remember current pinch state
        previous_click_gesture = click_gesture

        # THUMB + PINKY -> RIGHT CLICK
        # Distance between thumb and index
        thumb_index_distance = math.hypot(
            landmarks[4][1] - landmarks[8][1],
            landmarks[4][2] - landmarks[8][2]
        )       

        # Distance between thumb and middle
        thumb_middle_distance = math.hypot(
            landmarks[4][1] - landmarks[12][1],
            landmarks[4][2] - landmarks[12][2]
        )
        # THUMB + PINKY -> RIGHT CLICK
        # Required gesture: [1, 0, 0, 0, 1]
        right_click_gesture = (
            fingers == [1, 0, 0, 0, 1]
        )

        # Cooldown prevents repeated right clicks 
        # while loading the gesture.
        if right_click_cooldown > 0:
            right_click_cooldown -= 1
        if right_click_gesture and right_click_cooldown == 0:
            pyautogui.rightClick()
            print("Right Click")
            right_click_cooldown = 15

        # INDEX + MIDDLE -> SCROLL 
        scroll_gesture = (
            fingers[1] == 1 and
            fingers[2] == 1 and
            thumb_middle_distance > 45
        )
        if scroll_gesture:
            # Use both INDEX + MIDDLE Fingertips
            index_y_scroll = landmarks[8][2]
            middle_y_scroll = landmarks[12][2]

            # Average position of index + middle
            current_scroll_y = (
                index_y_scroll + middle_y_scroll
            ) / 2

            # First frame of scrolling
            if previous_scroll_y is None:
                previous_scroll_y = current_scroll_y
            else:
                # Calculate vertical movement
                movement = previous_scroll_y - current_scroll_y

                #Scroll speed
                # Higher sensitivity = faster scrolling
                scroll_amount = int(abs(movement) / 3)

                # Always scroll atleast 1 unit
                scroll_amount = max(1, scroll_amount)

                # Scroll UP
                if movement > scroll_threshold:
                    pyautogui.scroll(scroll_amount)
                    previous_scroll_y = current_scroll_y
                # Scroll DOWN
                elif movement < -scroll_threshold:
                    pyautogui.scroll(-scroll_amount)
                    previous_scroll_y = current_scroll_y
        else:
            #Reset when scroll gesture ends
            previous_scroll_y = None

        # INDEX + PINKY -> VOLUME CONTROL
        volume_gesture = (
            fingers[1] == 1 and
            fingers[2] == 0 and
            fingers[3] == 0 and
            fingers[4] == 1
        )

        if volume_gesture:

            # Index fingertip Y
            index_y_volume = landmarks[8][2]

            # Pinky fingertip Y
            pinky_y_volume = landmarks[20][2]

            # Average position of index + pinky
            current_volume_y = (
                index_y_volume + pinky_y_volume
            ) / 2

            # First frame of volume gesture
            if previous_volume_y is None:

                previous_volume_y = current_volume_y

            else:

                # Calculate movement ONLY inside this block
                movement = previous_volume_y - current_volume_y

                # Volume UP
                if movement > volume_threshold:

                    current_volume = volume.GetMasterVolumeLevel()

                    new_volume = min(
                        current_volume + volume_step,
                        volume_max
                    )
                    volume.SetMasterVolumeLevel(
                        new_volume,
                        None
                    )
                    previous_volume_y = current_volume_y

                # Volume DOWN
                elif movement < -volume_threshold:
                    current_volume = volume.GetMasterVolumeLevel()
                    new_volume = max(
                        current_volume - volume_step,
                        volume_min
                    )
                    volume.SetMasterVolumeLevel(
                        new_volume,
                        None
                    )
                    previous_volume_y = current_volume_y
                else:
                    previous_volume_y = None

        # ==================================================
        # GESTURE STABILIZATION
        # ==================================================

        gesture_history.append(gesture)


        if len(gesture_history) > history_size:
            gesture_history.pop(0)


        most_common_gesture = Counter(
            gesture_history
        ).most_common(1)[0][0]


        # Display recognized gesture
        cv2.putText(
            frame,
            most_common_gesture,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )


    # ==================================================
    # SHOW CAMERA WINDOW
    # ==================================================

    cv2.imshow(
        "Gesture Controlled PC",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release camera
cap.release()
cv2.destroyAllWindows()