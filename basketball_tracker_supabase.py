import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
from datetime import datetime

# -------------------------------
# Supabase credentials
# -------------------------------
SUPABASE_URL = "https://yegkoltoaqzfjyzbhdrc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllZ2tvbHRvYXF6Zmp5emJoZHJjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY2OTYxNTIsImV4cCI6MjA3MjI3MjE1Mn0.dumcEar9kCvFQMRemqq0-PB4P1QYZSRm1MdFKGfwwcg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Session state
# -------------------------------
if "user_id" not in st.session_state:
    # For now we can just generate a random ID per session; later you can implement login
    import uuid
    st.session_state.user_id = str(uuid.uuid4())

# -------------------------------
# App UI
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")
st.title("🏀 Basketball Tracker with Supabase")

activity = st.radio("Select Activity to Log:", ["Games Stats", "Shooting Practice", "Conditioning", "Dribbling"])

# -------------------------------
# Data Entry
# -------------------------------
if activity == "Games Stats":
    points = st.number_input("Points", min_value=0)
    assists = st.number_input("Assists", min_value=0)
    turnovers = st.number_input("Turnovers", min_value=0)
    steals = st.number_input("Steals", min_value=0)
    threes_made = st.number_input("3P Made", min_value=0)
    twos_made = st.number_input("2P Made", min_value=0)

    if st.button("Save Game Stats"):
        supabase.table("user_stats").insert({
            "user_id": st.session_state.user_id,
            "activity": "Games",
            "points": points,
            "assists": assists,
            "turnovers": turnovers,
            "steals": steals,
            "threes_made": threes_made,
            "twos_made": twos_made,
            "three_pct": round(threes_made / (threes_made if threes_made else 1) * 100, 2),
            "two_pct": round(twos_made / (twos_made if twos_made else 1) * 100, 2),
            "timestamp": datetime.now()
        }).execute()
        st.success("✅ Game stats saved!")

elif activity == "Shooting Practice":
    s21_time = st.number_input("21 Drill Time (seconds)", min_value=0)
    layups_time = st.number_input("10 Layups Time (seconds)", min_value=0)
    around_key = st.number_input("Around Key Shots", min_value=0)
    three_4min = st.number_input("3P in 4 min", min_value=0)

    if st.button("Save Shooting Practice"):
        supabase.table("user_stats").insert({
            "user_id": st.session_state.user_id,
            "activity": "Shooting",
            "drill_21_time": s21_time,
            "layups_time": layups_time,
            "around_key": around_key,
            "three_4min": three_4min,
            "timestamp": datetime.now()
        }).execute()
        st.success("✅ Shooting practice saved!")

elif activity == "Conditioning":
    drill_17_time = st.number_input("17s Drill Time (seconds)", min_value=0)
    suicide1_time = st.number_input("1 Suicide Time (seconds)", min_value=0)
    suicide5_time = st.number_input("5 Suicides Time (seconds)", min_value=0)
    defensive_slides = st.number_input("Defensive Slides", min_value=0)

    if st.button("Save Conditioning"):
        supabase.table("user_stats").insert({
            "user_id": st.session_state.user_id,
            "activity": "Conditioning",
            "drill_17_time": drill_17_time,
            "suicide1_time": suicide1_time,
            "suicide5_time": suicide5_time,
            "defensive_slides": defensive_slides,
            "timestamp": datetime.now()
        }).execute()
        st.success("✅ Conditioning saved!")

elif activity == "Dribbling":
    dribble_1 = st.number_input("1-Ball Dribbles (minutes)", min_value=0)
    dribble_2 = st.number_input("2-Ball Dribbles (minutes)", min_value=0)

    if st.button("Save Dribbling"):
        supabase.table("user_stats").insert({
            "user_id": st.session_state.user_id,
            "activity": "Dribbling",
            "dribble_1ball_minutes": dribble_1,
            "dribble_2ball_minutes": dribble_2,
            "timestamp": datetime.now()
        }).execute()
        st.success("✅ Dribbling saved!")

# -------------------------------
# Fetch Data & Show Graphs
# -------------------------------
def show_graph(activity_filter):
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).eq("activity", activity_filter).execute()
    data = res.data
    if not data:
        st.info(f"No {activity_filter} data yet.")
        return
    df = pd.DataFrame(data)
    numeric_cols = [c for c in df.columns if df[c].dtype in ['int64','float64']]
    for col in numeric_cols:
        fig = px.line(df, y=col, x="timestamp", title=f"{activity_filter} - {col}", markers=True)
        st.plotly_chart(fig, use_container_width=True)

st.write("### Games Metrics")
show_graph("Games")
st.write("### Shooting Practice Metrics")
show_graph("Shooting")
st.write("### Conditioning Metrics")
show_graph("Conditioning")
st.write("### Dribbling Metrics")
show_graph("Dribbling")