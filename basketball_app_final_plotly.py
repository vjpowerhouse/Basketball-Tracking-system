Perfect! Let’s make this fully polished and ready to deploy. I’ll provide:

1. **A final `requirements.txt`** with everything the app needs.
2. **Full Streamlit app code** with:

   * Clean, **pretty data entry page**
   * Colors, header with **basketball logo**, picture of **Kobe Bryant**, and a **quote**
   * Side-by-side minutes/seconds input for drills
   * Dynamic fields per activity type
   * Separate graphs for each metric
   * Excel export using **openpyxl**

---

### **requirements.txt**

```
streamlit
pandas
plotly
gspread
oauth2client
openpyxl
Pillow
```

* **Pillow** is needed for displaying images (Kobe picture & basketball logo).

---

### **Full Streamlit App Code**

```python
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import os
import io
from PIL import Image

# --------------------- PAGE CONFIG ---------------------
st.set_page_config(page_title="Basketball Tracking Dashboard", layout="wide")

# --------------------- HEADER ---------------------
col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.image("basketball_logo.png", width=60)  # Add your logo in the folder
with col2:
    st.markdown("<h1 style='text-align:center;color:#FF4500'>Basketball Tracking Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#FFA500;font-size:16px'><em>\"The most important thing is to try and inspire people so that they can be great in whatever they want to do.\" - Kobe Bryant</em></p>", unsafe_allow_html=True)
with col3:
    st.image("kobe_bryant.png", width=80)  # Add Kobe image in the folder

st.markdown("---")

# --------------------- DATA FILE ---------------------
DATA_FILE = "basketball_data.csv"
DATA_COLUMNS = ["Date", "Player", "Activity Type",
                "Metric1","Metric2","Metric3","Metric4","Metric5","Metric6",
                "ThreeMade","ThreeAttempted","TwoMade","TwoAttempted","Notes"]

# Load or initialize
if os.path.exists(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
    for col in DATA_COLUMNS:
        if col not in data.columns:
            data[col] = None
else:
    data = pd.DataFrame(columns=DATA_COLUMNS)

# --------------------- DATA ENTRY ---------------------
st.markdown("## Add New Activity")
st.markdown("Fill out the fields below based on the type of activity.", unsafe_allow_html=True)

with st.form("activity_form"):
    date = st.date_input("Date", datetime.today())
    player = st.text_input("Player Name")
    activity_type = st.selectbox("Select Activity Type", ["Games", "Shooting Practice", "Conditioning"])

    # Initialize metrics
    metric1=metric2=metric3=metric4=metric5=metric6=0
    three_made=three_attempted=two_made=two_attempted=0
    notes=""

    # --------------------- GAMES ---------------------
    if activity_type=="Games":
        st.markdown("### Games Metrics", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            points = st.number_input("Points", min_value=0)
            assists = st.number_input("Assists", min_value=0)
            turnovers = st.number_input("Turnovers", min_value=0)
            steals = st.number_input("Steals", min_value=0)
        with col2:
            three_made = st.number_input("# 3-pointers made", min_value=0)
            three_attempted = st.number_input("# 3-pointers attempted", min_value=0)
            two_made = st.number_input("# 2-pointers made", min_value=0)
            two_attempted = st.number_input("# 2-pointers attempted", min_value=0)

        metric1, metric2, metric3, metric4 = points, assists, turnovers, steals
        notes = f"3pt: {three_made}/{three_attempted}, 2pt: {two_made}/{two_attempted}"

    # --------------------- SHOOTING PRACTICE ---------------------
    elif activity_type=="Shooting Practice":
        st.markdown("### Shooting Practice Metrics", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            t21_min = st.number_input("21-pts drill (min)", min_value=0)
        with col2:
            t21_sec = st.number_input("21-pts drill (sec)", min_value=0)

        col3, col4 = st.columns(2)
        with col3:
            t10_min = st.number_input("10 layups (min)", min_value=0)
        with col4:
            t10_sec = st.number_input("10 layups (sec)", min_value=0)

        around_key = st.number_input("# Around Key shots in 4 mins", min_value=0)
        three_p_4min = st.number_input("# 3-pointers in 4 mins", min_value=0)
        three_made_p = st.number_input("3-point shots made", min_value=0)
        three_attempted_p = st.number_input("3-point shots attempted", min_value=0)
        mid_made = st.number_input("Mid-range shots made", min_value=0)
        mid_attempted = st.number_input("Mid-range shots attempted", min_value=0)

        metric1 = t21_min*60 + t21_sec
        metric2 = t10_min*60 + t10_sec
        metric3 = around_key
        metric4 = three_p_4min
        metric5 = round(three_made_p / three_attempted_p * 100, 1) if three_attempted_p else 0
        metric6 = round(mid_made / mid_attempted * 100, 1) if mid_attempted else 0
        notes = f"3pt: {three_made_p}/{three_attempted_p} ({metric5}%), Mid-range: {mid_made}/{mid_attempted} ({metric6}%)"

    # --------------------- CONDITIONING ---------------------
    elif activity_type=="Conditioning":
        st.markdown("### Conditioning Metrics", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            t17_min = st.number_input("17s drill (min)", min_value=0)
        with col2:
            t17_sec = st.number_input("17s drill (sec)", min_value=0)
        col3, col4 = st.columns(2)
        with col3:
            t1s_min = st.number_input("1 suicide (min)", min_value=0)
        with col4:
            t1s_sec = st.number_input("1 suicide (sec)", min_value=0)
        col5, col6 = st.columns(2)
        with col5:
            t5s_min = st.number_input("5 suicides (min)", min_value=0)
        with col6:
            t5s_sec = st.number_input("5 suicides (sec)", min_value=0)

        defensive_slides = st.number_input("Number of defensive slides in 30s", min_value=0)
        metric1 = t17_min*60 + t17_sec
        metric2 = t1s_min*60 + t1s_sec
        metric3 = t5s_min*60 + t5s_sec
        metric4 = defensive_slides

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

# --------------------- ANALYTICS & EXPORT ---------------------
st.markdown("---")
st.subheader("Analytics & Data Export")
tabs = ["Games", "Shooting Practice", "Conditioning", "Export Data"]
selected_tab = st.radio("Select View", tabs, horizontal=True)

# --------------------- TRENDING GRAPHS ---------------------
def plot_trends(filtered_data, metric_names):
    for m, name in metric_names.items():
        if m in filtered_data.columns:
            fig = px.line(filtered_data, x="Date", y=m, color="Player", markers=True,
                          title=f"{name} Trend")
            st.plotly_chart(fig, use_container_width=True)

if selected_tab in ["Shooting Practice","Conditioning"]:
    filtered_data = data[data["Activity Type"]==selected_tab]
    if not filtered_data.empty:
        filtered_data["Date"] = pd.to_datetime(filtered_data["Date"], errors="coerce")
        for col in ["Metric1","Metric2","Metric3","Metric4","Metric5","Metric6"]:
            filtered_data[col] = pd.to_numeric(filtered_data[col], errors="coerce")
        filtered_data = filtered_data.dropna(subset=["Metric1"])
        # Convert seconds to minutes
        for c in ["Metric1","Metric2","Metric3"]:
            filtered_data[c] = (filtered_data[c]/60).round(2)

        if selected_tab=="Shooting Practice":
            metric_names = {"Metric1":"21pts drill (min)", "Metric2":"10 layups (min)", "Metric3":"# Around Key shots",
                            "Metric4":"# 3pt in 4min", "Metric5":"3pt %", "Metric6":"Mid-range %"}
        else:
            metric_names = {"Metric1":"17s drill (min)", "Metric2":"1 suicide (min)", "Metric3":"5 suicides (
```
