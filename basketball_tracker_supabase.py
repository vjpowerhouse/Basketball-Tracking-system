import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from supabase import create_client, Client

# -------------------------------
# Supabase credentials
# -------------------------------
SUPABASE_URL = "https://yegkoltoaqzfjyzbhdrc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # use your anon/public key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")
st.title("🏀 Basketball Performance Tracker")

# -------------------------------
# Initialize session state
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = st.text_input("Enter your User ID", "")

if "games" not in st.session_state: st.session_state.games = []
if "shooting" not in st.session_state: st.session_state.shooting = []
if "conditioning" not in st.session_state: st.session_state.conditioning = []
if "dribbling" not in st.session_state: st.session_state.dribbling = []

# -------------------------------
# Activity selection
# -------------------------------
activity = st.radio("Select Activity to Log:", ["Games Stats", "Shooting Practice", "Conditioning", "Dribbling"])

# -------------------------------
# Data Entry Forms
# -------------------------------
def save_to_supabase(activity_name, row_dict):
    row_dict["user_id"] = st.session_state.user_id
    row_dict["activity"] = activity_name
    row_dict["timestamp"] = datetime.now().isoformat()
    supabase.table("user_stats").insert(row_dict).execute()

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
        threes_attempt = st.number_input("3P Attempt", min_value=0)
    with col4:
        twos_made = st.number_input("2P Made", min_value=0)
        twos_attempt = st.number_input("2P Attempt", min_value=0)

    if st.button("Save Game Stats"):
        row = {
            "Points": points,
            "Assists": assists,
            "Turnovers": turnovers,
            "Steals": steals,
            "3P Made": threes_made,
            "3P Attempt": threes_attempt,
            "2P Made": twos_made,
            "2P Attempt": twos_attempt,
            "3P %": round(threes_made / threes_attempt * 100, 2) if threes_attempt else 0,
            "2P %": round(twos_made / twos_attempt * 100, 2) if twos_attempt else 0
        }
        save_to_supabase("Games", row)
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
        row = {
            "21 Drill Time (s)": s21_m*60 + s21_s,
            "10 Layups Time (s)": layups_m*60 + layups_s,
            "Around Key": around_key,
            "3P in 4min": threes_4min,
            "3P Made": threes_made,
            "2P Made": twos_made,
            "3P %": round(threes_made / (threes_made if threes_made else 1) * 100,2),
            "2P %": round(twos_made / (twos_made if twos_made else 1) * 100,2)
        }
        save_to_supabase("Shooting", row)
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
        row = {
            "17s Drill Time (s)": drill17_m*60 + drill17_s,
            "1 Suicide Time (s)": suicide1_m*60 + suicide1_s,
            "5 Suicides Time (s)": suicide5_m*60 + suicide5_s,
            "Defensive Slides": slides
        }
        save_to_supabase("Conditioning", row)
        st.success("✅ Conditioning data saved!")

# ----------- Dribbling -----------
elif activity == "Dribbling":
    st.subheader("🤾 Dribbling Entry")
    col1, col2 = st.columns(2)
    with col1:
        one_ball = st.number_input("1-Ball Dribble Minutes", min_value=0)
    with col2:
        two_ball = st.number_input("2-Ball Dribble Minutes", min_value=0)

    if st.button("Save Dribbling"):
        row = {
            "1-Ball Minutes": one_ball,
            "2-Ball Minutes": two_ball
        }
        save_to_supabase("Dribbling", row)
        st.success("✅ Dribbling data saved!")

# -------------------------------
# Backup / Import
# -------------------------------
st.subheader("💾 Backup / Restore")
col1, col2 = st.columns(2)

def export_user_data():
    if not st.session_state.user_id:
        return None
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).execute()
    if not res.data:
        return None
    df = pd.DataFrame(res.data)
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    return output.getvalue()

with col1:
    excel_data = export_user_data()
    if excel_data:
        st.download_button(
            label="📥 Download My Data Backup",
            data=excel_data,
            file_name=f"{st.session_state.user_id}_basketball_backup.xlsx"
        )

with col2:
    import_file = st.file_uploader("📂 Import My Data Backup", type=["xlsx"])
    if import_file is not None:
        try:
            df_import = pd.read_excel(import_file, engine="openpyxl")
            for _, row in df_import.iterrows():
                row_dict = row.to_dict()
                row_dict["user_id"] = st.session_state.user_id
                if "timestamp" not in row_dict or pd.isna(row_dict["timestamp"]):
                    row_dict["timestamp"] = datetime.now().isoformat()
                supabase.table("user_stats").insert(row_dict).execute()
            st.success("✅ Data imported successfully!")
        except Exception as e:
            st.error(f"Failed to import data. Error: {e}")

# -------------------------------
# Graph Section
# -------------------------------
st.subheader("📈 Graphs")
activities = ["Games", "Shooting", "Conditioning", "Dribbling"]

def show_graphs(activity_filter):
    res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).eq("activity", activity_filter).execute()
    if not res.data:
        st.info(f"No data for {activity_filter} yet.")
        return
    df = pd.DataFrame(res.data)
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64'] and col not in ["3P Attempt", "2P Attempt"]:
            fig = px.line(df, y=col, x="timestamp", title=f"{activity_filter} - {col}", markers=True)
            st.plotly_chart(fig, use_container_width=True)

for act in activities:
    show_graphs(act)