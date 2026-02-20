import pyautogui
import time

class MediaController:
    def __init__(self):
        self.last_trigger_time = {}
        self.default_cooldown = 0.5 
        
        # The flag to tell the main program when it is time to stop
        self.should_exit = False 
        
        self.cooldowns = {
            "Left_Open Palm": 1.0,           # Play/Pause
            "Left_Fist": 1.0,                # Full Screen
            "Left_1 Finger": 0.5,            # Rewind (Moved from Right Hand)
            "Left_Thumb_Index_Middle": 1.0,  # Exit the program
            "Right_1 Finger": 0.5,           # Fast Forward
            "Right_2 Fingers": 0.2,          # Volume Up
            "Right_3 Fingers": 0.2,          # Volume Down
            "Right_Fist": 1.0                # Mute Toggle
        }

    def trigger_action(self, gesture):
        if gesture == "None":
            return False

        current_time = time.time()
        cooldown_ms = self.cooldowns.get(gesture, self.default_cooldown)
        last_time = self.last_trigger_time.get(gesture, 0)
        
        if (current_time - last_time) > cooldown_ms:
            self._execute(gesture)
            self.last_trigger_time[gesture] = current_time 
            return True 
            
        return False 

    def _execute(self, gesture):
        # --- LEFT HAND (Playback, Screen, Rewind, Exit) ---
        if gesture == "Left_Open Palm":
            pyautogui.press('playpause')          
            print("▶️/⏸️ Action: Play/Pause (Left Hand)")
            
        elif gesture == "Left_Fist":
            pyautogui.press('f')              
            print("🔲 Action: Fullscreen Toggle (Left Hand)")
            
        elif gesture == "Left_1 Finger":   
            pyautogui.hotkey('shift', 'left')   
            print("⏪ Action: Rewind (Left Hand)")
            
        elif gesture == "Left_Thumb_Index_Middle":
            # Flip the exit switch!
            self.should_exit = True
            print("🛑 Action: EXIT TRIGGERED (Left Hand)")
            
        # --- RIGHT HAND (Navigation & Volume) ---
        elif gesture == "Right_1 Finger":        
            pyautogui.hotkey('shift', 'right')  
            print("⏩ Action: Fast Forward (Right Hand)")
            
        elif gesture == "Right_2 Fingers":      
            pyautogui.press('volumeup')    
            print("🔊 Action: Volume Up (Right Hand)")
            
        elif gesture == "Right_3 Fingers":           
            pyautogui.press('volumedown')  
            print("🔉 Action: Volume Down (Right Hand)")
            
        elif gesture == "Right_Fist":
            pyautogui.press('volumemute')
            print("🔇 Action: Mute Toggle (Right Hand)")