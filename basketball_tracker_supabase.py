import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import uuid
from supabase import create_client, Client

# -------------------------------
# Supabase setup
# -------------------------------
with open("supabase_key.txt") as f:
    lines = f.read().splitlines()
SUPABASE_URL = lines[0]
SUPABASE_KEY = lines[1]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")

# -------------------------------
# Generate unique user_id
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# -------------------------------
# Sidebar: Upload optional images
# -------------------------------
st.sidebar.subheader("Upload Images (optional)")
kobe_file = st.sidebar.file_uploader("Kobe Bryant Image", type=["png","jpg"])
logo_file = st.sidebar.file_uploader("Basketball Logo", type=["png","jpg"])
court_file = st.sidebar.file_uploader("Court Background", type=["png","jpg"])
court_bg_base64 = None
if court_file:
    import base64
    court_bg_base64 = base64.b64encode(court_file.read()).decode()

# -------------------------------
# Header
# -------------------------------
if kobe_file:
    st.image(kobe_file, width=120)

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
# Data entry forms
# -------------------------------
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
    with col4:
        twos_made = st.number_input("2P Made", min_value=0)

    if st.button("Save Game Stats"):
        record = {
            "user_id": st.session_state.user_id,
            "activity": "Games",
            "timestamp": datetime.now(),
            "Points": points,
            "Assists": assists,
            "Turnovers": turnovers,
            "Steals": steals,
            "3P Made": threes_made,
            "2P Made": twos_made
        }
        supabase.table("user_stats").insert(record).execute()
        st.success("✅ Game stats saved!")

elif activity == "Shooting Practice":
    st.subheader("🏀 Shooting Practice Entry")
    col1, col2 = st.columns(2)
    with col1:
        s21_m = st.number_input("21-points drill - Minutes", min_value=0)
        s21_s = st.number_input("21-points drill - Seconds", min_value=0)
        layups_m = st.number_input("10 Layups - Minutes", min_value=0)
        layups_s = st.number_input("10 Layups - Seconds", min_value=0)
        around_key = st.number_input("Around the Key Shots in 4 mins", min_value=0)
        threes_4min = st.number_input("3P in 4 mins", min_value=0)
    with col2:
        threes_made = st.number_input("3P Made", min_value=0)
        twos_made = st.number_input("2P Made", min_value=0)

    if st.button("Save Shooting Practice"):
        record = {
            "user_id": st.session_state.user_id,
            "activity": "Shooting",
            "timestamp": datetime.now(),
            "21 Drill Time (s)": s21_m*60 + s21_s,
            "10 Layups Time (s)": layups_m*60 + layups_s,
            "Around Key": around_key,
            "3P in 4min": threes_4min,
            "3P Made": threes_made,
            "2P Made": twos_made
        }
        supabase.table("user_stats").insert(record).execute()
        st.success("✅ Shooting practice saved!")

elif activity == "Conditioning":
    st.subheader("💪 Conditioning Entry")
    col1, col2, col3 = st.columns(3)
    with col1:
        drill17_m = st.number_input("17s Drill - Minutes", min_value=0)
        drill17_s = st.number_input("17s Drill - Seconds", min_value=0)
        suicide1_m = st.number_input("1 Suicide - Minutes", min_value=0)
        suicide1_s = st.number_input("1 Suicide - Seconds", min_value=0)
    with col2:
        suicide5_m = st.number_input("5 Suicides - Minutes", min_value=0)
        suicide5_s = st.number_input("5 Suicides - Seconds", min_value=0)
    with col3:
        slides = st.number_input("Defensive Slides in 30s", min_value=0)

    if st.button("Save Conditioning"):
        record = {
            "user_id": st.session_state.user_id,
            "activity": "Conditioning",
            "timestamp": datetime.now(),
            "17s Drill Time (s)": drill17_m*60 + drill17_s,
            "1 Suicide Time (s)": suicide1_m*60 + suicide1_s,
            "5 Suicides Time (s)": suicide5_m*60 + suicide5_s,
            "Defensive Slides": slides
        }
        supabase.table("user_stats").insert(record).execute()
        st.success("✅ Conditioning data saved!")

elif activity == "Dribbling":
    st.subheader("🏀 Dribbling Entry")
    col1, col2 = st.columns(2)
    with col1:
        one_ball = st.number_input("1 Ball Dribble - Minutes", min_value=0)
    with col2:
        two_ball = st.number_input("2 Ball Dribble - Minutes", min_value=0)

    if st.button("Save Dribbling"):
        record = {
            "user_id": st.session_state.user_id,
            "activity": "Dribbling",
            "timestamp": datetime.now(),
            "1 Ball Minutes": one_ball,
            "2 Ball Minutes": two_ball
        }
        supabase.table("user_stats").insert(record).execute()
        st.success("✅ Dribbling data saved!")

# -------------------------------
# Graph display
# -------------------------------
def show_graphs(activity_filter):
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).eq("activity", activity_filter).execute()
    df = pd.DataFrame(res.data)
    if df.empty:
        st.info(f"No data for {activity_filter} yet.")
        return
    st.subheader(f"{activity_filter} Metrics")
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns
    for col in numeric_cols:
        fig = px.line(df, x="timestamp", y=col, title=f"{activity_filter} - {col}", markers=True)
        if court_bg_base64:
            fig.update_layout(
                images=[dict(
                    source=f"data:image/png;base64,{court_bg_base64}",
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=1, sizey=1,
                    xanchor="left",
                    yanchor="top",
                    layer="below",
                    opacity=0.2
                )],
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
        st.plotly_chart(fig, use_container_width=True)

# Show graphs for all activities
for act in ["Games", "Shooting", "Conditioning", "Dribbling"]:
    show_graphs(act)