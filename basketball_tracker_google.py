import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("🏀 Basketball Tracker - Google Sheets Debug")

try:
    st.write("Step 1: Loading credentials...")

    # Load credentials
    creds = Credentials.from_service_account_file(
        "basketballtrackerapp-9e471979a8bc.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    st.write("✅ Step 1: Credentials loaded")

    # Authorize client
    client = gspread.authorize(creds)
    st.write("✅ Step 2: Authorized client")

    # Open Google Sheet
    sheet = client.open("Basketball Tracker").sheet1
    st.write("✅ Step 3: Connected to Google Sheet")

    # Test read
    data = sheet.get_all_records()
    st.write("✅ Step 4: Data read successfully")
    st.write("Preview of sheet data:", data[:5])

except Exception as e:
    st.error(f"❌ ERROR: {str(e)}")