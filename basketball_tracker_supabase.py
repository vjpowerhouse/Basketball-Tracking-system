import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from supabase import create_client, Client
import base64
import json

# -------------------------------
# Supabase config
# -------------------------------
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")

# -------------------------------
# Sidebar: Image Uploads
# -------------------------------
st.sidebar.subheader("Upload Images (optional)")
kobe_file = st.sidebar.file_uploader("Kobe Bryant Image", type=["png","jpg"])
logo_file = st.sidebar.file_uploader("Basketball Logo", type=["png","jpg"])
court_file = st.sidebar.file_uploader("Court Background", type=["png","jpg"])
court_bg_base64 = None
if court_file:
    court_bg_base64 = base64.b64encode(court_file.read()).decode()

# -------------------------------
# Header with optional Kobe image
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
# Multi-user input
# -------------------------------
user_id = st.text_input("Enter your user ID (any unique name)")

# -------------------------------
# Activity selection
# -------------------------------
activity = st.radio("Select Activity to Log:", ["Games Stats", "Shooting Practice", "Conditioning", "Dribbling"])

# -------------------------------
# Functions
# -------------------------------
def save_to_supabase(user_id, activity_type, data_dict):
    data = {
        "user_id": user_id,
        "activity_type": activity_type,
        "data": data_dict,
        "timestamp": datetime.now().isoformat()
    }
    supabase.table("user_stats").insert(data).execute()
    st.success(f"✅ {activity_type} saved!")

def get_user_data(user_id):
    res = supabase.table("user_stats").select("*").eq("user_id", user_id).execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

def show_graphs(df, activity_name):
    if df.empty:
        st.info(f"No data for {activity_name} yet.")
        return
    data_list = df[df['activity_type'] == activity_name]['data'].apply(pd.Series)
    if data_list.empty:
        st.info(f"No data for {activity_name} yet.")
        return
    data_list['timestamp'] = pd.to_datetime(df[df['activity_type'] == activity_name]['timestamp'])
    for col in data_list.columns:
        if col != 'timestamp' and pd.api.types.is_numeric_dtype(data_list[col]):
            fig = px.line(data_list, x='timestamp', y=col, title=f"{activity_name} - {col}", markers=True)
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

# -------------------------------
# Data Entry Forms
# -------------------------------
if user_id:
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
            data_dict = {
                "Points": points,
                "Assists": assists,
                "Turnovers": turnovers,
                "Steals": steals,
                "3P Made": threes_made,
                "3P %": round(threes_made / threes_made * 100, 2) if threes_made else 0,
                "2P Made": twos_made,
            }
            save_to_supabase(user_id, "Games Stats", data_dict)

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
            data_dict = {
                "21 Drill Time (s)": s21_m*60 + s21_s,
                "10 Layups Time (s)": layups_m*60 + layups_s,
                "Around Key": around_key,
                "3P in 4min": threes_4min,
                "3P Made": threes_made,
                "2P Made": twos_made,
                "3P %": round(threes_made / threes_made * 100, 2) if threes_made else 0,
            }
            save_to_supabase(user_id, "Shooting Practice", data_dict)

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
            data_dict = {
                "17s Drill Time (s)": drill17_m*60 + drill17_s,
                "1 Suicide Time (s)": suicide1_m*60 + suicide1_s,
                "5 Suicides Time (s)": suicide5_m*60 + suicide5_s,
                "Defensive Slides": slides
            }
            save_to_supabase(user_id, "Conditioning", data_dict)

    elif activity == "Dribbling":
        st.subheader("🤾 Dribbling Entry")
        one_ball = st.number_input("1 Ball Dribble Minutes", min_value=0)
        two_ball = st.number_input("2 Ball Dribble Minutes", min_value=0)
        if st.button("Save Dribbling"):
            data_dict = {
                "1 Ball Dribble Minutes": one_ball,
                "2 Ball Dribble Minutes": two_ball
            }
            save_to_supabase(user_id, "Dribbling", data_dict)

    # -------------------------------
    # Show graphs in separate tabs
    # -------------------------------
    st.write("---")
    tabs = st.tabs(["Games", "Shooting", "Conditioning", "Dribbling"])
    user_df = get_user_data(user_id)
    with tabs[0]:
        show_graphs(user_df, "Games Stats")
    with tabs[1]:
        show_graphs(user_df, "Shooting Practice")
    with tabs[2]:
        show_graphs(user_df, "Conditioning")
    with tabs[3]:
        show_graphs(user_df, "Dribbling")
