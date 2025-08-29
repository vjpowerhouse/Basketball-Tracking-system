import streamlit as st
import pandas as pd
import plotly.express as px
import os
from io import BytesIO

# -------------------
# File settings
# -------------------
EXCEL_FILE = "basketball_tracker.xlsx"

# -------------------
# Page Config
# -------------------
st.set_page_config(
    page_title="Basketball Performance Tracker",
    page_icon="🏀",
    layout="wide"
)

# -------------------
# Custom CSS
# -------------------
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)),
                    url("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Basketball_court_illustration.svg/1920px-Basketball_court_illustration.svg.png");
        background-size: cover;
    }
    .title {
        text-align: center;
        color: #E74C3C;
        font-size: 36px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        font-style: italic;
        font-size: 20px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------
# Header with Kobe Bryant
# -------------------
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/6/63/Kobe_Bryant_8.jpg",
    use_container_width=True
)
st.markdown('<div class="title">Basketball Performance Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">"The most important thing is to try and inspire people so that they can be great in whatever they want to do." – Kobe Bryant</div>', unsafe_allow_html=True)
st.markdown("---")

# -------------------
# Initialize DataFrames
# -------------------
if os.path.exists(EXCEL_FILE):
    xl = pd.ExcelFile(EXCEL_FILE)
    games_df = pd.read_excel(xl, "Games")
    shooting_df = pd.read_excel(xl, "Shooting")
    conditioning_df = pd.read_excel(xl, "Conditioning")
else:
    games_df = pd.DataFrame(columns=["Date", "Points", "Assists", "Turnovers", "Steals",
                                     "3pt Made", "3pt Attempted", "2pt Made", "2pt Attempted"])
    shooting_df = pd.DataFrame(columns=["Date", "21 Drill (min)", "21 Drill (sec)",
                                        "10 Layups (min)", "10 Layups (sec)",
                                        "Around Key (shots)", "3pt in 4min",
                                        "3pt Made", "3pt Attempted", "2pt Made", "2pt Attempted"])
    conditioning_df = pd.DataFrame(columns=["Date", "17s Drill (sec)",
                                            "1 Suicide (sec)", "5 Suicides (sec)",
                                            "Def Slides (30s)"])

# -------------------
# Tabs for Data Entry
# -------------------
tab1, tab2, tab3, tab4 = st.tabs(["🏀 Games", "🎯 Shooting Practice", "💪 Conditioning", "📊 Metrics & Export"])

with tab1:
    st.subheader("Enter Game Data")
    with st.form("games_form", clear_on_submit=True):
        date = st.date_input("Date")
        points = st.number_input("Points", min_value=0, step=1)
        assists = st.number_input("Assists", min_value=0, step=1)
        turnovers = st.number_input("Turnovers", min_value=0, step=1)
        steals = st.number_input("Steals", min_value=0, step=1)
        g3m = st.number_input("3pt Made", min_value=0, step=1)
        g3a = st.number_input("3pt Attempted", min_value=0, step=1)
        g2m = st.number_input("2pt Made", min_value=0, step=1)
        g2a = st.number_input("2pt Attempted", min_value=0, step=1)
        submitted = st.form_submit_button("Save Game Data")
    if submitted:
        new_row = pd.DataFrame([[date, points, assists, turnovers, steals, g3m, g3a, g2m, g2a]],
                               columns=games_df.columns)
        games_df = pd.concat([games_df, new_row], ignore_index=True)
        st.success("✅ Game data saved!")

with tab2:
    st.subheader("Enter Shooting Practice Data")
    with st.form("shooting_form", clear_on_submit=True):
        date = st.date_input("Date", key="shooting_date")
        c1, c2 = st.columns(2)
        d21m = c1.number_input("21 Drill (min)", min_value=0, step=1)
        d21s = c2.number_input("21 Drill (sec)", min_value=0, step=1)
        c3, c4 = st.columns(2)
        laym = c3.number_input("10 Layups (min)", min_value=0, step=1)
        lays = c4.number_input("10 Layups (sec)", min_value=0, step=1)
        around_key = st.number_input("Around the Key Shots in 4 min", min_value=0, step=1)
        threes_4min = st.number_input("3pt in 4 min", min_value=0, step=1)
        c5, c6 = st.columns(2)
        s3m = c5.number_input("3pt Made", min_value=0, step=1)
        s3a = c6.number_input("3pt Attempted", min_value=0, step=1)
        c7, c8 = st.columns(2)
        s2m =
