import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")
def get_gemini_response(message):
    try:
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"
