import cv2
import numpy as np
from collections import deque

class HUDOverlay:
    def __init__(self):
        # A lightweight buffer to hold the last 5 gestures
        self.history = deque(maxlen=5)
        self.last_gesture = None
        
    def update_history(self, gesture):
        """Adds to history only when a new, distinct gesture is detected."""
        if gesture != "None" and gesture != self.last_gesture:
            self.history.appendleft(gesture) # Add newest to the top
            self.last_gesture = gesture

    def draw(self, frame, current_gesture, fps, confidence=100):
        """Renders the transparent dashboard on the current frame."""
        # Get frame dimensions
        h, w, _ = frame.shape
        
        # 1. Create a semi-transparent header bar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 50), (30, 30, 30), -1) # Dark grey header
        alpha = 0.6  # Transparency factor
        # Blend the overlay with the original frame
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # 2. Render Top Header Metrics (FPS, Confidence, Gesture)
        cv2.putText(frame, f"FPS: {int(fps)}", (15, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
        cv2.putText(frame, f"Conf: {confidence}%", (150, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
        cv2.putText(frame, f"Active: {current_gesture}", (w - 300, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # 3. Render the "Gesture History Ribbon" in the bottom corner
        ribbon_x = w - 220
        ribbon_y = h - 180
        
        # Draw a transparent backing for the history ribbon
        overlay_ribbon = frame.copy()
        cv2.rectangle(overlay_ribbon, (ribbon_x - 10, ribbon_y - 25), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay_ribbon, 0.5, frame, 0.5, 0, frame)

        # Draw the history text
        cv2.putText(frame, "Recent Actions:", (ribbon_x, ribbon_y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        for i, hist_gesture in enumerate(self.history):
            y_offset = ribbon_y + 20 + (i * 25)
            # Make the newest gesture bright white, and older ones fade to grey
            color = (255, 255, 255) if i == 0 else (150, 150, 150)
            cv2.putText(frame, f"> {hist_gesture}", (ribbon_x, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

        return frame