import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import os
import json

st.set_page_config(page_title="Basketball Tracking Dashboard", layout="wide")
st.title("Basketball Tracking Dashboard")

DATA_FILE = "basketball_data.csv"
DATA_COLUMNS = ["Date", "Player", "Activity Type",
                "Metric1","Metric2","Metric3","Metric4","Metric5","Metric6","Notes"]

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

    metric1 = metric2 = metric3 = metric4 = metric5 = metric6 = None
    notes = ""

    if activity_type == "Games":
        points = st.number_input("Points", min_value=0)
        assists = st.number_input("Assists", min_value=0)
        turnovers = st.number_input("Turnovers", min_value=0)
        steals = st.number_input("Steals", min_value=0)
        metric1 = points
        metric2 = assists
        metric3 = turnovers
        metric4 = steals

    elif activity_type == "Practice":
        time_21 = st.number_input("Time for 21-points drill (s)", min_value=0)
        time_layups = st.number_input("Time for 10 layups (s)", min_value=0)
        around_key = st.number_input("# Around the Key shots in 4 mins", min_value=0)
        three_p_4min = st.number_input("# 3-pointers in 4 mins", min_value=0)
        three_made = st.number_input("3-point shots made", min_value=0)
        three_attempted = st.number_input("3-point shots attempted", min_value=0)
        mid_made = st.number_input("Mid-range shots made", min_value=0)
        mid_attempted = st.number_input("Mid-range shots attempted", min_value=0)

        three_pct = round(three_made / three_attempted * 100, 1) if three_attempted else 0
        mid_pct = round(mid_made / mid_attempted * 100, 1) if mid_attempted else 0

        metric1 = time_21
        metric2 = time_layups
        metric3 = around_key
        metric4 = three_p_4min
        metric5 = three_pct
        metric6 = mid_pct
        notes = f"3pt: {three_made}/{three_attempted} ({three_pct}%), Mid-range: {mid_made}/{mid_attempted} ({mid_pct}%)"

    elif activity_type == "Conditioning":
        time_17s = st.number_input("Time for 17s drill (s)", min_value=0)
        time_1_suicide = st.number_input("Time for 1 suicide (s)", min_value=0)
        time_5_suicides = st.number_input("Time for 5 suicides (s)", min_value=0)
        defensive_slides = st.number_input("Number of defensive slides in 30s", min_value=0)
        metric1 = time_17s
        metric2 = time_1_suicide
        metric3 = time_5_suicides
        metric4 = defensive_slides

    submit = st.form_submit_button("Add Activity")

if submit:
    new_row = pd.DataFrame({
        "Date": [date.strftime("%Y-%m-%d")],
        "Player": [player],
        "Activity Type": [activity_type],
        "Metric1": [metric1],
        "Metric2": [metric2],
        "Metric3": [metric3],
        "Metric4": [metric4],
        "Metric5": [metric5],
        "Metric6": [metric6],
        "Notes": [notes]
    })
    data = pd.concat([data, new_row], ignore_index=True)
    data.to_csv(DATA_FILE, index=False)
    st.success(f"Added new {activity_type} for {player} on {date.strftime('%Y-%m-%d')}")

# ======================
# Current Data Table
# ======================
st.subheader("Current Data")
st.dataframe(data)

# ======================
# Trending Analysis
# ======================
st.subheader("Trending Analysis")

if not data.empty:
    filtered_data = data[data["Activity Type"] == activity_type].copy()
    if not filtered_data.empty:
        filtered_data["Date"] = pd.to_datetime(filtered_data["Date"], errors="coerce")
        for col in ["Metric1","Metric2","Metric3","Metric4","Metric5","Metric6"]:
            if col in filtered_data.columns:
                filtered_data[col] = pd.to_numeric(filtered_data[col], errors="coerce")
        filtered_data = filtered_data.dropna(subset=["Metric1"])

        if not filtered_data.empty:
            # Define meaningful metric per activity type
            if activity_type == "Games":
                metric_plot = ["Metric1","Metric2"]  # Points & Assists
            elif activity_type == "Practice":
                metric_plot = ["Metric5","Metric6"]  # 3pt% & Mid%
            else:
                metric_plot = ["Metric1","Metric2"]  # Time for 17s & 1 suicide

            for metric in metric_plot:
                fig = px.line(filtered_data, x="Date", y=metric, color="Player",
                              title=f"{activity_type} - {metric} Trend", markers=True)
                st.plotly_chart(fig, use_container_width=True)

# ======================
# Export Data
# ======================
st.subheader("Export Data")
csv_export = data.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv_export,
    file_name='basketball_data_export.csv',
    mime='text/csv'
)

# Optional Google Sheets export
if os.path.exists("gcp_credentials.json") and st.checkbox("Export to Google Sheets"):
    try:
        import gspread
        with open("gcp_credentials.json") as f:
            gcp_json = json.load(f)
        gc = gspread.service_account_from_dict(gcp_json)
        sheet_name = st.text_input("Google Sheet Name", "BasketballData")
        if st.button("Push to Google Sheets"):
            sh = gc.open(sheet_name).sheet1
            sh.update([data.columns.values.tolist()] + data.values.tolist())
            st.success(f"Data exported to Google Sheet: {sheet_name}")
    except Exception as e:
        st.error(f"Error exporting to Google Sheets: {e}")
