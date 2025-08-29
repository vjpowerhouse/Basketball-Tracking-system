import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Excel file path
EXCEL_FILE = "basketball_data.xlsx"

# Load existing data if available
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Drill", "Makes", "Misses", "Notes"])

# ------------------- UI -------------------
st.set_page_config(page_title="Basketball Tracker", layout="wide")

# Header with Kobe
st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://i.ibb.co/fx1xZ8M/kobe.png" width="200">
        <h2 style="color:orange;">"The most important thing is to try and inspire people so that they can be great in whatever they want to do." – Kobe Bryant</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar - Data entry
st.sidebar.header("🏀 Enter Practice Data")
with st.sidebar.form("entry_form", clear_on_submit=True):
    date = st.date_input("Date")
    drill = st.text_input("Drill")
    makes = st.number_input("Makes", min_value=0, step=1)
    misses = st.number_input("Misses", min_value=0, step=1)
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Save Entry")

    if submitted:
        new_row = {"Date": date, "Drill": drill, "Makes": makes, "Misses": misses, "Notes": notes}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        st.sidebar.success("✅ Entry saved!")

# ------------------- Dashboard -------------------
st.subheader("📊 Performance Dashboard")

if not df.empty:
    # Accuracy column
    df["Accuracy %"] = df["Makes"] / (df["Makes"] + df["Misses"] + 1e-6) * 100

    # Chart with basketball court background
    fig = px.scatter(
        df,
        x="Date",
        y="Accuracy %",
        color="Drill",
        size="Makes",
        hover_data=["Notes"],
        title="Shooting Accuracy Over Time",
    )

    # Add court image
    fig.add_layout_image(
        dict(
            source="https://i.ibb.co/XCkWd3K/basketball-court.png",
            xref="paper", yref="paper",
            x=0, y=1,
            sizex=1, sizey=1,
            xanchor="left", yanchor="top",
            sizing="stretch", opacity=0.2, layer="below"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show data table
    st.dataframe(df, use_container_width=True)

    # Download button
    st.download_button(
        "⬇️ Download Data as Excel",
        df.to_excel(index=False, engine="openpyxl"),
        file_name="basketball_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No data yet. Enter practice results in the sidebar.")
