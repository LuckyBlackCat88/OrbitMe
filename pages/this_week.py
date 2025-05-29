import streamlit as st
import pandas as pd
import json
import os
import datetime

# === Load Profile ===
def load_profile():
    default_profile = {
        "age": 21,
        "height": 67,
        "weight": 150,
        "gender": "female",
        "goal_loss_lbs": 8
    }
    if os.path.exists("profile_settings.json"):
        with open("profile_settings.json", "r") as f:
            return json.load(f)
    return default_profile

# === Calculate BMR ===
def calculate_bmr(weight, height, age, gender):
    if gender == "female":
        return round((4.536 * weight) + (15.88 * height) - (5 * age) - 161, 2)
    else:
        return round((4.536 * weight) + (15.88 * height) - (5 * age) + 5, 2)

# === Load Logs ===
def load_logs():
    food_log = pd.read_csv("food_log_active.csv") if os.path.exists("food_log_active.csv") else pd.DataFrame(columns=["date", "meal_type", "item", "calories", "carbs", "fats", "protein"])
    burned_log = pd.read_csv("burned_log_active.csv") if os.path.exists("burned_log_active.csv") else pd.DataFrame(columns=["date", "activity", "calories_burned", "notes"])
    return food_log, burned_log

# === Save Logs ===
def save_log(df, path):
    df.to_csv(path, index=False)

# === Get This Week's Dates ===
def get_week_dates():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    return [(monday + datetime.timedelta(days=i)) for i in range(7)]

# === Setup Page ===
st.set_page_config(page_title="This Week - OrbitMe", page_icon="📆", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1639852656724-827b82462231?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .dark-box {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 28px;
        color: #bbd1ff;
    }
    .section-subtitle {
        font-size: 18px;
        color: #eeeeee;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align:center;">
        <h1 style='color:#bbd1ff;'>📆 This Week</h1>
        <p style='font-size:18px; color:#eeeeee;'>Track daily meals and burned calories</p>
    </div>
""", unsafe_allow_html=True)

# === Load Everything ===
profile = load_profile()
food_log, burned_log = load_logs()
week_dates = get_week_dates()
bmr = calculate_bmr(profile["weight"], profile["height"], profile["age"], profile["gender"])

# === Day Selector ===
day_labels = [d.strftime("%A (%m/%d)") for d in week_dates]
day_map = dict(zip(day_labels, week_dates))
selected_day_label = st.selectbox("Select Day of the Week", day_labels, index=datetime.date.today().weekday())
selected_date = day_map[selected_day_label].strftime("%Y-%m-%d")

st.markdown("---")

# === Meal Log Display ===
st.markdown(f"### 🍽️ Meals for {selected_day_label}")
day_meals = food_log[food_log["date"] == selected_date]

if not day_meals.empty:
    st.dataframe(day_meals.drop(columns=["date"]))
else:
    st.info("No meals logged for this day.")

with st.expander("➕ Add Meal Entry"):
    with st.form("add_meal_form"):
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
        item = st.text_input("Food Item")
        calories = st.number_input("Calories", min_value=0)
        carbs = st.number_input("Carbs (g)", min_value=0)
        fats = st.number_input("Fats (g)", min_value=0)
        protein = st.number_input("Protein (g)", min_value=0)
        submitted = st.form_submit_button("Add Meal")
        if submitted:
            new_row = pd.DataFrame([{
                "date": selected_date, "meal_type": meal_type, "item": item,
                "calories": calories, "carbs": carbs, "fats": fats, "protein": protein
            }])
            food_log = pd.concat([food_log, new_row], ignore_index=True)
            save_log(food_log, "food_log_active.csv")
            st.success("Meal added!")

# === Burn Log Display ===
st.markdown(f"### 🔥 Calories Burned for {selected_day_label}")
day_burned = burned_log[burned_log["date"] == selected_date]

if not day_burned.empty:
    st.dataframe(day_burned.drop(columns=["date"]))
else:
    st.info("No burn entries logged for this day.")

with st.expander("➕ Add Burned Calories Entry"):
    with st.form("add_burn_form"):
        activity = st.text_input("Activity")
        calories_burned = st.number_input("Calories Burned", min_value=0)
        notes = st.text_input("Notes (optional)")
        submitted = st.form_submit_button("Add Burn Entry")
        if submitted:
            new_row = pd.DataFrame([{
                "date": selected_date, "activity": activity,
                "calories_burned": calories_burned, "notes": notes
            }])
            burned_log = pd.concat([burned_log, new_row], ignore_index=True)
            save_log(burned_log, "burned_log_active.csv")
            st.success("Burn entry added!")

# === Daily Summary ===
st.markdown("---")
st.markdown(f"### 📊 Summary for {selected_day_label}")

# Get today's entries again
meals_today = food_log[food_log["date"] == selected_date]
burns_today = burned_log[burned_log["date"] == selected_date]

total_in = meals_today["calories"].sum()
total_burned = burns_today["calories_burned"].sum()
carbs = meals_today["carbs"].sum()
fats = meals_today["fats"].sum()
protein = meals_today["protein"].sum()

# Get today's weight if available (assume latest food log row has most recent weight if tracked)
weight_lbs = 150  # ← static placeholder (we can later track weight if you'd like)
total_out = total_burned + bmr

# Summary Display
st.markdown(f"""
<div style="background-color: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px; text-align:center;">
    <p><b>Total Calories In:</b> {int(total_in)} kcal</p>
    <p><b>Total Burned:</b> {int(total_burned)} kcal + <b>BMR:</b> {int(bmr)} kcal = <b>{int(total_out)} kcal</b> out</p>
    <p><b>Net Calories:</b> {int(total_in - total_out)} kcal</p>
    <hr>
    <p><b>Carbs:</b> {int(carbs)} g &nbsp; | &nbsp; <b>Fats:</b> {int(fats)} g &nbsp; | &nbsp; <b>Protein:</b> {int(protein)} g</p>
</div>
""", unsafe_allow_html=True)
