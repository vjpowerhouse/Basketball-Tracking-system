import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from datetime import datetime
import uuid

# -------------------------------
# Supabase configuration
# -------------------------------
SUPABASE_URL = "https://yegkoltoaqzfjyzbhdrc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllZ2tvbHRvYXF6Zmp5emJoZHJjIiwicm9sIjoibm9uIiwiaWF0IjoxNzU2Njk2MTUyLCJleHAiOjIwNzIyNzIxNTJ9.dumcEar9kCvFQMRemqq0-PB4P1QYZSRm1MdFKGfwwcg"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")
st.title("🏀 Basketball Performance Tracker")

# -------------------------------
# Initialize user session
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# -------------------------------
# Activity selection
# -------------------------------
activity = st.radio("Select Activity:", ["Games Stats", "Shooting Practice", "Conditioning", "Dribbling"])

# -------------------------------
# Data entry
# -------------------------------

def save_to_supabase(data):
    data["user_id"] = st.session_state.user_id
    data["timestamp"] = datetime.now().isoformat()
    supabase.table("user_stats").insert(data).execute()
    st.success("✅ Data saved to Supabase!")

# -------- Games Stats --------
if activity == "Games Stats":
    st.subheader("📊 Games Stats Entry")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        points = st.number_input("Points", min_value=0)
        assists = st.number_input("Assists", min_value=0)
    with col2:
        turnovers = st.number_input("Turnovers", min_value=0)
        steals = st.number_input("Steals", min_value=0)
    with col3:
        threes_made = st.number_input("3P Made", min_value=0)
        threes_attempt = st.number_input("3P Attempt", min_value=0)
    with col4:
        twos_made = st.number_input("2P Made", min_value=0)
        twos_attempt = st.number_input("2P Attempt", min_value=0)

    if st.button("Save Game Stats"):
        save_to_supabase({
            "activity": "Games",
            "points": points,
            "assists": assists,
            "turnovers": turnovers,
            "steals": steals,
            "threes_made": threes_made,
            "twos_made": twos_made,
            "three_pct": round(threes_made/threes_attempt*100,2) if threes_attempt else 0,
            "two_pct": round(twos_made/twos_attempt*100,2) if twos_attempt else 0
        })

# -------- Shooting Practice --------
elif activity == "Shooting Practice":
    st.subheader("🏀 Shooting Practice Entry")
    col1, col2 = st.columns(2)
    with col1:
        drill_21_m = st.number_input("21 Drill - Minutes", min_value=0)
        drill_21_s = st.number_input("21 Drill - Seconds", min_value=0)
        layups_m = st.number_input("10 Layups - Minutes", min_value=0)
        layups_s = st.number_input("10 Layups - Seconds", min_value=0)
        around_key = st.number_input("Around the Key Shots", min_value=0)
        three_4min = st.number_input("3P in 4 min", min_value=0)
    with col2:
        threes_made = st.number_input("3P Made", min_value=0)
        threes_attempt = st.number_input("3P Attempt", min_value=0)
        twos_made = st.number_input("2P Made", min_value=0)
        twos_attempt = st.number_input("2P Attempt", min_value=0)

    if st.button("Save Shooting Practice"):
        save_to_supabase({
            "activity": "Shooting",
            "drill_21_time": drill_21_m*60+drill_21_s,
            "layups_time": layups_m*60+layups_s,
            "around_key": around_key,
            "three_4min": three_4min,
            "threes_made": threes_made,
            "twos_made": twos_made,
            "three_pct": round(threes_made/threes_attempt*100,2) if threes_attempt else 0,
            "two_pct": round(twos_made/twos_attempt*100,2) if twos_attempt else 0
        })

# -------- Conditioning --------
elif activity == "Conditioning":
    st.subheader("💪 Conditioning Entry")
    col1, col2, col3 = st.columns(3)
    with col1:
        drill_17_m = st.number_input("17s Drill - Minutes", min_value=0)
        drill_17_s = st.number_input("17s Drill - Seconds", min_value=0)
        suicide1_m = st.number_input("1 Suicide - Minutes", min_value=0)
        suicide1_s = st.number_input("1 Suicide - Seconds", min_value=0)
    with col2:
        suicide5_m = st.number_input("5 Suicides - Minutes", min_value=0)
        suicide5_s = st.number_input("5 Suicides - Seconds", min_value=0)
    with col3:
        slides = st.number_input("Defensive Slides in 30s", min_value=0)

    if st.button("Save Conditioning"):
        save_to_supabase({
            "activity": "Conditioning",
            "drill_17_time": drill_17_m*60 + drill_17_s,
            "suicide1_time": suicide1_m*60 + suicide1_s,
            "suicide5_time": suicide5_m*60 + suicide5_s,
            "defensive_slides": slides
        })

# -------- Dribbling --------
elif activity == "Dribbling":
    st.subheader("🤾 Dribbling Entry")
    col1, col2 = st.columns(2)
    with col1:
        one_ball = st.number_input("1 Ball Dribble - Minutes", min_value=0)
    with col2:
        two_ball = st.number_input("2 Ball Dribble - Minutes", min_value=0)

    if st.button("Save Dribbling"):
        save_to_supabase({
            "activity": "Dribbling",
            "dribble_1ball_minutes": one_ball,
            "dribble_2ball_minutes": two_ball
        })

# -------------------------------
# Show graphs
# -------------------------------
st.header("📈 Your Metrics")

def show_graphs(activity_filter):
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).eq("activity", activity_filter).execute()
    data = pd.DataFrame(res.data)
    if data.empty:
        st.info(f"No data for {activity_filter} yet.")
        return
    for col in data.columns:
        if col not in ["id", "user_id", "activity", "timestamp"] and pd.api.types.is_numeric_dtype(data[col]):
            fig = px.line(data, x="timestamp", y=col, title=f"{activity_filter} - {col}", markers=True)
            st.plotly_chart(fig, use_container_width=True)

for act in ["Games", "Shooting", "Conditioning", "Dribbling"]:
    show_graphs(act)