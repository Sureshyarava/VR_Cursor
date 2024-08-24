# Hand Gesture-Controlled Cursor

This project implements a hand gesture-controlled cursor using computer vision and hand tracking. It allows users to control their computer's cursor and perform mouse actions using hand gestures captured by a webcam.

## Features

- Control cursor movement using hand gestures
- Perform left-click, right-click, and drag-and-drop actions
- Stabilized cursor movement for improved accuracy
- Real-time hand tracking visualization

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI

## Installation

1. Clone this repository or download the script.
2. Install the required packages:


## Usage

1. Run the script: python hand_gesture_cursor.py | python3 hand_gesture_cursor.py


2. Position your hand in front of the webcam.
3. Use the following gestures to control the cursor:
   - Move your hand to move the cursor
   - Raise only your index finger for a left-click
   - Raise only your middle finger for a right-click
   - Raise both index and middle fingers to start dragging
   - Raise index, middle, and ring fingers to drop (end dragging)

4. Press 'q' to quit the application.

## Customization

You can adjust the following parameters in the script to fine-tune the behavior:

- `smoothing`: Higher values increase stability but may introduce lag
- `dead_zone`: Adjust to change sensitivity to small movements
- `ema_factor`: Controls the exponential moving average (lower for more smoothing)
- `stability_threshold`: Increase to make the cursor more stable when the hand is still
- `movement_scale`: Adjust overall cursor sensitivity

## Limitations

- Requires good lighting conditions for accurate hand tracking
- May not work well with complex backgrounds or multiple moving objects in the frame
- Performance may vary depending on the computer's processing power

## Future Improvements

- Add more gestures for additional mouse actions
- Implement palm orientation detection for 3D cursor control
- Enhance stability and accuracy of hand tracking
- Add user interface for easy parameter adjustment


## Acknowledgements

This project uses the MediaPipe library for hand tracking and OpenCV for image processing.
