import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

st.set_page_config(page_title="Basketball Tracker", layout="wide")

# -------------------------------
# Image Upload Section
# -------------------------------
st.sidebar.subheader("Upload Images (optional)")

kobe_file = st.sidebar.file_uploader("Kobe Bryant Image", type=["png","jpg"])
logo_file = st.sidebar.file_uploader("Basketball Logo", type=["png","jpg"])
court_file = st.sidebar.file_uploader("Court Background", type=["png","jpg"])

court_bg_base64 = None
if court_file:
    court_bg_base64 = base64.b64encode(court_file.read()).decode()

# -------------------------------
# Header
# -------------------------------
st.markdown(
    """
    <div style="text-align:center;">
    """, unsafe_allow_html=True
)

if kobe_file:
    st.image(kobe_file, width=120)

st.markdown(
    """
    <h1>🏀 Basketball Performance Tracker</h1>
    <h3 style="font-style:italic;color:#555;">
    "The most important thing is you must put everybody on notice that you're here and you are for real." – Kobe Bryant
    </h3>
    </div>
    """, unsafe_allow_html=True
)

# -------------------------------
# Session State
# -------------------------------
if "games" not in st.session_state: st.session_state.games = []
if "shooting" not in st.session_state: st.session_state.shooting = []
if "conditioning" not in st.session_state: st.session_state.conditioning = []

# -------------------------------
# Activity Selection
# -------------------------------
activity = st.radio("Select Activity to Log:", ["Games Stats", "Shooting Practice", "Conditioning"])

# -------------------------------
# Data Entry Sections (same as before)
# -------------------------------
# [Keep all Games, Shooting, Conditioning input code from previous version]
# Ensure Minutes + Seconds input for all time fields

# -------------------------------
# Excel Export (same as before)
# -------------------------------

# -------------------------------
# Graph Section
# -------------------------------
def show_graphs(data, activity_name):
    if not data:
        st.info(f"No data for {activity_name} yet.")
        return
    df = pd.DataFrame(data)
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            fig = px.line(df, y=col, title=f"{activity_name} - {col}", markers=True)
            if court_bg_base64:
                fig.update_layout(
                    images=[dict(
                        source=f"data:image/png;base64,{court_bg_base64}",
                        xref="paper", yref="paper",
                        x=0, y=1,
                        sizex=1, sizey=1,
                        xanchor="left",
                        yanchor="top",
                        layer="below",
                        opacity=0.2
                    )],
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)"
                )
            st.plotly_chart(fig, use_container_width=True)

st.write("### Games Metrics")
show_graphs(st.session_state.games, "Games")

st.write("### Shooting Practice Metrics")
show_graphs(st.session_state.shooting, "Shooting Practice")

st.write("### Conditioning Metrics")
show_graphs(st.session_state.conditioning, "Conditioning")