import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import base64

# -------------------------------
# Google Sheets Setup
# -------------------------------
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Basketball Tracker")  # Change to your Google Sheet name

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")

# -------------------------------
# Sidebar: Images
# -------------------------------
st.sidebar.subheader("Upload Images (optional)")
kobe_file = st.sidebar.file_uploader("Kobe Bryant Image", type=["png","jpg"])
logo_file = st.sidebar.file_uploader("Basketball Logo", type=["png","jpg"])
court_file = st.sidebar.file_uploader("Court Background", type=["png","jpg"])
court_bg_base64 = None
if court_file:
    court_bg_base64 = base64.b64encode(court_file.read()).decode()

if kobe_file:
    st.image(kobe_file, width=120)

# -------------------------------
# Header & Quote
# -------------------------------
st.markdown("""
<h1 style="text-align:center;">🏀 Basketball Performance Tracker</h1>
<h3 style="text-align:center;font-style:italic;color:#555;">
"The most important thing is you must put everybody on notice that you're here and you are for real." – Kobe Bryant
</h3>
""", unsafe_allow_html=True)

# -------------------------------
# User Login / Name
# -------------------------------
user_name = st.text_input("Enter Player Name:", value="Player1")
if not user_name:
    st.warning("Please enter your name to continue.")
    st.stop()

# -------------------------------
# Worksheet per user
# -------------------------------
try:
    ws = sheet.worksheet(user_name)
except gspread.exceptions.WorksheetNotFound:
    ws = sheet.add_worksheet(title=user_name, rows="1000", cols="20")

# -------------------------------
# Initialize session state
# -------------------------------
activities = ["Games", "Shooting Practice", "Conditioning", "Dribbling"]
for act in activities:
    if act not in st.session_state:
        st.session_state[act] = []

# Load existing data from Google Sheet
df_existing = get_as_dataframe(ws, evaluate_formulas=True, header=0)
if df_existing is not None and not df_existing.empty:
    for act in activities:
        st.session_state[act] = df_existing[df_existing['Activity']==act].to_dict('records')

# -------------------------------
# Activity Selection
# -------------------------------
activity = st.radio("Select Activity to Log:", activities)

# -------------------------------
# Data Entry Forms
# -------------------------------
if activity == "Games":
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
        row = {"Activity":"Games", "DateTime":datetime.now(),
               "Points":points, "Assists":assists,
               "Turnovers":turnovers, "Steals":steals,
               "3P Made":threes_made, "2P Made":twos_made}
        st.session_state["Games"].append(row)
        st.success("✅ Game stats saved!")

elif activity == "Shooting Practice":
    st.subheader("🏀 Shooting Practice Entry")
    col1, col2 = st.columns(2)
    with col1:
        s21_m = st.number_input("21 Drill Minutes", min_value=0)
        s21_s = st.number_input("21 Drill Seconds", min_value=0)
        layups_m = st.number_input("10 Layups Minutes", min_value=0)
        layups_s = st.number_input("10 Layups Seconds", min_value=0)
    with col2:
        threes_made = st.number_input("3P Made", min_value=0)
        twos_made = st.number_input("2P Made", min_value=0)

    if st.button("Save Shooting Practice"):
        row = {"Activity":"Shooting Practice", "DateTime":datetime.now(),
               "21 Drill Time (s)":s21_m*60+s21_s,
               "10 Layups Time (s)":layups_m*60+layups_s,
               "3P Made":threes_made, "2P Made":twos_made}
        st.session_state["Shooting Practice"].append(row)
        st.success("✅ Shooting practice saved!")

elif activity == "Conditioning":
    st.subheader("💪 Conditioning Entry")
    drill17_m = st.number_input("17s Drill Minutes", min_value=0)
    drill17_s = st.number_input("17s Drill Seconds", min_value=0)
    suicide1_m = st.number_input("1 Suicide Minutes", min_value=0)
    suicide1_s = st.number_input("1 Suicide Seconds", min_value=0)
    slides = st.number_input("Defensive Slides in 30s", min_value=0)

    if st.button("Save Conditioning"):
        row = {"Activity":"Conditioning","DateTime":datetime.now(),
               "17s Drill Time (s)":drill17_m*60+drill17_s,
               "1 Suicide Time (s)":suicide1_m*60+suicide1_s,
               "Defensive Slides":slides}
        st.session_state["Conditioning"].append(row)
        st.success("✅ Conditioning saved!")

elif activity == "Dribbling":
    st.subheader("🤾 Dribbling Entry")
    two_ball = st.number_input("2-Ball Dribbles (minutes)", min_value=0)
    one_ball = st.number_input("1-Ball Dribbles (minutes)", min_value=0)
    if st.button("Save Dribbling"):
        row = {"Activity":"Dribbling","DateTime":datetime.now(),
               "2-Ball Minutes":two_ball,"1-Ball Minutes":one_ball}
        st.session_state["Dribbling"].append(row)
        st.success("✅ Dribbling saved!")

# -------------------------------
# Save to Google Sheet
# -------------------------------
def save_to_sheet():
    all_data = []
    for act in activities:
        for row in st.session_state[act]:
            all_data.append(row)
    df = pd.DataFrame(all_data)
    if not df.empty:
        set_with_dataframe(ws, df)

save_to_sheet()

# -------------------------------
# Graphs
# -------------------------------
st.write("## Performance Graphs")
def show_graphs(data, activity_name):
    if not data: 
        st.info(f"No data for {activity_name} yet.") 
        return
    df = pd.DataFrame(data)
    numeric_cols = [c for c in df.columns if df[c].dtype in ['int64','float64']]
    for col in numeric_cols:
        fig = px.line(df, x="DateTime", y=col, title=f"{activity_name} - {col}", markers=True)
        st.plotly_chart(fig, use_container_width=True)

for act in activities:
    st.write(f"### {act} Metrics")
    show_graphs(st.session_state[act], act)
