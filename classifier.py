import math

class GestureDetector:
    def __init__(self, threshold_data=None):
        self.finger_threshold = 0.0
        if threshold_data and "finger_open_y_threshold" in threshold_data:
            self.finger_threshold = threshold_data["finger_open_y_threshold"]

    def detect(self, hand_landmarks):
        landmarks = hand_landmarks.landmark
        
        # Determine Left vs Right Hand
        wrist_x = landmarks[0].x
        hand_side = "Left" if wrist_x < 0.5 else "Right"
        
        # 1. Standard Finger Counting 
        tips = [8, 12, 16, 20] 
        mcps = [5, 9, 13, 17]  
        
        fingers_up_list = []
        for tip, mcp in zip(tips, mcps):
            if (landmarks[tip].y - landmarks[mcp].y) < self.finger_threshold:
                fingers_up_list.append(1) 
            else:
                fingers_up_list.append(0) 
                
        fingers_up = sum(fingers_up_list)
        
        # --- 2. FOOLPROOF STRICT TRACKING FOR EXIT GESTURE ---
        # We check if the tip is physically lower than the middle joint (PIP)
        index_up_strict = landmarks[8].y < landmarks[6].y
        middle_up_strict = landmarks[12].y < landmarks[10].y
        ring_down_strict = landmarks[16].y > landmarks[14].y
        pinky_down_strict = landmarks[20].y > landmarks[18].y
        
        # A thumb is "extended" if the tip (4) is far away from the pinky base (17)
        thumb_extended = math.hypot(landmarks[4].x - landmarks[17].x, landmarks[4].y - landmarks[17].y) > 0.12

        shape = "None"
        
        # --- 3. THE EXIT COMMAND ---
        if thumb_extended and index_up_strict and middle_up_strict and ring_down_strict and pinky_down_strict:
            shape = "Thumb_Index_Middle"
        
        # Standard shapes fallback
        elif fingers_up >= 4:
            shape = "Open Palm"
        elif fingers_up == 0:
            shape = "Fist"
        elif fingers_up == 1:
            shape = "1 Finger"
        elif fingers_up == 2:
            shape = "2 Fingers"
        elif fingers_up == 3:
            shape = "3 Fingers"

        if shape != "None":
            return f"{hand_side}_{shape}"
        return "None"