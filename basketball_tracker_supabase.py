import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64
from supabase import create_client, Client
from datetime import datetime

# -----------------------------
# Supabase connection
# -----------------------------
SUPABASE_URL = "https://yegkoltoaqzfjyzbhdrc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllZ2tvbHRvYXF6Zmp5emJoZHJjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY2OTYxNTIsImV4cCI6MjA3MjcyMTUyMn0.dumcEar9kCvFQMRemqq0-PB4P1QYZSRm1MdFKGfwwcg"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
# Data Entry Forms
# -------------------------------

def save_to_supabase(data_dict):
    # Append timestamp
    data_dict['timestamp'] = datetime.now().isoformat()
    supabase.table("user_stats").insert(data_dict).execute()

# ----------- Games Stats -----------
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
        save_to_supabase({
            "activity":"games",
            "points": points,
            "assists": assists,
            "turnovers": turnovers,
            "steals": steals,
            "3P_Made": threes_made,
            "2P_Made": twos_made
        })
        st.success("✅ Game stats saved!")

# ----------- Shooting Practice -----------
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
        save_to_supabase({
            "activity":"shooting",
            "21_drill_s": s21_m*60 + s21_s,
            "10_layups_s": layups_m*60 + layups_s,
            "around_key": around_key,
            "3P_4min": threes_4min,
            "3P_Made": threes_made,
            "2P_Made": twos_made
        })
        st.success("✅ Shooting practice saved!")

# ----------- Conditioning -----------
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
        save_to_supabase({
            "activity":"conditioning",
            "drill17_s": drill17_m*60 + drill17_s,
            "1suicide_s": suicide1_m*60 + suicide1_s,
            "5suicides_s": suicide5_m*60 + suicide5_s,
            "def_slides": slides
        })
        st.success("✅ Conditioning data saved!")

# ----------- Dribbling -----------
elif activity == "Dribbling":
    st.subheader("🤾 Dribbling Entry")
    two_ball = st.number_input("2 Ball Dribbles (minutes)", min_value=0)
    one_ball = st.number_input("1 Ball Dribbles (minutes)", min_value=0)

    if st.button("Save Dribbling"):
        save_to_supabase({
            "activity":"dribbling",
            "two_ball_min": two_ball,
            "one_ball_min": one_ball
        })
        st.success("✅ Dribbling data saved!")

# -------------------------------
# Graph Section
# -------------------------------
def show_graph(activity_name):
    res = supabase.table("user_stats").select("*").eq("activity", activity_name).execute()
    data = res.data
    if not data:
        st.info(f"No data for {activity_name} yet.")
        return
    df = pd.DataFrame(data)
    for col in df.columns:
        if col not in ["id","activity","timestamp"] and pd.api.types.is_numeric_dtype(df[col]):
            fig = px.line(df, y=col, x="timestamp", title=f"{activity_name.capitalize()} - {col}", markers=True)
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

st.write("### Games Metrics")
show_graph("games")

st.write("### Shooting Practice Metrics")
show_graph("shooting")

st.write("### Conditioning Metrics")
show_graph("conditioning")

st.write("### Dribbling Metrics")
show_graph("dribbling")

# -------------------------------
# Backup & Import
# -------------------------------
def export_to_excel(data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(data).to_excel(writer, index=False)
    return output.getvalue()

backup_data = supabase.table("user_stats").select("*").execute().data
st.download_button("💾 Backup Data", data=export_to_excel(backup_data), file_name="basketball_backup.xlsx")

import_file = st.file_uploader("📂 Import Backup Excel", type=["xlsx"])
if import_file:
    df_import = pd.read_excel(import_file, engine="openpyxl")
    for _, row in df_import.iterrows():
        row_dict = row.to_dict()
        row_dict['timestamp'] = row_dict.get('timestamp', datetime.now().isoformat())
        supabase.table("user_stats").insert(row_dict).execute()
    st.success("✅ Backup imported!")