import os
import json
import uuid
from datetime import datetime
from django.conf import settings
from .models import AIChatLog, Prediction, Disease

# Try to import openai, but don't fail if it's not installed
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIChatService:
    def __init__(self):
        # Initialize OpenAI client (you'll need to set OPENAI_API_KEY in settings)
        self.api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if self.api_key and OPENAI_AVAILABLE:
            openai.api_key = self.api_key
        else:
            # Fallback to mock responses for development
            self.api_key = None
    
    def generate_conversation_id(self):
        """Generate a unique conversation ID"""
        return str(uuid.uuid4())
    
    def is_health_related(self, message):
        """Check if the message is health-related"""
        message_lower = message.lower()
        
        # Health-related keywords
        health_keywords = [
            # Medical terms
            'symptom', 'pain', 'ache', 'fever', 'headache', 'cough', 'cold', 'flu',
            'disease', 'illness', 'sick', 'health', 'medical', 'doctor', 'hospital',
            'medicine', 'medication', 'treatment', 'therapy', 'diagnosis',
            
            # Body parts
            'heart', 'lung', 'liver', 'kidney', 'stomach', 'head', 'chest', 'back',
            'arm', 'leg', 'hand', 'foot', 'eye', 'ear', 'nose', 'throat', 'skin',
            
            # Health conditions
            'diabetes', 'hypertension', 'asthma', 'cancer', 'stroke', 'heart disease',
            'blood pressure', 'cholesterol', 'glucose', 'sugar', 'insulin',
            
            # Lifestyle and prevention
            'diet', 'exercise', 'weight', 'bmi', 'smoking', 'alcohol', 'sleep',
            'stress', 'anxiety', 'depression', 'mental health', 'physical health',
            
            # Common health questions
            'how to', 'what is', 'why do', 'when should', 'can i', 'should i',
            'prevent', 'avoid', 'reduce', 'manage', 'control', 'improve',
            
            # Risk factors
            'risk', 'chance', 'probability', 'family history', 'genetic',
            'age', 'gender', 'lifestyle', 'occupation', 'environment',
            
            # General health terms
            'wellness', 'fitness', 'nutrition', 'vitamin', 'supplement',
            'checkup', 'screening', 'test', 'examination', 'consultation'
        ]
        
        # Strong non-health indicators (check these first as they override health keywords)
        strong_non_health = [
            'how do i cook', 'how to cook', 'recipe for', 'best movie', 'watch movie',
            'capital of', 'learn to play', 'how to play', 'teach me', 'cooking',
            'movie recommendation', 'film recommendation', 'music recommendation',
            'learn to play guitar', 'how to play guitar', 'guitar lessons'
        ]
        
        # Check for strong non-health indicators first (these override everything)
        for indicator in strong_non_health:
            if indicator in message_lower:
                return False
        
        # Check if any health keyword is present
        for keyword in health_keywords:
            if keyword in message_lower:
                return True
        
        # Check for common non-health topics to explicitly exclude
        non_health_topics = [
            'weather', 'politics', 'sports', 'entertainment', 'movies', 'music',
            'cooking', 'recipes', 'travel', 'vacation', 'shopping', 'fashion',
            'technology', 'computer', 'phone', 'car', 'house', 'job', 'work',
            'school', 'education', 'math', 'science', 'history', 'geography',
            'joke', 'funny', 'humor', 'game', 'play', 'hobby', 'pet', 'animal',
            'cook', 'pasta', 'food', 'recipe', 'movie', 'film', 'watch', 'capital',
            'country', 'city', 'guitar', 'instrument', 'music', 'learn', 'teach'
        ]
        
        # If message contains non-health topics without health context, it's likely not health-related
        non_health_count = sum(1 for topic in non_health_topics if topic in message_lower)
        if non_health_count > 0 and not any(keyword in message_lower for keyword in health_keywords):
            return False
        
        # Default to health-related for ambiguous cases
        return True
    
    def create_initial_context_message(self, prediction):
        """Create the initial context-aware message from AI"""
        risk_level = prediction.risk_level.title()
        disease_name = prediction.disease.name
        
        initial_message = f"""Hello! I see you just received a {risk_level} risk prediction for {disease_name}. 

I can answer questions about:
• Symptoms and warning signs
• Risk factors and prevention
• Lifestyle modifications
• When to consult a healthcare professional
• General health information

Please note: I'm here to provide general information and support, but I always recommend consulting with a qualified healthcare professional for personalized medical advice and definitive diagnoses.

How can I help you today?"""
        
        return initial_message
    
    def get_system_prompt(self, prediction=None):
        """Get the system prompt for the AI"""
        base_prompt = """You are a helpful but cautious AI health advisor for SymptoScan, an AI-powered health prediction platform. 

IMPORTANT GUIDELINES:
1. Always be supportive and empathetic while maintaining medical accuracy
2. NEVER provide definitive diagnoses - always recommend consulting healthcare professionals
3. Provide general information about symptoms, risk factors, and prevention
4. Encourage healthy lifestyle choices and regular medical checkups
5. If someone reports severe symptoms, immediately recommend seeking emergency medical care
6. Be clear about the limitations of AI health advice
7. Use simple, understandable language while being medically accurate
8. ONLY answer health-related questions - if a question is not health-related, politely redirect the user

Your role is to:
- Provide educational information about health conditions
- Help users understand their risk factors
- Suggest lifestyle modifications
- Guide users toward appropriate medical care
- Offer emotional support and encouragement
- Politely redirect non-health questions to health topics

Remember: You are a supportive health companion, not a replacement for professional medical care."""

        if prediction:
            disease_info = f"""
CONTEXT: The user has received a {prediction.risk_level.title()} risk prediction for {prediction.disease.name}.

Disease Information:
- Name: {prediction.disease.name}
- Description: {prediction.disease.description}
- Common Symptoms: {prediction.disease.symptoms}
- Prevention Tips: {prediction.disease.prevention}

Use this context to provide more relevant and personalized responses while following all safety guidelines.
"""
            return base_prompt + disease_info
        
        return base_prompt
    
    def get_chat_history(self, user, conversation_id, limit=10):
        """Get recent chat history for context"""
        chat_logs = AIChatLog.objects.filter(
            user=user,
            conversation_id=conversation_id
        ).order_by('-timestamp')[:limit]
        
        history = []
        for log in reversed(chat_logs):  # Reverse to get chronological order
            if log.is_user_message:
                history.append({"role": "user", "content": log.message})
            else:
                history.append({"role": "assistant", "content": log.response})
        
        return history
    
    def generate_response(self, user, message, prediction=None, conversation_id=None):
        """Generate AI response using OpenAI API or fallback"""
        
        # Create conversation ID if not provided
        if not conversation_id:
            conversation_id = self.generate_conversation_id()
        
        # Check if the message is health-related
        is_health_related = self.is_health_related(message)
        
        # If not health-related, provide a warning response
        if not is_health_related:
            warning_response = """⚠️ **Health Focus Reminder**

I'm designed specifically to help with health-related questions and concerns. Your question appears to be outside my area of expertise.

I can help you with:
• Health symptoms and conditions
• Disease risk factors and prevention
• Lifestyle and wellness advice
• Medical terminology explanations
• General health information

Please feel free to ask me any health-related questions! How can I assist you with your health concerns today?"""
            
            # Save the conversation to database
            self._save_conversation(user, message, warning_response, prediction, conversation_id)
            
            return {
                'response': warning_response,
                'conversation_id': conversation_id,
                'is_health_related': False
            }
        
        # Get chat history for context
        chat_history = self.get_chat_history(user, conversation_id)
        
        # Prepare messages for API
        messages = [
            {"role": "system", "content": self.get_system_prompt(prediction)}
        ]
        
        # Add chat history
        messages.extend(chat_history)
        
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        try:
            if self.api_key and OPENAI_AVAILABLE:
                # Use OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7,
                    presence_penalty=0.1,
                    frequency_penalty=0.1
                )
                ai_response = response.choices[0].message.content.strip()
            else:
                # Fallback mock response for development
                ai_response = self._generate_mock_response(message, prediction)
            
            # Save the conversation to database
            self._save_conversation(user, message, ai_response, prediction, conversation_id)
            
            return {
                'response': ai_response,
                'conversation_id': conversation_id,
                'is_health_related': True
            }
            
        except Exception as e:
            # Fallback response in case of API error
            fallback_response = "I apologize, but I'm experiencing technical difficulties right now. Please try again later, and remember to consult with a healthcare professional for any medical concerns."
            
            # Save the conversation even with fallback response
            self._save_conversation(user, message, fallback_response, prediction, conversation_id)
            
            return {
                'response': fallback_response,
                'conversation_id': conversation_id,
                'error': str(e),
                'is_health_related': True  # Assume health-related for error cases
            }
    
    def _generate_mock_response(self, message, prediction):
        """Generate mock responses for development when API is not available"""
        message_lower = message.lower()
        
        # Check if the message is health-related
        if not self.is_health_related(message):
            return """⚠️ **Health Focus Reminder**

I'm designed specifically to help with health-related questions and concerns. Your question appears to be outside my area of expertise.

I can help you with:
• Health symptoms and conditions
• Disease risk factors and prevention
• Lifestyle and wellness advice
• Medical terminology explanations
• General health information

Please feel free to ask me any health-related questions! How can I assist you with your health concerns today?"""
        
        if prediction:
            disease_name = prediction.disease.name
            risk_level = prediction.risk_level.title()
            
            if any(word in message_lower for word in ['symptom', 'sign', 'feel']):
                return f"Common symptoms of {disease_name} include {prediction.disease.symptoms[:100]}... However, symptoms can vary between individuals. It's important to consult with a healthcare professional for proper evaluation."
            
            elif any(word in message_lower for word in ['prevent', 'avoid', 'reduce']):
                return f"To help reduce your risk of {disease_name}, consider: {prediction.disease.prevention[:150]}... Remember, these are general guidelines and you should discuss personalized prevention strategies with your doctor."
            
            elif any(word in message_lower for word in ['doctor', 'medical', 'consult']):
                return f"Given your {risk_level} risk prediction for {disease_name}, I strongly recommend consulting with a healthcare professional. They can provide personalized advice, conduct proper assessments, and create a management plan tailored to your specific situation."
            
            elif any(word in message_lower for word in ['risk', 'chance', 'probability']):
                return f"Your {risk_level} risk prediction for {disease_name} is based on the information you provided. However, this is an AI assessment and should not replace professional medical evaluation. Your actual risk may vary based on many factors that only a healthcare professional can properly assess."
        
        # General health responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm here to help you with health-related questions. Remember, I provide general information and support, but always consult healthcare professionals for medical advice."
        
        elif any(word in message_lower for word in ['thank', 'thanks']):
            return "You're welcome! I'm glad I could help. Remember to prioritize your health and consult with healthcare professionals for personalized medical advice."
        
        else:
            return "Thank you for your question. I'm here to provide general health information and support. For specific medical advice, diagnosis, or treatment, please consult with a qualified healthcare professional who can evaluate your individual situation."
    
    def _save_conversation(self, user, user_message, ai_response, prediction, conversation_id):
        """Save the conversation to the database"""
        # Save user message
        AIChatLog.objects.create(
            user=user,
            disease=prediction.disease if prediction else None,
            prediction=prediction,
            conversation_id=conversation_id,
            message=user_message,
            response="",  # User messages don't have AI responses
            is_user_message=True
        )
        
        # Save AI response
        AIChatLog.objects.create(
            user=user,
            disease=prediction.disease if prediction else None,
            prediction=prediction,
            conversation_id=conversation_id,
            message="",  # AI responses don't have user messages
            response=ai_response,
            is_user_message=False
        )
    
    def get_user_conversations(self, user):
        """Get all conversations for a user"""
        conversations = AIChatLog.objects.filter(
            user=user
        ).values('conversation_id', 'disease__name', 'prediction__risk_level').distinct()
        
        return conversations

# Global instance
ai_chat_service = AIChatService()
