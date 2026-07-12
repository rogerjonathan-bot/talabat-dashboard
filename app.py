import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(
    page_title="Talabat Training Hub",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep CSS override - targets real Streamlit DOM nodes
st.markdown("""
<style>
/* ---- PAGE CHROME ---- */
.stApp { background: #F7F7F5; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1200px; }

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #1A1A18 !important;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #C8C8C0 !important; }
[data-testid="stSidebar"] .stRadio label { 
    padding: 6px 10px; border-radius: 6px; display: block;
    transition: background 0.15s;
}
[data-testid="stSidebar"] .stRadio label:hover { background: #2A2A28; }
[data-testid="stSidebar"] hr { border-color: #2A2A28 !important; }
[data-testid="stSidebar"] .stButton button {
    background: #2A2A28 !important; border: 1px solid #3A3A38 !important;
    color: #C8C8C0 !important; border-radius: 8px;
}
[data-testid="stSidebar"] .stButton button:hover { background: #3A3A38 !important; }
[data-testid="stSidebar"] .stDateInput input {
    background: #2A2A28 !important; border: 1px solid #3A3A38 !important;
    color: #C8C8C0 !important;
}

/* ---- RADIO & SELECT BUTTONS ---- */
.stRadio [data-testid="stWidgetLabel"] { 
    font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: 0.08em !important; color: #9CA3AF !important;
    text-transform: uppercase;
}
div[role="radiogroup"] label {
    border: 1px solid #E5E7EB !important; border-radius: 8px !important;
    padding: 4px 14px !important; margin-right: 6px;
    font-size: 13px !important; font-weight: 500 !important;
    background: white !important; cursor: pointer;
    transition: all 0.15s;
}
div[role="radiogroup"] label:has(input:checked) {
    background: #FF6B35 !important; border-color: #FF6B35 !important;
    color: white !important;
}

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
    overflow: hidden;
    background: white;
}

/* ---- TABS ---- */
.stTabs [data-baseweb="tab-list"] {
    background: transparent; gap: 4px;
    border-bottom: 2px solid #E5E7EB;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border: none;
    font-size: 13px; font-weight: 600;
    color: #9CA3AF; padding: 8px 16px;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: #FF6B35 !important;
    border-bottom-color: #FF6B35 !important;
}

/* ---- TEXT INPUTS ---- */
.stTextInput input {
    border: 1px solid #E5E7EB !important; border-radius: 8px !important;
    font-size: 13px !important; background: white !important;
}
.stTextInput input:focus { border-color: #FF6B35 !important; box-shadow: 0 0 0 3px rgba(255,107,53,0.1) !important; }

/* ---- MULTISELECT ---- */
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background: #FFF0EB !important; color: #C94C1A !important;
    border: 1px solid #FED0BB !important;
}

/* ---- SELECTBOX ---- */
[data-testid="stSelectbox"] [data-baseweb="select"] {
    border: 1px solid #E5E7EB !important; border-radius: 8px !important;
    background: white !important;
}

/* ---- CHART - change vega-lite default orange ---- */
[data-testid="stArrowVegaLiteChart"] canvas { border-radius: 8px; }

/* ---- AREA/BAR CHART COLOR OVERRIDE via Vega ---- */
.vega-embed { border-radius: 8px; }

/* ---- TOAST ---- */
[data-testid="stToast"] { border-left: 3px solid #FF6B35; }

/* ---- SECTION HEADER helper ---- */
.sh {
    font-size: 11px; font-weight: 700; color: #9CA3AF;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin: 1.6rem 0 0.75rem; padding-bottom: 6px;
    border-bottom: 1px solid #E5E7EB;
}

/* ---- KPI CARD ---- */
.kpi {
    background: white; border-radius: 12px;
    border: 1px solid #E5E7EB;
    padding: 18px 20px 14px;
    position: relative; overflow: hidden;
}
.kpi::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
}
.kpi.o::before { background: #FF6B35; }
.kpi.g::before { background: #10B981; }
.kpi.r::before { background: #EF4444; }
.kpi.b::before { background: #3B82F6; }
.kpi.p::before { background: #8B5CF6; }
.kpi-l { font-size: 10px; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase; color: #9CA3AF; margin-bottom: 4px; }
.kpi-v { font-size: 32px; font-weight: 800; color: #0F172A; line-height: 1; margin-bottom: 4px; }
.kpi-s { font-size: 11px; color: #CBD5E1; }

/* ---- CITY BAR ---- */
.city-table { width: 100%; border-collapse: collapse; }
.city-table tr { border-bottom: 1px solid #F1F5F9; }
.city-table tr:last-child { border-bottom: none; }
.city-table td { padding: 9px 4px; vertical-align: middle; }
.c-name { font-size: 13px; font-weight: 500; color: #1E293B; width: 90px; }
.c-bar-wrap { background: #F1F5F9; border-radius: 999px; height: 7px; overflow: hidden; }
.c-bar { height: 7px; border-radius: 999px; }
.c-pct { font-size: 12px; font-weight: 700; text-align: right; width: 46px; }
.c-ct { font-size: 11px; color: #94A3B8; text-align: right; width: 64px; }

/* ---- STATUS BADGE ---- */
.badge { display: inline-block; font-size: 11px; font-weight: 600; padding: 2px 9px; border-radius: 999px; }
.b-att { background: #D1FAE5; color: #065F46; }
.b-ns  { background: #FEE2E2; color: #991B1B; }
.b-rs  { background: #FEF3C7; color: #92400E; }

/* ---- PROGRESS BAR (status) ---- */
.stat-bar-row { margin-bottom: 12px; }
.stat-bar-label { display: flex; justify-content: space-between; font-size: 12px; color: #64748B; margin-bottom: 4px; }
.stat-bar-label span:last-child { font-weight: 600; color: #1E293B; }
.stat-bar-bg { background: #F1F5F9; border-radius: 999px; height: 8px; overflow: hidden; }
.stat-bar-fill { height: 8px; border-radius: 999px; }

/* Hide default streamlit radio dot */
div[role="radiogroup"] input[type="radio"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ---- DATA ---------------------------------------------------------------
@st.cache_data(ttl=1800)
def load_data():
    np.random.seed(42)
    n = 600
    partners = ["Vendor A Logistics", "Vendor B UAE", "Speedy Delivery LLC",
                "Al Ain Fleet Pros", "Direct Delivery Corp"]
    modules  = ["Road Safety Compliance", "Customer Experience", "App Performance & Flow"]
    cities   = ["Dubai", "Abu Dhabi", "Al Ain", "Sharjah", "Ajman", "RAK", "Fujairah"]
    statuses = ["Attended", "Not Attended", "Rescheduled"]
    base = pd.Timestamp('2026-07-12')
    dates = [base - pd.Timedelta(days=int(d)) for d in np.random.randint(0, 90, size=n)]
    df = pd.DataFrame({
        'Rider ID':      np.random.randint(100000, 999999, size=n).astype(str),
        'Name':          [f"Rider {i:04d}" for i in range(1, n+1)],
        'Contract Name': np.random.choice(partners, size=n),
        'City':          np.random.choice(cities, size=n),
        'Module':        np.random.choice(modules, size=n),
        'Timestamp':     pd.to_datetime(dates),
        'Status':        np.random.choice(statuses, size=n, p=[0.75, 0.18, 0.07]),
    })
    df['Planned Date']  = df['Timestamp'].dt.strftime('%d-%m-%Y')
    df['Contract Name'] = df['Contract Name'].fillna("Unknown").astype(str)
    df['Date_Str']      = df['Timestamp'].dt.strftime('%Y-%m-%d')
    df['Week_Str']      = df['Timestamp'].dt.strftime('%Y-W%U')
    df['Month_Str']     = df['Timestamp'].dt.strftime('%Y-%m')
    df['Pure_Date']     = df['Timestamp'].dt.date
    df['Speed_Score']   = np.random.randint(75, 100, size=n).astype(float)
    df['Cancel_Rate']   = np.random.uniform(0.5, 4.5, size=n)
    df['Rating']        = np.random.uniform(4.2, 5.0, size=n)
    return df

try:
    master_df = load_data()
except Exception as e:
    st.error(f"Data load failed: {e}")
    st.stop()


# ---- SIDEBAR ------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🍊 talabat")
    st.markdown("#### Training Control Hub")
    st.caption("UAE Fleet Operations")
    st.divider()

    view = st.radio("View", [
        "📊  Overview",
        "📋  Training Ledger",
        "🏙️  City Analytics",
        "⚡  Performance",
        "🏆  Partner Rankings",
        "🏕️  T-Camp",
        "📖  Docs",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("**Date range**")
    raw_min = master_df['Pure_Date'].min()
    raw_max = master_df['Pure_Date'].max()
    min_d = datetime.date(raw_min.year, raw_min.month, raw_min.day)
    max_d = datetime.date(raw_max.year, raw_max.month, raw_max.day)

    dr = st.date_input("Window", value=[min_d, max_d],
                       min_value=min_d, max_value=max_d,
                       label_visibility="collapsed")
    if isinstance(dr, (list, tuple)) and len(dr) == 2:
        s, e = dr
        fdf = master_df[(master_df['Pure_Date'] >= s) & (master_df['Pure_Date'] <= e)]
    else:
        fdf = master_df

    st.divider()
    st.caption(f"{len(fdf):,} records in window")
    if st.button("🔄 Refresh cache", use_container_width=True):
        st.cache_data.clear()
        st.toast("Cache cleared", icon="⚡")
        st.rerun()


# ---- HELPERS ------------------------------------------------------------
def kpi_row(metrics):
    """
    metrics = list of (label, value, sub, color_class)
    color_class: o=orange, g=green, r=red, b=blue, p=purple
    """
    cols = st.columns(len(metrics))
    for col, (label, value, sub, cls) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="kpi {cls}">
                <div class="kpi-l">{label}</div>
                <div class="kpi-v">{value}</div>
                <div class="kpi-s">{sub}</div>
            </div>""", unsafe_allow_html=True)

def city_bars(df_in, highlight=None):
    city_df = (df_in.groupby('City')
               .agg(Total=('Status','count'),
                    Attended=('Status', lambda x: (x=='Attended').sum()))
               .reset_index())
    city_df['Rate'] = (city_df['Attended'] / city_df['Total'] * 100).round(1)
    city_df = city_df.sort_values('Rate', ascending=False)
    max_t = city_df['Total'].max()

    rows = ""
    for _, r in city_df.iterrows():
        bar_w = round(r['Total'] / max_t * 100)
        clr = "#10B981" if r['Rate'] >= 75 else "#F59E0B" if r['Rate'] >= 65 else "#EF4444"
        bold = "font-weight:700;" if r['City'] == highlight else ""
        rows += f"""
        <tr>
          <td class="c-name" style="{bold}">{r['City']}</td>
          <td style="width:100%">
            <div class="c-bar-wrap">
              <div class="c-bar" style="width:{bar_w}%;background:{clr}"></div>
            </div>
          </td>
          <td class="c-pct" style="color:{clr}">{r['Rate']}%</td>
          <td class="c-ct">{int(r['Attended'])}/{int(r['Total'])}</td>
        </tr>"""
    st.markdown(f'<table class="city-table">{rows}</table>', unsafe_allow_html=True)

def section(label):
    st.markdown(f'<div class="sh">{label}</div>', unsafe_allow_html=True)

def trend_chart(df_in, key, label="Riders"):
    data = (df_in.groupby(key).size()
            .reset_index(name=label)
            .sort_values(key)
            .set_index(key))
    return data


# =========================================================================
# VIEW 1: OVERVIEW
# =========================================================================
if "Overview" in view:
    st.markdown("## Operations Overview")
    st.caption("UAE Existing Rider Training · real-time compliance snapshot")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    total   = len(fdf)
    trained = int((fdf['Status'] == 'Attended').sum())
    noshows = int((fdf['Status'] == 'Not Attended').sum())
    resched = int((fdf['Status'] == 'Rescheduled').sum())
    rate    = trained / total * 100 if total else 0

    kpi_row([
        ("Scheduled",     f"{total:,}",        "total pipeline",   "o"),
        ("Trained",       f"{trained:,}",       "assets verified",  "g"),
        ("No-shows",      f"{noshows:,}",       "action required",  "r"),
        ("Compliance",    f"{rate:.1f}%",        "attendance rate",  "b"),
        ("Active cities", f"{fdf['City'].nunique()}", "hubs in window", "p"),
    ])

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ---- Trend chart
    section("Attendance trend")
    tf = st.radio("Group by", ["Daily", "Weekly", "Monthly"], horizontal=True, key="ov_tf")
    ct = st.radio("Chart style", ["Area", "Bar"], horizontal=True, key="ov_ct")
    key_map = {'Daily': 'Date_Str', 'Weekly': 'Week_Str', 'Monthly': 'Month_Str'}
    trend_data = trend_chart(fdf, key_map[tf])
    if ct == "Area":
        st.area_chart(trend_data, color="#FF6B35", height=260)
    else:
        st.bar_chart(trend_data, color="#FF6B35", height=260)

    # ---- Two panels side by side
    section("City compliance & status breakdown")
    left, right = st.columns([1, 1])

    with left:
        st.markdown("**Compliance by city**")
        city_bars(fdf)

    with right:
        st.markdown("**Status breakdown**")
        max_s = max(trained, noshows, resched)
        for label, val, clr in [
            ("Attended",    trained, "#10B981"),
            ("No-show",     noshows, "#EF4444"),
            ("Rescheduled", resched, "#F59E0B"),
        ]:
            bar_w = round(val / max_s * 100) if max_s else 0
            st.markdown(f"""
            <div class="stat-bar-row">
                <div class="stat-bar-label"><span>{label}</span><span>{val:,}</span></div>
                <div class="stat-bar-bg">
                    <div class="stat-bar-fill" style="width:{bar_w}%;background:{clr}"></div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("**Module distribution**")
        mod_counts = fdf['Module'].value_counts()
        max_m = mod_counts.max()
        for mod, cnt in mod_counts.items():
            bar_w = round(cnt / max_m * 100)
            short = mod.replace("Compliance","").replace("Performance","Perf").strip()
            st.markdown(f"""
            <div class="stat-bar-row">
                <div class="stat-bar-label"><span>{short}</span><span>{cnt:,}</span></div>
                <div class="stat-bar-bg">
                    <div class="stat-bar-fill" style="width:{bar_w}%;background:#FF6B35"></div>
                </div>
            </div>""", unsafe_allow_html=True)


# =========================================================================
# VIEW 2: TRAINING LEDGER
# =========================================================================
elif "Ledger" in view:
    st.markdown("## Training Ledger")
    st.caption("Full attendance records with search and fleet-partner filter")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    fps = sorted(fdf['Contract Name'].unique().tolist())
    sel_fps = st.multiselect("Fleet partner", options=fps, default=fps)
    ldf = fdf[fdf['Contract Name'].isin(sel_fps)] if sel_fps else fdf

    d_tot = len(ldf)
    d_att = int((ldf['Status'] == 'Attended').sum())
    d_ns  = int((ldf['Status'] == 'Not Attended').sum())
    d_rt  = d_att / d_tot * 100 if d_tot else 0

    kpi_row([
        ("Scheduled",  f"{d_tot:,}",  "in selection", "o"),
        ("Attended",   f"{d_att:,}",  "",             "g"),
        ("No-shows",   f"{d_ns:,}",   "",             "r"),
        ("Compliance", f"{d_rt:.1f}%","",             "b"),
    ])

    section("Records")
    q = st.text_input("Search rider ID or name", placeholder="e.g. 482391 or Rider 0042").strip()
    if q:
        ldf = ldf[ldf['Rider ID'].str.contains(q, case=False) |
                  ldf['Name'].str.contains(q, case=False)]

    if ldf.empty:
        st.info("No records match current filters.")
    else:
        show = ldf[['Rider ID', 'Name', 'Contract Name', 'City',
                    'Module', 'Planned Date', 'Status']].copy()
        st.dataframe(show, use_container_width=True, hide_index=True)


# =========================================================================
# VIEW 3: CITY ANALYTICS
# =========================================================================
elif "City" in view:
    st.markdown("## City Analytics")
    st.caption("Hub-level compliance, trends, and module breakdown")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    all_cities = sorted(fdf['City'].unique().tolist())
    sel_city   = st.selectbox("Drill into city", ["All cities"] + all_cities)
    cdf = fdf if sel_city == "All cities" else fdf[fdf['City'] == sel_city]

    c_total = len(cdf)
    c_att   = int((cdf['Status'] == 'Attended').sum())
    c_ns    = int((cdf['Status'] == 'Not Attended').sum())
    c_rate  = c_att / c_total * 100 if c_total else 0

    kpi_row([
        ("Scheduled",  f"{c_total:,}", "", "o"),
        ("Attended",   f"{c_att:,}",   "", "g"),
        ("No-shows",   f"{c_ns:,}",    "", "r"),
        ("Compliance", f"{c_rate:.1f}%","","b"),
    ])

    section("City comparison")
    city_bars(fdf, highlight=sel_city if sel_city != "All cities" else None)

    section("Attendance trend")
    tf2 = st.radio("Group by", ["Daily", "Weekly", "Monthly"], horizontal=True, key="c_tf")
    key2 = {'Daily': 'Date_Str', 'Weekly': 'Week_Str', 'Monthly': 'Month_Str'}[tf2]
    st.area_chart(trend_chart(cdf, key2), color="#FF6B35", height=220)

    section("Module split by city")
    mod_city = (fdf.groupby(['City', 'Module']).size()
                   .reset_index(name='Count')
                   .pivot(index='City', columns='Module', values='Count')
                   .fillna(0).astype(int))
    st.dataframe(mod_city, use_container_width=True)

    section("Rider records")
    st.dataframe(
        cdf[['Rider ID', 'Name', 'Contract Name', 'Module', 'Planned Date', 'Status']],
        use_container_width=True, hide_index=True
    )


# =========================================================================
# VIEW 4: PERFORMANCE
# =========================================================================
elif "Performance" in view:
    st.markdown("## Fleet Performance Engine")
    st.caption("Post-training operational behaviour analytics")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    kpi_row([
        ("Avg speed compliance", f"{fdf['Speed_Score'].mean():.1f}%",  "fleet average", "g"),
        ("Avg cancel rate",      f"{fdf['Cancel_Rate'].mean():.2f}%",  "fleet average", "r"),
        ("Avg customer rating",  f"{fdf['Rating'].mean():.2f} ★",       "fleet average", "b"),
    ])

    section("High-risk riders")
    hr = fdf[(fdf['Cancel_Rate'] > 3.5) | (fdf['Speed_Score'] < 80)]
    st.caption(f"{len(hr)} riders flagged across fleet")
    st.dataframe(
        hr[['Rider ID', 'Name', 'Contract Name', 'City',
            'Speed_Score', 'Cancel_Rate', 'Rating']],
        use_container_width=True, hide_index=True
    )

    section("Speed compliance by city")
    speed_city = (fdf.groupby('City')['Speed_Score']
                     .mean().sort_values(ascending=False)
                     .reset_index()
                     .set_index('City'))
    speed_city.columns = ['Avg Speed Score']
    st.bar_chart(speed_city, color="#10B981", height=220)


# =========================================================================
# VIEW 5: PARTNER RANKINGS
# =========================================================================
elif "Partner" in view:
    st.markdown("## Fleet Partner Rankings")
    st.caption("SLA compliance and vendor performance leaderboard")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    fp = (fdf.groupby('Contract Name')
             .agg(Total=('Rider ID','count'),
                  Attended=('Status', lambda x: (x=='Attended').sum()),
                  Avg_Speed=('Speed_Score','mean'),
                  Avg_Rating=('Rating','mean'))
             .reset_index())
    fp['SLA_%'] = (fp['Attended'] / fp['Total'] * 100).round(1)
    fp = fp.sort_values('SLA_%', ascending=False).reset_index(drop=True)
    fp.index += 1

    st.dataframe(
        fp.style.format({'SLA_%': '{:.1f}%', 'Avg_Speed': '{:.1f}', 'Avg_Rating': '{:.2f}'}),
        use_container_width=True
    )

    section("SLA rate by partner")
    st.bar_chart(fp.set_index('Contract Name')['SLA_%'], color="#FF6B35", height=220)


# =========================================================================
# VIEW 6: T-CAMP
# =========================================================================
elif "T-Camp" in view:
    st.markdown("## T-Camp Operations")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.warning("Coming soon - accommodation matrix mapping pending pipeline config")


# =========================================================================
# VIEW 7: DOCS
# =========================================================================
elif "Docs" in view:
    st.markdown("## Reference documentation")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Architecture v1.0", "Glossary"])
    with t1:
        st.markdown("""
- **Python / pandas / numpy** - data ingestion and transformation
- **Streamlit >= 1.28** - UI framework, PWA-pinnable on mobile home screen
- **Google Apps Script** - daily 6 PM partner compliance email trigger
- **Google Sheets** - live data source (replace mock data with gspread connector)
        """)
    with t2:
        st.markdown("""
| Term | Definition |
|---|---|
| Compliance rate | `(Attended / Total Scheduled) x 100` |
| High-risk rider | Cancel rate > 3.5% or Speed score < 80 |
| SLA rate | Compliance rate scoped to a fleet partner |
        """)


# ---- FOOTER -------------------------------------------------------------
st.markdown("""
<div style="text-align:center;margin-top:60px;padding:16px;border-top:1px solid #E5E7EB;">
    <p style="font-size:11px;color:#94A3B8;margin:0;">
        talabat Logistics · UAE Existing Rider Training · v2.1
    </p>
</div>
""", unsafe_allow_html=True)
