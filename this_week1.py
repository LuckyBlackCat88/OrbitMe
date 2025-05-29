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

# === Filter logs for selected day ===
def filter_logs_by_day(log, selected_date):
    return log[log["date"] == selected_date.strftime("%Y-%m-%d")]

# === Display Daily Summary ===
def display_day_summary(food_day, burned_day, bmr):
    calories_in = food_day["calories"].sum()
    calories_burned = burned_day["calories_burned"].sum()
    calories_out = bmr + calories_burned
    net = calories_in - calories_out

    st.markdown("""
        <div class="dark-box">
            <h4>🔍 Daily Summary</h4>
            <p><strong>Calories In:</strong> {} kcal</p>
            <p><strong>Calories Burned:</strong> {} kcal</p>
            <p><strong>BMR:</strong> {} kcal</p>
            <p><strong>Calories Out (BMR + Burned):</strong> {} kcal</p>
            <p><strong>Net Calories:</strong> {} kcal</p>
        </div>
    """.format(int(calories_in), int(calories_burned), int(bmr), int(calories_out), int(net)), unsafe_allow_html=True)

# === Page Setup ===
st.set_page_config(page_title="This Week - Calorie Tracker", page_icon="🔄", layout="centered")

# === Background + Styling ===
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
        color: white;
        margin-bottom: 20px;
    }
    label {
        color: #eeeeee !important;
    }
    </style>
""", unsafe_allow_html=True)

# === Title ===
st.markdown("""
    <div class="dark-box">
        <h1>🔄 This Week</h1>
        <p>View and log your meals and calories burned for the current week.</p>
    </div>
""", unsafe_allow_html=True)

# === Load Data ===
profile = load_profile()
food_log, burned_log = load_logs()
bmr = calculate_bmr(profile["weight"], profile["height"], profile["age"], profile["gender"])

# === Date Selector ===
today = datetime.date.today()
week_start = today - datetime.timedelta(days=today.weekday())
week_dates = [week_start + datetime.timedelta(days=i) for i in range(7)]

selected_day = st.selectbox("📅 Select a Day", week_dates, format_func=lambda d: d.strftime("%A, %b %d"))

# === Display Logs ===
food_day = filter_logs_by_day(food_log, selected_day)
burned_day = filter_logs_by_day(burned_log, selected_day)

st.markdown("### 🍽️ Meal Log")
st.dataframe(food_day.drop(columns=["date"]), use_container_width=True)

st.markdown("### 🔥 Calories Burned Log")
st.dataframe(burned_day.drop(columns=["date"]), use_container_width=True)

# === Daily Summary ===
display_day_summary(food_day, burned_day, bmr)
