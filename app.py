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

st.markdown("""
<style>
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

  .kpi-card {
    background: #ffffff;
    border: 1px solid #f0f0ee;
    border-radius: 12px;
    padding: 20px 22px 16px;
    position: relative;
    overflow: hidden;
  }
  .kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }
  .kpi-card.orange::before { background: #FF6B35; }
  .kpi-card.green::before  { background: #10b981; }
  .kpi-card.red::before    { background: #ef4444; }
  .kpi-card.blue::before   { background: #3b82f6; }
  .kpi-card.purple::before { background: #8b5cf6; }

  .kpi-label { font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 6px; }
  .kpi-value { font-size: 34px; font-weight: 700; color: #0f172a; line-height: 1; margin-bottom: 6px; }
  .kpi-sub   { font-size: 12px; color: #64748b; }
  .kpi-pos   { color: #10b981; font-weight: 600; }
  .kpi-neg   { color: #ef4444; font-weight: 600; }

  .city-row {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 0; border-bottom: 1px solid #f1f5f9;
  }
  .city-name { font-size: 14px; font-weight: 500; color: #1e293b; min-width: 90px; }
  .city-bar-wrap { flex: 1; background: #f1f5f9; border-radius: 999px; height: 8px; overflow: hidden; }
  .city-bar { height: 8px; border-radius: 999px; background: #FF6B35; }
  .city-pct  { font-size: 13px; font-weight: 600; color: #FF6B35; min-width: 44px; text-align: right; }
  .city-count { font-size: 12px; color: #94a3b8; min-width: 60px; text-align: right; }

  .status-pill {
    display: inline-block; font-size: 12px; font-weight: 600;
    padding: 3px 10px; border-radius: 999px;
  }
  .pill-attended   { background: #d1fae5; color: #065f46; }
  .pill-nshow      { background: #fee2e2; color: #991b1b; }
  .pill-rescheduled{ background: #fef3c7; color: #92400e; }

  .section-head { font-size: 13px; font-weight: 700; color: #94a3b8; letter-spacing: 0.08em; text-transform: uppercase; margin: 1.6rem 0 0.8rem; }

  [data-testid="stMetricValue"] { font-size: 28px !important; }
</style>
""", unsafe_allow_html=True)


# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800)
def load_data():
    np.random.seed(42)
    n = 600
    partners = ["Vendor A Logistics", "Vendor B UAE", "Speedy Delivery LLC", "Al Ain Fleet Pros", "Direct Delivery Corp"]
    modules  = ["Road Safety Compliance", "Customer Experience", "App Performance & Flow"]
    cities   = ["Dubai", "Abu Dhabi", "Al Ain", "Sharjah", "Ajman", "RAK", "Fujairah"]
    statuses = ["Attended", "Not Attended", "Rescheduled"]

    base = pd.Timestamp('2026-07-12')
    dates = [base - pd.Timedelta(days=int(d)) for d in np.random.randint(0, 90, size=n)]

    df = pd.DataFrame({
        'Rider ID':       np.random.randint(100000, 999999, size=n).astype(str),
        'Name':           [f"Rider {i:04d}" for i in range(1, n+1)],
        'Contract Name':  np.random.choice(partners, size=n),
        'City':           np.random.choice(cities, size=n),
        'Module':         np.random.choice(modules, size=n),
        'Timestamp':      pd.to_datetime(dates),
        'Status':         np.random.choice(statuses, size=n, p=[0.75, 0.18, 0.07]),
    })

    df['Planned Date']  = df['Timestamp'].dt.strftime('%d-%m-%Y')
    df['Contract Name'] = df['Contract Name'].fillna("Unknown").astype(str)

    # ── FIX: ISO-sortable keys so charts render chronologically ──────────────
    df['Date_Str']  = df['Timestamp'].dt.strftime('%Y-%m-%d')   # daily
    df['Week_Str']  = df['Timestamp'].dt.strftime('%Y-W%U')     # weekly  (was "Week %U (%Y)" → alpha-sorted wrong)
    df['Month_Str'] = df['Timestamp'].dt.strftime('%Y-%m')      # monthly (was "%B %Y" → alpha-sorted wrong = CRASH)
    df['Pure_Date'] = df['Timestamp'].dt.date

    df['Speed_Score']  = np.random.randint(75, 100, size=n).astype(float)
    df['Cancel_Rate']  = np.random.uniform(0.5, 4.5, size=n)
    df['Rating']       = np.random.uniform(4.2, 5.0, size=n)
    return df

