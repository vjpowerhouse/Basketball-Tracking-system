import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from supabase import create_client, Client

# -------------------------------
# Supabase connection using Streamlit secrets
# -------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# App Setup
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")

# -------------------------------
# User session
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = st.text_input("Enter your unique User ID:", "")

if not st.session_state.user_id:
    st.stop()

# -------------------------------
# Header
# -------------------------------
st.markdown("""
<h1 style="text-align:center;">🏀 Basketball Performance Tracker</h1>
<h3 style="text-align:center;font-style:italic;color:#555;">
"The most important thing is you must put everybody on notice that you're here and you are for real." – Kobe Bryant
</h3>
""", unsafe_allow_html=True)

# -------------------------------
# Activity selection
# -------------------------------
activity = st.radio("Select Activity to Log:", ["Games Stats", "Shooting Practice", "Conditioning", "Dribbling"])

# -------------------------------
# Input Forms
# -------------------------------
def log_activity(activity_type):
    data = {"user_id": st.session_state.user_id, "activity": activity_type, "timestamp": datetime.now()}
    
    if activity_type == "Games Stats":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            data["Points"] = st.number_input("Points", min_value=0)
            data["Assists"] = st.number_input("Assists", min_value=0)
        with col2:
            data["Turnovers"] = st.number_input("Turnovers", min_value=0)
            data["Steals"] = st.number_input("Steals", min_value=0)
        with col3:
            threes_made = st.number_input("3P Made", min_value=0)
            threes_attempt = st.number_input("3P Attempt", min_value=0)
            data["3P Made"] = threes_made
            data["3P Attempt"] = threes_attempt
            data["3P %"] = round(threes_made / threes_attempt * 100, 2) if threes_attempt else 0
        with col4:
            twos_made = st.number_input("2P Made", min_value=0)
            twos_attempt = st.number_input("2P Attempt", min_value=0)
            data["2P Made"] = twos_made
            data["2P Attempt"] = twos_attempt
            data["2P %"] = round(twos_made / twos_attempt * 100, 2) if twos_attempt else 0

    elif activity_type == "Shooting Practice":
        col1, col2 = st.columns(2)
        with col1:
            s21_m = st.number_input("21 Drill - Minutes", min_value=0)
            s21_s = st.number_input("21 Drill - Seconds", min_value=0)
            layups_m = st.number_input("10 Layups - Minutes", min_value=0)
            layups_s = st.number_input("10 Layups - Seconds", min_value=0)
            data["21 Drill Time (s)"] = s21_m*60 + s21_s
            data["10 Layups Time (s)"] = layups_m*60 + layups_s
        with col2:
            around_key = st.number_input("Around Key Shots in 4 mins", min_value=0)
            threes_4min = st.number_input("3P in 4 mins", min_value=0)
            threes_made = st.number_input("3P Made", min_value=0)
            threes_attempt = st.number_input("3P Attempt", min_value=0)
            twos_made = st.number_input("2P Made", min_value=0)
            twos_attempt = st.number_input("2P Attempt", min_value=0)
            data["Around Key"] = around_key
            data["3P in 4min"] = threes_4min
            data["3P Made"] = threes_made
            data["3P Attempt"] = threes_attempt
            data["2P Made"] = twos_made
            data["2P Attempt"] = twos_attempt
            data["3P %"] = round(threes_made / threes_attempt * 100, 2) if threes_attempt else 0
            data["2P %"] = round(twos_made / twos_attempt * 100, 2) if twos_attempt else 0

    elif activity_type == "Conditioning":
        col1, col2, col3 = st.columns(3)
        with col1:
            drill17_m = st.number_input("17s Drill - Minutes", min_value=0)
            drill17_s = st.number_input("17s Drill - Seconds", min_value=0)
            suicide1_m = st.number_input("1 Suicide - Minutes", min_value=0)
            suicide1_s = st.number_input("1 Suicide - Seconds", min_value=0)
            data["17s Drill Time (s)"] = drill17_m*60 + drill17_s
            data["1 Suicide Time (s)"] = suicide1_m*60 + suicide1_s
        with col2:
            suicide5_m = st.number_input("5 Suicides - Minutes", min_value=0)
            suicide5_s = st.number_input("5 Suicides - Seconds", min_value=0)
            data["5 Suicides Time (s)"] = suicide5_m*60 + suicide5_s
        with col3:
            slides = st.number_input("Defensive Slides in 30s", min_value=0)
            data["Defensive Slides"] = slides

    elif activity_type == "Dribbling":
        data["2 Ball Dribble (min)"] = st.number_input("2 Ball Dribble Minutes", min_value=0)
        data["1 Ball Dribble (min)"] = st.number_input("1 Ball Dribble Minutes", min_value=0)

    if st.button(f"Save {activity_type}"):
        supabase.table("user_stats").insert(data).execute()
        st.success(f"✅ {activity_type} saved!")

log_activity(activity)

# -------------------------------
# Graphing Section
# -------------------------------
def show_graphs(activity_filter):
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).eq("activity", activity_filter).execute()
    data = res.data
    if not data:
        st.info(f"No data for {activity_filter} yet.")
        return
    df = pd.DataFrame(data)
    for col in df.columns:
        if col not in ["id", "user_id", "activity", "timestamp"] and df[col].dtype in ["int", "float"]:
            fig = px.line(df, y=col, x="timestamp", title=f"{activity_filter} - {col}", markers=True)
            st.plotly_chart(fig, use_container_width=True)

st.write("## Your Performance Graphs")
for act in ["Games Stats", "Shooting Practice", "Conditioning", "Dribbling"]:
    show_graphs(act)