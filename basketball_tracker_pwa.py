import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

st.set_page_config(page_title="Basketball Tracker", layout="wide")

# -------------------------------
# Sidebar: Image Uploads
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
if kobe_file:
    st.image(kobe_file, width=120)

st.markdown("""
<h1 style="text-align:center;">🏀 Basketball Performance Tracker</h1>
<h3 style="text-align:center;font-style:italic;color:#555;">
"The most important thing is you must put everybody on notice that you're here and you are for real." – Kobe Bryant
</h3>
""", unsafe_allow_html=True)

# -------------------------------
# Initialize session state
# -------------------------------
for key in ["games","shooting","conditioning","dribbling"]:
    if key not in st.session_state:
        st.session_state[key] = []

# -------------------------------
# Backup / Import
# -------------------------------
st.sidebar.subheader("Backup / Import")
import_file = st.sidebar.file_uploader("📂 Import Backup", type=["xlsx"])
if import_file:
    xls = pd.ExcelFile(import_file)
    if "Games" in xls.sheet_names:
        st.session_state.games = pd.read_excel(xls, sheet_name="Games").to_dict('records')
    if "Shooting Practice" in xls.sheet_names:
        st.session_state.shooting = pd.read_excel(xls, sheet_name="Shooting Practice").to_dict('records')
    if "Conditioning" in xls.sheet_names:
        st.session_state.conditioning = pd.read_excel(xls, sheet_name="Conditioning").to_dict('records')
    if "Dribbling Practice" in xls.sheet_names:
        st.session_state.dribbling = pd.read_excel(xls, sheet_name="Dribbling Practice").to_dict('records')
    st.success("✅ Backup imported successfully!")

# -------------------------------
# Activity selection
# -------------------------------
activity = st.radio("Select Activity to Log:", [
    "Games Stats", 
    "Shooting Practice", 
    "Conditioning", 
    "Dribbling Practice"
])

# -------------------------------
# Data Entry Forms
# -------------------------------
if activity == "Games Stats":
    st.subheader("📊 Games Stats Entry")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        points = st.number_input("Points", min_value=0)
        assists = st.number_input("Assists", min_value=0)
    with col2:
        turnovers = st.number_input("Turnovers", min_value=0)
        steals = st.number_input("Steals", min_value=0)
    with col3:
        threes_made = st.number_input("3P Made", min_value=0)
    with col4:
        twos_made = st.number_input("2P Made", min_value=0)
    if st.button("Save Game Stats"):
        st.session_state.games.append({
            "Points": points,
            "Assists": assists,
            "Turnovers": turnovers,
            "Steals": steals,
            "3P Made": threes_made,
            "2P Made": twos_made,
            "3P %": round(threes_made / (threes_made+0.0001) * 100, 2),  # avoid div0
            "2P %": round(twos_made / (twos_made+0.0001) * 100, 2)
        })
        st.success("✅ Game stats saved!")

elif activity == "Shooting Practice":
    st.subheader("🏀 Shooting Practice Entry")
    col1, col2 = st.columns(2)
    with col1:
        s21_m = st.number_input("21-points drill - Minutes", min_value=0)
        s21_s = st.number_input("21-points drill - Seconds", min_value=0)
        layups_m = st.number_input("10 Layups - Minutes", min_value=0)
        layups_s = st.number_input("10 Layups - Seconds", min_value=0)
        around_key = st.number_input("Around the Key Shots in 4 mins", min_value=0)
        threes_4min = st.number_input("3P in 4 mins", min_value=0)
    with col2:
        threes_made = st.number_input("3P Made", min_value=0)
        twos_made = st.number_input("2P Made", min_value=0)
    if st.button("Save Shooting Practice"):
        st.session_state.shooting.append({
            "21 Drill Time (s)": s21_m*60 + s21_s,
            "10 Layups Time (s)": layups_m*60 + layups_s,
            "Around Key": around_key,
            "3P in 4min": threes_4min,
            "3P Made": threes_made,
            "2P Made": twos_made,
            "3P %": round(threes_made / (threes_made+0.0001) * 100, 2),
            "2P %": round(twos_made / (twos_made+0.0001) * 100, 2)
        })
        st.success("✅ Shooting practice saved!")

elif activity == "Conditioning":
    st.subheader("💪 Conditioning Entry")
    col1, col2, col3 = st.columns(3)
    with col1:
        drill17_m = st.number_input("17s Drill - Minutes", min_value=0)
        drill17_s = st.number_input("17s Drill - Seconds", min_value=0)
        suicide1_m = st.number_input("1 Suicide - Minutes", min_value=0)
        suicide1_s = st.number_input("1 Suicide - Seconds", min_value=0)
    with col2:
        suicide5_m = st.number_input("5 Suicides - Minutes", min_value=0)
        suicide5_s = st.number_input("5 Suicides - Seconds", min_value=0)
    with col3:
        slides = st.number_input("Defensive Slides in 30s", min_value=0)
    if st.button("Save Conditioning"):
        st.session_state.conditioning.append({
            "17s Drill Time (s)": drill17_m*60 + drill17_s,
            "1 Suicide Time (s)": suicide1_m*60 + suicide1_s,
            "5 Suicides Time (s)": suicide5_m*60 + suicide5_s,
            "Defensive Slides": slides
        })
        st.success("✅ Conditioning data saved!")

elif activity == "Dribbling Practice":
    st.subheader("🤹 Dribbling Practice Entry")
    col1, col2 = st.columns(2)
    with col1:
        two_ball = st.number_input("2-ball dribbles (minutes)", min_value=0)
    with col2:
        one_ball = st.number_input("1-ball dribbles (minutes)", min_value=0)
    if st.button("Save Dribbling Practice"):
        st.session_state.dribbling.append({
            "2-ball Minutes": two_ball,
            "1-ball Minutes": one_ball
        })
        st.success("✅ Dribbling practice saved!")

# -------------------------------
# Export / Backup Function
# -------------------------------
def export_to_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        if st.session_state.games:
            pd.DataFrame(st.session_state.games).to_excel(writer, index=False, sheet_name="Games")
        if st.session_state.shooting:
            pd.DataFrame(st.session_state.shooting).to_excel(writer, index=False, sheet_name="Shooting Practice")
        if st.session_state.conditioning:
            pd.DataFrame(st.session_state.conditioning).to_excel(writer, index=False, sheet_name="Conditioning")
        if st.session_state.dribbling:
            pd.DataFrame(st.session_state.dribbling).to_excel(writer, index=False, sheet_name="Dribbling Practice")
    return output.getvalue()

st.download_button(
    label="💾 Backup Data",
    data=export_to_excel(),
    file_name="basketball_backup.xlsx"
)

# -------------------------------
# Graph Section
# -------------------------------
def show_graphs(data, activity_name, exclude_columns=None):
    if not data:
        st.info(f"No data for {activity_name} yet.")
        return
    df = pd.DataFrame(data)
    for col in df.columns:
        if exclude_columns and col in exclude_columns:
            continue
        if df[col].dtype in ['int64','float64']:
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
show_graphs(st.session_state.games, "Games", exclude_columns=["2P Attempt","3P Attempt"])

st.write("### Shooting Practice Metrics")
show_graphs(st.session_state.shooting, "Shooting Practice", exclude_columns=["2P Attempt","3P Attempt"])

st.write("### Conditioning Metrics")
show_graphs(st.session_state.conditioning, "Conditioning")

st.write("### Dribbling Metrics")
show_graphs(st.session_state.dribbling, "Dribbling Practice")
