# basketball_app_final_plotly.py

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import plotly.express as px

# -----------------------------
# Google Sheets setup (via Secrets)
# -----------------------------
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
gcp_json = st.secrets["gcp"]["json"]       # JSON credentials stored in Streamlit Secrets
SHEET_NAME = st.secrets["gcp"]["sheet_name"]

credentials_dict = json.loads(gcp_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME)

# -----------------------------
# Helpers
# -----------------------------
def get_worksheet(name):
    try:
        ws = sheet.worksheet(name)
    except gspread.WorksheetNotFound:
        ws = sheet.add_worksheet(title=name, rows="1000", cols="20")
        ws.append_row(["Date", "Metric", "Value"])
    return ws

def log_data(section, metric, value):
    ws = get_worksheet(section)
    ws.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), metric, value])

def get_data(section):
    ws = get_worksheet(section)
    df = pd.DataFrame(ws.get_all_records())
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
    return df

# -----------------------------
# UI
# -----------------------------
st.title("🏀 Basketball Performance Tracker (Streamlit Cloud)")

# -----------------------------
# Quick Summary KPIs
# -----------------------------
st.subheader("📌 Quick Performance Summary")
sections = ["Games", "Practice", "Conditioning"]

for sec in sections:
    df_sec = get_data(sec)
    if not df_sec.empty:
        st.markdown(f"**{sec}**")
        latest_metrics = df_sec.groupby("Metric").last()["Value"]
        for metric, value in latest_metrics.items():
            st.write(f"{metric}: {value}")
        if len(df_sec) >= 2:
            score = 0
            time_metrics = ["21 Points Drill Time", "10 Layups Time", "17s Drill Time", "1 Suicide Time", "5 Suicides Time"]
            for metric_name in df_sec["Metric"].unique():
                df_metric = df_sec[df_sec["Metric"] == metric_name].sort_values("Date")
                latest = df_metric["Value"].iloc[-1]
                prev = df_metric["Value"].iloc[-2]
                if metric_name in time_metrics:
                    score += 1 if prev > latest else -1
                else:
                    score += 1 if latest > prev else -1
            st.write(f"**{sec} Overall Trend Score:** {score} ✅/❌")

# -----------------------------
# Navigation Menu
# -----------------------------
menu = st.sidebar.radio("Navigate", ["Games", "Practice", "Conditioning", "Analytics"])

# -----------------------------
# Games
# -----------------------------
if menu == "Games":
    st.header("🎮 Log Game Stats")
    points = st.number_input("Points", min_value=0, step=1)
    assists = st.number_input("Assists", min_value=0, step=1)
    turnovers = st.number_input("Turnovers", min_value=0, step=1)
    steals = st.number_input("Steals", min_value=0, step=1)
    if st.button("Save Game Stats"):
        log_data("Games", "Points", points)
        log_data("Games", "Assists", assists)
        log_data("Games", "Turnovers", turnovers)
        log_data("Games", "Steals", steals)
        st.success("Game stats saved to Google Sheet!")

# -----------------------------
# Practice
# -----------------------------
elif menu == "Practice":
    st.header("🏋️ Practice Drills")
    t21 = st.number_input("Time for 21 Points Drill (sec)", min_value=0.0)
    tlayups = st.number_input("Time for 10 Layups (sec)", min_value=0.0)
    shots_key = st.number_input("Shots Around Key in 4 min (# made)", min_value=0)
    threes_attempt = st.number_input("3 Pointers Attempted (4 min)", min_value=0)
    threes_made = st.number_input("3 Pointers Made (4 min)", min_value=0)
    mid_attempt = st.number_input("Mid Range Attempted", min_value=0)
    mid_made = st.number_input("Mid Range Made", min_value=0)
    if st.button("Save Practice Stats"):
        log_data("Practice", "21 Points Drill Time", t21)
        log_data("Practice", "10 Layups Time", tlayups)
        log_data("Practice", "Shots Around Key (Made)", shots_key)
        if threes_attempt > 0:
            log_data("Practice", "3 Point %", (threes_made / threes_attempt) * 100)
        if mid_attempt > 0:
            log_data("Practice", "Mid Range %", (mid_made / mid_attempt) * 100)
        st.success("Practice stats saved to Google Sheet!")

# -----------------------------
# Conditioning
# -----------------------------
elif menu == "Conditioning":
    st.header("💨 Conditioning Drills")
    t17 = st.number_input("Time for 17s Drill (sec)", min_value=0.0)
    tsuicide = st.number_input("Time for 1 Suicide (sec)", min_value=0.0)
    t5suicides = st.number_input("Time for 5 Suicides (sec)", min_value=0.0)
    slides = st.number_input("Number of Slides in 30s", min_value=0)
    if st.button("Save Conditioning Stats"):
        log_data("Conditioning", "17s Drill Time", t17)
        log_data("Conditioning", "1 Suicide Time", tsuicide)
        log_data("Conditioning", "5 Suicides Time", t5suicides)
        log_data("Conditioning", "Slides in 30s", slides)
        st.success("Conditioning stats saved to Google Sheet!")

# -----------------------------
# Analytics with Conditional Coloring
# -----------------------------
elif menu == "Analytics":
    st.subheader("📊 Performance Trends")
    section_choice = st.selectbox("Select section", ["Games", "Practice", "Conditioning"])
    df = get_data(section_choice)
    if df.empty:
        st.info("No data yet. Enter stats first.")
    else:
        metric_choice = st.selectbox("Select metric", sorted(df["Metric"].unique()))
        df_metric = df[df["Metric"] == metric_choice].sort_values("Date")
        st.dataframe(df_metric)

        # Determine colors
        time_metrics = ["21 Points Drill Time", "10 Layups Time", "17s Drill Time", "1 Suicide Time", "5 Suicides Time"]
        colors = []
        for i in range(len(df_metric)):
            if i == 0:
                colors.append("gray")
            else:
                prev = df_metric["Value"].iloc[i-1]
                curr = df_metric["Value"].iloc[i]
                if metric_choice in time_metrics:
                    colors.append("green" if curr < prev else "red")
                else:
                    colors.append("green" if curr > prev else "red")

        fig = px.line(df_metric, x="Date", y="Value", markers=True)
        fig.update_traces(marker=dict(color=colors, size=10), line=dict(color="blue"))
        st.plotly_chart(fig)

        # Latest trend indicator
        if len(df_metric) >= 2:
            latest = df_metric["Value"].iloc[-1]
            prev = df_metric["Value"].iloc[-2]
            if metric_choice in time_metrics:
                trend_up = prev > latest
            else:
                trend_up = latest > prev
            st.markdown(f"**Trend:** {'✅ Improving' if trend_up else '❌ Declining'} ({prev} → {latest})")
