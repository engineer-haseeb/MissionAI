import os
from google import genai
from google.genai import types

def get_ai_client():
    # Codespace secrets ya settings se API key automatically detect hogi
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def ask_ai_coach(prompt_context: str, user_message: str):
    client = get_ai_client()
    if not client:
        return "⚠️ Gemini API Key detect nahi hui environment variables me. Please configure it to unlock the AI Chief of Staff."
    
    system_instruction = (
        "You are the AI Chief of Staff and Executive Coach inside MissionControlAI (GEOS). "
        "The user is Abdul Haseeb, a Master's student in Computer Science. "
        "Be direct, action-oriented, supportive but sharp. Optimize for execution, not just talking. "
        "Respond in a natural tone mixed with Urdu/English (Roman Urdu) where appropriate to keep it highly personalized."
    )
    
    full_prompt = f"Context of active system data:\n{prompt_context}\n\nUser Message: {user_message}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        return response.text
    except Exception as e:
        return f"Error connecting to AI Orchestrator: {str(e)}"