import streamlit as st
import pandas as pd
import numpy as np

# --- 1. CORE APP CONTEXT CONFIGURATION ---
st.set_page_config(
    page_title="Talabat Training Control Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom branding adjustments for responsive tables and elements
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: bold; color: rgb(232, 52, 61); }
        .stButton>button { border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)


# --- 2. SECURE DATA REPOSITORY INGESTION ENGINE ---
@st.cache_data(ttl=3600)  # Caches data for 1 hour unless the purge button is clicked
def fetch_operations_data():
    """
    Connects to your master Google Sheet repository and cleanses the rows dynamically.
    Replace the template URL string below with your actual Google Sheet CSV Export link.
    """
    # SHEET_ID = "YOUR_SPREADSHEET_ID_HERE"
    # SHEET_NAME = "Existing%20Riders%20Training"
    # csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    
    # --- DUMMY GENERATOR FOR TESTING & ROBUST INITIALIZATION ---
    # Delete or comment out this block when attaching your live sheet connection URL string.
    np.random.seed(42)
    sample_size = 120
    mock_partners = ["Vendor A Logistics", "Vendor B UAE", "Speedy Delivery LLC", "Al Ain Fleet Pros"]
    mock_modules = ["Road Safety Compliance Deck", "Customer Experience Optimization", "App Performance & Flow"]
    mock_cities = ["Dubai", "Abu Dhabi", "Al Ain", "Sharjah", "Ajman", "RAK", "Fujairah"]
    mock_statuses = ["Attended", "Not Attended", "Rescheduled"]
    
    df = pd.DataFrame({
        'Rider ID': np.random.randint(100000, 999999, size=sample_size),
        'Name': [f"Rider Asset {i}" for i in range(1, sample_size + 1)],
        'Contract Name': np.random.choice(mock_partners, size=sample_size),
        'City': np.random.choice(mock_cities, size=sample_size),
        'Module': np.random.choice(mock_modules, size=sample_size),
        'Planned Date': [pd.Timestamp('2026-07-10').strftime('%d-%m-%Y')] * sample_size,
        'Status': np.random.choice(mock_statuses, size=sample_size, p=[0.70, 0.20, 0.10])
    })
    return df

# Initialize dataframe load state
try:
    raw_df = fetch_operations_data()
    # Clean data string formatting parameters natively
    raw_df['Rider ID'] = raw_df['Rider ID'].astype(str)
    raw_df['Contract Name'] = raw_df['Contract Name'].fillna("Not Documented").strip() if hasattr(raw_df['Contract Name'], 'strip') else raw_df['Contract Name']
except Exception as e:
    st.error(f"Critical Ingestion Error encountered connecting to primary sheets registry: {e}")
    st.stop()


# --- 3. REVISION MANAGEMENT HEADER ---
col_title, col_reset = st.columns([4, 1.5])
with col_title:
    st.title("Talabat Existing Rider Training Dashboard")
    st.caption("UAE Existing Rider Training")
with col_reset:
    # Live data reload cache flush mechanism
    if st.button("🔄 Purge System Cache", use_container_width=True):
        st.cache_data.clear()
        st.toast("System cache purged successfully. Reloading live rows...", icon="⚡")
        st.rerun()

st.divider()


# --- 4. DATA MATRIX FILTER PILLS ---
st.markdown("### 🔍 Filter Parameters")
col_pill_city, col_pill_mod, col_pill_fp = st.columns(3)

with col_pill_city:
    available_cities = sorted(raw_df['City'].unique().tolist())
    selected_cities = st.multiselect("Select City Hub:", options=available_cities, default=available_cities)

with col_pill_mod:
    available_modules = sorted(raw_df['Module'].unique().tolist())
    selected_modules = st.multiselect("Select Training Module:", options=available_modules, default=available_modules)

with col_pill_fp:
    available_fps = sorted(raw_df['Contract Name'].unique().tolist())
    selected_fps = st.multiselect("Select Fleet Partner (FP):", options=available_fps, default=available_fps)

# Apply filter masks dynamically based on inputs
filtered_df = raw_df[
    (raw_df['City'].isin(selected_cities)) &
    (raw_df['Module'].isin(selected_modules)) &
    (raw_df['Contract Name'].isin(selected_fps))
]


# --- 5. HIGH-LEVEL EXECUTIVE METRICS ---
total_scheduled = len(filtered_df)
attended_count = len(filtered_df[filtered_df['Status'].str.lower() == 'attended'])
no_show_count = len(filtered_df[filtered_df['Status'].str.lower() == 'not attended'])

attendance_rate = (attended_count / total_scheduled * 100) if total_scheduled > 0 else 0.0

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
with metric_col1:
    st.metric(label="Total Scheduled Tasks", value=f"{total_scheduled:,}")
with metric_col2:
    st.metric(label="Attended Assets", value=f"{attended_count:,}")
with metric_col3:
    st.metric(label="Logged No-Shows", value=f"{no_show_count:,}")
with metric_col4:
    st.metric(label="Compliance Core Rate", value=f"{attendance_rate:.1f}%")

st.divider()


# --- 6. TARGET DATA LEDGER GRID & SEARCH ---
st.markdown("### 📋 Active Training Ledger Rows")

# Quick search layout parameter
search_query = st.text_input("⚡ Quick Search (Enter Rider ID or Name):", placeholder="Type keywords here to filter the table rows...").strip()
if search_query:
    filtered_df = filtered_df[
        (filtered_df['Rider ID'].str.contains(search_query, case=False)) |
        (filtered_df['Name'].str.contains(search_query, case=False))
    ]

# Display data interactive spreadsheet interface window
if not filtered_df.empty:
    st.dataframe(
        filtered_df[['Rider ID', 'Name', 'Contract Name', 'City', 'Module', 'Planned Date', 'Status']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rider ID": st.column_config.TextColumn("Rider ID"),
            "Planned Date": st.column_config.TextColumn("Planned Date"),
            "Status": st.column_config.TextColumn("Status", help="Attended, Not Attended, or Rescheduled logs")
        }
    )
else:
    st.info("No records match the current filter selection arrays or search string queries.")


# --- 7. FOOTER METADATA SECURITY BANNER ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 15px; border-top: 1px solid #eeeeee;">
        <p style="font-size: 11px; color: #94a3b8; font-family: sans-serif; margin: 0;">
            Talabat Logistics Engine Framework • Controlled Asset Portfolio Data Access Stream
        </p>
    </div>
""", unsafe_allow_html=True)
