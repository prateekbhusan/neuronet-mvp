import streamlit as st
import requests
import os

# -- CONFIG --
GROQ_API_KEY = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# -- FUNCTIONS --
def call_llama(preferences, situation):
    prompt = f"""
You are a personal AI assistant trained to make decisions on behalf of a user, based strictly on their personal values and preferences.

User Preferences: {preferences}

Situation: {situation}

Based on these preferences, what should the user do? Respond as the AI agent with a clear decision and a brief explanation.
"""

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful and value-aligned personal AI agent."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# -- STREAMLIT APP --
st.set_page_config(page_title="neuronet", layout="centered")
st.title("🧠 neuronet — your second self")
st.markdown("an agent that makes decisions like you would. this is just the beginning.")

# Input user values / preferences
preferences = st.text_area("📜 your personal values & preferences", placeholder="e.g. no meetings after 6pm, prefer async communication, dislike spam")

# Simulated scenario
scenarios = [
    "Meeting request at 7:30pm from someone new",
    "Cold email asking to schedule a call",
    "Internal meeting invite during lunch",
    "Event invite for a weekend webinar",
    "Follow-up email from a recruiter"
]
situation = st.selectbox("📩 simulate a real-world situation", scenarios)

# Trigger decision
if st.button("🤖 ask your AI"):
    if preferences.strip() == "":
        st.warning("Please enter your preferences first.")
    else:
        with st.spinner("thinking like you would..."):
            response = call_llama(preferences, situation)
        st.success("💡 your AI agent decided:")
        st.write(response)

# Feedback
st.markdown("---")
st.markdown("### feedback")
feedback = st.radio("was the response aligned with your values?", ["👍 yes", "👎 no", "🤔 kinda"], horizontal=True)
st.caption("this will help improve future decision logic.")
