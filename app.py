
import streamlit as st
from gemini_api import get_meal_plan
from ml_model import recommend_meals
import pandas as pd
from weather_api import get_location_and_weather

st.set_page_config(page_title="NutriGenie – AI Nutrition Assistant", layout="centered")
st.title("🥗 NutriGenie – Your Smartest AI Nutrition Coach")

# User Inputs
user_goal = st.selectbox("Health Goal", ["Weight Loss", "Muscle Gain", "Maintain"])
user_age = st.slider("Age", 10, 80, 25)
user_conditions = st.text_input("Medical Conditions (comma-separated)", "None")
user_allergies = st.text_input("Allergies (comma-separated)", "None")
user_culture = st.selectbox("Preferred Food Culture", ["South Indian", "North Indian", "Continental", "Global"])
user_fitness = st.selectbox("Activity Level", ["Sedentary", "Moderate", "Active"])

# Fetch weather and location
city, weather = get_location_and_weather()
st.markdown(f"📍 Location: **{city}**")
st.markdown(f"🌤 Weather: **{weather['condition']}** | 🌡 Temp: **{weather['temp']}°C**")

if st.button("Generate Personalized Meal Plan"):
    prompt = f"""
    You are NutriGenie, an AI nutrition assistant. Provide a personalized meal plan for:
    - Goal: {user_goal}
    - Age: {user_age}
    - Medical Conditions: {user_conditions}
    - Allergies: {user_allergies}
    - Cultural Preferences: {user_culture}
    - Fitness Routine: {user_fitness}
    - Location: {city}
    - Weather: {weather['condition']}, Temperature: {weather['temp']}°C

    Return meal plan for Breakfast, Lunch, Dinner, and Snacks with explanation and a healthy food swap suggestion.
    """
    plan = get_meal_plan(prompt)
    st.markdown("### 📝 Personalized Meal Plan")
    st.write(plan)

    #st.markdown("### 🍱 Smart Meal Suggestions from ML Model")
    #recs = recommend_meals(user_culture, user_allergies)
    #st.dataframe(recs)
