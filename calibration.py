# calibration.py
import cv2
import json
import time
import os

class CalibrationManager:
    def __init__(self, profile_path="profile.json"):
        self.profile_path = profile_path
        # Default fallback threshold if calibration hasn't run
        self.thresholds = {"finger_open_y_threshold": 0.0} 

    def load_profile(self):
        """Loads the user profile if it exists."""
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                self.thresholds = json.load(f)
            print(f"✅ User profile loaded from {self.profile_path}")
            return True
        return False

    def run_calibration(self, cap, hands):
        """Runs the 30-second guided onboarding to train gesture thresholds."""
        print("\n--- 🛠️ Starting Calibration Mode ---")
        
        target_gestures = ["Open Palm", "Fist"]
        calibration_data = {"Open Palm": [], "Fist": []}
        
        for gesture in target_gestures:
            print(f"Get ready to show your {gesture}...")
            cv2.waitKey(3000) # 3 second prep time
            
            print(f"Capturing {gesture}... Hold still for 2s!")
            start_time = time.time()
            
            # Capture data for 2 seconds
            while time.time() - start_time < 2.0:
                ret, frame = cap.read()
                if not ret: continue
                
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        landmarks = hand_landmarks.landmark
                        tips = [8, 12, 16, 20]
                        mcps = [5, 9, 13, 17]
                        
                        # Calculate the average Y-distance between tips and knuckles
                        avg_diff = sum([landmarks[tip].y - landmarks[mcp].y for tip, mcp in zip(tips, mcps)]) / 4.0
                        calibration_data[gesture].append(avg_diff)
                        
                # Draw UI for the user
                cv2.putText(frame, f"Calibrating: {gesture}", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                cv2.imshow('Calibration', frame)
                cv2.waitKey(1)
        
        # Calculate and save the personalized threshold
        if calibration_data["Open Palm"] and calibration_data["Fist"]:
            avg_open = sum(calibration_data["Open Palm"]) / len(calibration_data["Open Palm"])
            avg_fist = sum(calibration_data["Fist"]) / len(calibration_data["Fist"])
            
            # The ideal threshold is exactly between their open palm and closed fist values
            self.thresholds["finger_open_y_threshold"] = (avg_open + avg_fist) / 2.0
            
            with open(self.profile_path, 'w') as f:
                json.dump(self.thresholds, f)
            print(f"✅ Calibration saved to {self.profile_path}")
        else:
            print("❌ Calibration failed. Could not detect hands.")
        
        cv2.destroyAllWindows()