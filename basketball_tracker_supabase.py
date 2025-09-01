import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from supabase import create_client, Client

# -------------------------------
# Supabase credentials
# -------------------------------
SUPABASE_URL = "https://yegkoltoaqzfjyzbhdrc.supabase.co"

with open("supabase_key.txt") as f:
    SUPABASE_KEY = f.read().strip()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Initialize user
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = st.text_input("Enter your name or unique ID:")

if not st.session_state.user_id:
    st.warning("Please enter your unique ID to start logging data.")
    st.stop()

# -------------------------------
# Activity selection
# -------------------------------
activity = st.radio("Select Activity to Log:", ["Games Stats", "Shooting Practice", "Conditioning", "Dribbling"])

# -------------------------------
# Data Entry Forms
# -------------------------------
record = {"user_id": st.session_state.user_id, "timestamp": datetime.now()}

if activity == "Games Stats":
    st.subheader("📊 Games Stats Entry")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        record["points"] = st.number_input("Points", min_value=0)
        record["assists"] = st.number_input("Assists", min_value=0)
    with col2:
        record["turnovers"] = st.number_input("Turnovers", min_value=0)
        record["steals"] = st.number_input("Steals", min_value=0)
    with col3:
        record["3P Made"] = st.number_input("3P Made", min_value=0)
        record["3P Attempt"] = st.number_input("3P Attempt", min_value=0)
    with col4:
        record["2P Made"] = st.number_input("2P Made", min_value=0)
        record["2P Attempt"] = st.number_input("2P Attempt", min_value=0)

elif activity == "Shooting Practice":
    st.subheader("🏀 Shooting Practice Entry")
    col1, col2 = st.columns(2)
    with col1:
        record["21 Drill Time (s)"] = st.number_input("21-points drill - Total Seconds", min_value=0)
        record["10 Layups Time (s)"] = st.number_input("10 Layups - Total Seconds", min_value=0)
        record["Around Key"] = st.number_input("Around the Key Shots in 4 mins", min_value=0)
        record["3P in 4min"] = st.number_input("3P in 4 mins", min_value=0)
    with col2:
        record["3P Made"] = st.number_input("3P Made", min_value=0)
        record["3P Attempt"] = st.number_input("3P Attempt", min_value=0)
        record["2P Made"] = st.number_input("2P Made", min_value=0)
        record["2P Attempt"] = st.number_input("2P Attempt", min_value=0)

elif activity == "Conditioning":
    st.subheader("💪 Conditioning Entry")
    record["17s Drill Time (s)"] = st.number_input("17s Drill - Total Seconds", min_value=0)
    record["1 Suicide Time (s)"] = st.number_input("1 Suicide - Total Seconds", min_value=0)
    record["5 Suicides Time (s)"] = st.number_input("5 Suicides - Total Seconds", min_value=0)
    record["Defensive Slides"] = st.number_input("Defensive Slides in 30s", min_value=0)

elif activity == "Dribbling":
    st.subheader("🤾 Dribbling Entry")
    record["2 Ball Dribble (min)"] = st.number_input("2 Ball Dribbles - Minutes", min_value=0)
    record["1 Ball Dribble (min)"] = st.number_input("1 Ball Dribbles - Minutes", min_value=0)

# -------------------------------
# Save record to Supabase
# -------------------------------
if st.button("Save Record"):
    record["activity"] = activity
    supabase.table("user_stats").insert(record).execute()
    st.success(f"✅ {activity} record saved!")

# -------------------------------
# Show Graphs
# -------------------------------
def show_graphs(activity_filter):
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).eq("activity", activity_filter).execute()
    data = res.data
    if not data:
        st.info(f"No data yet for {activity_filter}")
        return
    df = pd.DataFrame(data)
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    for col in numeric_cols:
        fig = px.line(df, x="timestamp", y=col, title=f"{activity_filter} - {col}", markers=True)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Your Performance Trends")
for act in ["Games Stats", "Shooting Practice", "Conditioning", "Dribbling"]:
    show_graphs(act)

# -------------------------------
# Backup & Export
# -------------------------------
st.subheader("💾 Backup / Export Data")
if st.button("Download All My Data"):
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).execute()
    df = pd.DataFrame(res.data)
    if not df.empty:
        st.download_button("📥 Download Excel", df.to_excel(index=False), file_name="basketball_backup.xlsx")
    else:
        st.warning("No data to download.")