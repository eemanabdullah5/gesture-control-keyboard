import json

def load_config():
    """Loads the user configuration settings."""
    with open("config.json", "r") as file:
        return json.load(file)

def get_finger_states(hand_landmarks):
    """
    Determines if fingers are open (True) or closed (False).
    With the modern API, hand_landmarks is a direct list, so we read it using index notation.
    """
    finger_tips = [8, 12, 16, 20]   # Index, Middle, Ring, Pinky
    finger_pip_joints = [6, 10, 14, 18]
    
    states = []
    
    # Check 4 fingers (Index, Middle, Ring, Pinky)
    for tip, joint in zip(finger_tips, finger_pip_joints):
        # FIXED: Removed '.landmark' because hand_landmarks is already the list of landmarks!
        if hand_landmarks[tip].y < hand_landmarks[joint].y:
            states.append(True)  # Finger is open
        else:
            states.append(False) # Finger is closed
            
    return states

def recognize_gesture(hand_landmarks):
    """Matches finger states to a specific named gesture."""
    # Get states for [Index, Middle, Ring, Pinky]
    fingers = get_finger_states(hand_landmarks)
    
    # Check Thumb separately using direct list index
    # FIXED: Removed '.landmark'
    thumb_is_open = hand_landmarks[4].x < hand_landmarks[3].x
    
    # Logic matching
    if not thumb_is_open and all(f == False for f in fingers):
        return "FIST"
    
    elif thumb_is_open and all(f == False for f in fingers):
        return "THUMB_UP"
        
    elif not thumb_is_open and fingers[0] == True and fingers[1] == True and fingers[2] == False and fingers[3] == False:
        return "PEACE_SIGN"
        
    return "UNKNOWN"