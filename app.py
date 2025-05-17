import streamlit as st
import pandas as pd
from gemini_api import get_meal_plan
from ml_modell import load_and_train_model, predict_healthiness
from weather_api import get_location_and_weather
import matplotlib.pyplot as plt

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

# --- Health Analysis using ML Model ---
st.header("📊 Nutrient Analyzer")
st.markdown("Enter your meal’s nutritional details to analyze its health impact.")

col1, col2 = st.columns(2)
with col1:
    cal = st.number_input("Calories (kcal)", 0, 1000, 300)
    protein = st.number_input("Protein (g)", 0.0, 100.0, 20.0)
    carbs = st.number_input("Carbs (g)", 0.0, 150.0, 40.0)
    fat = st.number_input("Fat (g)", 0.0, 100.0, 10.0)
    fiber = st.number_input("Fiber (g)", 0.0, 50.0, 5.0)
with col2:
    sugar = st.number_input("Sugar (g)", 0.0, 100.0, 10.0)
    sodium = st.number_input("Sodium (mg)", 0, 3000, 700)
    chol_mg = st.number_input("Cholesterol (mg)", 0, 500, 100)
    water = st.number_input("Water Intake (ml)", 0, 3000, 500)

if st.button("🧠 Analyze Meal"):
    model, scaler = load_and_train_model()
    input_data = [cal, protein, carbs, fat, fiber, sugar, sodium, chol_mg, water]
    label = predict_healthiness(model, scaler, input_data)
    
    st.success(f"🔍 Prediction: **{label}**")

    # Pie chart
    labels = ['Protein', 'Carbs', 'Fat']
    sizes = [protein, carbs, fat]
    colors = ['#6ab04c', '#f0932b', '#eb4d4b']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%")
    ax.set_title("Macronutrient Breakdown")
    st.pyplot(fig)
