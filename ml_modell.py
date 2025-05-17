import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# --- Function to apply rules and generate labels ---
def classify_row(row):
    if row["Cholesterol (mg)"] > 200:
        return "Unhealthy"
    if row["Sugars (g)"] > 35:
        return "Unhealthy"
    if row["Sodium (mg)"] > 900:
        return "Unhealthy"
    if row["Fat (g)"] > 30:
        return "Unhealthy"
    return "Healthy"

# --- Load data, label it, and train model ---
def load_and_train_model():
    df = pd.read_csv("daily_food_nutrition_dataset.csv")

    # Apply labeling if 'Label' column is missing
    if 'Label' not in df.columns:
        df["Label"] = df.apply(classify_row, axis=1)

    # Drop rows with missing required data
    df.dropna(subset=[
        "Calories (kcal)", "Protein (g)", "Carbohydrates (g)", "Fat (g)",
        "Fiber (g)", "Sugars (g)", "Sodium (mg)", "Cholesterol (mg)",
        "Water_Intake (ml)"
    ], inplace=True)

    # Features and target
    X = df[[
        "Calories (kcal)", "Protein (g)", "Carbohydrates (g)", "Fat (g)",
        "Fiber (g)", "Sugars (g)", "Sodium (mg)", "Cholesterol (mg)",
        "Water_Intake (ml)"
    ]]
    y = df["Label"]

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    return model, scaler

# --- Predict meal health label ---
def predict_healthiness(model, scaler, features):
    scaled = scaler.transform([features])
    return model.predict(scaled)[0]
