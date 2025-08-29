import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import os
import json

st.set_page_config(page_title="Basketball Tracking Dashboard", layout="wide")
st.title("Basketball Tracking Dashboard")

DATA_FILE = "basketball_data.csv"

# ======================
# Load or initialize data
# ======================
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
else:
    data = pd.DataFrame(columns=["Date", "Player", "Activity Type", "Metric1", "Metric2", "Notes"])

# ======================
# Add New Activity Form
# ======================
st.subheader("Add New Activity")

with st.form("activity_form"):
    date = st.date_input("Date", datetime.today())
    player = st.text_input("Player Name")
    activity_type = st.selectbox("Activity Type", ["Game", "Shooting Drill", "Conditioning"])
    metric1 = st.text_input("Metric 1 (e.g., Points, Made, Minutes)")
    metric2 = st.text_input("Metric 2 (e.g., Rebounds, Attempts, HR Avg)")
    notes = st.text_area("Notes (optional)")
    submit = st.form_submit_button("Add Activity")

if submit:
    new_row = pd.DataFrame({
        "Date": [date.strftime("%Y-%m-%d")],
        "Player": [player],
        "Activity Type": [activity_type],
        "Metric1": [metric1],
        "Metric2": [metric2],
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
    # Filter by activity type
    activity_filter = st.selectbox("Select Activity Type for Trending", data["Activity Type"].unique())
    filtered_data = data[data["Activity Type"] == activity_filter].copy()

    if not filtered_data.empty:
        filtered_data["Date"] = pd.to_datetime(filtered_data["Date"], errors="coerce")
        filtered_data["Metric1"] = pd.to_numeric(filtered_data["Metric1"], errors="coerce")
        filtered_data = filtered_data.dropna(subset=["Date", "Metric1"])

        if not filtered_data.empty:
            fig1 = px.line(filtered_data, x="Date", y="Metric1", color="Player",
                           title=f"{activity_filter} - Metric1 Trend", markers=True)
            st.plotly_chart(fig1, use_container_width=True)

            # Optional Metric2 chart if numeric
            filtered_data["Metric2"] = pd.to_numeric(filtered_data["Metric2"], errors="coerce")
            if filtered_data["Metric2"].notnull().any():
                fig2 = px.line(filtered_data, x="Date", y="Metric2", color="Player",
                               title=f"{activity_filter} - Metric2 Trend", markers=True)
                st.plotly_chart(fig2, use_container_width=True)

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

# Optional: Export to Google Sheets if credentials exist
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
