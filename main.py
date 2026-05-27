import cv2
import numpy as np
from gesture_recognition import GestureRecognizer
from face_recognition_module import FaceRecognizer
from text_to_speech import TextToSpeech
from communication_dictionary import CommunicationDictionary
import threading
import time

class JarvisDeafDumbCommunication:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.gesture_recognizer = GestureRecognizer()
        self.face_recognizer = FaceRecognizer()
        self.tts = TextToSpeech()
        self.dictionary = CommunicationDictionary()
        
        self.detected_text = ""
        self.gesture_cooldown = 0
        self.running = True
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
    def process_frame(self, frame):
        """Process frame for face and gesture detection"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Face detection
        faces, face_frame = self.face_recognizer.detect_faces(frame)
        
        # Gesture recognition
        gesture, hand_frame = self.gesture_recognizer.process_frame(frame)
        
        # Get gesture meaning
        if gesture and self.gesture_cooldown <= 0:
            meaning = self.dictionary.get_gesture_meaning(gesture)
            if meaning:
                self.detected_text += meaning + " "
                self.gesture_cooldown = 30  # 1 second cooldown at 30 FPS
                print(f"Detected: {gesture} -> {meaning}")
                # Speak in background thread
                threading.Thread(target=self.tts.speak, args=(meaning,), daemon=True).start()
        
        if self.gesture_cooldown > 0:
            self.gesture_cooldown -= 1
        
        # Combine frames
        output_frame = cv2.addWeighted(face_frame, 0.5, hand_frame, 0.5, 0)
        
        return output_frame
    
    def draw_ui(self, frame):
        """Draw user interface elements"""
        # FPS calculation
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        if elapsed > 1:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = time.time()
        
        # Draw text box
        cv2.rectangle(frame, (10, 60), (1270, 120), (0, 0, 0), -1)
        cv2.putText(frame, f"Detected: {self.detected_text}", (20, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw FPS
        cv2.putText(frame, f"FPS: {self.fps:.1f}", (1100, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw controls
        controls = ["Q: Quit", "C: Clear", "S: Speak", "D: Dictionary"]
        for i, control in enumerate(controls):
            cv2.putText(frame, control, (10, 650 + i*25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        return frame
    
    def show_dictionary(self):
        """Display gesture dictionary"""
        dictionary_text = self.dictionary.get_all_meanings()
        print("\n" + "="*50)
        print("GESTURE DICTIONARY")
        print("="*50)
        for gesture, meaning in dictionary_text.items():
            print(f"{gesture:20s} -> {meaning}")
        print("="*50 + "\n")
    
    def run(self):
        """Main application loop"""
        print("JARVIS - Deaf & Dumb Communication System")
        print("Starting... Press Q to quit")
        
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            # Process detections
            frame = self.process_frame(frame)
            
            # Draw UI
            frame = self.draw_ui(frame)
            
            cv2.imshow("JARVIS - Deaf & Dumb Communication", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
            elif key == ord('c'):
                self.detected_text = ""
                print("Text cleared")
            elif key == ord('s'):
                if self.detected_text:
                    threading.Thread(target=self.tts.speak, args=(self.detected_text,), daemon=True).start()
            elif key == ord('d'):
                self.show_dictionary()
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = JarvisDeafDumbCommunication()
    app.run()
