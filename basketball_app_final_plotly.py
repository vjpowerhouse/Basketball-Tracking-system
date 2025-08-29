import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import os
import json
import io

st.set_page_config(page_title="Basketball Tracking Dashboard", layout="wide")
st.title("Basketball Tracking Dashboard")

DATA_FILE = "basketball_data.csv"
DATA_COLUMNS = ["Date", "Player", "Activity Type",
                "Metric1","Metric2","Metric3","Metric4","Metric5","Metric6",
                "ThreeMade","ThreeAttempted","TwoMade","TwoAttempted","Notes"]

# ======================
# Load or initialize data
# ======================
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
    for col in DATA_COLUMNS:
        if col not in data.columns:
            data[col] = None
else:
    data = pd.DataFrame(columns=DATA_COLUMNS)

# ======================
# Preserve activity type across reruns
# ======================
if "activity_type" not in st.session_state:
    st.session_state["activity_type"] = "Games"

activity_type = st.selectbox(
    "Select Activity Type",
    ["Games", "Practice", "Conditioning"],
    index=["Games","Practice","Conditioning"].index(st.session_state["activity_type"])
)
st.session_state["activity_type"] = activity_type

# ======================
# Add New Activity Form
# ======================
st.subheader("Add New Activity")

with st.form("activity_form"):
    date = st.date_input("Date", datetime.today())
    player = st.text_input("Player Name")

    # Default placeholders
    metric1 = metric2 = metric3 = metric4 = metric5 = metric6 = 0
    three_made = three_attempted = two_made = two_attempted = 0
    notes = ""

    if activity_type == "Games":
        points = st.number_input("Points", min_value=0)
        assists = st.number_input("Assists", min_value=0)
        turnovers = st.number_input("Turnovers", min_value=0)
        steals = st.number_input("Steals", min_value=0)
        three_made = st.number_input("# 3-pointers made", min_value=0)
        three_attempted = st.number_input("# 3-pointers attempted", min_value=0)
        two_made = st.number_input("# 2-pointers made", min_value=0)
        two_attempted = st.number_input("# 2-pointers attempted", min_value=0)
        metric1, metric2, metric3, metric4 = points, assists, turnovers, steals
        notes = f"3pt: {three_made}/{three_attempted}, 2pt: {two_made}/{two_attempted}"

    elif activity_type == "Practice":
        time_21 = st.number_input("Time for 21-points drill (s)", min_value=0)
        time_layups = st.number_input("Time for 10 layups (s)", min_value=0)
        around_key = st.number_input("# Around Key shots in 4 mins", min_value=0)
        three_p_4min = st.number_input("# 3-pointers in 4 mins", min_value=0)
        three_made_p = st.number_input("3-point shots made", min_value=0)
        three_attempted_p = st.number_input("3-point shots attempted", min_value=0)
        mid_made = st.number_input("Mid-range shots made", min_value=0)
        mid_attempted = st.number_input("Mid-range shots attempted", min_value=0)

        # Calculate %
        three_pct = round(three_made_p / three_attempted_p * 100, 1) if three_attempted_p else 0
        mid_pct = round(mid_made / mid_attempted * 100, 1) if mid_attempted else 0

        metric1, metric2, metric3, metric4, metric5, metric6 = time_21, time_layups, around_key, three_p_4min, three_pct, mid_pct
        notes = f"3pt: {three_made_p}/{three_attempted_p} ({three_pct}%), Mid-range: {mid_made}/{mid_attempted} ({mid_pct}%)"

    elif activity_type == "Conditioning":
        time_17s = st.number_input("Time for 17s drill (s)", min_value=0)
        time_1_suicide = st.number_input("Time for 1 suicide (s)", min_value=0)
        time_5_suicides = st.number_input("Time for 5 suicides (s)", min_value=0)
        defensive_slides = st.number_input("Number of defensive slides in 30s", min_value=0)
        metric1, metric2, metric3, metric4 = time_17s, time_1_suicide, time_5_suicides, defensive_slides

    submit = st.form_submit_button("Add Activity")

if submit:
    new_row = pd.DataFrame({
        "Date": [date.strftime("%Y-%m-%d")],
        "Player": [player],
        "Activity Type": [activity_type],
        "Metric1":[metric1], "Metric2":[metric2], "Metric3":[metric3],
        "Metric4":[metric4], "Metric5":[metric5], "Metric6":[metric6],
        "ThreeMade":[three_made], "ThreeAttempted":[three_attempted],
        "TwoMade":[two_made], "TwoAttempted":[two_attempted],
        "Notes":[notes]
    })
    data = pd.concat([data, new_row], ignore_index=True)
    data.to_csv(DATA_FILE, index=False)
    st.success(f"Added new {activity_type} for {player} on {date.strftime('%Y-%m-%d')}")

