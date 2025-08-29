import streamlit as st
import pandas as pd
import plotly.express as px
import os
from io import BytesIO

# -----------------------------
# Excel file to store all data
# -----------------------------
EXCEL_FILE = "basketball_data.xlsx"

# -----------------------------
# Load existing data or initialize
# -----------------------------
if os.path.exists(EXCEL_FILE):
    xl = pd.ExcelFile(EXCEL_FILE)
    try:
        games_df = pd.read_excel(xl, "Games")
        shooting_df = pd.read_excel(xl, "Shooting")
        conditioning_df = pd.read_excel(xl, "Conditioning")
    except:
        games_df = pd.DataFrame(columns=["Date", "Points", "Assists", "Turnovers", "Steals",
                                         "3pt Made", "3pt Attempted", "2pt Made", "2pt Attempted"])
        shooting_df = pd.DataFrame(columns=["Date", "21 Drill Min", "21 Drill Sec", "10 Layups Min", "10 Layups Sec",
                                            "Around Key Shots", "3pt in 4min", "3pt Made", "3pt Attempted",
                                            "2pt Made", "2pt Attempted"])
        conditioning_df = pd.DataFrame(columns=["Date", "17s Drill Sec", "1 Suicide Sec", "5 Suicides Sec", "Def Slides 30s"])
else:
    games_df = pd.DataFrame(columns=["Date", "Points", "Assists", "Turnovers", "Steals",
                                     "3pt Made", "3pt Attempted", "2pt Made", "2pt Attempted"])
    shooting_df = pd.DataFrame(columns=["Date", "21 Drill Min", "21 Drill Sec", "10 Layups Min", "10 Layups Sec",
                                        "Around Key Shots", "3pt in 4min", "3pt Made", "3pt Attempted",
                                        "2pt Made", "2pt Attempted"])
    conditioning_df = pd.DataFrame(columns=["Date", "17s Drill Sec", "1 Suicide Sec", "5 Suicides Sec", "Def Slides 30s"])

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/63/Kobe_Bryant_8.jpg" width="200">
        <h2 style="color:orange;">"The most important thing is to try and inspire people so that they can be great in whatever they want to do." – Kobe Bryant</h2>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# -----------------------------
# Activity selection
# -----------------------------
activity = st.radio("Select Activity Type", ["Games Stats", "Shooting Practice", "Conditioning"])

# -----------------------------
# Data Entry
# -----------------------------
if activity == "Games Stats":
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
        new_row = pd.DataFrame([[date, points, assists, turnovers, steals, g3m, g3a, g2m, g2a]], columns=games_df.columns)
        games_df = pd.concat([games_df, new_row], ignore_index=True)
        st.success("✅ Game data saved!")

elif activity == "Shooting Practice":
    st.subheader("Enter Shooting Practice Data")
    with st.form("shooting_form", clear_on_submit=True):
        date = st.date_input("Date", key="shooting_date")
        col1, col2 = st.columns(2)
        d21m = col1.number_input("21 Drill (Min)", min_value=0, step=1)
        d21s = col2.number_input("21 Drill (Sec)", min_value=0, step=1)
        col3, col4 = st.columns(2)
        laym = col3.number_input("10 Layups (Min)", min_value=0, step=1)
        lays = col4.number_input("10 Layups (Sec)", min_value=0, step=1)
        around_key = st.number_input("Around the Key Shots (4 min)", min_value=0, step=1)
        threes_4min = st.number_input("3pt in 4min", min_value=0, step=1)
        col5, col6 = st.columns(2)
        s3m = col5.number_input("3pt Made", min_value=0, step=1)
        s3a = col6.number_input("3pt Attempted", min_value=0, step=1)
        col7, col8 = st.columns(2)
        s2m = col7.number_input("2pt Made", min_value=0, step=1)
        s2a = col8.number_input("2pt Attempted", min_value=0, step=1)
        submitted = st.form_submit_button("Save Shooting Data")
    if submitted:
        new_row = pd.DataFrame([[date, d21m, d21s, laym, lays, around_key, threes_4min, s3m, s3a, s2m, s2a]], columns=shooting_df.columns)
        shooting_df = pd.concat([shooting_df, new_row], ignore_index=True)
        st.success("✅ Shooting practice data saved!")

elif activity == "Conditioning":
    st.subheader("Enter Conditioning Data")
    with st.form("conditioning_form", clear_on_submit=True):
        date = st.date_input("Date", key="cond_date")
        d17 = st.number_input("17s Drill (Sec)", min_value=0.0, step=0.1)
        suicide1 = st.number_input("1 Suicide (Sec)", min_value=0.0, step=0.1)
        suicides5 = st.number_input("5 Suicides (Sec)", min_value=0.0, step=0.1)
        slides = st.number_input("Defensive Slides (30s)", min_value=0, step=1)
        submitted = st.form_submit_button("Save Conditioning Data")
    if submitted:
        new_row = pd.DataFrame([[date, d17, suicide1, suicides5, slides]], columns=conditioning_df.columns)
        conditioning_df = pd.concat([conditioning_df, new_row], ignore_index=True)
        st.success("✅ Conditioning data saved!")

# -----------------------------
# Graphs + Export
# -----------------------------
st.markdown("---")
st.subheader("📊 Metrics & Export")

# Excel export function
def export_to_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        games_df.to_excel(writer, sheet_name="Games", index=False)
        shooting_df.to_excel(writer, sheet_name="Shooting", index=False)
        conditioning_df.to_excel(writer, sheet_name="Conditioning", index=False)
    return output

# Games graphs
if not games_df.empty:
    games_df["3pt %"] = (games_df["3pt Made"] / games_df["3pt Attempted"].replace(0, pd.NA)) * 100
    games_df["2pt %"] = (games_df["2pt Made"] / games_df["2pt Attempted"].replace(0, pd.NA)) * 100
    st.markdown("### 🏀 Games Metrics")
    for col in ["Points", "Assists", "Turnovers", "Steals", "3pt Made", "3pt Attempted", "2pt Made", "2pt Attempted", "3pt %", "2pt %"]:
        fig = px.line(games_df, x="Date", y=col, markers=True, title=col)
        st.plotly_chart(fig, use_container_width=True)

# Shooting graphs
if not shooting_df.empty:
    shooting_df["3pt %"] = (shooting_df["3pt Made"] / shooting_df["3pt Attempted"].replace(0, pd.NA)) * 100
    shooting_df["2pt %"] = (shooting_df["2pt Made"] / shooting_df["2pt Attempted"].replace(0, pd.NA)) * 100
    st.markdown("### 🎯 Shooting Practice Metrics")
    for col in ["21 Drill Min", "21 Drill Sec", "10 Layups Min", "10 Layups Sec", "Around Key Shots", "3pt in 4min", "3pt Made", "3pt Attempted", "2pt Made", "2pt Attempted", "3pt %", "2pt %"]:
        fig = px.line(shooting_df, x="Date", y=col, markers=True, title=col)
        st.plotly_chart(fig, use_container_width=True)

# Conditioning graphs
if not conditioning_df.empty:
    st.markdown("### 💪 Conditioning Metrics")
    for col in ["17s Drill Sec", "1 Suicide Sec", "5 Suicides Sec", "Def Slides 30s"]:
        fig = px.line(conditioning_df, x="Date", y=col, markers=True, title=col)
        st.plotly_chart(fig, use_container_width=True)

# Export button
st.download_button(
    label="⬇️ Download All Data (Excel)",
    data=export_to_excel().getvalue(),
    file_name="basketball_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
