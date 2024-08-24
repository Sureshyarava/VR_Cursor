import cv2
import mediapipe as mp
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hand = mp_hands.Hands(min_detection_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

# Smoothing and stability parameters
smoothing = 20
dead_zone = 0.05
ema_factor = 1
stability_threshold = 20
stability_counter = 0

prev_x, prev_y = screen_width // 2, screen_height // 2
ema_x, ema_y = prev_x, prev_y

is_dragging = False
movement_scale = 1.2


def get_hand_depth(landmarks):
    return np.mean([lm.z for lm in landmarks])


def get_palm_center(hand_landmarks):
    palm_landmarks = [0, 1, 5, 9, 13, 17]
    landmarks = hand_landmarks.landmark
    return np.mean([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in palm_landmarks], axis=0)


def is_finger_raised(hand_landmarks, finger_tip_id, finger_pip_id):
    return hand_landmarks.landmark[finger_tip_id].y < hand_landmarks.landmark[finger_pip_id].y


def scale_movement(x, y, scale):
    center_x, center_y = 0.5, 0.5
    scaled_x = (x - center_x) * scale + center_x
    scaled_y = (y - center_y) * scale + center_y
    return max(0, min(1, scaled_x)), max(0, min(1, scaled_y))


while True:
    success, frame = cap.read()
    if success:
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(rgb_frame)
        if result.multi_hand_landmarks:
            result_handmarks = result.multi_hand_landmarks[0]  # Use the first detected hand

            mp_drawing.draw_landmarks(frame, result_handmarks, mp_hands.HAND_CONNECTIONS)

            palm_center = get_palm_center(result_handmarks)
            scaled_x, scaled_y = scale_movement(palm_center[0], palm_center[1], movement_scale)

            x = int(scaled_x * screen_width)
            y = int(scaled_y * screen_height)

            # Apply dead zone
            if abs(x - prev_x) < dead_zone * screen_width and abs(y - prev_y) < dead_zone * screen_height:
                stability_counter += 1
                if stability_counter > stability_threshold:
                    x, y = prev_x, prev_y
            else:
                stability_counter = 0

            # Apply EMA
            ema_x = ema_factor * x + (1 - ema_factor) * ema_x
            ema_y = ema_factor * y + (1 - ema_factor) * ema_y

            # Smooth the movement
            x = int(prev_x + (ema_x - prev_x) / smoothing)
            y = int(prev_y + (ema_y - prev_y) / smoothing)

            # Move cursor
            pyautogui.moveTo(x, y)

            prev_x, prev_y = x, y

            # Check finger states
            index_raised = is_finger_raised(result_handmarks, 8, 6)
            middle_raised = is_finger_raised(result_handmarks, 12, 10)
            ring_raised = is_finger_raised(result_handmarks, 16, 14)

            if index_raised and not middle_raised and not ring_raised:
                pyautogui.click()
                print("Left Click!")
            elif not index_raised and middle_raised and not ring_raised:
                pyautogui.rightClick()
                print("Right Click!")
            elif index_raised and middle_raised and not ring_raised:
                if not is_dragging:
                    pyautogui.mouseDown()
                    is_dragging = True
                    print("Start Dragging")
                else:
                    print("Dragging...")
            elif index_raised and middle_raised and ring_raised:
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                    print("Drop")
            else:
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                    print("Stop Dragging")

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
