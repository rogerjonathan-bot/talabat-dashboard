import streamlit as st
import pandas as pd
import numpy as np
import datetime

# --- 1. SYSTEM INITIALIZATION & DASHBOARD KIT THEMING ---
st.set_page_config(
    page_title="Talabat Training Control Hub",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injecting clean Dashboard Kit styled container cards & styling overrides
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
        
        /* Dashboard Kit Custom Metric Cards Styling */
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            text-align: left;
        }
        .metric-label { font-size: 14px; color: #64748b; font-weight: 500; }
        .metric-value { font-size: 30px; font-weight: 700; color: #0f172a; margin: 4px 0; }
        .metric-delta { font-size: 13px; font-weight: 600; }
        .delta-positive { color: #10b981; }
        .delta-negative { color: #ef4444; }
    </style>
""", unsafe_allow_html=True)


# --- 2. DATA ACQUISITION & CHRONO-PROCESSING ENGINE ---
@st.cache_data(ttl=1800)
def load_comprehensive_operations_data():
    np.random.seed(42)
    sample_size = 600
    
    mock_partners = ["Vendor A Logistics", "Vendor B UAE", "Speedy Delivery LLC", "Al Ain Fleet Pros", "Direct Delivery Corp"]
    mock_modules = ["Road Safety Compliance Deck", "Customer Experience Optimization", "App Performance & Flow"]
    mock_cities = ["Dubai", "Abu Dhabi", "Al Ain", "Sharjah", "Ajman", "RAK", "Fujairah"]
    mock_statuses = ["Attended", "Not Attended", "Rescheduled"]
    
    # Generate continuous historical data points over the last 90 days
    base_date = pd.Timestamp('2026-07-12')
    date_pool = [base_date - pd.Timedelta(days=int(d)) for d in np.random.randint(0, 90, size=sample_size)]
    
    df = pd.DataFrame({
        'Rider ID': np.random.randint(100000, 999999, size=sample_size),
        'Name': [f"Rider Asset {i}" for i in range(1, sample_size + 1)],
        'Contract Name': np.random.choice(mock_partners, size=sample_size),
        'City': np.random.choice(mock_cities, size=sample_size),
        'Module': np.random.choice(mock_modules, size=sample_size),
        'Timestamp': pd.to_datetime(date_pool),
        'Status': np.random.choice(mock_statuses, size=sample_size, p=[0.75, 0.18, 0.07])
    })
    
    df['Rider ID'] = df['Rider ID'].astype(str)
    df['Planned Date'] = df['Timestamp'].dt.strftime('%d-%m-%Y')
    df['Contract Name'] = df['Contract Name'].fillna("Not Documented").astype(str)
    
    # Time intelligence variables for trend slicing
    df['Date'] = df['Timestamp'].dt.date
    df['Week'] = df['Timestamp'].dt.to_period('W').dt.start_time
    df['Month'] = df['Timestamp'].dt.to_period('M').dt.start_time
    
    # Behavior data maps
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
    
    # Interactive Date Range Picker Component from Dashboard Kit Reference
    st.markdown("### 📅 Global Time Boundary Filter")
    min_date = master_df['Date'].min()
    max_date = master_df['Date'].max()
    
    selected_date_range = st.date_input(
        "Select Target Window:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply time constraints safely
    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        time_filtered_df = master_df[(master_df['Date'] >= start_date) & (master_df['Date'] <= end_date)]
    else:
        time_filtered_df = master_df

    st.divider()
    if st.button("🔄 Clear System Cache Engine", use_container_width=True):
        st.cache_data.clear()
        st.toast("Internal caching cleared...", icon="⚡")
        st.rerun()


# --- 4. RENDER ROUTER VIEWS ---

# VIEW 1: OVERVIEW PORTAL (WITH DASHBOARD KIT TIME SLICING)
if app_view == "Overview Portal":
    st.title("Operations Overview Portal")
    st.caption("UAE Existing Rider Training • Time-Variant Analytics Summary")
    st.divider()
    
    # Calculate performance metrics
    total_planned = len(time_filtered_df)
    total_trained = len(time_filtered_df[time_filtered_df['Status'] == 'Attended'])
    total_no_shows = len(time_filtered_df[time_filtered_df['Status'] == 'Not Attended'])
    conv_rate = (total_trained / total_planned * 100) if total_planned > 0 else 0.0
    
    # Custom HTML Layout using Dashboard Kit's aesthetic design styles
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Scheduled</div><div class="metric-value">{total_planned:,}</div><div class="metric-delta delta-positive">▲ Base Pipeline</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Trained</div><div class="metric-value">{total_trained:,}</div><div class="metric-delta delta-positive">▲ Assets Verified</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Logged No-Shows</div><div class="metric-value">{total_no_shows:,}</div><div class="metric-delta delta-negative">▼ Action Required</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Conversion Rate</div><div class="metric-value">{conv_rate:.1f}%</div><div class="metric-delta delta-positive">📊 Target Alignment</div></div>', unsafe_allow_html=True)
        
    st.divider()
    
    # Time frame chart selector controls (Daily, Weekly, Monthly)
    st.markdown("### 📉 Operational Chrono-Trends")
    time_frame = st.radio("Group Trend Visualizations By:", ["Daily Logs", "Weekly Logs", "Monthly Logs"], horizontal=True)
    chart_type = st.selectbox("Select Visual Display Style:", ["Area Chart View", "Bar Chart View"])
    
    # Dynamically resample dates based on selection
    if time_frame == "Daily Logs":
        trend_data = time_filtered_df.groupby('Date').size().reset_index(name='Riders Planned')
        trend_data = trend_data.set_index('Date')
    elif time_frame == "Weekly Logs":
        trend_data = time_filtered_df.groupby('Week').size().reset_index(name='Riders Planned')
        trend_data = trend_data.set_index('Week')
    else:
        trend_data = time_filtered_df.groupby('Month').size().reset_index(name='Riders Planned')
        trend_data = trend_data.set_index('Month')
        
    if chart_type == "Area Chart View":
        st.area_chart(trend_data, color="#e8343d")
    else:
        st.bar_chart(trend_data, color="#475569")
        
    st.markdown("#### Hub Breakdown Summary")
    st.dataframe(time_filtered_df.groupby('City')[['Rider ID']].count().rename(columns={'Rider ID': 'Riders Planned'}), use_container_width=True)


# VIEW 2: MAIN DASHBOARD GRID
elif app_view == "Main Dashboard Grid":
    st.title("Talabat Existing Rider Training Dashboard")
    st.caption("UAE Existing Rider Training")
    st.divider()
    
    st.markdown("### 🔍 Delivery Company Focus")
    available_fps = sorted(time_filtered_df['Contract Name'].unique().tolist())
    selected_fps = st.multiselect("Filter by Delivery Company (Fleet Partner):", options=available_fps, default=available_fps)
    
    dash_filtered_df = time_filtered_df[time_filtered_df['Contract Name'].isin(selected_fps)]
    
    d_total = len(dash_filtered_df)
    d_attended = len(dash_filtered_df[dash_filtered_df['Status'] == 'Attended'])
    d_no_show = len(dash_filtered_df[dash_filtered_df['Status'] == 'Not Attended'])
    d_rate = (d_attended / d_total * 100) if d_total > 0 else 0.0
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Scheduled Tasks</div><div class="metric-value">{d_total:,}</div></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Attended Assets</div><div class="metric-value">{d_attended:,}</div></div>', unsafe_allow_html=True)
    with col_m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Logged No-Shows</div><div class="metric-value">{d_no_show:,}</div></div>', unsafe_allow_html=True)
    with col_m4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Compliance Rate</div><div class="metric-value">{d_rate:.1f}%</div></div>', unsafe_allow_html=True)
    
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
    with perf_col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Avg Speed Compliance</div><div class="metric-value">{time_filtered_df["Speed_Compliance_Score"].mean():.1f}%</div></div>', unsafe_allow_html=True)
    with perf_col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Avg Cancellation Rate</div><div class="metric-value">{time_filtered_df["Order_Cancellation_Rate"].mean():.2f}%</div></div>', unsafe_allow_html=True)
    with perf_col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Avg Customer Rating</div><div class="metric-value">{time_filtered_df["Customer_Rating"].mean():.2f} ★</div></div>', unsafe_allow_html=True)
    
    st.markdown("#### High-Risk Asset Review Ledger")
    high_risk_df = time_filtered_df[(time_filtered_df['Order_Cancellation_Rate'] > 3.5) | (time_filtered_df['Speed_Compliance_Score'] < 80)]
    st.dataframe(high_risk_df[['Rider ID', 'Name', 'Contract Name', 'City', 'Speed_Compliance_Score', 'Order_Cancellation_Rate', 'Customer_Rating']], use_container_width=True, hide_index=True)


# VIEW 4: FLEET PARTNER LEADERBOARD
elif app_view == "Fleet Partner Leaderboard":
    st.title("Fleet Partner Compliance & Rankings Ledger")
    st.caption("Vendor Ranking Framework & SLA Target Audits")
    st.divider()
    
    fp_metrics = time_filtered_df.groupby('Contract Name').agg(
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


# VIEW 6: REFERENCE DOCUMENTATION & GLOSSARY
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
