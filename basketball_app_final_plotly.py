import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------
# File settings
# -------------------
EXCEL_FILE = "basketball_metrics.xlsx"

# -------------------
# Page Config
# -------------------
st.set_page_config(
    page_title="Basketball Performance Tracker",
    page_icon="🏀",
    layout="wide"
)

# -------------------
# Custom CSS
# -------------------
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)),
                    url("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Basketball_court_illustration.svg/1920px-Basketball_court_illustration.svg.png");
        background-size: cover;
    }
    .title {
        text-align: center;
        color: #E74C3C;
        font-size: 36px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        font-style: italic;
        font-size: 20px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------
# Header with Kobe Bryant
# -------------------
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/6/63/Kobe_Bryant_8.jpg",
    use_container_width=True
)
st.markdown('<div class="title">Basketball Performance Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">"The most important thing is to try and inspire people so that they can be great in whatever they want to do." – Kobe Bryant</div>', unsafe_allow_html=True)
st.markdown("---")

# -------------------
# Load / Initialize Data
# -------------------
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Shots Made", "Shots Attempted", "1 Dribble Pullups", "Lateral Shuffle Time", "Bronco Test Time"])

# -------------------
# Data Entry Form
# -------------------
st.header("📊 Enter Today's Metrics")

with st.form("entry_form", clear_on_submit=True):
    date = st.date_input("Date")
    shots_made = st.number_input("Shots Made", min_value=0, step=1)
    shots_attempted = st.number_input("Shots Attempted", min_value=0, step=1)
    pullups = st.number_input("1 Dribble Pullups Made", min_value=0, step=1)
    shuffle_time = st.number_input("Lateral Shuffle Time (seconds)", min_value=0.0, step=0.1)
    bronco_time = st.number_input("Bronco Test Time (seconds)", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Save Entry 🏀")

if submitted:
    new_data = pd.DataFrame([[date, shots_made, shots_attempted, pullups, shuffle_time, bronco_time]],
                            columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    st.success("✅ Entry saved successfully!")

# -------------------
# Display Data
# -------------------
st.header("📂 Data Table")
st.dataframe(df, use_container_width=True)

# -------------------
# Charts
# -------------------
st.header("📈 Performance Charts")

if not df.empty:
    metrics = {
        "Shooting Percentage": (df["Shots Made"] / df["Shots Attempted"]) * 100,
        "1 Dribble Pullups": df["1 Dribble Pullups"],
        "Lateral Shuffle Time": df["Lateral Shuffle Time"],
        "Bronco Test Time": df["Bronco Test Time"]
    }

    for metric, values in metrics.items():
        chart_df = pd.DataFrame({"Date": df["Date"], metric: values})
        fig = px.line(chart_df, x="Date", y=metric, markers=True, title=metric)
        st.plotly_chart(fig, use_container_width=True)
