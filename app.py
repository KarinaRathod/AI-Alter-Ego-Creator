import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import datetime

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="AI Alter Ego Creator", layout="wide")
st.title("🎭 AI Alter Ego Creator")
st.caption("Design the version of yourself you want to become")

# -----------------------------
# SESSION STATE
# -----------------------------
if "personas" not in st.session_state:
    st.session_state.personas = []

# -----------------------------
# INPUT
# -----------------------------
name = st.text_input("👤 Your Name")
goal = st.text_input("🎯 Your Goal (e.g., become confident)")
weakness = st.text_input("⚠️ Your Weakness")

# -----------------------------
# GENERATE
# -----------------------------
if st.button("🚀 Create Alter Ego"):

    if not goal.strip():
        st.warning("⚠️ Enter your goal")
        st.stop()

    with st.spinner("🧠 Creating your alter ego..."):

        prompt = f"""
        User name: {name}
        Goal: {goal}
        Weakness: {weakness}

        Create an alter ego with:

        1. Name of alter ego
        2. Identity statement
        3. Key personality traits
        4. Rules this person follows
        5. Behavior system
        6. Daily mission

        Make it practical and powerful.
        """

        response = model.generate_content(prompt)
        result = response.text

        # Save
        st.session_state.personas.append({
            "time": str(datetime.datetime.now()),
            "goal": goal,
            "persona": result
        })

        # Display
        st.subheader("🎭 Your Alter Ego")
        st.success(result)

# -----------------------------
# HISTORY
# -----------------------------
if st.session_state.personas:
    st.subheader("📜 Saved Personas")

    for p in reversed(st.session_state.personas[-5:]):
        st.write(f"🕒 {p['time']}")
        st.write(f"🎯 Goal: {p['goal']}")
        st.write(p['persona'])
        st.divider()