# ======================
# Display Current Data
# ======================
st.subheader("Current Data")
st.dataframe(data)

# ======================
# Trending Analysis
# ======================
st.subheader("Trending Analysis")
if not data.empty:
    filtered_data = data[data["Activity Type"]==activity_type].copy()
    if not filtered_data.empty:
        filtered_data["Date"] = pd.to_datetime(filtered_data["Date"], errors="coerce")
        for col in ["Metric1","Metric2","Metric3","Metric4","Metric5","Metric6"]:
            filtered_data[col] = pd.to_numeric(filtered_data[col], errors="coerce")
        filtered_data = filtered_data.dropna(subset=["Metric1"])
        if not filtered_data.empty:
            if activity_type=="Games":
                metrics_plot = ["Metric1","Metric2"]  # Points & Assists
            elif activity_type=="Practice":
                metrics_plot = ["Metric5","Metric6"]  # 3pt % & Mid %
            else:
                metrics_plot = ["Metric1","Metric2"]  # Time 17s & 1 suicide

            for m in metrics_plot:
                fig = px.line(filtered_data, x="Date", y=m, color="Player",
                              title=f"{activity_type} - {m} Trend", markers=True)
                st.plotly_chart(fig, use_container_width=True)

# ======================
# Export to Excel with Tabs
# ======================
def export_to_excel(data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Games
        games = data[data["Activity Type"]=="Games"]
        if not games.empty:
            games_excel = pd.DataFrame({
                "Date": games["Date"], "Player": games["Player"], "Points": games["Metric1"],
                "Assists": games["Metric2"], "Turnovers": games["Metric3"], "Steals": games["Metric4"],
                "# 3pt made": games["ThreeMade"], "# 3pt attempted": games["ThreeAttempted"],
                "3pt %": round(games["ThreeMade"]/games["ThreeAttempted"]*100,1).fillna(0),
                "# 2pt made": games["TwoMade"], "# 2pt attempted": games["TwoAttempted"],
                "2pt %": round(games["TwoMade"]/games["TwoAttempted"]*100,1).fillna(0),
                "Notes": games["Notes"]
            })
            games_excel.to_excel(writer, sheet_name="Games", index=False)

        # Shooting Practice
        practice = data[data["Activity Type"]=="Practice"]
        if not practice.empty:
            practice_excel = pd.DataFrame({
                "Date": practice["Date"], "Player": practice["Player"],
                "Time 21pts drill (min)": (practice["Metric1"]//60).astype(int),
                "Time 21pts drill (sec)": (practice["Metric1"]%60).astype(int),
                "Time 10 layups (min)": (practice["Metric2"]//60).astype(int),
                "Time 10 layups (sec)": (practice["Metric2"]%60).astype(int),
                "# Around Key shots": practice["Metric3"],
                "# 3pt in 4min": practice["Metric4"], "3pt %": practice["Metric5"],
                "Mid-range %": practice["Metric6"], "Notes": practice["Notes"]
            })
            practice_excel.to_excel(writer, sheet_name="Shooting Practice", index=False)

        # Conditioning
        cond = data[data["Activity Type"]=="Conditioning"]
        if not cond.empty:
            cond_excel = pd.DataFrame({
                "Date": cond["Date"], "Player": cond["Player"],
                "Time 17s drill (min)": (cond["Metric1"]//60).astype(int),
                "Time 17s drill (sec)": (cond["Metric1"]%60).astype(int),
                "Time 1 suicide (min)": (cond["Metric2"]//60).astype(int),
                "Time 1 suicide (sec)": (cond["Metric2"]%60).astype(int),
                "Time 5 suicides (min)": (cond["Metric3"]//60).astype(int),
                "Time 5 suicides (sec)": (cond["Metric3"]%60).astype(int),
                "# Defensive slides": cond["Metric4"], "Notes": cond["Notes"]
            })
            cond_excel.to_excel(writer, sheet_name="Conditioning", index=False)

        writer.save()
        processed_data = output.getvalue()
    return processed_data

st.subheader("Export Data")
st.download_button(
    label="Download Excel",
    data=export_to_excel(data),
    file_name="basketball_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
