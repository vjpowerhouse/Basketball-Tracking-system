import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Initialize session state
if "games" not in st.session_state:
    st.session_state.games = []
if "shooting" not in st.session_state:
    st.session_state.shooting = []
if "conditioning" not in st.session_state:
    st.session_state.conditioning = []

st.set_page_config(page_title="Basketball Tracker", layout="wide")

# Header with Kobe Bryant quote
st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://upload.wikimedia.org/wikipedia/en/2/21/Kobe_Bryant_8.png" width="120"/>
        <h1>🏀 Basketball Performance Tracker</h1>
        <h3>"The most important thing is to try and inspire people so that they can be great in whatever they want to do." – Kobe Bryant</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# Activity selection
activity = st.radio(
    "Which activity do you want to log?",
    ["Games Stats", "Shooting Practice", "Conditioning"]
)

# -------------------------------
# Games Stats
# -------------------------------
if activity == "Games Stats":
    st.subheader("📊 Game Stats Entry")

    points = st.number_input("Points", min_value=0, step=1)
    assists = st.number_input("Assists", min_value=0, step=1)
    turnovers = st.number_input("Turnovers", min_value=0, step=1)
    steals = st.number_input("Steals", min_value=0, step=1)
    threes_made = st.number_input("3-pointers Made", min_value=0, step=1)
    threes_attempt = st.number_input("3-pointers Attempted", min_value=0, step=1)
    twos_made = st.number_input("2-pointers Made", min_value=0, step=1)
    twos_attempt = st.number_input("2-pointers Attempted", min_value=0, step=1)

    if st.button("Save Game Stats"):
        st.session_state.games.append({
            "Points": points,
            "Assists": assists,
            "Turnovers": turnovers,
            "Steals": steals,
            "3P Made": threes_made,
            "3P Attempt": threes_attempt,
            "2P Made": twos_made,
            "2P Attempt": twos_attempt
        })
        st.success("✅ Game stats saved!")

# -------------------------------
# Shooting Practice
# -------------------------------
elif activity == "Shooting Practice":
    st.subheader("🏀 Shooting Practice Entry")

    # 21-point drill
    s1m = st.number_input("21-points drill - Minutes", min_value=0, step=1)
    s1s = st.number_input("21-points drill - Seconds", min_value=0, step=1)

    # 10 layups drill
    s2m = st.number_input("10 Layups - Minutes", min_value=0, step=1)
    s2s = st.number_input("10 Layups - Seconds", min_value=0, step=1)

    around_key = st.number_input("Around the Key Shots in 4 mins", min_value=0, step=1)
    threes_in_4 = st.number_input("3-pointers in 4 mins", min_value=0, step=1)

    threes_made = st.number_input("3P Made (Practice)", min_value=0, step=1)
    threes_attempt = st.number_input("3P Attempt (Practice)", min_value=0, step=1)
    twos_made = st.number_input("2P Made (Practice)", min_value=0, step=1)
    twos_attempt = st.number_input("2P Attempt (Practice)", min_value=0, step=1)

    if st.button("Save Shooting Practice"):
        st.session_state.shooting.append({
            "21 Drill Time": s1m*60 + s1s,
            "10 Layups Time": s2m*60 + s2s,
            "Around Key": around_key,
            "3P in 4min": threes_in_4,
            "3P Made": threes_made,
            "3P Attempt": threes_attempt,
            "2P Made": twos_made,
            "2P Attempt": twos_attempt
        })
        st.success("✅ Shooting practice saved!")

# -------------------------------
# Conditioning
# -------------------------------
elif activity == "Conditioning":
    st.subheader("💪 Conditioning Entry")

    c1m = st.number_input("17s Drill - Minutes", min_value=0, step=1)
    c1s = st.number_input("17s Drill - Seconds", min_value=0, step=1)

    c2m = st.number_input("1 Suicide - Minutes", min_value=0, step=1)
    c2s = st.number_input("1 Suicide - Seconds", min_value=0, step=1)

    c3m = st.number_input("5 Suicides - Minutes", min_value=0, step=1)
    c3s = st.number_input("5 Suicides - Seconds", min_value=0, step=1)

    slides = st.number_input("Defensive Slides in 30s", min_value=0, step=1)

    if st.button("Save Conditioning"):
        st.session_state.conditioning.append({
            "17s Drill Time": c1m*60 + c1s,
            "1 Suicide Time": c2m*60 + c2s,
            "5 Suicides Time": c3m*60 + c3s,
            "Defensive Slides": slides
        })
        st.success("✅ Conditioning data saved!")

# -------------------------------
# Export to Excel
# -------------------------------
if st.button("📥 Export All Data to Excel"):
    with pd.ExcelWriter("basketball_data.xlsx") as writer:
        if st.session_state.games:
            pd.DataFrame(st.session_state.games).to_excel(writer, sheet_name="Games", index=False)
        if st.session_state.shooting:
            pd.DataFrame(st.session_state.shooting).to_excel(writer, sheet_name="Shooting", index=False)
        if st.session_state.conditioning:
            pd.DataFrame(st.session_state.conditioning).to_excel(writer, sheet_name="Conditioning", index=False)
    st.success("✅ Data exported to basketball_data.xlsx")