import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import matplotlib.pyplot as plt

# ------------------------------------------------
# 1. Authenticate with Google Service Account
# ------------------------------------------------
SERVICE_ACCOUNT_FILE = "basketballtrackerapp-9e471979a8bc.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# ------------------------------------------------
# 2. Open (or create) Google Sheet
# ------------------------------------------------
SHEET_NAME = "Basketball Tracker"
try:
    sheet = client.open(SHEET_NAME).sheet1
except Exception as e:
    st.error(f"Could not open Google Sheet: {e}")
    st.stop()

# ------------------------------------------------
# 3. Helper: load existing data into DataFrame
# ------------------------------------------------
def load_data():
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# ------------------------------------------------
# 4. Streamlit UI
# ------------------------------------------------
st.title("🏀 Basketball Training & Game Tracker")

menu = ["Game Stats", "Shooting Drills", "Dribbling Drills", "View Data & Trends"]
choice = st.sidebar.selectbox("Choose Section", menu)

# ------------------------------------------------
# 5. Game Stats
# ------------------------------------------------
if choice == "Game Stats":
    st.header("📊 Game Stats")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    opponent = st.text_input("Opponent")
    points = st.number_input("Points", min_value=0, step=1)
    rebounds = st.number_input("Rebounds", min_value=0, step=1)
    assists = st.number_input("Assists", min_value=0, step=1)

    if st.button("Save Game Stats"):
        sheet.append_row(
            ["Game", date, opponent, points, rebounds, assists]
        )
        st.success("✅ Game stats saved!")

# ------------------------------------------------
# 6. Shooting Drills
# ------------------------------------------------
elif choice == "Shooting Drills":
    st.header("🎯 Shooting Drills")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = st.selectbox("Shot Location", ["Corner 3", "Wing 3", "Top of Key", "Midrange", "Layup"])
    makes = st.number_input("Shots Made", min_value=0, step=1)
    attempts = st.number_input("Shots Attempted", min_value=0, step=1)

    if st.button("Save Shooting Drill"):
        sheet.append_row(
            ["Shooting", date, location, makes, attempts]
        )
        st.success("✅ Shooting drill saved!")

# ------------------------------------------------
# 7. Dribbling Drills
# ------------------------------------------------
elif choice == "Dribbling Drills":
    st.header("🤹 Dribbling Drills")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    one_ball = st.number_input("Minutes – 1 Ball Dribble", min_value=0, step=1)
    two_ball = st.number_input("Minutes – 2 Ball Dribble", min_value=0, step=1)

    if st.button("Save Dribbling Drill"):
        sheet.append_row(
            ["Dribbling", date, one_ball, two_ball]
        )
        st.success("✅ Dribbling drill saved!")

# ------------------------------------------------
# 8. View Data & Trends
# ------------------------------------------------
elif choice == "View Data & Trends":
    st.header("📈 Training & Game Trends")

    df = load_data()
    if df.empty:
        st.warning("No data yet!")
    else:
        st.dataframe(df)

        # Basic shooting % trend
        shooting_df = df[df.iloc[:,0] == "Shooting"].copy()
        if not shooting_df.empty:
            shooting_df["FG%"] = shooting_df.iloc[:,3] / shooting_df.iloc[:,4] * 100
            fig, ax = plt.subplots()
            shooting_df.plot(x=1, y="FG%", ax=ax, marker="o", legend=False)
            plt.title("Shooting % Over Time")
            plt.ylabel("Field Goal %")
            plt.xticks(rotation=45)
            st.pyplot(fig)

# ------------------------------------------------
# 9. Backup Button
# ------------------------------------------------
st.sidebar.subheader("⚙️ Data Management")
if st.sidebar.button("Backup Data (Download CSV)"):
    df = load_data()
    csv = df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="Download Backup CSV",
        data=csv,
        file_name="basketball_backup.csv",
        mime="text/csv",
    )