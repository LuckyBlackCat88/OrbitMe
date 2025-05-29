import streamlit as st

# === Page Config ===
st.set_page_config(
    page_title="OrbitMe",
    page_icon="🌠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === Styles ===
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://i.pinimg.com/736x/e8/05/c2/e805c2d732bbccba558a65919912ffbf.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
        }

        .stButton > button {
            background-color: #add8e6;  /* Baby blue */
            color: #333333;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            margin: 10px 0;
            font-size: 16px;
            font-weight: 500;
            transition: background-color 0.2s ease;
        }

        .stButton > button:hover {
            background-color: #f4c2c2;  /* Baby pink */
            color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# === OrbitMe Header + Quote in Lavender Panel ===
st.markdown("""
<div style='background-color: rgba(230, 230, 250, 0.4); 
            padding: 25px; 
            border-radius: 15px; 
            color: #333333;
            backdrop-filter: blur(4px);
            text-align: center;
            margin-bottom: 30px;'>

    <h1 style='color:#bbd1ff;'>🌠 OrbitMe</h1>
    <p style='font-size:18px;'>
        ~ Small Changes Are The Gravity That Shift Your Orbit ~
    </p>

    <h2 style='margin-top: 20px;'>🚀 Trackers</h2>
</div>
""", unsafe_allow_html=True)

# === Module Buttons ===
modules = [
    ("🍱 Calories", "calorie"),
    ("🏋️ Workout", "workout"),
    ("✅ Habits", "habits"),
    ("🩺 Health", "health"),
    ("💸 Finance", "finance"),
    ("📅 Schedule", "schedule"),
]

# Center the buttons using columns
button_cols = st.columns(6)

for col, (label, key) in zip(button_cols, modules):
    with col:
        if st.button(label):
            st.session_state.page = key

# === Placeholder for Selected Page ===
page = st.session_state.get("page", None)

if page == "calorie":
    st.write("🍱 Calorie Tracker module coming soon!")
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