try:
    master_df = load_data()
except Exception as e:
    st.error(f"Data load failed: {e}")
    st.stop()


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
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

    dr = st.date_input("Window", value=[min_d, max_d], min_value=min_d, max_value=max_d, label_visibility="collapsed")
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


# ── HELPERS ───────────────────────────────────────────────────────────────────
def kpi(col, label, value, sub="", color="orange"):
    with col:
        st.markdown(f"""
        <div class="kpi-card {color}">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

def status_pill(s):
    if s == "Attended":    return f'<span class="status-pill pill-attended">Attended</span>'
    if s == "Not Attended":return f'<span class="status-pill pill-nshow">No-show</span>'
    return f'<span class="status-pill pill-rescheduled">Rescheduled</span>'


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 1 — OVERVIEW  (the beautiful one)
# ══════════════════════════════════════════════════════════════════════════════
if "Overview" in view:
    st.markdown("## Operations Overview")
    st.caption("UAE Existing Rider Training · real-time compliance snapshot")

    total   = len(fdf)
    trained = (fdf['Status'] == 'Attended').sum()
    noshows = (fdf['Status'] == 'Not Attended').sum()
    resched = (fdf['Status'] == 'Rescheduled').sum()
    rate    = trained / total * 100 if total else 0
    cities_active = fdf['City'].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi(c1, "Scheduled",     f"{total:,}",          "total pipeline",          "orange")
    kpi(c2, "Trained",       f"{trained:,}",         "assets verified",         "green")
    kpi(c3, "No-shows",      f"{noshows:,}",         "action required",         "red")
    kpi(c4, "Compliance",    f"{rate:.1f}%",         "attendance rate",         "blue")
    kpi(c5, "Active cities", f"{cities_active}",     "hubs in window",          "purple")

    st.markdown('<div class="section-head">Trend</div>', unsafe_allow_html=True)
    tf = st.radio("Group by", ["Daily", "Weekly", "Monthly"], horizontal=True, key="ov_tf")
    ct = st.radio("Chart", ["Area", "Bar"], horizontal=True, key="ov_ct")

    key = {'Daily': 'Date_Str', 'Weekly': 'Week_Str', 'Monthly': 'Month_Str'}[tf]
    # Sort by key to guarantee chronological order (ISO keys sort correctly)
    trend = (fdf.groupby(key)
               .size()
               .reset_index(name='Riders Planned')
               .sort_values(key)          # ← explicit sort: fixes monthly crash
               .set_index(key))

    if ct == "Area":
        st.area_chart(trend, color="#FF6B35")
    else:
        st.bar_chart(trend, color="#FF6B35")

    st.markdown('<div class="section-head">Status breakdown</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])

    with col_a:
        status_counts = fdf['Status'].value_counts()
        st.bar_chart(status_counts, color="#FF6B35")

    with col_b:
        st.markdown('<div class="section-head">City snapshot</div>', unsafe_allow_html=True)
        city_df = (fdf.groupby('City')
                      .agg(Total=('Status','count'),
                           Attended=('Status', lambda x: (x=='Attended').sum()))
                      .reset_index())
        city_df['Rate'] = (city_df['Attended'] / city_df['Total'] * 100).round(1)
        city_df = city_df.sort_values('Total', ascending=False)
        max_total = city_df['Total'].max()

        rows = ""
        for _, r in city_df.iterrows():
            bar_w = r['Total'] / max_total * 100
            rows += f"""
            <div class="city-row">
              <span class="city-name">{r['City']}</span>
              <div class="city-bar-wrap"><div class="city-bar" style="width:{bar_w:.0f}%"></div></div>
              <span class="city-pct">{r['Rate']}%</span>
              <span class="city-count">{int(r['Total'])} riders</span>
            </div>"""
        st.markdown(rows, unsafe_allow_html=True)

    st.markdown('<div class="section-head">Module distribution</div>', unsafe_allow_html=True)
    module_df = fdf['Module'].value_counts().reset_index()
    module_df.columns = ['Module', 'Count']
    st.dataframe(module_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 2 — TRAINING LEDGER
# ══════════════════════════════════════════════════════════════════════════════
elif "Ledger" in view:
    st.markdown("## Training Ledger")
    st.caption("Full attendance records with search & fleet-partner filter")

    fps = sorted(fdf['Contract Name'].unique().tolist())
    sel_fps = st.multiselect("Fleet partner", options=fps, default=fps)
    ldf = fdf[fdf['Contract Name'].isin(sel_fps)]

    d_tot = len(ldf)
    d_att = (ldf['Status'] == 'Attended').sum()
    d_ns  = (ldf['Status'] == 'Not Attended').sum()
    d_rt  = d_att / d_tot * 100 if d_tot else 0

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Scheduled",  f"{d_tot:,}",   "", "orange")
    kpi(c2, "Attended",   f"{d_att:,}",   "", "green")
    kpi(c3, "No-shows",   f"{d_ns:,}",    "", "red")
    kpi(c4, "Compliance", f"{d_rt:.1f}%", "", "blue")

    st.markdown('<div class="section-head">Records</div>', unsafe_allow_html=True)
    q = st.text_input("Search rider ID or name", placeholder="e.g. 482391 or Rider 0042").strip()
    if q:
        ldf = ldf[ldf['Rider ID'].str.contains(q, case=False) | ldf['Name'].str.contains(q, case=False)]

    if ldf.empty:
        st.info("No records match current filters.")
    else:
        show = ldf[['Rider ID', 'Name', 'Contract Name', 'City', 'Module', 'Planned Date', 'Status']].copy()
        st.dataframe(show, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 3 — CITY ANALYTICS  (new)
# ══════════════════════════════════════════════════════════════════════════════
elif "City" in view:
    st.markdown("## City Analytics")
    st.caption("Hub-level compliance, attendance trends, and module breakdown by city")

    all_cities = sorted(fdf['City'].unique().tolist())
    sel_city   = st.selectbox("Select city to drill into", ["All cities"] + all_cities)

    cdf = fdf if sel_city == "All cities" else fdf[fdf['City'] == sel_city]

    c_total   = len(cdf)
    c_att     = (cdf['Status'] == 'Attended').sum()
    c_ns      = (cdf['Status'] == 'Not Attended').sum()
    c_rate    = c_att / c_total * 100 if c_total else 0

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Scheduled",  f"{c_total:,}",  "", "orange")
    kpi(c2, "Attended",   f"{c_att:,}",    "", "green")
    kpi(c3, "No-shows",   f"{c_ns:,}",     "", "red")
    kpi(c4, "Compliance", f"{c_rate:.1f}%","", "blue")

    st.markdown('<div class="section-head">City comparison</div>', unsafe_allow_html=True)
    city_summary = (fdf.groupby('City')
                       .agg(Total=('Status','count'),
                            Attended=('Status', lambda x: (x=='Attended').sum()),
                            No_shows=('Status', lambda x: (x=='Not Attended').sum()))
                       .reset_index())
    city_summary['Rate_%'] = (city_summary['Attended'] / city_summary['Total'] * 100).round(1)
    city_summary = city_summary.sort_values('Rate_%', ascending=False)

    max_t = city_summary['Total'].max()
    rows = ""
    for _, r in city_summary.iterrows():
        highlight = "font-weight:700;" if r['City'] == sel_city else ""
        bar_w = r['Total'] / max_t * 100
        rate_color = "#10b981" if r['Rate_%'] >= 75 else "#f59e0b" if r['Rate_%'] >= 65 else "#ef4444"
        rows += f"""
        <div class="city-row" style="{highlight}">
          <span class="city-name" style="{highlight}">{r['City']}</span>
          <div class="city-bar-wrap"><div class="city-bar" style="width:{bar_w:.0f}%;background:{rate_color}"></div></div>
          <span class="city-pct" style="color:{rate_color}">{r['Rate_%']}%</span>
          <span class="city-count">{int(r['Attended'])}/{int(r['Total'])}</span>
        </div>"""
    st.markdown(rows, unsafe_allow_html=True)

    st.markdown('<div class="section-head">Attendance trend for selected city</div>', unsafe_allow_html=True)
    tf2 = st.radio("Group by", ["Daily", "Weekly", "Monthly"], horizontal=True, key="city_tf")
    key2 = {'Daily': 'Date_Str', 'Weekly': 'Week_Str', 'Monthly': 'Month_Str'}[tf2]
    trend2 = (cdf.groupby(key2).size()
                 .reset_index(name='Riders Planned')
                 .sort_values(key2)
                 .set_index(key2))
    st.area_chart(trend2, color="#FF6B35")

    st.markdown('<div class="section-head">Module split by city</div>', unsafe_allow_html=True)
    mod_city = (fdf.groupby(['City', 'Module'])
                   .size()
                   .reset_index(name='Count')
                   .pivot(index='City', columns='Module', values='Count')
                   .fillna(0)
                   .astype(int))
    st.dataframe(mod_city, use_container_width=True)

    st.markdown('<div class="section-head">Rider records for this city</div>', unsafe_allow_html=True)
    st.dataframe(cdf[['Rider ID', 'Name', 'Contract Name', 'Module', 'Planned Date', 'Status']],
                 use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 4 — PERFORMANCE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
elif "Performance" in view:
    st.markdown("## Fleet Performance Engine")
    st.caption("Post-training operational behaviour analytics")

    c1, c2, c3 = st.columns(3)
    kpi(c1, "Avg speed compliance", f"{fdf['Speed_Score'].mean():.1f}%",  "", "green")
    kpi(c2, "Avg cancellation rate",f"{fdf['Cancel_Rate'].mean():.2f}%",  "", "red")
    kpi(c3, "Avg customer rating",  f"{fdf['Rating'].mean():.2f} ★",       "", "blue")

    st.markdown('<div class="section-head">High-risk riders</div>', unsafe_allow_html=True)
    hr = fdf[(fdf['Cancel_Rate'] > 3.5) | (fdf['Speed_Score'] < 80)]
    st.caption(f"{len(hr)} riders flagged")
    st.dataframe(hr[['Rider ID', 'Name', 'Contract Name', 'City', 'Speed_Score', 'Cancel_Rate', 'Rating']],
                 use_container_width=True, hide_index=True)

    st.markdown('<div class="section-head">Speed compliance by city</div>', unsafe_allow_html=True)
    speed_city = fdf.groupby('City')['Speed_Score'].mean().sort_values(ascending=False).reset_index()
    speed_city.columns = ['City', 'Avg Speed Score']
    st.bar_chart(speed_city.set_index('City'), color="#10b981")


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 5 — PARTNER RANKINGS
# ══════════════════════════════════════════════════════════════════════════════
elif "Partner" in view:
    st.markdown("## Fleet Partner Rankings")
    st.caption("SLA compliance and vendor performance leaderboard")

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
        fp.style.format({'SLA_%': '{:.1f}%', 'Avg_Speed': '{:.1f}%', 'Avg_Rating': '{:.2f} ★'}),
        use_container_width=True
    )

    st.markdown('<div class="section-head">SLA rate by partner</div>', unsafe_allow_html=True)
    st.bar_chart(fp.set_index('Contract Name')['SLA_%'], color="#FF6B35")


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 6 — T-CAMP
# ══════════════════════════════════════════════════════════════════════════════
elif "T-Camp" in view:
    st.markdown("## T-Camp Operations")
    st.warning("🚧 Coming soon — accommodation matrix mapping pending pipeline config")


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 7 — DOCS
# ══════════════════════════════════════════════════════════════════════════════
elif "Docs" in view:
    st.markdown("## Reference documentation")
    t1, t2 = st.tabs(["Architecture v1.0", "Glossary"])
    with t1:
        st.markdown("""
- **Python / pandas / numpy** — data ingestion and transformation
- **Streamlit ≥ 1.28** — UI framework, PWA-pinnable on mobile
- **Google Apps Script** — daily 6 PM partner compliance email trigger
- **Google Sheets** — live data source (replace mock data with `gspread` connector)
        """)
    with t2:
        st.markdown("""
| Term | Definition |
|---|---|
| Compliance rate | `(Attended / Total Scheduled) × 100` |
| High-risk rider | Cancel rate > 3.5% **or** Speed score < 80 |
| SLA rate | Same as compliance rate, scoped to a fleet partner |
        """)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:60px;padding:16px;border-top:1px solid #f1f5f9;">
  <p style="font-size:11px;color:#94a3b8;margin:0;">
    talabat Logistics · UAE Existing Rider Training · v2.0
  </p>
</div>
""", unsafe_allow_html=True)
