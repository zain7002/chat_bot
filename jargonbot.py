import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import random

# Optional: Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except:
    OLLAMA_AVAILABLE = False

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Cricket Tactical AI Pro", page_icon="🏏", layout="wide")
st.title("🏏 Cricket Tactical Intelligence Dashboard")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙ Match Controls")
match_format = st.sidebar.selectbox("Format", ["T20", "ODI", "Test"])
overs_left = st.sidebar.slider("Overs Left", 1, 50, 10)
runs_needed = st.sidebar.slider("Runs Needed", 1, 300, 80)
wickets_left = st.sidebar.slider("Wickets Left", 1, 10, 6)

# -----------------------------
# PLAYER DATABASE
# -----------------------------
data = {
    "Player": ["Virat Kohli", "Rohit Sharma", "Joe Root", "Steve Smith", "Ben Stokes"],
    "Matches": [274, 243, 265, 239, 110],
    "Runs": [12898, 9825, 10890, 9784, 5345],
    "Bat Avg": [57.32, 48.64, 50.12, 44.85, 38.7],
    "Strike Rate": [93.25, 90.12, 86.75, 87.33, 95.4],
    "Wickets": [4, 8, 26, 17, 197],
    "Bowl Avg": [166.0, 65.2, 30.5, 34.7, 31.2]
}
df = pd.DataFrame(data)

# -----------------------------
# PLAYER STATS
# -----------------------------
st.subheader("📊 Player Analytics")
col1, col2 = st.columns(2)
with col1:
    player1 = st.selectbox("Select Player 1", df["Player"], key="p1")
with col2:
    player2 = st.selectbox("Select Player 2", df["Player"], index=1, key="p2")
p1 = df[df["Player"] == player1].iloc[0]
p2 = df[df["Player"] == player2].iloc[0]
st.dataframe(df)

# -----------------------------
# COMPARISON CHART
# -----------------------------
st.subheader("📈 Batting Average Comparison")
fig, ax = plt.subplots()
ax.bar([player1, player2], [p1["Bat Avg"], p2["Bat Avg"]])
plt.xticks(rotation=20)
st.pyplot(fig)

# -----------------------------
# WIN PROBABILITY
# -----------------------------
st.subheader("🎯 Win Probability Predictor")
if overs_left > 0:
    run_rate_required = runs_needed / overs_left
else:
    run_rate_required = 0
pressure_factor = (10 - wickets_left) * 2
win_probability = max(0, 100 - (run_rate_required * 5) - pressure_factor)
col3, col4 = st.columns(2)
with col3:
    st.metric("Required Run Rate", round(run_rate_required, 2))
with col4:
    st.metric("Win Probability %", round(win_probability, 2))

# -----------------------------
# FIELD PLACEMENT
# -----------------------------
st.subheader("🗺 Suggested Field Placement")
field_positions = ["Slip", "Gully", "Point", "Cover", "Mid-off", "Mid-on",
                   "Square Leg", "Fine Leg", "Deep Midwicket"]
st.write(random.sample(field_positions, 4))

# -----------------------------
# TACTICAL AI CHATBOT WITH DROPDOWN
# -----------------------------
st.subheader("🧠 Tactical Strategy Assistant")

system_prompt = """
You are a professional cricket strategist.
Respond in EXACTLY 4 words.
Use only cricket jargon.
Tactical tone only.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# --- Dropdown of situations ---
situations = [
    "Powerplay 6 overs left",
    "Death overs 3 overs left",
    "Tailender batting 10 runs",
    "New batsman at crease",
    "Last over defending 12 runs",
    "Spinners bowling middle overs",
    "Fast bowler opening spell",
    "Set batsman on strike"
]

user_input = st.selectbox("Select Match Situation", situations)

if st.button("Get Tactical Advice"):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Analyzing...")
        time.sleep(1)

        if OLLAMA_AVAILABLE:
            response = ollama.chat(
                model="gemma3:latest",
                messages=st.session_state.messages
            )
            reply = response["message"]["content"]
            reply = " ".join(reply.split()[:4])
        else:
            reply = "Short ball leg trap"

        placeholder.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("---")
st.markdown("🏏 Cricket Tactical AI System")
