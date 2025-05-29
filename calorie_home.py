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
    colors = ['#ff9999','#c2c2f0']

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

# === Page Setup ===
st.set_page_config(page_title="Calorie Tracker - OrbitMe", page_icon="🍱", layout="centered")
st.markdown("""
    <div style="text-align:center">
        <h1 style='color:#bbd1ff;'>🍱 Calorie Tracker</h1>
        <p style='font-size:18px;color:#eeeeee;'>Track your intake, progress, and goals this quarter.</p>
    </div>
""", unsafe_allow_html=True)

# === Load Data ===
profile = load_profile()
food_log, burned_log = load_logs()

goal_kcal = profile.get("goal_loss_lbs", 0) * 3500

total_in, total_burned, remaining = calculate_summary(food_log, burned_log, goal_kcal)

# === Display Summary ===
st.markdown("""---\n### 📊 Q2 Summary\n""")
st.write(f"**Quarter:** Q2 2025")
st.write(f"**Total Calories In:** {int(total_in)} kcal")
st.write(f"**Total Calories Burned:** {int(total_burned)} kcal")
st.write(f"**Net Calories:** {int(total_in - total_burned)} kcal")

st.write("#### 🔥 Goal Progress")
plot_pie(total_burned, remaining)

# === Navigation Buttons ===
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 This Week"):
        st.switch_page("this_week.py")
with col2:
    if st.button("📅 Previous Weeks"):
        st.switch_page("previous_weeks.py")
with col3:
    if st.button("📋 Profile"):
        st.switch_page("profile.py")

# === Export Button ===
if st.button("⬇️ Export Q2"):
    st.success("Exported Q2 logs successfully.")
    if st.confirm("Do you want to start Q3 now?"):
        os.rename("food_log_active.csv", "food_log_Q2.csv")
        os.rename("burned_log_active.csv", "burned_log_Q2.csv")
        pd.DataFrame(columns=food_log.columns).to_csv("food_log_active.csv", index=False)
        pd.DataFrame(columns=burned_log.columns).to_csv("burned_log_active.csv", index=False)
        st.success("Q3 tracking started!")
