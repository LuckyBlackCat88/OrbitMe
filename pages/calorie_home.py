import streamlit as st
import pandas as pd
import json
import os
import datetime
import matplotlib.pyplot as plt


# === Load Profile Settings ===
def load_profile():
    default_profile = {"age": 21, "height": 67, "gender": "female", "goal_loss_lbs": 8}
    if os.path.exists("profile_settings.json"):
        with open("profile_settings.json", "r") as f:
            return json.load(f)
    else:
        return default_profile

# === Load Logs ===
def load_logs():
    food_log = pd.read_csv("food_log_active.csv") if os.path.exists("food_log_active.csv") else pd.DataFrame(columns=["date", "meal_type", "item", "calories", "carbs", "fats", "protein"])
    burned_log = pd.read_csv("burned_log_active.csv") if os.path.exists("burned_log_active.csv") else pd.DataFrame(columns=["date", "activity", "calories_burned", "notes"])
    return food_log, burned_log

# === Calculate Totals ===
def calculate_summary(food_log, burned_log, goal_kcal):
    total_in = food_log["calories"].sum()
    total_burned = burned_log["calories_burned"].sum()
    remaining = max(goal_kcal - total_burned, 0)
    return total_in, total_burned, remaining

# === Render Pie Chart ===
def plot_pie(total_burned, remaining):
    labels = ['Burned', 'Remaining']
    values = [total_burned, remaining]
    colors = ['#222222','#000000']

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.pie(values, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%',
           textprops={'color': 'white'})
    ax.axis('equal')
    st.pyplot(fig)

# === Page Setup ===
st.set_page_config(page_title="Calorie Tracker - OrbitMe", page_icon="🍱", layout="centered")

# === Background Styling ===
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1639852656724-827b82462231?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;

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

# === Load Data ===
profile = load_profile()
food_log, burned_log = load_logs()
goal_kcal = profile.get("goal_loss_lbs", 0) * 3500
total_in, total_burned, remaining = calculate_summary(food_log, burned_log, goal_kcal)

# === Header Section ===
st.markdown(f"""
    <div class="dark-box">
        <div class="section-title">🍱 Calorie Tracker</div>
        <div class="section-subtitle">Track your intake, progress, and goals this quarter.</div>
    </div>
""", unsafe_allow_html=True)

# === Navigation Buttons ===
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🔄 This Week"):
        st.switch_page("pages/this_week.py")
with col2:
    if st.button("📅 Previous Weeks"):
        st.switch_page("pages/previous_weeks.py")
with col3:
    if st.button("📋 Profile"):
        st.switch_page("pages/profile.py")
with col4:
    if st.button("⬇️ Export"):
        st.switch_page("pages/export.py")

# === Summary Section ===
st.markdown("""
    <div class="dark-box">
        <div class="section-title">📊 Summary</div>
        <div class="section-subtitle">Quarter: Q2 2025 (Apr 1 – Jun 30)</div>
        <p style="color:white;">
            <strong>Total Calories In:</strong> {} kcal<br>
            <strong>Total Calories Burned:</strong> {} kcal<br>
            <strong>Net Calories:</strong> {} kcal
        </p>
    </div>
""".format(int(total_in), int(total_burned), int(total_in - total_burned)), unsafe_allow_html=True)

# === Goal Progress Section ===
st.markdown("""
    <div class="dark-box">
        <div class="section-title">🔥 Goal Progress</div>
""", unsafe_allow_html=True)

plot_pie(total_burned, remaining)
st.markdown("</div>", unsafe_allow_html=True)
