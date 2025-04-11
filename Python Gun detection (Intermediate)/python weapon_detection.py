import numpy as np
import cv2
import imutils
import datetime
import os
import time
import pygame
from pathlib import Path
import torch
import gc


pygame.mixer.init()

class WeaponDetectionSystem:
    def __init__(self):
        # Create directory for storing detected weapon images if it doesn't exist
        self.save_dir = Path("detected_weapons")
        self.save_dir.mkdir(exist_ok=True)
        
        # Force CUDA usage if available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if self.device == 'cuda':
            # Clear GPU memory
            torch.cuda.empty_cache()
            gc.collect()
            print("🚀 Using GPU acceleration!")
        else:
            print("⚠️ GPU not available, using CPU")
        
        # Load YOLOv5 model - use a slightly larger model for better detection
        print("🔄 Loading YOLOv5s model for better detection accuracy...")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, force_reload=True)
        
        # Force model to use CUDA if available
        self.model.to(self.device)
        
        # Set model parameters for better detection (lower confidence threshold)
        self.model.conf = 0.2      # Lower confidence threshold for better detection
        self.model.iou = 0.4       # Slightly lower IOU threshold for NMS
        self.model.agnostic = True # Class-agnostic NMS
        self.model.multi_label = False # Single-label per box
        self.model.max_det = 20    # Maximum number of detections
        
        # Expanded list of weapon classes to detect
        self.weapon_classes = [
            "knife", "scissors", "fork", "bottle", 
            "pistol", "revolver", "shotgun", "rifle",
            "sword", "axe", "dagger", "machete", "bat"
        ]
        
        # Class IDs in COCO dataset that might represent weapons
        # 43: knife, 76: scissors, 44: spoon, 46: wine glass, 41: cup
        self.weapon_class_ids = [43, 76, 44, 46, 41]
        
        # Load alarm sound
        self.alarm_sound = pygame.mixer.Sound("alarm.wav")
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Could not open video device")
        
        # Set camera properties
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Frame processing settings - process every other frame for better performance/detection balance
        self.process_every_n_frames = 2 # Process every 2nd frame instead of every 3rd
        self.frame_count = 0
        self.last_result = []  # Cache last detection result
        
        print(f"Enhanced Weapon Detection System initialized successfully!")

    def is_weapon(self, class_name, class_id):
        """Improved method to determine if the detected object is a potential weapon"""
        # Check if class name is in our weapon classes
        if class_name.lower() in [c.lower() for c in self.weapon_classes]:
            return True
            
        # Check if class ID is in our list of potential weapon class IDs
        if class_id in self.weapon_class_ids:
            return True
            
        # Enhanced check for knife-related terms with more keywords
        weapon_keywords = ["knife", "blade", "sword", "cutter", "dagger", "gun", "pistol", "rifle"]
        for keyword in weapon_keywords:
            if keyword in class_name.lower():
                return True
            
        return False

    @torch.no_grad()  # Disable gradient calculation for faster inference
    def detect_weapons(self, frame):
        try:
            # Convert OpenCV BGR to RGB format for the model
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Run inference with half precision for faster GPU processing
            with torch.cuda.amp.autocast(enabled=self.device=='cuda'):
                results = self.model(rgb_frame, size=416)  # Increased inference size for better detection
            
            # Extract predictions
            predictions = results.pandas().xyxy[0]
            
            detected_weapons = []
            
            # Process the results
            for _, prediction in predictions.iterrows():
                # Extract class and confidence
                class_id = int(prediction['class'])
                class_name = prediction['name']
                confidence = float(prediction['confidence'])
                
                # Skip if not a potential weapon
                if not self.is_weapon(class_name, class_id):
                    continue
                
                # Extract bounding box coordinates
                x1, y1 = int(prediction['xmin']), int(prediction['ymin'])
                x2, y2 = int(prediction['xmax']), int(prediction['ymax'])
                
                detected_weapons.append({
                    'class': class_name,
                    'confidence': confidence,
                    'box': (x1, y1, x2, y2)
                })
            
            return detected_weapons
        except Exception as e:
            print(f"Error during detection: {e}")
            return []

    def run(self):
        alarm_active = False
        alarm_cooldown = 0
        
        # FPS calculation variables
        fps_start_time = time.time()
        fps_frame_count = 0
        fps = 0
        
        # Cache for detections with detection streak counter
        cached_detections = []
        detection_streak = 0  # Count consecutive frames with detections
        
        # Configure OpenCV for maximum performance
        cv2.setUseOptimized(True)
        cv2.setNumThreads(4)  # Use multiple threads
        
        while True:
            try:
                # Measure time for FPS calculation
                frame_start_time = time.time()
                
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Count frames
                self.frame_count += 1
                
                # For display purposes
                display_frame = frame.copy()
                
                # Process more frames for better detection
                if self.frame_count % self.process_every_n_frames == 0:
                    # Resize frame
                    frame = cv2.resize(frame, (416, 312))  # Slight increase in size
                    
                    # Apply simple contrast enhancement to help with detection
                    frame = cv2.convertScaleAbs(frame, alpha=1.1, beta=5)
                    
                    # Detect weapons in the frame
                    detected_weapons = self.detect_weapons(frame)
                    
                    # Update our cache
                    cached_detections = detected_weapons
                    
                    # Update detection streak
                    if detected_weapons:
                        detection_streak += 1
                    else:
                        detection_streak = 0
                else:
                    # Use cached detections for frames we skip processing
                    detected_weapons = cached_detections
                
                # Scale detection boxes to display frame size if needed
                scale_x = display_frame.shape[1] / 416
                scale_y = display_frame.shape[0] / 312
                
                # If weapons are detected or we have a detection streak, trigger alarm
                current_time = time.time()
                if (detected_weapons or detection_streak >= 2) and current_time > alarm_cooldown:
                    if not alarm_active:
                        # Play alarm sound
                        self.alarm_sound.play(-1)
                        alarm_active = True
                        
                        # Save a snapshot
                        if detected_weapons:
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            full_path = str(self.save_dir / f"weapon_{timestamp}.jpg")
                            cv2.imwrite(full_path, display_frame)
                            
                        # Set alarm cooldown
                        alarm_cooldown = current_time + 3  # Reduced cooldown to 3 seconds
                elif not detected_weapons and detection_streak < 2 and alarm_active:
                    # Stop alarm if no weapons are detected
                    pygame.mixer.stop()
                    alarm_active = False
                
                # Draw detection results on the display frame
                for weapon in detected_weapons:
                    x1, y1, x2, y2 = weapon['box']
                    
                    # Scale coordinates if frame was resized
                    if self.frame_count % self.process_every_n_frames != 0:
                        x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
                        y1, y2 = int(y1 * scale_y), int(y2 * scale_y)
                    
                    weapon_class = weapon['class']
                    confidence = weapon['confidence']
                    
                    # Use rectangle with filled red background for better visibility
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    
                    # Enhanced label with confidence
                    label = f"{weapon_class} ({confidence:.2f})"
                    cv2.putText(display_frame, label, (x1, y1 - 5),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                # Calculate FPS
                fps_frame_count += 1
                if fps_frame_count >= 5:
                    current_time = time.time()
                    fps = fps_frame_count / (current_time - fps_start_time)
                    fps_start_time = current_time
                    fps_frame_count = 0
                
                # Add status information
                if detected_weapons:
                    status_text = f"ALERT! {len(detected_weapons)} weapon(s)"
                    cv2.putText(display_frame, status_text, (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    cv2.putText(display_frame, "No weapons detected", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Add FPS counter
                cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                # Add detection mode info
                detection_mode = "HIGH SENSITIVITY" if self.model.conf <= 0.2 else "NORMAL"
                cv2.putText(display_frame, f"Mode: {detection_mode}", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                # Display the frame
                cv2.imshow("Enhanced Weapon Detection System", display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):  # Toggle sensitivity
                    if self.model.conf > 0.15:
                        self.model.conf = 0.15  # Higher sensitivity
                        print("Switched to high sensitivity mode")
                    else:
                        self.model.conf = 0.25  # Normal sensitivity
                        print("Switched to normal sensitivity mode")
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                continue
        
        # Clean up
        if alarm_active:
            pygame.mixer.stop()
        self.camera.release()
        cv2.destroyAllWindows()
        
        # Clean up CUDA memory
        if self.device == 'cuda':
            torch.cuda.empty_cache()
            gc.collect()

if __name__ == "__main__":
    try:
        # Check if we need to create a dummy alarm file
        if not os.path.exists("alarm.wav"):
            print("Alarm sound file not found, creating a simple one...")
            import wave
            import struct
            
            # Create a simple alarm sound file
            with wave.open("alarm.wav", "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(44100)
                for i in range(0, 44100 * 1):  # 1 second of sound
                    value = 32767 if i % 1000 < 500 else -32767  # Simple square wave
                    f.writeframes(struct.pack('h', int(value)))
            print("Created alarm.wav file")
            
        # Create and run the detection system
        weapon_detector = WeaponDetectionSystem()
        weapon_detector.run()
        
    except Exception as e:
        print(f"Error: {e}")