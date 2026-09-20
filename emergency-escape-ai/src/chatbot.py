from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Chatbot:
    def __init__(self):
        self.intents = {
            "fire emergency": ["fire", "smoke", "flames", "burning", "blaze", "burn"],
            "medical help": ["hurt", "injury", "pain", "sick", "bleeding", "breathe", "broken", "fracture", "ambulance", "doctor"],
            "hazard": ["danger", "risk", "hazard", "unsafe", "collapse", "trapped", "stuck"],
            "general inquiry": ["help", "assistance", "question", "info", "where", "how", "what", "exit"]
        }
        self.responses = {
            "fire emergency": "🚨 FIRE EMERGENCY!\n\n✅ IMMEDIATE ACTIONS:\n1. Evacuate immediately!\n2. Use stairs, NOT elevators\n3. Crawl if smoke is present\n4. Close doors behind you\n5. Meet at assembly point\n6. Emergency services called",
            
            "medical help": "🚑 MEDICAL EMERGENCY!\n\n✅ IMMEDIATE ACTIONS:\n1. Stay calm and take deep breaths\n2. Sit or lie down safely\n3. Help is on the way\n4. Don't move if spinal injury suspected\n5. Apply pressure if bleeding\n6. Ambulance ETA: 4-5 minutes",
            
            "hazard": "⚠️ HAZARD DETECTED!\n\n✅ IMMEDIATE ACTIONS:\n1. Avoid the hazardous area\n2. Seek a safe location\n3. Alert nearby people\n4. Emergency services notified\n5. Rerouting to safe exit\n6. Stay calm and follow directions",
            
            "general inquiry": "👋 EMERGENCY ASSISTANCE\n\n❓ To help you better, please describe:\n- What type of emergency? (fire, medical, hazard)\n- Your current location?\n- Number of people affected?\n- Any injuries?\n\nEmergency Line: 112"
        }

    def classify_intent(self, user_input):
        """Classify user input into an intent category"""
        if not user_input:
            return "general inquiry"
        
        user_input_lower = user_input.lower().strip()
        intent_scores = {}

        for intent, keywords in self.intents.items():
            score = sum(1 for keyword in keywords if keyword in user_input_lower)
            intent_scores[intent] = score

        # Find best matching intent
        best_intent = max(intent_scores, key=intent_scores.get)
        
        # Return best intent if it has at least 1 match, otherwise general inquiry
        if intent_scores[best_intent] > 0:
            return best_intent
        else:
            return "general inquiry"

    def get_response(self, user_input):
        """Get chatbot response based on user input"""
        try:
            if not user_input or not user_input.strip():
                return "Please describe your emergency situation."
            
            intent = self.classify_intent(user_input)
            response = self.responses.get(intent, self.responses["general inquiry"])
            
            return response
        except Exception as e:
            return f"⚠️ Error processing request. Emergency services contacted. Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    chatbot = Chatbot()
    user_input = input("Enter your emergency message: ")
    response = chatbot.get_response(user_input)
    print(response)