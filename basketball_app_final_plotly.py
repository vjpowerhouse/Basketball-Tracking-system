import pandas as pd
import streamlit as st
import plotly.express as px
import json

st.set_page_config(page_title="Basketball Tracking App", layout="wide")
st.title("Basketball Player Performance Tracker")

# ======================
# Load Data
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("basketball_data.csv")  # Put your CSV in the same folder

data = load_data()
st.subheader("Raw Data")
st.dataframe(data)

# ======================
# Trending Analysis
# ======================
st.subheader("Trending Analysis")

# Example: Points trend over time
if "GameDate" in data.columns and "Points" in data.columns:
    fig = px.line(data, x="GameDate", y="Points", title="Points Trend Over Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# Example: Rebounds trend
if "GameDate" in data.columns and "Rebounds" in data.columns:
    fig2 = px.line(data, x="GameDate", y="Rebounds", title="Rebounds Trend Over Time", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# ======================
# Export Data
# ======================
st.subheader("Export Data")

# Export to CSV
csv = data.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='basketball_data_export.csv',
    mime='text/csv'
)

# Optional: Export to Google Sheets (if JSON credentials available)
if st.checkbox("Export to Google Sheets (requires GCP credentials)"):
    try:
        import gspread
        from gspread.exceptions import APIError

        # Load credentials JSON locally (replace filename if needed)
        with open("gcp_credentials.json") as f:
            gcp_json = json.load(f)

        gc = gspread.service_account_from_dict(gcp_json)
        sheet_name = st.text_input("Google Sheet Name", "BasketballData")
        if st.button("Push to Google Sheets"):
            sh = gc.open(sheet_name).sheet1
            sh.update([data.columns.values.tolist()] + data.values.tolist())
            st.success(f"Data exported to Google Sheet: {sheet_name}")

    except FileNotFoundError:
        st.error("gcp_credentials.json not found. Place your JSON file in the app folder.")
    except Exception as e:
        st.error(f"Error exporting to Google Sheets: {e}")
