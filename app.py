import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Premium wide page layout engine
st.set_page_config(
    page_title="talabat UAE Logistics Deck",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom talabat Brand Styling Blocks (Orange Accent Palette)
st.markdown("""
    <style>
        .stMainBlock { background-color: #0f172a; }
        h1 { color: #ff5000 !important; font-weight: 900 !important; letter-spacing: -1px; }
        h3 { color: #f8fafc !important; font-weight: 700 !important; }
        .stMetric { background-color: #1e293b; border: 1px solid #334155; padding: 22px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        div[data-testid="stMetricValue"] { color: #ffffff !important; font-family: monospace; font-size: 2.6rem !important; font-weight: 700; }
        div[data-row="true"] { gap: 12px !important; }
        div[data-testid="stWidgetLabel"] p { color: #94a3b8 !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Resilient Internal Data Extraction Pipeline
@st.cache_data(ttl=10)
def load_native_data():
    # Read CSV and drop completely empty unparsed structural padding columns
    df = pd.read_csv("data.csv")
    df = df.dropna(how='all', axis=1)
    
    # Strip whitespace from column headers
    df.columns = df.columns.str.strip()
    
    # Standardize our targeted operational tags safely
    standard_map = {}
    for col in df.columns:
        c_low = col.lower()
        if 'rider id' in c_low: standard_map[col] = 'Rider ID'
        elif 'contract' in c_low: standard_map[col] = 'Contract Name'
        elif 'city' in c_low: standard_map[col] = 'City'
        elif 'module' in c_low: standard_map[col] = 'Module'
        elif 'status' in c_low: standard_map[col] = 'Status'
        elif 'performance' in c_low: standard_map[col] = 'Performance'
        elif 'feedback' in c_low: standard_map[col] = 'Feedback'
        elif 'date' in c_low: standard_map[col] = 'Planned Date'
        elif col == 'Name': standard_map[col] = 'Name'
    
    df = df.rename(columns=standard_map)
    
    # Ensure target core fields exist; if missing, pad cleanly
    core_architecture = ['Rider ID', 'Name', 'Contract Name', 'City', 'Module', 'Planned Date', 'Status', 'Performance', 'Feedback']
    for element in core_architecture:
        if element not in df.columns:
            df[element] = "Not Documented"
            
    # CRASH PROTECTION: Force conversion to simple strings before clearing whitespaces
    for element in core_architecture:
        # If duplicated columns exist, pick the first one to avoid DataFrame subset exceptions
        if isinstance(df[element], pd.DataFrame):
            df[element] = df[element].iloc[:, 0]
        df[element] = df[element].astype(str).str.strip()
            
    # Drop rows that are just empty pivot remnants
    df = df[df["Rider ID"] != "nan"]
    df = df[df["Rider ID"] != ""]
    
    return df

try:
    df_raw = load_native_data()
except Exception as error_logs:
    st.error(f"Local Ledger Pipeline Disrupted. Diagnostics: {error_logs}")
    st.stop()

# Dashboard Header
col_branding, col_title, col_reset = st.columns([0.8, 4, 1.5])
with col_title:
    st.title("🍊 talabat Operations Hub")
    st.caption("Secure Local Data Repository Execution Active • UAE Fleet Framework")
with col_reset:
    if st.button("🔄 Purge System Cache", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.write("---")

# 3. INTERACTIVE SLIDER PANELS
st.write("### 📍 Fleet Control Parameters")
control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    unique_cities = sorted([c for c in df_raw["City"].unique() if c not in ["N/A", "nan", "Not Documented"]])
    valid_cities = ["All Focus Areas"] + unique_cities
    selected_city = st.radio("Regional Hub Location Focus", options=valid_cities, index=0, horizontal=True)

with control_col2:
    unique_modules = sorted([m for m in df_raw["Module"].unique() if m not in ["N/A", "nan", "Not Documented"]])
    valid_modules = ["All Operational Segments"] + unique_modules
    selected_module = st.radio("Core Optimization Module Focus", options=valid_modules, index=0, horizontal=True)

with control_col3:
    unique_statuses = sorted([s for s in df_raw["Status"].unique() if s not in ["N/A", "nan", "Not Documented"]])
    valid_status = ["All Status Outputs"] + unique_statuses
    selected_status = st.radio("Training Attendance Logs Filter", options=valid_status, index=0, horizontal=True)

# 4. Fleet Data Matrix Filtration Engine
df_filtered = df_raw.copy()

if selected_city != "All Focus Areas":
    df_filtered = df_filtered[df_filtered["City"] == selected_city]
if selected_module != "All Operational Segments":
    df_filtered = df_filtered[df_filtered["Module"] == selected_module]
if selected_status != "All Status Outputs":
    df_filtered = df_filtered[df_filtered["Status"] == selected_status]

# Global Query Search Indexer Bar
search_query = st.text_input("🔍 Quick Global Audit Registry Index Search (Type Rider Name, Company, or ID Number)", placeholder="Start typing...")
if search_query:
    df_filtered = df_filtered[
        df_filtered["Name"].str.contains(search_query, case=False) |
        df_filtered["Rider ID"].str.contains(search_query, case=False) |
        df_filtered["Contract Name"].str.contains(search_query, case=False)
    ]

# 5. INDUSTRIAL PERFORMANCE KPIS
st.write("### ⚡ Macro Visual Operations Metrics")
metric_col1, metric_col2, metric_col3 = st.columns(3)

total_logged_pool = len(df_filtered)
validated_attendance_cohort = len(df_filtered[df_filtered["Status"].str.lower() == "attended"])
engagement_conversion_ratio = round((validated_attendance_cohort / total_logged_pool) * 100) if total_logged_pool > 0 else 0

with metric_col1:
    st.metric(label="Riders Accounted Pool", value=f"{total_logged_pool:,}")
with metric_col2:
    st.metric(label="Validated Attendance Registry", value=f"{validated_attendance_cohort:,}")
with metric_col3:
    st.metric(label="Operational Engagement Rate", value=f"{engagement_conversion_ratio}%")

# 6. CHART GEOMETRY DESIGNS
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if not df_filtered.empty:
        distribution_chart_df = df_filtered.groupby(["Module", "Status"]).size().reset_index(name="Riders Count")
        fig1 = px.bar(
            distribution_chart_df,
            x="Module",
            y="Riders Count",
            color="Status",
            title="Volume Density Classification Mix",
            barmode="stack",
            color_discrete_map={"Attended": "#10b981", "Not Attended": "#ef4444", "Not Documented": "#64748b"}
        )
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Awaiting structural filters calculation values.")

with chart_col2:
    if not df_filtered.empty:
        fig2 = px.pie(
            df_filtered,
            names="City",
            title="Geographic Hub Distribution Densities Matrix",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Oranges_r
        )
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig2, use_container_width=True)

# 7. INTERACTIVE PERFORMANCE LEDGER REGISTER TABLE
st.write("### 📋 Deep-Dive Operational Records Audit Table Ledger")
viewable_columns_schema = [col for col in df_filtered.columns if col in [
    "Rider ID", "Name", "Contract Name", "City", "Module", "Planned Date", "Status", "Performance", "Feedback"
]]
st.dataframe(df_filtered[viewable_columns_schema], use_container_width=True, hide_index=True)
