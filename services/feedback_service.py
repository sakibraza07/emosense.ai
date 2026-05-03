import google.generativeai as genai
import os

def generate_feedback(emotion: str) -> str:
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
You are an emotionally intelligent AI assistant.

User emotion detected: {emotion}

Respond like a calm, supportive human.

Structure:
- 1 line empathy
- 2 lines explanation
- 2 practical tips
- 1 short motivational line

Keep it natural, not robotic.
"""
    
    response = model.generate_content(prompt)
    return response.text
