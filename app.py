import streamlit as st
import pandas as pd
import numpy as np

# --- 1. SYSTEM INITIALIZATION ---
st.set_page_config(
    page_title="Talabat Training Control Hub",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom responsive table overrides
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
        div[data-testid="stMetricValue"] { font-size: 32px !important; font-weight: bold; color: rgb(232, 52, 61); }
        .stButton>button { border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)


# --- 2. DATA LOAD ENGINE ---
@st.cache_data(ttl=1800)
def load_comprehensive_operations_data():
    np.random.seed(10)
    sample_size = 500
    
    mock_partners = ["Vendor A Logistics", "Vendor B UAE", "Speedy Delivery LLC", "Al Ain Fleet Pros", "Direct Delivery Corp"]
    mock_modules = ["Road Safety Compliance Deck", "Customer Experience Optimization", "App Performance & Flow"]
    mock_cities = ["Dubai", "Abu Dhabi", "Al Ain", "Sharjah", "Ajman", "RAK", "Fujairah"]
    mock_statuses = ["Attended", "Not Attended", "Rescheduled"]
    
    base_date = pd.Timestamp('2026-07-11')
    date_pool = [base_date - pd.Timedelta(days=int(d)) for d in np.random.randint(0, 45, size=sample_size)]
    
    df = pd.DataFrame({
        'Rider ID': np.random.randint(100000, 999999, size=sample_size),
        'Name': [f"Rider Asset {i}" for i in range(1, sample_size + 1)],
        'Contract Name': np.random.choice(mock_partners, size=sample_size),
        'City': np.random.choice(mock_cities, size=sample_size),
        'Module': np.random.choice(mock_modules, size=sample_size),
        'Timestamp': date_pool,
        'Status': np.random.choice(mock_statuses, size=sample_size, p=[0.72, 0.20, 0.08])
    })
    
    df['Rider ID'] = df['Rider ID'].astype(str)
    df['Planned Date'] = df['Timestamp'].dt.strftime('%d-%m-%Y')
    df['Contract Name'] = df['Contract Name'].fillna("Not Documented").astype(str)
    df['Week_Number'] = df['Timestamp'].dt.isocalendar().week
    df['Month_Name'] = df['Timestamp'].dt.strftime('%B %Y')
    
    df['Speed_Compliance_Score'] = np.random.randint(75, 100, size=sample_size)
    df['Order_Cancellation_Rate'] = np.random.uniform(0.5, 4.5, size=sample_size)
    df['Customer_Rating'] = np.random.uniform(4.2, 5.0, size=sample_size)
    
    return df

try:
    master_df = load_comprehensive_operations_data()
except Exception as e:
    st.error(f"Data Fetch Failure: {e}")
    st.stop()


# --- 3. SIDEBAR NAVIGATION CONTEXT ---
with st.sidebar:
    st.markdown("### 🍊 talabat Framework")
    st.markdown("## Navigation Hub")
    
    # 🚨 PURE STRINGS FOR SCRIPT NAVIGATION SAFETY 🚨
    app_view = st.radio(
        "Jump directly to operational node:",
        options=[
            "Overview Portal", 
            "Main Dashboard Grid", 
            "Performance Engine", 
            "Fleet Partner Leaderboard", 
            "T-Camp Hub", 
            "Reference Documentation"
        ]
    )
    
    st.divider()
    
    if st.button("🔄 Clear System Cache Engine", use_container_width=True):
        st.cache_data.clear()
        st.toast("Internal caching cleared...", icon="⚡")
        st.rerun()


# --- 4. RENDER ROUTER VIEWS ---

# VIEW 1: OVERVIEW
if app_view == "Overview Portal":
    st.title("Operations Overview Portal")
    st.caption("UAE Existing Rider Training • High-Level Performance Aggregations")
    st.divider()
    
    t_planned = len(master_df)
    t_trained = len(master_df[master_df['Status'] == 'Attended'])
    
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Total Riders Planned", f"{t_planned:,}")
    m_col2.metric("Total Riders Trained", f"{t_trained:,}")
    m_col3.metric("Global Attended Conversion Rate", f"{(t_trained/t_planned * 100):.1f}%")
    
    st.divider()
    st.markdown("### 🗓️ Core Time-Variant Tracking Analytics")
    time_tab_week, time_tab_month = st.tabs(["Weekly Ingestion Analytics", "Monthly Aggregations"])
    
    with time_tab_week:
        st.markdown("#### Weekly Training Logs Matrix")
        weekly_summary = master_df.groupby(['Week_Number', 'City']).agg(
            Planned=('Rider ID', 'count'),
            Trained=('Status', lambda x: (x == 'Attended').sum())
        ).reset_index()
        
        target_week = st.selectbox("Select Week Window View:", options=sorted(weekly_summary['Week_Number'].unique().tolist(), reverse=True))
        week_df = weekly_summary[weekly_summary['Week_Number'] == target_week]
        
        st.info(f"👉 **UAE Weekly Performance Summary:** In Week {target_week}, **{week_df['Planned'].sum()}** riders were planned and **{week_df['Trained'].sum()}** completed modules.")
        st.dataframe(week_df.groupby('City')[['Planned', 'Trained']].sum(), use_container_width=True)
        
    with time_tab_month:
        st.markdown("#### Monthly Macro Training Logs Matrix")
        monthly_summary = master_df.groupby(['Month_Name', 'City']).agg(
            Planned=('Rider ID', 'count'),
            Trained=('Status', lambda x: (x == 'Attended').sum())
        ).reset_index()
        
        target_month = st.selectbox("Select Month Window View:", options=sorted(monthly_summary['Month_Name'].unique().tolist()))
        month_df = monthly_summary[monthly_summary['Month_Name'] == target_month]
        
        st.info(f"👉 **UAE Monthly Performance Summary:** In {target_month}, **{month_df['Planned'].sum()}** riders were planned.")
        st.dataframe(month_df.groupby('City')[['Planned', 'Trained']].sum(), use_container_width=True)


# VIEW 2: MAIN DASHBOARD
elif app_view == "Main Dashboard Grid":
    st.title("Talabat Existing Rider Training Dashboard")
    st.caption("UAE Existing Rider Training")
    st.divider()
    
    st.markdown("### 🔍 Delivery Company Focus")
    available_fps = sorted(master_df['Contract Name'].unique().tolist())
    selected_fps = st.multiselect("Filter by Delivery Company (Fleet Partner):", options=available_fps, default=available_fps)
    
    dash_filtered_df = master_df[master_df['Contract Name'].isin(selected_fps)]
    
    d_total = len(dash_filtered_df)
    d_attended = len(dash_filtered_df[dash_filtered_df['Status'] == 'Attended'])
    d_no_show = len(dash_filtered_df[dash_filtered_df['Status'] == 'Not Attended'])
    d_rate = (d_attended / d_total * 100) if d_total > 0 else 0.0
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Scheduled Tasks", f"{d_total:,}")
    col_m2.metric("Attended Assets", f"{d_attended:,}")
    col_m3.metric("Logged No-Shows", f"{d_no_show:,}")
    col_m4.metric("Compliance Rate", f"{d_rate:.1f}%")
    
    st.divider()
    st.markdown("### 📋 Active Training Ledger Rows")
    search_query = st.text_input("⚡ Quick Search (Enter Rider ID or Name Keyphrase):", placeholder="Search records...").strip()
    
    if search_query:
        dash_filtered_df = dash_filtered_df[
            (dash_filtered_df['Rider ID'].str.contains(search_query, case=False)) |
            (dash_filtered_df['Name'].str.contains(search_query, case=False))
        ]
        
    if not dash_filtered_df.empty:
        st.dataframe(dash_filtered_df[['Rider ID', 'Name', 'Contract Name', 'City', 'Module', 'Planned Date', 'Status']], use_container_width=True, hide_index=True)
    else:
        st.info("No records locate matching filter thresholds.")


# VIEW 3: PERFORMANCE ENGINE
elif app_view == "Performance Engine":
    st.title("Rider Fleet Performance Engine")
    st.caption("Post-Training Operational Behavior Analytics")
    st.divider()
    
    perf_col1, perf_col2, perf_col3 = st.columns(3)
    perf_col1.metric("Avg Speed Compliance Score", f"{master_df['Speed_Compliance_Score'].mean():.1f}%")
    perf_col2.metric("Avg Order Cancellation Rate", f"{master_df['Order_Cancellation_Rate'].mean():.2f}%")
    perf_col3.metric("Avg Customer Service Rating", f"{master_df['Customer_Rating'].mean():.2f} ★")
    
    st.markdown("#### High-Risk Asset Review Ledger")
    high_risk_df = master_df[(master_df['Order_Cancellation_Rate'] > 3.5) | (master_df['Speed_Compliance_Score'] < 80)]
    st.dataframe(high_risk_df[['Rider ID', 'Name', 'Contract Name', 'City', 'Speed_Compliance_Score', 'Order_Cancellation_Rate', 'Customer_Rating']], use_container_width=True, hide_index=True)


# VIEW 4: FLEET PARTNER LEADERBOARD
elif app_view == "Fleet Partner Leaderboard":
    st.title("Fleet Partner Compliance & Rankings Ledger")
    st.caption("Vendor Ranking Framework & SLA Target Audits")
    st.divider()
    
    fp_metrics = master_df.groupby('Contract Name').agg(
        Total_Assigned=('Rider ID', 'count'),
        Attended_Count=('Status', lambda x: (x == 'Attended').sum()),
        Avg_Speed_Score=('Speed_Compliance_Score', 'mean'),
        Avg_Customer_Score=('Customer_Rating', 'mean')
    ).reset_index()
    
    fp_metrics['SLA_Attendance_Rate'] = (fp_metrics['Attended_Count'] / fp_metrics['Total_Assigned']) * 100
    fp_metrics = fp_metrics.sort_values(by='SLA_Attendance_Rate', ascending=False)
    
    st.dataframe(fp_metrics.style.format({'SLA_Attendance_Rate': '{:.1f}%', 'Avg_Speed_Score': '{:.1f}%', 'Avg_Customer_Score': '{:.2f} ★'}), use_container_width=True, hide_index=True)


# VIEW 5: T-CAMP HUB
elif app_view == "T-Camp Hub":
    st.title("T-Camp Operations Center")
    st.caption("Integrated Rider Onboarding & Accommodation Matrix Mapping")
    st.divider()
    st.warning("🚧 Coming Soon: System Node Pending Pipeline Configuration")


# VIEW 6: GLOSSARY / DOCUMENTATION
elif app_view == "Reference Documentation":
    st.title("Dashboard Reference Engine")
    st.caption("System Architecture Controls, Dynamic Glossary, & Version Control Logs")
    st.divider()
    
    tab_doc, tab_glossary = st.tabs(["📋 Architectural Documentation (v1.0)", "📚 Interactive Operations Glossary"])
    with tab_doc:
        st.markdown("""
        ### System Architecture Specification — Version 1.0
        * **Python Engine:** Ingests libraries and cleans up raw matrices natively.
        * **Streamlit Framework:** Provides an enterprise interface capable of full-screen PWA pinning on field mobile devices.
        * **Google Apps Script Engine:** Processes target daily records to trigger 6:00 PM partner escalation alerts.
        """)
    with tab_glossary:
        st.markdown("""
        * **Total Scheduled Tasks:** Raw count of assigned records.
        * **Compliance Core Rate:** `(Attended Assets / Total Scheduled Tasks) * 100`.
        * **High-Risk Asset Tracker:** Flags records with Cancellations > 3.5% or Safety Scores < 80%.
        """)


# --- 5. FOOTER CONTROL ---
st.markdown("""
    <div style="text-align: center; margin-top: 55px; padding: 15px; border-top: 1px solid #eeeeee;">
        <p style="font-size: 11px; color: #94a3b8; font-family: sans-serif; margin: 0;">
            Talabat Logistics Engine Framework • UAE Existing Rider Training Data Stream
        </p>
    </div>
""", unsafe_allow_html=True)
