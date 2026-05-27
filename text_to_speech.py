import pyttsx3
import threading
import queue

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        self.speech_queue = queue.Queue()
        self.speaking = False
        
    def speak(self, text):
        """Convert text to speech"""
        if not text:
            return
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
    
    def set_rate(self, rate):
        """Set speech rate (50-300)"""
        self.engine.setProperty('rate', max(50, min(300, rate)))
    
    def set_volume(self, volume):
        """Set volume (0.0-1.0)"""
        self.engine.setProperty('volume', max(0, min(1, volume)))
