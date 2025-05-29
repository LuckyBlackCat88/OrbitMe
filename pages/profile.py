import streamlit as st
import json
import os

# === Load/Save Profile ===
PROFILE_PATH = "profile_settings.json"
default_profile = {
    "age": 21,
    "height": 67,
    "weight": 150,
    "gender": "female",
    "goal_loss_lbs": 8
}

def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return default_profile.copy()

def save_profile(data):
    with open(PROFILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

# === Page Setup ===
st.set_page_config(page_title="Profile - Calorie Tracker", page_icon="📋", layout="centered")

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
    label {
        color: #eeeeee !important;
    }
    </style>
""", unsafe_allow_html=True)

# === Header ===
st.markdown("""
    <div class="dark-box">
        <div class="section-title">📋 Profile Settings</div>
        <div class="section-subtitle">Enter your information to calculate BMR and set your quarterly goal.</div>
    </div>
""", unsafe_allow_html=True)

# === Load & Display Form ===
profile = load_profile()

with st.form("profile_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=10, max_value=100, value=profile.get("age", 21))
        height = st.number_input("Height (inches)", min_value=48, max_value=84, value=profile.get("height", 67))
        weight = st.number_input("Current Weight (lbs)", min_value=50, max_value=500, value=profile.get("weight", 150))
    with col2:
        gender = st.selectbox("Gender", options=["female", "male"], index=0 if profile.get("gender") == "female" else 1)
        goal_loss_lbs = st.number_input("Quarter Weight Loss Goal (lbs)", min_value=0, max_value=100, value=profile.get("goal_loss_lbs", 8))
    
    submitted = st.form_submit_button("Save Changes")

if submitted:
    profile.update({
        "age": age,
        "height": height,
        "weight": weight,
        "gender": gender,
        "goal_loss_lbs": goal_loss_lbs
    })
    save_profile(profile)
    st.success("✅ Profile updated successfully!")
