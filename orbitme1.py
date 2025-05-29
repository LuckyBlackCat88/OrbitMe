import streamlit as st

# === Page Config ===
st.set_page_config(
    page_title="OrbitMe",
    page_icon="🌠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === Optional Custom Background ===
st.markdown("""
    <style>
        .stApp {
            background-image: url("http://papers.co/wallpaper/papers.co-ni77-space-star-night-galaxy-nature-dark-milkyway-33-iphone6-wallpaper.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Button styling with baby blue + baby pink */
        .stButton > button {
            background-color: #add8e6;  /* Baby blue */
            color: #333333;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            margin: 10px 0;
            font-size: 16px;
	    font-weight: 700;
            transition: background-color 0.2s ease;
        }

        .stButton > button:hover {
            background-color: #f4c2c2;  /* Baby pink */
            color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# === OrbitMe Header ===
st.markdown("""
    <div style="text-align:center">
        <h1 style='color:#bbd1ff;'>🌠 OrbitMe 🌠</h1>
        <p style='font-size:18px;color:#eeeeee;'>~ Small Changes Are The Gravity That Shift Your Orbit ~</p>
    </div>
""", unsafe_allow_html=True)

# === Module Buttons ===
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
