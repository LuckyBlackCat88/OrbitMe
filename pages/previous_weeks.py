import streamlit as st
import pandas as pd
import os
import datetime

# === Load Logs ===
def load_logs():
    food_log = pd.read_csv("food_log_active.csv") if os.path.exists("food_log_active.csv") else pd.DataFrame(columns=["date", "meal_type", "item", "calories", "carbs", "fats", "protein"])
    burned_log = pd.read_csv("burned_log_active.csv") if os.path.exists("burned_log_active.csv") else pd.DataFrame(columns=["date", "activity", "calories_burned", "notes"])
    food_log["date"] = pd.to_datetime(food_log["date"]).dt.date
    burned_log["date"] = pd.to_datetime(burned_log["date"]).dt.date
    return food_log, burned_log

# === Group Weeks ===
def get_weeks(dates):
    dates = sorted(set(dates))
    week_map = {}
    for d in dates:
        monday = d - datetime.timedelta(days=d.weekday())
        sunday = monday + datetime.timedelta(days=6)
        label = f"Week of {monday.strftime('%b %d')} – {sunday.strftime('%b %d')}"
        if label not in week_map:
            week_map[label] = []
        week_map[label].append(d)
    return week_map

# === Page Setup ===
st.set_page_config(page_title="Previous Weeks - Calorie Tracker", page_icon="📅", layout="centered")

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
    <div style="text-align:center">
        <h1 style='color:#bbd1ff;'>📅 Previous Weeks</h1>
        <p style='font-size:18px;color:#eeeeee;'>View your past logs by week.</p>
    </div>
""", unsafe_allow_html=True)

# === Load Data ===
food_log, burned_log = load_logs()
all_dates = list(food_log["date"].unique()) + list(burned_log["date"].unique())
week_map = get_weeks(all_dates)

# === Current Week Reference ===
today = datetime.date.today()
current_monday = today - datetime.timedelta(days=today.weekday())

# === Show Expanders for Each Past Week ===
for week_label, week_dates in sorted(week_map.items(), reverse=True):
    monday = week_dates[0] - datetime.timedelta(days=week_dates[0].weekday())
    if monday == current_monday:
        continue  # skip this week

    with st.expander(week_label):
        weekly_totals = {"Calories In": 0, "Calories Burned": 0, "Carbs": 0, "Fats": 0, "Protein": 0}

        for i in range(7):
            day = monday + datetime.timedelta(days=i)
            day_name = day.strftime("%A")
            meals = food_log[food_log["date"] == day]
            burns = burned_log[burned_log["date"] == day]
            cal_in = meals["calories"].sum()
            cal_out = burns["calories_burned"].sum()
            carbs = meals["carbs"].sum()
            fats = meals["fats"].sum()
            protein = meals["protein"].sum()

            if not meals.empty or not burns.empty:
                st.markdown(f"### {day_name} ({day.strftime('%Y-%m-%d')})", unsafe_allow_html=True)
                st.markdown(f"""
                **Calories In:** {int(cal_in)} kcal  
                **Calories Burned:** {int(cal_out)} kcal  
                **Carbs:** {int(carbs)}g, **Fats:** {int(fats)}g, **Protein:** {int(protein)}g
                """)

                if not meals.empty:
                    st.markdown("*Food Log:*")
                    st.dataframe(meals[["meal_type", "item", "calories", "carbs", "fats", "protein"]], use_container_width=True)

                if not burns.empty:
                    st.markdown("*Burned Activity Log:*")
                    st.dataframe(burns[["activity", "calories_burned", "notes"]], use_container_width=True)

                st.markdown("---")

                weekly_totals["Calories In"] += cal_in
                weekly_totals["Calories Burned"] += cal_out
                weekly_totals["Carbs"] += carbs
                weekly_totals["Fats"] += fats
                weekly_totals["Protein"] += protein

        # === Weekly Summary ===
        st.markdown("## Weekly Summary")
        st.markdown(f"""
        **Total Calories In:** {int(weekly_totals['Calories In'])} kcal  
        **Total Calories Burned:** {int(weekly_totals['Calories Burned'])} kcal  
        **Carbs:** {int(weekly_totals['Carbs'])}g, **Fats:** {int(weekly_totals['Fats'])}g, **Protein:** {int(weekly_totals['Protein'])}g
        """)
