import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
from datetime import datetime
import base64

# -------------------------------
# Streamlit page config
# -------------------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")

# -------------------------------
# Supabase config
# -------------------------------
SUPABASE_URL = "https://yegkoltoaqzfjyzbhdrc.supabase.co"  # Replace with your URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Replace with anon/public key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# Sidebar: Images and User ID
# -------------------------------
st.sidebar.subheader("Upload Images (optional)")
kobe_file = st.sidebar.file_uploader("Kobe Bryant Image", type=["png","jpg"])
logo_file = st.sidebar.file_uploader("Basketball Logo", type=["png","jpg"])
court_file = st.sidebar.file_uploader("Court Background", type=["png","jpg"])
court_bg_base64 = None
if court_file:
    court_bg_base64 = base64.b64encode(court_file.read()).decode()

st.sidebar.subheader("Enter User ID")
if "user_id" not in st.session_state: st.session_state.user_id = ""
st.session_state.user_id = st.sidebar.text_input("User ID", st.session_state.user_id)

# -------------------------------
# Header & Quote
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
# Save to Supabase function
# -------------------------------
def save_to_supabase(activity_name, data_dict):
    data_dict["user_id"] = st.session_state.user_id
    data_dict["activity"] = activity_name
    data_dict["timestamp"] = datetime.now().isoformat()
    supabase.table("user_stats").insert(data_dict).execute()

# -------------------------------
# Activity forms
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
        save_to_supabase("Games", {
            "Points": points,
            "Assists": assists,
            "Turnovers": turnovers,
            "Steals": steals,
            "3P Made": threes_made,
            "2P Made": twos_made
        })
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
        save_to_supabase("Shooting", {
            "21 Drill Time (s)": s21_m*60 + s21_s,
            "10 Layups Time (s)": layups_m*60 + layups_s,
            "Around Key": around_key,
            "3P in 4min": threes_4min,
            "3P Made": threes_made,
            "2P Made": twos_made
        })
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
        save_to_supabase("Conditioning", {
            "17s Drill Time (s)": drill17_m*60 + drill17_s,
            "1 Suicide Time (s)": suicide1_m*60 + suicide1_s,
            "5 Suicides Time (s)": suicide5_m*60 + suicide5_s,
            "Defensive Slides": slides
        })
        st.success("✅ Conditioning data saved!")

elif activity == "Dribbling":
    st.subheader("🤾 Dribbling Entry")
    col1, col2 = st.columns(2)
    with col1:
        two_ball_mins = st.number_input("2 Ball Dribbles - Minutes", min_value=0)
    with col2:
        one_ball_mins = st.number_input("1 Ball Dribbles - Minutes", min_value=0)

    if st.button("Save Dribbling"):
        save_to_supabase("Dribbling", {
            "2 Ball Dribbles (min)": two_ball_mins,
            "1 Ball Dribbles (min)": one_ball_mins
        })
        st.success("✅ Dribbling data saved!")

# -------------------------------
# Backup & Import
# -------------------------------
st.write("## 💾 Backup & Import")
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Backup Data to Excel"):
        if not st.session_state.user_id:
            st.warning("Enter your username/ID first")
        else:
            res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).execute()
            if res.data:
                df = pd.DataFrame(res.data)
                with pd.ExcelWriter("temp.xlsx", engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                with open("temp.xlsx", "rb") as f:
                    st.download_button(
                        label="Download Backup",
                        data=f,
                        file_name=f"{st.session_state.user_id}_basketball_backup.xlsx"
                    )
            else:
                st.info("No data to backup yet.")

with col2:
    import_file = st.file_uploader("Import Data from Backup (Excel)", type=["xlsx"])
    if import_file:
        try:
            df_import = pd.read_excel(import_file)
            for _, row in df_import.iterrows():
                data_dict = row.to_dict()
                save_to_supabase(data_dict.get("activity", "Imported"), data_dict)
            st.success("✅ Backup data imported successfully!")
        except Exception as e:
            st.error(f"Error importing backup: {e}")

# -------------------------------
# Graphs in Tabs
# -------------------------------
st.write("## 📈 Graphs")
tabs = st.tabs(["Games", "Shooting", "Conditioning", "Dribbling"])

for idx, act in enumerate(["Games", "Shooting", "Conditioning", "Dribbling"]):
    with tabs[idx]:
        res = supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).eq("activity", act).execute()
        if not res.data:
            st.info(f"No data for {act} yet.")
            continue
        df = pd.DataFrame(res.data)
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                fig = px.line(df, y=col, x="timestamp", title=f"{act} - {col}", markers=True)
                st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Excel Export Button
# -------------------------------
st.download_button(
    label="📥 Export All Data to Excel",
    data=pd.DataFrame(supabase.table("user_stats").select("*").eq("user_id", st.session_state.user_id).execute().data).to_excel(index=False),
    file_name="basketball_data.xlsx"
)