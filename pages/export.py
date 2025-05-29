import streamlit as st
import pandas as pd
import datetime
import os

# === Style & Background ===
st.set_page_config(page_title="Export - Calorie Tracker", page_icon="⬇️", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1639852656724-827b82462231?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .dark-box {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# === Helper: Detect current quarter ===
def get_current_quarter():
    month = datetime.date.today().month
    if 1 <= month <= 3:
        return "Q1"
    elif 4 <= month <= 6:
        return "Q2"
    elif 7 <= month <= 9:
        return "Q3"
    else:
        return "Q4"

# === Load CSVs if they exist ===
def load_csv(filename):
    return pd.read_csv(filename) if os.path.exists(filename) else pd.DataFrame()

# === Save empty CSV with same structure ===
def clear_and_save_empty(filename, columns):
    pd.DataFrame(columns=columns).to_csv(filename, index=False)

# === UI: Page Header ===
st.markdown("""
    <div class="dark-box">
        <h1>⬇️ Export & Backup</h1>
        <p>Download your current quarter’s logs and archive your progress.</p>
    </div>
""", unsafe_allow_html=True)

quarter = get_current_quarter()
st.markdown(f"<h3 style='text-align:center;color:white;'>📆 Current Quarter: {quarter}</h3>", unsafe_allow_html=True)

# === Load Data ===
food_log = load_csv("food_log_active.csv")
burned_log = load_csv("burned_log_active.csv")

# === Export Buttons ===
st.download_button("📤 Download Food Log", food_log.to_csv(index=False), "food_log.csv", mime="text/csv")
st.download_button("🔥 Download Burned Log", burned_log.to_csv(index=False), "burned_log.csv", mime="text/csv")

# === Archive & Reset Button ===
st.markdown("---")
if st.button("🗃 Archive and Start Next Quarter"):
    # Save with quarter label
    food_log.to_csv(f"food_log_{quarter}.csv", index=False)
    burned_log.to_csv(f"burned_log_{quarter}.csv", index=False)

    # Clear active logs
    clear_and_save_empty("food_log_active.csv", food_log.columns)
    clear_and_save_empty("burned_log_active.csv", burned_log.columns)

    st.success(f"{quarter} logs archived and cleared! You're ready for the next quarter 🚀")

