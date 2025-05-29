import streamlit as st

# === Page Config ===
st.set_page_config(
    page_title="OrbitMe",
    page_icon="🌠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === Optional Custom Background + Button Style ===
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1639852656724-827b82462231?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .stButton > button {
            background-color: #add8e6;
            color: #333333;
            font-weight: 700;  /* Make button text bold */
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            margin: 10px 0;
            font-size: 16px;
            transition: background-color 0.2s ease;
        }

        .stButton > button:hover {
            background-color: #f4c2c2;
            color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# === OrbitMe Title ===
st.markdown("""
<div style='text-align:center;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 10px;'>
    <h1 style='color:#bbd1ff; margin-bottom:0;'>✨ OrbitMe ✨</h1>
</div>
""", unsafe_allow_html=True)

# === Inspirational Quote ===
st.markdown("""
<div style='text-align:center;
            padding: 10px 20px;
            border-radius: 10px;
            margin-bottom: 20px;'>
    <p style='font-size:18px; font-style: italic; color:#ffffff;'>
        ~ Small Changes Are The Gravity That Shift Your Orbit ~
    </p>
</div>
""", unsafe_allow_html=True)

# === Section Title: Trackers ===


# === Module Buttons ===
modules = [
    ("🍱 Calories", "calorie"),
    ("🏋️ Workout", "workout"),
    ("✅ Habits", "habits"),
    ("🩺 Health", "health"),
    ("💸 Finance", "finance"),
    ("📅 Schedule", "schedule"),
]

cols = st.columns(6)

for col, (label, key) in zip(cols, modules):
    with col:
        if st.button(label):
            st.session_state.page = key

# === Placeholder for Selected Page ===
page = st.session_state.get("page", None)

if page == "calorie":
    st.switch_page("pages/calorie_home.py")
elif page == "workout":
    st.write("🏋️ Workout Tracker module coming soon!")
elif page == "habits":
    st.write("✅ Habits Tracker module coming soon!")
elif page == "health":
    st.write("🩺 Health Tracker module coming soon!")
elif page == "finance":
    st.write("💸 Finance Tracker module coming soon!")
elif page == "schedule":
    st.write("📅 Schedule Tracker module coming soon!")

# === Footer ===
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Made with 💫 in Streamlit</p>",
    unsafe_allow_html=True
)
