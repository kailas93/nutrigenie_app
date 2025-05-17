import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

from gemini_api import get_meal_plan
from weather_api import get_location_and_weather

st.set_page_config(page_title="NutriGenie – AI Nutrition Assistant", layout="centered")
st.title("🥗 NutriGenie – Your Smartest AI Nutrition Coach")

# --- User Inputs ---
st.header("👤 Your Profile")
goal = st.selectbox("Health Goal", ["Weight Loss", "Muscle Gain", "Maintain"])
age = st.slider("Age", 10, 80, 25)
weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
height = st.number_input("Height (cm)", 100.0, 220.0, 170.0)
bmi = round(weight / ((height / 100) ** 2), 2)
st.markdown(f"**Calculated BMI:** {bmi}")

systolic = st.number_input("Blood Pressure - Systolic", 80, 200, 120)
diastolic = st.number_input("Blood Pressure - Diastolic", 50, 130, 80)
chol = st.number_input("Cholesterol Level (mg/dL)", 100, 300, 180)
vitamin_d = st.number_input("Vitamin D Level (ng/mL)", 10, 100, 40)

conditions = st.text_input("Medical Conditions (comma-separated)", "None")
allergies = st.text_input("Allergies (comma-separated)", "None")
culture = st.selectbox("Preferred Food Culture", ["South Indian", "North Indian", "Continental", "Global"])
fitness = st.selectbox("Activity Level", ["Sedentary", "Moderate", "Active"])

city, weather = get_location_and_weather()
st.markdown(f"📍 **Location**: {city}")
st.markdown(f"🌤 **Weather**: {weather['condition']} | 🌡 Temp: {weather['temp']}°C")

# --- Meal Plan Parsing ---
def extract_items_by_meal(plan_text, meal_name):
    pattern = re.compile(rf"{meal_name}:(.*?)(?:\n\n|\Z)", re.IGNORECASE | re.DOTALL)
    match = pattern.search(plan_text)
    if match:
        items = match.group(1).split('\n')
        return [item.strip("•- ").strip() for item in items if item.strip()]
    return []


# --- Generate Gemini Meal Plan ---
if st.button("🍽 Generate Personalized Meal Plan"):
    prompt = f"""
    You are NutriGenie, an AI nutrition assistant. Provide a meal plan for:
    Goal: {goal}, Age: {age}, BMI: {bmi}, Cholesterol: {chol}, Vitamin D: {vitamin_d},
    BP: {systolic}/{diastolic}, Conditions: {conditions}, Allergies: {allergies},
    Culture: {culture}, Fitness: {fitness}, Location: {city}, Weather: {weather['condition']}
    Return Breakfast, Lunch, Dinner, Snacks with healthy swap suggestions.
    """
    plan = get_meal_plan(prompt)
    st.subheader("📝 Personalized Meal Plan")
    st.write(plan)

    
