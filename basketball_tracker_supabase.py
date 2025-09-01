import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from datetime import datetime
import uuid

# -------------------------------
# Supabase Setup
# -------------------------------
SUPABASE_URL = "https://yegkoltoaqzfjyzbhdrc.supabase.co"
SUPABASE_KEY = "YOUR_ANON_KEY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Session State
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# -------------------------------
# App Header
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")
st.title("🏀 Basketball Tracker")
st.subheader("Personal performance tracker")

# -------------------------------
# Activity Selection
# -------------------------------
activity = st.radio("Select Activity:", ["Games", "Shooting", "Conditioning", "Dribbling"])

# -------------------------------
# Data Entry Forms
# -------------------------------
def save_to_supabase(record):
    record["user_id"] = st.session_state.user_id
    record["timestamp"] = datetime.now()
    supabase.table("user_stats").insert(record).execute()

if activity == "Games":
    points = st.number_input("Points", 0)
    assists = st.number_input("Assists", 0)
    turnovers = st.number_input("Turnovers", 0)
    steals = st.number_input("Steals", 0)
    threes_made = st.number_input("3P Made", 0)
    twos_made = st.number_input("2P Made", 0)

    if st.button("Save Game Stats"):
        three_pct = round(threes_made / threes_made * 100, 2) if threes_made else 0
        two_pct = round(twos_made / twos_made * 100, 2) if twos_made else 0
        save_to_supabase({
            "activity": "Games",
            "points": points,
            "assists": assists,
            "turnovers": turnovers,
            "steals": steals,
            "threes_made": threes_made,
            "twos_made": twos_made,
            "three_pct": three_pct,
            "two_pct": two_pct
        })
        st.success("✅ Saved to Supabase")

elif activity == "Shooting":
    drill_21 = st.number_input("21-points drill time (s)", 0)
    layups = st.number_input("10 Layups time (s)", 0)
    around_key = st.number_input("Around Key shots in 4 mins", 0)
    three_4min = st.number_input("3P in 4 mins", 0)

    if st.button("Save Shooting Stats"):
        save_to_supabase({
            "activity": "Shooting",
            "drill_21_time": drill_21,
            "layups_time": layups,
            "around_key": around_key,
            "three_4min": three_4min
        })
        st.success("✅ Saved to Supabase")

elif activity == "Conditioning":
    drill_17 = st.number_input("17s Drill (s)", 0)
    suicide1 = st.number_input("1 Suicide (s)", 0)
    suicide5 = st.number_input("5 Suicides (s)", 0)
    defensive_slides = st.number_input("Defensive Slides (30s)", 0)

    if st.button("Save Conditioning Stats"):
        save_to_supabase({
            "activity": "Conditioning",
            "drill_17_time": drill_17,
            "suicide1_time": suicide1,
            "suicide5_time": suicide5,
            "defensive_slides": defensive_slides
        })
        st.success("✅ Saved to Supabase")

elif activity == "Dribbling":
    dribble_1 = st.number_input("1-ball Dribble (minutes)", 0)
    dribble_2 = st.number_input("2-ball Dribble (minutes)", 0)

    if st.button("Save Dribbling Stats"):
        save_to_supabase({
            "activity": "Dribbling",
            "dribble_1ball_minutes": dribble_1,
            "dribble_2ball_minutes": dribble_2
        })
        st.success("✅ Saved to Supabase")

# -------------------------------
# Fetch and display graphs
# -------------------------------
def show_graphs(activity_filter):
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).eq("activity", activity_filter).execute()
    data = res.data
    if not data:
        st.info(f"No data for {activity_filter} yet.")
        return

    df = pd.DataFrame(data)
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns
    for col in numeric_cols:
        fig = px.line(df, y=col, x="timestamp", title=f"{activity_filter} - {col}", markers=True)
        st.plotly_chart(fig, use_container_width=True)

st.write("### Performance Graphs")
for act in ["Games", "Shooting", "Conditioning", "Dribbling"]:
    show_graphs(act)

# -------------------------------
# Export to Excel
# -------------------------------
def export_to_excel():
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).execute()
    df = pd.DataFrame(res.data)
    return df.to_excel(index=False, engine='openpyxl')

st.download_button(
    label="📥 Export My Data to Excel",
    data=export_to_excel(),
    file_name="basketball_data.xlsx"
)