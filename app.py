import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Premium wide page layout engine
st.set_page_config(
    page_title="Talabat Existing Rider Training Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom talabat Brand Visual Refinements (Clean White Headers, Gray Contours)
st.markdown("""
    <style>
        .stMainBlock { background-color: #0f172a; }
        /* Clean white layout headers */
        h1 { color: #ffffff !important; font-weight: 800 !important; letter-spacing: -1px; }
        h3 { color: #f8fafc !important; font-weight: 700 !important; margin-top: 20px; }
        .stMetric { background-color: #1e293b; border: 1px solid #334155; padding: 22px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        div[data-testid="stMetricValue"] { color: #ffffff !important; font-family: monospace; font-size: 2.6rem !important; font-weight: 700; }
        div[data-row="true"] { gap: 12px !important; }
        div[data-testid="stWidgetLabel"] p { color: #94a3b8 !important; font-weight: 600 !important; font-size: 0.95rem; }
    </style>
""", unsafe_allow_html=True)

# 2. Data Connection Engine
@st.cache_data(ttl=10)
def load_native_data():
    df = pd.read_csv("data.csv")
    df = df.dropna(how='all', axis=1)
    df.columns = df.columns.str.strip()
    
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
        elif 'pre-training' in c_low: standard_map[col] = 'Pre-Training Metric'
        elif 'post-training' in c_low: standard_map[col] = 'Post-Training Metric'
        elif col == 'Name': standard_map[col] = 'Name'
    
    df = df.rename(columns=standard_map)
    
    core_architecture = ['Rider ID', 'Name', 'Contract Name', 'City', 'Module', 'Planned Date', 'Status', 'Performance', 'Feedback', 'Pre-Training Metric', 'Post-Training Metric']
    for element in core_architecture:
        if element not in df.columns:
            df[element] = "Not Documented"
            
    for element in core_architecture:
        if isinstance(df[element], pd.DataFrame):
            df[element] = df[element].iloc[:, 0]
        df[element] = df[element].astype(str).str.strip()
            
    df = df[df["Rider ID"] != "nan"]
    df = df[df["Rider ID"] != ""]
    return df

try:
    df_raw = load_native_data()
except Exception as error_logs:
    st.error(f"Local Ledger Pipeline Disrupted. Diagnostics: {error_logs}")
    st.stop()

# Dashboard Header Layout
col_title, col_reset = st.columns([4, 1.5])
with col_title:
    st.title("🍊 Talabat Existing Rider Training Dashboard")
    st.caption("Secure Local Data Repository Execution Active • UAE Fleet Framework")
with col_reset:
    if st.button("🔄 Purge System Cache", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.write("---")

# 3. TYPE-SAFE RECTANGULAR PILL BOX PANELS
st.write("### 📍 Fleet Control Parameters")

unique_cities = sorted([str(c) for c in df_raw["City"].unique() if str(c) not in ["N/A", "nan", "Not Documented"]])
valid_cities = ["All Focus Areas"] + unique_cities
selected_city = st.pills("Regional Hub Location Focus", options=valid_cities, default="All Focus Areas")

unique_modules = sorted([str(m) for m in df_raw["Module"].unique() if str(m) not in ["N/A", "nan", "Not Documented"]])
valid_modules = ["All Operational Segments"] + unique_modules
selected_module = st.pills("Core Optimization Module Focus", options=valid_modules, default="All Operational Segments")

unique_statuses = sorted([str(s) for s in df_raw["Status"].unique() if str(s) not in ["N/A", "nan", "Not Documented"]])
valid_status = ["All Status Outputs"] + unique_statuses
selected_status = st.pills("Training Attendance Logs Filter", options=valid_status, default="All Status Outputs")

# 4. GRANULAR DROPDOWN CONTROL DECK
st.write("### 🔍 Granular Dropdown Selectors")
drop_col1, drop_col2, drop_col3, drop_col4 = st.columns(4)

with drop_col1:
    unique_cos = sorted([str(co) for col in [df_raw["Contract Name"].unique()] for co in col if str(co) not in ["N/A", "nan", "Not Documented"]])
    selected_co = st.selectbox("Filter by Delivery Company", options=["All Partner Vendors"] + unique_cos)

with drop_col2:
    selected_drop_city = st.selectbox("Dropdown Quick-Jump: City", options=["Synchronized with Pill Panel"] + unique_cities)

with drop_col3:
    selected_drop_module = st.selectbox("Dropdown Quick-Jump: Module", options=["Synchronized with Pill Panel"] + unique_modules)

with drop_col4:
    selected_drop_status = st.selectbox("Dropdown Quick-Jump: Status", options=["Synchronized with Pill Panel"] + unique_statuses)

# 5. Filtration Intersect Logic
df_filtered = df_raw.copy()

# Sync Dropdowns with Pills if explicitly selected
city_filter_val = selected_drop_city if selected_drop_city != "Synchronized with Pill Panel" else selected_city
module_filter_val = selected_drop_module if selected_drop_module != "Synchronized with Pill Panel" else selected_module
status_filter_val = selected_drop_status if selected_drop_status != "Synchronized with Pill Panel" else selected_status

if city_filter_val != "All Focus Areas" and city_filter_val != "Synchronized with Pill Panel":
    df_filtered = df_filtered[df_filtered["City"] == city_filter_val]
if module_filter_val != "All Operational Segments" and module_filter_val != "Synchronized with Pill Panel":
    df_filtered = df_filtered[df_filtered["Module"] == module_filter_val]
if status_filter_val != "All Status Outputs" and status_filter_val != "Synchronized with Pill Panel":
    df_filtered = df_filtered[df_filtered["Status"] == status_filter_val]
if selected_co != "All Partner Vendors":
    df_filtered = df_filtered[df_filtered["Contract Name"] == selected_co]

# Global Query Search Indexer Bar
search_query = st.text_input("🔍 Search Registry Index (Type Rider Name, Vendor Company, or ID Number)", placeholder="Start typing...")
if search_query:
    df_filtered = df_filtered[
        df_filtered["Name"].str.contains(search_query, case=False) |
        df_filtered["Rider ID"].str.contains(search_query, case=False) |
        df_filtered["Contract Name"].str.contains(search_query, case=False)
    ]

# 6. MACRO PERFORMANCE KPIS
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

# 7. VISUAL GEOMETRY DESIGNS & FUTURE-PROOF RECONCILIATION CHARTS
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if not df_filtered.empty:
        distribution_chart_df = df_filtered.groupby(["Module", "Status"]).size().reset_index(name="Riders Count")
        fig1 = px.bar(
            distribution_chart_df, x="Module", y="Riders Count", color="Status",
            title="Volume Density Classification Mix", barmode="stack",
            color_discrete_map={"Attended": "#10b981", "Not Attended": "#ef4444", "Not Documented": "#64748b"}
        )
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    if not df_filtered.empty:
        fig2 = px.pie(
            df_filtered, names="City", title="Geographic Hub Distribution Densities Matrix",
            hole=0.4, color_discrete_sequence=px.colors.sequential.Oranges_r
        )
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig2, use_container_width=True)

# FUTURE METRICS ENGINE CHECK: Renders instantly when performance columns are populated
has_perf_data = not df_filtered.empty and df_filtered["Performance"].iloc[0] != "Not Documented"
has_metric_data = not df_filtered.empty and df_filtered["Pre-Training Metric"].iloc[0] != "Not Documented"

if has_perf_data or has_metric_data:
    st.write("---")
    st.write("### 📈 Deep Growth & Performance Quality Analytics")
    perf_chart_col1, perf_chart_col2 = st.columns(2)
    
    with perf_chart_col1:
        if has_perf_data:
            perf_chart_df = df_filtered.groupby(["Module", "Performance"]).size().reset_index(name="Count")
            fig_perf = px.bar(
                perf_chart_df, x="Module", y="Count", color="Performance",
                title="Rider Performance Evolution by Segment", barmode="group",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_perf.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_perf, use_container_width=True)
            
    with perf_chart_col2:
        if_has_metric_data:
            try:
                df_filtered["Pre-Training Metric"] = pd.to_numeric(df_filtered["Pre-Training Metric"], errors='coerce')
                df_filtered["Post-Training Metric"] = pd.to_numeric(df_filtered["Post-Training Metric"], errors='coerce')
                avg_pre = df_filtered["Pre-Training Metric"].mean()
                avg_post = df_filtered["Post-Training Metric"].mean()
                
                fig_delta = go.Figure(data=[
                    go.Bar(name='Historical Pre-Training Average', x=['Fleet Score Average'], y=[avg_pre], marker_color='#94a3b8'),
                    go.Bar(name='Validated Post-Training Average', x=['Fleet Score Average'], y=[avg_post], marker_color='#ff5000')
                ])
                fig_delta.update_layout(title="Strategic Metric Delta Pre vs Post Evaluation", template="plotly_dark", barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_delta, use_container_width=True)
            except Exception:
                pass

# 8. INTERACTIVE PERFORMANCE LEDGER REGISTER TABLE
st.write("### 📋 Deep-Dive Rider Records Audit Table Ledger")
viewable_columns_schema = [col for col in df_filtered.columns if col in [
    "Rider ID", "Name", "Contract Name", "City", "Module", "Planned Date", "Status", "Performance", "Pre-Training Metric", "Post-Training Metric", "Feedback"
]]
st.dataframe(df_filtered[viewable_columns_schema], use_container_width=True, hide_index=True)
