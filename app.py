import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Talabat UAE Rider Training Hub",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .stMainBlock { background-color: #0f172a; }
        h1 { color: #ff5000 !important; font-weight: 900 !important; }
        .stMetric { background-color: #1e293b; border: 1px solid #334155; padding: 20px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
        div[data-testid="stMetricValue"] { color: #ffffff !important; font-family: monospace; font-size: 2.5rem !important; }
        div[data-row="true"] { gap: 10px !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60) 
def load_data():
    # Direct local file pull from your GitHub repository folder!
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip()
    
    mapping = {}
    for col in df.columns:
        if col.lower() == 'performance': mapping[col] = 'Performance'
        if col.lower() == 'city': mapping[col] = 'City'
        if col.lower() == 'module': mapping[col] = 'Module'
        if col.lower() == 'name': mapping[col] = 'Name'
        if col.lower() == 'rider id': mapping[col] = 'Rider ID'
        if col.lower() == 'status': mapping[col] = 'Status'
    df = df.rename(columns=mapping)
    
    fallback_cols = ["Performance", "City", "Module", "Name", "Rider ID", "Status"]
    for c in fallback_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
        else:
            df[c] = "N/A"
            
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Local Data Read Error: {e}")
    st.stop()

col_logo, col_title, col_sync = st.columns([1, 4, 1.5])
with col_title:
    st.title("🍊 talabat Operations Hub")
    st.caption("Secure Native Local Ledger Mode Active")
with col_sync:
    if st.button("🔄 Force Clear App Cache", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.write("---")

st.write("### 📍 Operational Controls")
deck_col1, deck_col2, deck_col3 = st.columns(3)

with deck_col1:
    unique_cities = ["All"] + [c for c in list(df_raw["City"].unique()) if c != "N/A" and c != "nan"]
    selected_city = st.radio(label="Select Location Focus", options=unique_cities, index=0, horizontal=True, key="city_filter")

with deck_col2:
    unique_modules = ["All"] + [m for m in list(df_raw["Module"].unique()) if m != "N/A" and m != "nan"]
    selected_module = st.radio(label="Select Core Training Segment", options=unique_modules, index=0, horizontal=True, key="module_filter")

with deck_col3:
    unique_status = ["All"] + [s for s in list(df_raw["Status"].unique()) if s != "N/A" and s != "nan"]
    selected_status = st.radio(label="Training Attendance Output", options=unique_status, index=0, horizontal=True, key="status_filter")

df_filtered = df_raw.copy()

if selected_city != "All":
    df_filtered = df_filtered[df_filtered["City"] == selected_city]
if selected_module != "All":
    df_filtered = df_filtered[df_filtered["Module"] == selected_module]
if selected_status != "All":
    df_filtered = df_filtered[df_filtered["Status"] == selected_status]

search_query = st.text_input("🔍 Quick Search Filter (Type Rider Name or unique ID Number)", placeholder="Start typing...")
if search_query:
    df_filtered = df_filtered[
        df_filtered["Name"].astype(str).str.contains(search_query, case=False) |
        df_filtered["Rider ID"].astype(str).str.contains(search_query, case=False)
    ]

st.write("### ⚡ Macro Visual Metrics")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

total_riders = len(df_filtered)
attended_riders = len(df_filtered[df_filtered["Status"].str.lower() == "attended"])
attendance_rate = round((attended_riders / total_riders) * 100) if total_riders > 0 else 0

with kpi_col1:
    st.metric(label="Riders Logged Pool", value=f"{total_riders:,}")
with kpi_col2:
    st.metric(label="Validated Attendance Cohort", value=f"{attended_riders:,}")
with kpi_col3:
    st.metric(label="Cohort Engagement Rate", value=f"{attendance_rate}%")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if not df_filtered.empty and df_filtered["Module"].iloc[0] != "N/A":
        chart_data = df_filtered.groupby(["Module", "Status"]).size().reset_index(name="Riders")
        fig1 = px.bar(
            chart_data, 
            x="Module", 
            y="Riders", 
            color="Status",
            title="Volume Density By Training Module",
            barmode="stack",
            color_discrete_map={"Attended": "#10b981", "Not Attended": "#ef4444"}
        )
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Waiting for valid data attributes.")

with chart_col2:
    if not df_filtered.empty and df_filtered["Status"].iloc[0] != "N/A":
        fig2 = px.pie(
            df_filtered, 
            names="Status", 
            title="Macro Operational Attendance Mix",
            hole=0.4,
            color="Status",
            color_discrete_map={"Attended": "#10b981", "Not Attended": "#ef4444"}
        )
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Waiting for valid data attributes.")

st.write("### 📋 Deep-Dive Rider Records Audit Table")
available_cols = [c for c in df_filtered.columns if c in [
    "Rider ID", "Name", "Contract Name", "City", 
    "Module", "Actual Planned Date", "Status", 
    "Performance", "Pre-Training metric", "Post-Training Metric", "Feedback"
]]
st.dataframe(df_filtered[available_cols], use_container_width=True, hide_index=True)
