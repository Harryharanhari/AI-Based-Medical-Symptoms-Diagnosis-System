import requests
import os
from flask import current_app
import dotenv
dotenv.load_dotenv()

class GrokChatbot:
    def __init__(self, api_key=None):
        self.api_key = os.getenv("GROK_API_KEY")
        self.base_url = "https://api.x.ai/v1/responses" # Placeholder for Grok API URL

    def get_response(self, user_input, chat_history=None):
        if not self.api_key:
            return "AI Chatbot is currently offline (API key missing). Please consult a medical professional."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Structured medical prompt
        system_prompt = (
            "You are a professional Medical Assistant AI. Your goal is to help users understand their symptoms. "
            "IMPORTANT: Always include a disclaimer that you are an AI and not a doctor. "
            "If symptoms seem severe (e.g., chest pain, difficulty breathing), immediately advise seeking emergency care. "
            "Provide symptom clarification, possible mild causes, and general health advice."
        )

        messages = [{"role": "system", "content": system_prompt}]
        
        if chat_history:
            messages.extend(chat_history)
            
        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": "grok-3-mini", 
            "messages": messages,
            "temperature": 0.7
        }

        try:
            # Note: Using a timeout to prevent the app from hanging
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            current_app.logger.error(f"Chatbot Error: {str(e)}")
            return "I'm having trouble connecting to my knowledge base right now. If your symptoms are urgent, please call emergency services."

def get_medical_advice(input_data):
    chatbot = GrokChatbot()
    if isinstance(input_data, list):
        prompt = f"I am experiencing the following symptoms: {', '.join(input_data)}. Can you explain what might be happening and what I should do next?"
    else:
        prompt = input_data # Direct query from chat
    return chatbot.get_response(prompt)


