import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="Basketball Tracking App", layout="wide")
st.title("Basketball Player Performance Tracker")

DATA_FILE = "basketball_data.csv"

# ======================
# Load or initialize data
# ======================
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
else:
    data = pd.DataFrame(columns=["GameDate", "Player", "Points", "Rebounds", "Assists"])

# ======================
# Add New Game Data Form
# ======================
st.subheader("Add New Game Data")

with st.form("game_form"):
    game_date = st.date_input("Game Date", datetime.today())
    player = st.text_input("Player Name")
    points = st.number_input("Points", min_value=0)
    rebounds = st.number_input("Rebounds", min_value=0)
    assists = st.number_input("Assists", min_value=0)
    submit = st.form_submit_button("Add Game")

if submit:
    new_row = pd.DataFrame({
        "GameDate": [game_date.strftime("%Y-%m-%d")],
        "Player": [player],
        "Points": [points],
        "Rebounds": [rebounds],
        "Assists": [assists]
    })
    data = pd.concat([data, new_row], ignore_index=True)
    data.to_csv(DATA_FILE, index=False)  # <-- persist to CSV
    st.success(f"Added new game for {player} on {game_date.strftime('%Y-%m-%d')}")

# Show current data
st.subheader("Current Data")
st.dataframe(data)

# ======================
# Trending Analysis
# ======================
st.subheader("Trending Analysis")

if not data.empty:
    fig = px.line(data, x="GameDate", y="Points", color="Player",
                  title="Points Trend Over Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(data, x="GameDate", y="Rebounds", color="Player",
                   title="Rebounds Trend Over Time", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# ======================
# Export Data
# ======================
st.subheader("Export Data")

csv_export = data.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv_export,
    file_name='basketball_data_export.csv',
    mime='text/csv'
)
