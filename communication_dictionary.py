class CommunicationDictionary:
    def __init__(self):
        self.gesture_meanings = {
            "Thumbs Up": "Yes, I agree with you",
            "OK Sign": "Okay, that's fine",
            "Peace Sign": "You are my friend",
            "Open Palm": "Stop, please",
            "Waving": "Hello, how are you?"
        }
        
        self.emergency_phrases = [
            "I need help",
            "Call the doctor",
            "I am in pain",
            "Please help me"
        ]
        
        self.common_phrases = [
            "Good morning",
            "Good afternoon",
            "Good night",
            "Thank you",
            "Yes",
            "No",
            "I don't understand",
            "Can you help me?",
            "Where is the bathroom?",
            "I am hungry",
            "I am thirsty",
            "What is your name?"
        ]
    
    def get_gesture_meaning(self, gesture):
        """Get meaning of a gesture"""
        return self.gesture_meanings.get(gesture, None)
    
    def add_custom_phrase(self, phrase):
        """Add custom phrase"""
        if phrase not in self.common_phrases:
            self.common_phrases.append(phrase)
    
    def search_phrase(self, keyword):
        """Search phrases by keyword"""
        results = [p for p in self.common_phrases if keyword.lower() in p.lower()]
        return results
    
    def get_all_meanings(self):
        """Get all gesture meanings"""
        return self.gesture_meanings
