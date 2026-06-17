import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui
import time
import utils

# 1. Load configuration settings
config = utils.load_config()
COOLDOWN = config["cooldown_time"]
GESTURE_MAP = config["gestures"]

last_action_time = 0

# 2. Setup Modern MediaPipe Hand Landmarker Tasks API
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO, # Configured specifically for webcams
    num_hands=1
)
detector = vision.HandLandmarker.create_from_options(options)

# 3. Start Video Capture
cap = cv2.VideoCapture(0)
print("Pipeline initialized successfully using Modern Tasks API. Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    # Mirror effect for natural UI interaction
    frame = cv2.flip(frame, 1)
    
    # MediaPipe Tasks require RGB format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
    # Calculate timestamps in milliseconds for the video tracker
    frame_timestamp_ms = int(time.time() * 1000)
    detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
    
    gesture_detected = "NONE"
    
    # If a hand skeleton is found
    if detection_result.hand_landmarks:
        # Pull the first detected hand
        hand_landmarks = detection_result.hand_landmarks[0]
        
        # Identify the gesture using our utils code
        # Note: Tasks structure returns object types, so we pass the object cleanly
        gesture_detected = utils.recognize_gesture(detection_result.hand_landmarks[0])
        
        # Match gesture to execution keys
        if gesture_detected in GESTURE_MAP:
            now = time.time()
            if now - last_action_time > COOLDOWN:
                target_key = GESTURE_MAP[gesture_detected]
                pyautogui.press(target_key)
                print(f"🔥 Triggered: {gesture_detected} -> Pressed: '{target_key}'")
                last_action_time = now

        # Draw raw bounding joints onto screen manually for feedback
        for landmark in hand_landmarks:
            cx, cy = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

    # 4. Display Status Dashboard HUD overlay
    cv2.rectangle(frame, (10, 10), (280, 50), (0, 0, 0), -1)
    cv2.putText(frame, f"Gesture: {gesture_detected}", (20, 38), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow('AI Gesture Keyboard Dashboard', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()