import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO

# --------------------------
# Google Sheets Setup
# --------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Basketball_Tracking")

games_ws = sheet.worksheet("Games")
shooting_ws = sheet.worksheet("Shooting Practice")
cond_ws = sheet.worksheet("Conditioning")

# --------------------------
# App Config
# --------------------------
st.set_page_config(page_title="🏀 Basketball Tracker", layout="wide")

# --------------------------
# Header with Kobe + Logo
# --------------------------
st.markdown(
    """
    <div style="text-align:center; background-color:#1a1a1a; padding:20px; border-radius:15px; margin-bottom:20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png" 
             width="80" style="margin-right:15px;">
        <img src="https://upload.wikimedia.org/wikipedia/en/0/03/Kobe_Bryant_2015.jpg" 
             width="120" style="border-radius:50%; border:3px solid orange;">
        <h1 style="color:orange;">🏀 Basketball Training & Game Tracker 🏀</h1>
        <h3 style="color:white;">"The most important thing is to try and inspire people so that they can be great in whatever they want to do." – Kobe Bryant</h3>
    </div>
    """, unsafe_allow_html=True
)

# --------------------------
# Tabs for Entry + Graphs
# --------------------------
tabs = st.tabs(["📋 Data Entry", "📊 Games Metrics", "🏀 Shooting Practice Metrics", "💪 Conditioning Metrics", "📂 Export Data"])

# --------------------------
# Data Entry Tab
# --------------------------
with tabs[0]:
    st.header("📋 Data Entry")

    activity_type = st.selectbox("Select Activity Type", ["Games", "Shooting Practice", "Conditioning"])
    date = st.date_input("Date")

    entry = {"Date": str(date)}

    if activity_type == "Games":
        entry["Points"] = st.number_input("Points", 0)
        entry["Assists"] = st.number_input("Assists", 0)
        entry["Turnovers"] = st.number_input("Turnovers", 0)
        entry["Steals"] = st.number_input("Steals", 0)
        entry["3PM"] = st.number_input("3PT Made", 0)
        entry["3PA"] = st.number_input("3PT Attempts", 0)
        entry["2PM"] = st.number_input("2PT Made", 0)
        entry["2PA"] = st.number_input("2PT Attempts", 0)

        if st.button("Save Game Entry"):
            games_ws.append_row(list(entry.values()))
            st.success("✅ Game data saved!")

    elif activity_type == "Shooting Practice":
        col1, col2 = st.columns(2)
        with col1:
            mins_21 = st.number_input("21-points Drill (Mins)", 0)
        with col2:
            secs_21 = st.number_input("21-points Drill (Secs)", 0)

        col3, col4 = st.columns(2)
        with col3:
            mins_layups = st.number_input("10 Layups Drill (Mins)", 0)
        with col4:
            secs_layups = st.number_input("10 Layups Drill (Secs)", 0)

        entry["21 Drill (min)"] = mins_21 + secs_21/60
        entry["10 Layups (min)"] = mins_layups + secs_layups/60
        entry["Around Key (shots)"] = st.number_input("Around the Key Shots in 4 mins", 0)
        entry["3PT in 4min"] = st.number_input("3-Pointers in 4 mins", 0)
        entry["3PM"] = st.number_input("3PT Made", 0)
        entry["3PA"] = st.number_input("3PT Attempts", 0)
        entry["2PM"] = st.number_input("2PT Made", 0)
        entry["2PA"] = st.number_input("2PT Attempts", 0)

        if st.button("Save Shooting Entry"):
            shooting_ws.append_row(list(entry.values()))
            st.success("✅ Shooting practice data saved!")

    elif activity_type == "Conditioning":
        entry["17s Drill (min)"] = st.number_input("Time for 17s drill (mins)", 0.0)
        entry["1 Suicide (min)"] = st.number_input("Time for 1 suicide (mins)", 0.0)
        entry["5 Suicides (min)"] = st.number_input("Time for 5 suicides (mins)", 0.0)
        entry["Defensive Slides"] = st.number_input("Number of defensive slides in 30s", 0)

        if st.button("Save Conditioning Entry"):
            cond_ws.append_row(list(entry.values()))
            st.success("✅ Conditioning data saved!")

# --------------------------
# Helper: Load Sheets
# --------------------------
def load_ws(ws):
    data = pd.DataFrame(ws.get_all_records())
    return data if not data.empty else pd.DataFrame()

# --------------------------
# Games Metrics
# --------------------------
with tabs[1]:
    st.header("📊 Games Metrics")
    df = load_ws(games_ws)
    if not df.empty:
        df["3P%"] = (df["3PM"] / df["3PA"].replace(0, 1))*100
        df["2P%"] = (df["2PM"] / df["2PA"].replace(0, 1))*100

        for col in ["Points", "Assists", "Turnovers", "Steals", "3PM", "2PM", "3P%", "2P%"]:
            st.plotly_chart(px.line(df, x="Date", y=col, markers=True, title=col), use_container_width=True)

# --------------------------
# Shooting Practice Metrics
# --------------------------
with tabs[2]:
    st.header("🏀 Shooting Practice Metrics")
    df = load_ws(shooting_ws)
    if not df.empty:
        df["3P%"] = (df["3PM"] / df["3PA"].replace(0, 1))*100
        df["2P%"] = (df["2PM"] / df["2PA"].replace(0, 1))*100

        for col in ["21 Drill (min)", "10 Layups (min)", "Around Key (shots)", "3PT in 4min", "3PM", "2PM", "3P%", "2P%"]:
            st.plotly_chart(px.line(df, x="Date", y=col, markers=True, title=col), use_container_width=True)

# --------------------------
# Conditioning Metrics
# --------------------------
with tabs[3]:
    st.header("💪 Conditioning Metrics")
    df = load_ws(cond_ws)
    if not df.empty:
        for col in ["17s Drill (min)", "1 Suicide (min)", "5 Suicides (min)", "Defensive Slides"]:
            st.plotly_chart(px.line(df, x="Date", y=col, markers=True, title=col), use_container_width=True)

# --------------------------
# Export Data
# --------------------------
with tabs[4]:
    st.header("📂 Export Data to Excel")
    gdf, sdf, cdf = load_ws(games_ws), load_ws(shooting_ws), load_ws(cond_ws)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        gdf.to_excel(writer, sheet_name="Games", index=False)
        sdf.to_excel(writer, sheet_name="Shooting", index=False)
        cdf.to_excel(writer, sheet_name="Conditioning", index=False)

    st.download_button("⬇️ Download Excel", data=output.getvalue(), file_name="basketball_data.xlsx", mime="application/vnd.ms-excel")
