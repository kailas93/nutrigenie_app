
import google.generativeai as genai

genai.configure(api_key="AIzaSyBf7rcIurfyCJ6aMChNHVjRUKkN1M3jDic")
model = genai.GenerativeModel("models/gemini-1.5-pro")

def get_meal_plan(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini: {e}"
