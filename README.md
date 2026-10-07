Gesture Controlled PC 🖐️💻

A real-time computer control system that allows users to interact with their Windows PC using hand gestures captured through a webcam.

The project uses computer vision and hand landmark detection to recognize predefined gestures and map them to actions such as mouse control, clicking, scrolling, volume control, brightness control, screenshots, YouTube play/pause, and presentation slide navigation.

🎥 Demo

Gesture Controlled PC — Working Demo

[▶️ Watch the Gesture Controlled PC Demo](https://youtu.be/JFckQpFbzxE)

The demo showcases the implemented gesture controls working in real time.


✨ Features

The system currently supports 9 computer-control features:

☝️ Index finger → Mouse movement
👍 + ☝️ Thumb + Index → Left click
👍 + 🤙 Thumb + Pinky → Right click
✌️ Index + Middle → Scroll
☝️ + 🤙 Index + Pinky → Volume control
👍 + ☝️ + 🤙 Thumb + Index + Pinky → Brightness control
🖐️ Open palm → YouTube play/pause
✊ Fist → Screenshot capture
🖐️ ↔️ Open palm + horizontal swipe → Presentation slide navigation


⚙️ How It Works

The system processes the user's hand movements in real time through a webcam.

### Processing Pipeline

Webcam
   ↓
OpenCV
   ↓
Hand Detection
   ↓
Hand Landmarks
   ↓
Finger State Detection
   ↓
Gesture Recognition
   ↓
Computer Action

Step-by-step

1. Webcam Capture
   OpenCV captures live video frames from the webcam.

2. Hand Detection
   The hand is detected and hand landmarks are obtained using MediaPipe.

3. Finger State Detection
   The system determines which fingers are raised or folded.

4. Gesture Recognition
   The detected finger-state pattern is matched with predefined gestures.

5. Action Execution
   The corresponding computer action is performed using libraries such as PyAutoGUI, Pycaw, and Screen Brightness Control.


🛠️ Technologies Used

* Python — Main programming language
* OpenCV — Webcam and real-time image processing
* MediaPipe — Hand landmark detection
* PyAutoGUI — Mouse, keyboard, and screenshot automation
* Pycaw — Windows system volume control
* Screen Brightness Control — Display brightness control


📂 Project Structure

gesturecontrolled-pc/
│
├── main.py
├── hand_detector.py
├── gesture_recognizer.py
├── testfingers.py
├── mainworking_backup.py
├── hand_landmarker.task
├── requirements.txt
└── README.md
└── screenshots/
   ├── screenshot1.png
   ├── screenshot2.png
   └── screenshot3.png

File Description

main.py — Main application and gesture-control logic
hand_detector.py — Hand detection and landmark processing
gesture_recognizer.py — Recognition of predefined finger gestures
testfingers.py — Testing finger-state detection
mainworking_backup.py — Backup of the working implementation
hand_landmarker.task — MediaPipe hand landmark model
requirements.txt — Python dependencies
README.md — Project documentation


🚀 Installation

Requirements

* Windows PC
* Python 3.x
* Working webcam
* Git

1. Clone the repository

git clone https://github.com/hpallavi23/gesturecontrolled-pc.git

2. Navigate to the project directory

cd gesturecontrolled-pc

3. Create a virtual environment

python -m venv venv

4. Activate the virtual environment

On Windows:

venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt

6. Run the application

python main.py


🎮 How to Use

1. Connect or enable your webcam.
2. Start the application using `main.py`.
3. Position your hand clearly in front of the camera.
4. Perform one of the supported gestures.
5. The corresponding computer action will be triggered.
6. Press `Q` to close the application.

Tips for Better Detection

* Use adequate lighting.
* Keep your hand clearly visible to the webcam.
* Avoid excessive background clutter.
* Perform gestures clearly and deliberately.
* Keep an appropriate distance from the camera.


🖐️ Gesture Recognition

The system represents the state of the five fingers using:

[Thumb, Index, Middle, Ring, Pinky]

For example:

[1, 1, 0, 0, 0]

represents:

Thumb   → Up
Index   → Up
Middle  → Down
Ring    → Down
Pinky   → Down

This pattern is mapped to the **Left Click** gesture.

The gesture-recognition module compares detected finger states with predefined patterns and identifies the corresponding gesture.


🔄 Gesture Stabilization

To make gesture detection more reliable, the system uses frame-based counting and gesture history.

For actions such as clicking and YouTube play/pause, the gesture must remain stable for a certain number of frames before the action is triggered.

This helps reduce accidental actions caused by brief changes in hand position or detection noise.


⚠️ Limitations

* Requires a working webcam.
* Designed and tested primarily for Windows.
* Gesture detection can be affected by poor lighting.
* Hand visibility and camera positioning can affect recognition.
* Gestures need to be performed clearly.
* Some controls rely on Windows-specific functionality.

🔮 Future Improvements

Possible future improvements include:

* Customizable gesture-to-action mappings.
* Improved recognition under different lighting conditions.
* Support for additional gestures.
* User interface for configuring gestures.
* Multiple-hand gesture support.
* Cross-platform support.


📌 Project Highlights

* Real-time webcam-based interaction
* Computer vision-based hand tracking
* 9 implemented computer-control features
* Gesture stabilization for improved reliability
* Windows system-level controls
* Hands-free interaction with common PC functions


💅 Author

Pallavi Hadgalle

B.Tech Computer Science Engineering Student

GitHub: [hpallavi23](https://github.com/hpallavi23)



📄 License

This project is intended for educational and portfolio purposes.
