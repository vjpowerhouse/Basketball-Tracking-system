import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Basketball Shooting Tracker",
    page_icon="🏀",
    layout="wide"
)

# -----------------------------
# Custom CSS for styling
# -----------------------------
st.markdown(
    """
    <style>
        .main {
            background-color: #fdf6ec; /* light court-like color */
        }
        .title {
            font-size: 36px;
            color: #ff6600;
            text-align: center;
            font-weight: bold;
        }
        .subtitle {
            font-size: 20px;
            color: #444444;
            text-align: center;
            font-style: italic;
        }
        .quote {
            font-size: 18px;
            color: #222222;
            text-align: center;
            margin-top: 10px;
        }
        .data-entry {
            background-color: #fff3e6;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# App Header with Kobe Bryant
# -----------------------------
st.markdown('<div class="title">🏀 Basketball Shooting Tracker</div>', unsafe_allow_html=True)

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/2/27/Kobe_Bryant_2015.jpg",
    use_container_width=True
)

st.markdown('<div class="subtitle">"The moment you give up, is the moment you let someone else win." – Kobe Bryant</div>', unsafe_allow_html=True)

st.write("---")

# -----------------------------
# Initialize Session State
# -----------------------------
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Date", "Shot Type", "Made", "Attempted", "Percentage"])

# -----------------------------
# Data Entry Section
# -----------------------------
st.markdown('<div class="data-entry">', unsafe_allow_html=True)
st.subheader("📋 Enter Shooting Data")

col1, col2, col3, col4 = st.columns(4)
with col1:
    shot_type = st.selectbox("Shot Type", ["2PT", "3PT", "Free Throw"])
with col2:
    made = st.number_input("Made", min_value=0, step=1)
with col3:
    attempted = st.number_input("Attempted", min_value=0, step=1)
with col4:
    date = st.date_input("Date", datetime.today())

if st.button("➕ Add Record"):
    if attempted > 0:
        pct = round((made / attempted) * 100, 2)
        new_entry = {
            "Date": date,
            "Shot Type": shot_type,
            "Made": made,
            "Attempted": attempted,
            "Percentage": pct
        }
        st.session_state["data"] = pd.concat(
            [st.session_state["data"], pd.DataFrame([new_entry])],
            ignore_index=True
        )
        st.success("✅ Record added!")
    else:
        st.error("❌ Attempted shots must be greater than 0.")
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# -----------------------------
# Show Data Table
# -----------------------------
st.subheader("📊 Shooting Log")
st.dataframe(st.session_state["data"], use_container_width=True)

# -----------------------------
# Export to Excel
# -----------------------------
def convert_df_to_excel(df):
    from io import BytesIO
    with pd.ExcelWriter(BytesIO(), engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Shooting Log")
        writer.save()
        processed_data = writer.book
    return processed_data

if not st.session_state["data"].empty:
    df_xlsx = st.session_state["data"].to_excel("shooting_log.xlsx", index=False, engine="openpyxl")
    with open("shooting_log.xlsx", "rb") as f:
        st.download_button("📥 Download Excel", f, "shooting_log.xlsx")

# -----------------------------
# Visualization Section
# -----------------------------
st.subheader("📈 Shooting Performance Trends")

if not st.session_state["data"].empty:
    df = st.session_state["data"]

    # 2PT Percentage
    df2 = df[df["Shot Type"] == "2PT"]
    if not df2.empty:
        fig2 = px.line(df2, x="Date", y="Percentage", markers=True, title="2PT Shooting % Over Time")
        st.plotly_chart(fig2, use_container_width=True)

    # 3PT Percentage
    df3 = df[df["Shot Type"] == "3PT"]
    if not df3.empty:
        fig3 = px.line(df3, x="Date", y="Percentage", markers=True, title="3PT Shooting % Over Time")
        st.plotly_chart(fig3, use_container_width=True)

    # Free Throw %
    dfft = df[df["Shot Type"] == "Free Throw"]
    if not dfft.empty:
        figft = px.line(dfft, x="Date", y="Percentage", markers=True, title="Free Throw % Over Time")
        st.plotly_chart(figft, use_container_width=True)
