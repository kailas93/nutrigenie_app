
import pandas as pd

def recommend_meals(culture, allergies):
    df = pd.read_csv("food_database.csv")
    df = df[df["Culture"] == culture]
    if allergies.lower() != "none":
        allergy_list = [a.strip().lower() for a in allergies.split(",")]
        df = df[~df["Allergens"].str.lower().isin(allergy_list)]
    return df[["Food Item", "Calories", "Meal Type", "Tags"]].head(5)
