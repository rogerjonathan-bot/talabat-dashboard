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

# UPDATED DATA CONNECTION ENGINE (Connecting to your new sheet link)
SHEET_ID = "1GTaLI9nBSMxgnZWCuarNL_GzPduhR6V-YXSXd7Tx_7U"
GID = "1834889034"
DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=15) 
def load_data():
    df = pd.read_csv(DATA_URL)
    
    # Smart Column Cleaner: Strips spaces, forces clean titles
    df.columns = df.columns.str.strip()
    
    # Safety Check: If a column has minor typos, map it correctly
    mapping = {}
    for col in df.columns:
        if col.lower() == 'performance': mapping[col] = 'Performance'
        if col.lower() == 'city': mapping[col] = 'City'
        if col.lower() == 'module': mapping[col] = 'Module'
        if col.lower() == 'name': mapping[col] = 'Name'
        if col.lower() == 'rider id': mapping[col] = 'Rider ID'
    df = df.rename(columns=mapping)
    
    # Fill structural missing strings so the filters don't crash
    fallback_cols = ["Performance", "City", "Module", "Name", "Rider ID"]
    for c in fallback_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
        else:
            # Create a blank column if the header is entirely missing from the sheet
            df[c] = "N/A"
            
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Pipeline Interrupted. Error: {e}")
    st.stop()

col_logo, col_title, col_sync = st.columns([1, 4, 1.5])
with col_title:
    st.title("🍊 talabat Operations Hub")
    st.caption("Real-Time Data Syncing Active via talabat.com corporate workspace network")
with col_sync:
    if st.button("🔄 Force Refresh Master Sheet", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.write("---")

st.write("### 📍 Operational Controls")
deck_col1, deck_col2, deck_col3 = st.columns(3)

with deck_col1:
    unique_cities = ["All"] + [c for c in list(df_raw["City"].unique()) if c != "N/A"]
    selected_city = st.radio(
        label="Select Location Focus",
        options=unique_cities,
        index=0,
        horizontal=True,
        key="city_filter"
    )

with deck_col2:
    unique_modules = ["All"] + [m for m in list(df_raw["Module"].unique()) if m != "N/A"]
    selected_module = st.radio(
        label="Select Core Training Segment",
        options=unique_modules,
        index=0,
        horizontal=True,
        key="module_filter"
    )

with deck_col3:
    selected_perf = st.radio(
        label="Performance Filter Output",
        options=["All", "Improved", "Not Improved"],
        index=0,
        horizontal=True,
        key="perf_filter"
    )

df_filtered = df_raw.copy()

if selected_city != "All":
    df_filtered = df_filtered[df_filtered["City"] == selected_city]
if selected_module != "All":
    df_filtered = df_filtered[df_filtered["Module"] == selected_module]
if selected_perf != "All":
    df_filtered = df_filtered[df_filtered["Performance"] == selected_perf]

search_query = st.text_input("🔍 Quick Search Filter (Type Rider Name or unique ID Number)", placeholder="Start typing...")
if search_query:
    df_filtered = df_filtered[
        df_filtered["Name"].astype(str).str.contains(search_query, case=False) |
        df_filtered["Rider ID"].astype(str).str.contains(search_query, case=False)
    ]

st.write("### ⚡ Macro Visual Metrics")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

total_riders = len(df_filtered)
improved_riders = len(df_filtered[df_filtered["Performance"].str.lower() == "improved"])
success_rate = round((improved_riders / total_riders) * 100) if total_riders > 0 else 0

with kpi_col1:
    st.metric(label="Riders Logged Pool", value=f"{total_riders:,}")
with kpi_col2:
    st.metric(label="Validated Growth Cohort", value=f"{improved_riders:,}")
with kpi_col3:
    st.metric(label="Cohort Conversion Rate", value=f"{success_rate}%")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if not df_filtered.empty and df_filtered["Module"].iloc[0] != "N/A":
        chart_data = df_filtered.groupby(["Module", "Performance"]).size().reset_index(name="Riders")
        fig1 = px.bar(
            chart_data, 
            x="Module", 
            y="Riders", 
            color="Performance",
            title="Volume Density By Training Module",
            barmode="stack",
            color_discrete_map={"Improved": "#10b981", "Not Improved": "#ef4444"}
        )
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Waiting for valid matching sheet criteria to generate module trends.")

with chart_col2:
    if not df_filtered.empty and df_filtered["Performance"].iloc[0] != "N/A":
        fig2 = px.pie(
            df_filtered, 
            names="Performance", 
            title="Macro Operational Success Mix",
            hole=0.4,
            color="Performance",
            color_discrete_map={"Improved": "#10b981", "Not Improved": "#ef4444"}
        )
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Waiting for valid matching sheet criteria to generate conversion mix.")

st.write("### 📋 Deep-Dive Rider Records Audit Table")
available_cols = [c for c in df_filtered.columns if c in [
    "Rider ID", "Name", "Contract Name", "City", 
    "Module", "Actual Planned Date", "Status", 
    "Performance", "Pre-Training metric", "Post-Training Metric", "Feedback"
]]
st.dataframe(df_filtered[available_cols], use_container_width=True, hide_index=True)
