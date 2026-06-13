"""
app.py
------
Bluestock Fintech — Mutual Fund Analytics Platform
Premium Streamlit Dashboard | Capstone Project | June 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Bluestock Fintech — MF Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# PREMIUM CSS — Glow, Animations, Glass UI
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #050d1a;
    color: #e8edf5;
}

.stApp {
    background: linear-gradient(135deg, #050d1a 0%, #0a1628 40%, #0d1f3c 100%);
    min-height: 100vh;
}

/* ── ANIMATED BACKGROUND PARTICLES ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(0,120,255,0.07) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(0,200,150,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, rgba(120,0,255,0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
    animation: bgPulse 8s ease-in-out infinite alternate;
}

@keyframes bgPulse {
    0%   { opacity: 0.6; }
    100% { opacity: 1.0; }
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071020 0%, #0a1830 100%) !important;
    border-right: 1px solid rgba(0,120,255,0.2);
    box-shadow: 4px 0 30px rgba(0,100,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #c8d8f0 !important;
}

/* ── SIDEBAR RADIO BUTTONS ── */
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 4px 0;
    cursor: pointer;
    transition: all 0.3s ease;
    display: block;
    font-size: 0.92rem;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(0,120,255,0.15);
    border-color: rgba(0,150,255,0.4);
    box-shadow: 0 0 12px rgba(0,120,255,0.2);
    transform: translateX(4px);
}

/* ── METRIC CARDS — Glass + Glow ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.06) 0%,
        rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(0,150,255,0.25);
    border-radius: 16px;
    padding: 20px 24px;
    backdrop-filter: blur(12px);
    box-shadow:
        0 0 20px rgba(0,120,255,0.08),
        inset 0 1px 0 rgba(255,255,255,0.08);
    transition: all 0.4s ease;
    animation: fadeSlideUp 0.6s ease both;
}

[data-testid="metric-container"]:hover {
    border-color: rgba(0,180,255,0.5);
    box-shadow:
        0 0 30px rgba(0,150,255,0.2),
        0 0 60px rgba(0,120,255,0.08),
        inset 0 1px 0 rgba(255,255,255,0.12);
    transform: translateY(-3px);
}

[data-testid="metric-container"] label {
    color: #7aa0c8 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 20px rgba(100,180,255,0.4);
}

[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #00e5a0 !important;
    font-size: 0.82rem !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,120,255,0.2);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0,100,255,0.06);
}

/* ── SELECTBOX & INPUTS ── */
[data-testid="stSelectbox"] > div,
[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,120,255,0.25) !important;
    border-radius: 10px !important;
    color: #e0eaf8 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #0066ff, #0044cc) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 0 20px rgba(0,100,255,0.35), 0 4px 15px rgba(0,0,0,0.3) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0080ff, #0055ee) !important;
    box-shadow: 0 0 35px rgba(0,120,255,0.55), 0 6px 20px rgba(0,0,0,0.3) !important;
    transform: translateY(-2px) !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] .stSlider {
    accent-color: #0066ff;
}

/* ── PAGE TITLE ── */
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2.2rem !important;
    background: linear-gradient(135deg, #ffffff 0%, #7ab8ff 50%, #00e5a0 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -0.02em !important;
    line-height: 1.2 !important;
}

h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #c8d8f0 !important;
    font-weight: 600 !important;
}

/* ── DIVIDER ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(0,120,255,0.15) !important;
    margin: 1.5rem 0 !important;
}

/* ── GLASS CARD ── */
.glass-card {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.06) 0%,
        rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(0,150,255,0.2);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(10px);
    box-shadow:
        0 0 25px rgba(0,100,255,0.07),
        inset 0 1px 0 rgba(255,255,255,0.07);
    margin-bottom: 20px;
    animation: fadeSlideUp 0.5s ease both;
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(0,180,255,0.35);
    box-shadow: 0 0 40px rgba(0,130,255,0.15),
                inset 0 1px 0 rgba(255,255,255,0.1);
    transform: translateY(-2px);
}

/* ── GLOW BADGE ── */
.glow-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,100,255,0.2), rgba(0,200,150,0.15));
    border: 1px solid rgba(0,150,255,0.35);
    border-radius: 30px;
    padding: 5px 16px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #7ab8ff;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    box-shadow: 0 0 12px rgba(0,120,255,0.2);
    margin-bottom: 12px;
}

/* ── RANK CARD ── */
.rank-card {
    background: linear-gradient(135deg,
        rgba(0,80,200,0.12) 0%,
        rgba(0,40,120,0.08) 100%);
    border: 1px solid rgba(0,120,255,0.25);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: all 0.35s ease;
    animation: fadeSlideUp 0.5s ease both;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.rank-card:hover {
    border-color: rgba(0,180,255,0.45);
    box-shadow: 0 0 30px rgba(0,120,255,0.18),
                0 8px 30px rgba(0,0,0,0.25);
    transform: translateY(-3px);
}

.rank-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0066ff, #00e5a0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}

.fund-name {
    font-size: 1.05rem;
    font-weight: 600;
    color: #e0eaf8;
    margin: 4px 0 2px 0;
}

.fund-meta {
    font-size: 0.8rem;
    color: #6a8ab0;
}

/* ── STAT PILL ── */
.stat-pill {
    display: inline-block;
    background: rgba(0,100,255,0.1);
    border: 1px solid rgba(0,120,255,0.2);
    border-radius: 8px;
    padding: 6px 14px;
    margin: 4px 6px 4px 0;
    font-size: 0.82rem;
    color: #a0c0e8;
}

.stat-pill span {
    color: #ffffff;
    font-weight: 700;
    margin-left: 4px;
}

/* ── PROJECTION CARD ── */
.projection-card {
    background: linear-gradient(135deg,
        rgba(0,200,120,0.1) 0%,
        rgba(0,100,200,0.08) 100%);
    border: 1px solid rgba(0,200,120,0.25);
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
    transition: all 0.3s ease;
}

.projection-card:hover {
    border-color: rgba(0,220,140,0.4);
    box-shadow: 0 0 25px rgba(0,200,120,0.12);
    transform: translateY(-2px);
}

.projection-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6a9ab0;
    margin-bottom: 8px;
}

.projection-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00e5a0;
    text-shadow: 0 0 20px rgba(0,220,140,0.3);
}

/* ── ANIMATIONS ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0);    }
}

@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 15px rgba(0,120,255,0.2); }
    50%       { box-shadow: 0 0 30px rgba(0,150,255,0.4); }
}

/* ── SECTION HEADER ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(0,120,255,0.15);
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #c8d8f0;
    margin: 0;
}

.section-icon {
    font-size: 1.3rem;
}

/* ── PLOTLY CHART BG ── */
.js-plotly-plot {
    border-radius: 12px;
    overflow: hidden;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb {
    background: rgba(0,120,255,0.3);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0,150,255,0.5); }

/* ── RADIO LABEL ── */
.stRadio > label {
    color: #7aa0c8 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* ── NUMBER INPUT ── */
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,120,255,0.25) !important;
    border-radius: 10px !important;
    color: #e0eaf8 !important;
}

/* ── CAPTION ── */
.stCaption, .caption {
    color: #3a5070 !important;
    font-size: 0.75rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# PLOTLY DARK THEME
# ─────────────────────────────────────────
CHART_THEME = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.02)',
    font=dict(family='Inter', color='#c8d8f0', size=12),
    margin=dict(l=20, r=20, t=50, b=20),
)

COLOR_SEQ = [
    '#0066ff','#00b4d8','#00e5a0','#7b2fff',
    '#ff6b35','#ffd60a','#06d6a0','#ef476f'
]

def style_fig(fig, title=''):
    fig.update_layout(
        **CHART_THEME,
        title=dict(
            text=title,
            font=dict(family='Space Grotesk', size=15, color='#c8d8f0'),
            x=0.02
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            zerolinecolor='rgba(255,255,255,0.08)',
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            zerolinecolor='rgba(255,255,255,0.08)',
            tickfont=dict(size=11)
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(255,255,255,0.08)',
            borderwidth=1,
            font=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor='#0a1628',
            bordercolor='rgba(0,150,255,0.4)',
            font=dict(family='Inter', size=12, color='#e0eaf8')
        )
    )
    return fig

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    nav          = pd.read_csv('data/processed/clean_nav.csv')
    transactions = pd.read_csv('data/processed/clean_transactions.csv')
    performance  = pd.read_csv('data/processed/clean_performance.csv')
    fund_master  = pd.read_csv('data/raw/01_fund_master.csv')
    aum          = pd.read_csv('data/raw/03_aum_by_fund_house.csv')
    sip          = pd.read_csv('data/raw/04_monthly_sip_inflows.csv')
    category     = pd.read_csv('data/raw/05_category_inflows.csv')
    folio        = pd.read_csv('data/raw/06_industry_folio_count.csv')
    benchmark    = pd.read_csv('data/raw/10_benchmark_indices.csv')

    nav['date'] = pd.to_datetime(nav['date'])
    transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
    benchmark['date'] = pd.to_datetime(benchmark['date'])
    return nav, transactions, performance, fund_master, aum, sip, category, folio, benchmark

nav, transactions, performance, fund_master, aum, sip, category, folio, benchmark = load_data()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 8px 0;">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.3rem;
                    font-weight:800; background:linear-gradient(135deg,#4da6ff,#00e5a0);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; letter-spacing:-0.01em;">
            🏦 Bluestock Fintech
        </div>
        <div style="font-size:0.72rem; color:#3a6090; margin-top:4px;
                    text-transform:uppercase; letter-spacing:0.1em;">
            MF Analytics Platform
        </div>
    </div>
    <div style="height:1px; background:linear-gradient(90deg,transparent,
                rgba(0,120,255,0.3),transparent); margin:12px 0 20px 0;"></div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATE",
        ["🏠  Industry Overview",
         "📈  Fund Performance",
         "👥  Investor Analytics",
         "📊  SIP & Market Trends",
         "🤖  Fund Recommender"],
        label_visibility="visible"
    )

    st.markdown("""
    <div style="height:1px; background:linear-gradient(90deg,transparent,
                rgba(0,120,255,0.3),transparent); margin:20px 0 16px 0;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.72rem;color:#3a6090;font-weight:600;'
                'letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">'
                'FILTERS</div>', unsafe_allow_html=True)

    all_houses   = ['All'] + sorted(fund_master['fund_house'].unique().tolist())
    selected_house = st.selectbox("Fund House", all_houses, label_visibility="collapsed")

    all_cats     = ['All'] + sorted(fund_master['category'].unique().tolist())
    selected_cat = st.selectbox("Category",   all_cats,   label_visibility="collapsed")

    st.markdown("""
    <div style="margin-top:auto; padding-top:30px;">
        <div style="font-size:0.68rem; color:#273a52; line-height:1.6;">
            Data: AMFI India · mfapi.in · NSE India<br>
            Capstone Project · June 2026<br>
            ⚠️ Educational purposes only
        </div>
    </div>
    """, unsafe_allow_html=True)

# filtered performance
filtered_perf = performance.copy()
if selected_house != 'All':
    filtered_perf = filtered_perf[filtered_perf['fund_house'] == selected_house]
if selected_cat != 'All':
    filtered_perf = filtered_perf[filtered_perf['category'] == selected_cat]

# ═══════════════════════════════════════════
# PAGE 1 — INDUSTRY OVERVIEW
# ═══════════════════════════════════════════
if "Industry" in page:
    st.markdown("""
    <div class="glow-badge">Industry Dashboard</div>
    <h1>India's Mutual Fund Industry</h1>
    <p style="color:#4a7090; font-size:0.95rem; margin-bottom:28px;">
        Real-time analytics across 40 schemes · 10 AMCs · 4.5 years of data
    </p>
    """, unsafe_allow_html=True)

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Industry AUM",        "₹81 Lakh Cr",   "↑ 18% YoY")
    c2.metric("📈 SIP Inflow Dec 2025", "₹31,002 Cr",    "All Time High")
    c3.metric("👥 Total Folios",         "26.12 Crore",   "↑ 2× since 2022")
    c4.metric("🔄 Active SIP Accounts", "9.35 Crore",    "↑ Growing")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if 'fund_house' in aum.columns and 'aum_crore' in aum.columns:
            aum_g = aum.groupby('fund_house')['aum_crore'].sum().reset_index()
            aum_g = aum_g.sort_values('aum_crore', ascending=True)
            fig = px.bar(aum_g, x='aum_crore', y='fund_house',
                         orientation='h', color='aum_crore',
                         color_continuous_scale=[[0,'#003580'],[0.5,'#0066ff'],[1,'#00e5a0']])
            fig = style_fig(fig, 'AUM by Fund House (₹ Crore)')
            fig.update_coloraxes(showscale=False)
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>AUM: ₹%{x:,.0f} Cr<extra></extra>',
                marker_line_width=0
            )
            fig.update_layout(height=380, yaxis_title='', xaxis_title='AUM (₹ Crore)')
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if 'sip_inflow_crore' in sip.columns:
            fig2 = go.Figure()
            x_col = sip.columns[0]
            fig2.add_trace(go.Scatter(
                x=sip[x_col], y=sip['sip_inflow_crore'],
                mode='lines+markers',
                line=dict(color='#0066ff', width=2.5),
                marker=dict(size=5, color='#00e5a0',
                            line=dict(color='#0066ff', width=1.5)),
                fill='tozeroy',
                fillcolor='rgba(0,100,255,0.08)',
                hovertemplate='<b>%{x}</b><br>SIP Inflow: ₹%{y:,.0f} Cr<extra></extra>'
            ))
            fig2 = style_fig(fig2, 'Monthly SIP Inflows (₹ Crore)')
            fig2.update_layout(height=380, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Folio count
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=folio[folio.columns[0]], y=folio[folio.columns[1]],
        mode='lines+markers',
        line=dict(color='#00e5a0', width=2.5),
        marker=dict(size=6, color='#00e5a0'),
        fill='tozeroy',
        fillcolor='rgba(0,229,160,0.06)',
        hovertemplate='<b>%{x}</b><br>Folios: %{y:.2f} Crore<extra></extra>'
    ))
    fig3 = style_fig(fig3, 'Total MF Folio Count Growth (Crore)')
    fig3.update_layout(height=280, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# PAGE 2 — FUND PERFORMANCE
# ═══════════════════════════════════════════
elif "Performance" in page:
    st.markdown("""
    <div class="glow-badge">Performance Analytics</div>
    <h1>Fund Performance Dashboard</h1>
    <p style="color:#4a7090; font-size:0.95rem; margin-bottom:28px;">
        Risk-adjusted metrics · Sharpe · Alpha · Beta · Max Drawdown · Scorecard
    </p>
    """, unsafe_allow_html=True)

    # Scatter
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if 'std_dev_ann_pct' in filtered_perf.columns and 'return_3yr_pct' in filtered_perf.columns:
        fig = px.scatter(
            filtered_perf,
            x='std_dev_ann_pct', y='return_3yr_pct',
            color='category',
            size='aum_crore' if 'aum_crore' in filtered_perf.columns else None,
            size_max=40,
            hover_name='scheme_name',
            color_discrete_sequence=COLOR_SEQ,
            labels={'std_dev_ann_pct': 'Risk — Annualised Std Dev (%)',
                    'return_3yr_pct':  '3-Year CAGR (%)'}
        )
        fig.add_hline(y=0, line_dash='dot',
                      line_color='rgba(255,255,255,0.1)')
        fig = style_fig(fig, 'Risk vs Return — All Funds (bubble size = AUM)')
        fig.update_traces(
            marker=dict(line=dict(width=1, color='rgba(255,255,255,0.2)')),
            hovertemplate=(
                '<b>%{hovertext}</b><br>'
                'Risk: %{x:.1f}%<br>'
                'Return: %{y:.1f}%<extra></extra>'
            )
        )
        fig.update_layout(height=460)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Scorecard table
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">'
                '<span class="section-icon">📋</span>'
                '<span class="section-title">Fund Scorecard — Sortable Table</span>'
                '</div>', unsafe_allow_html=True)
    display_cols = [c for c in [
        'scheme_name','category','return_1yr_pct','return_3yr_pct',
        'sharpe_ratio','alpha','max_drawdown_pct','expense_ratio_pct'
    ] if c in filtered_perf.columns]
    st.dataframe(
        filtered_perf[display_cols]
            .sort_values('sharpe_ratio', ascending=False)
            .reset_index(drop=True),
        use_container_width=True, height=380
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # NAV selector
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    selected_fund = st.selectbox("Select Fund to View NAV Trend:",
                                 fund_master['scheme_name'].tolist())
    fund_code = fund_master[
        fund_master['scheme_name'] == selected_fund
    ]['amfi_code'].values[0]
    fund_nav = nav[nav['amfi_code'] == fund_code].sort_values('date')

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=fund_nav['date'], y=fund_nav['nav'],
        mode='lines',
        line=dict(color='#0066ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,100,255,0.07)',
        hovertemplate='%{x|%b %Y}<br>NAV: ₹%{y:.2f}<extra></extra>'
    ))
    fig2 = style_fig(fig2, f'NAV Trend — {selected_fund}')
    fig2.update_layout(height=340, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# PAGE 3 — INVESTOR ANALYTICS
# ═══════════════════════════════════════════
elif "Investor" in page:
    st.markdown("""
    <div class="glow-badge">Investor Insights</div>
    <h1>Investor Analytics</h1>
    <p style="color:#4a7090; font-size:0.95rem; margin-bottom:28px;">
        Demographics · Geography · Behaviour patterns across 32,000+ transactions
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if 'state' in transactions.columns:
            state_data = (transactions.groupby('state')['amount_inr']
                          .sum().reset_index()
                          .sort_values('amount_inr', ascending=True))
            fig = px.bar(state_data, x='amount_inr', y='state',
                         orientation='h', color='amount_inr',
                         color_continuous_scale=[[0,'#002a60'],[1,'#0066ff']])
            fig.update_coloraxes(showscale=False)
            fig = style_fig(fig, 'Total Investment by State (₹)')
            fig.update_layout(height=400, yaxis_title='', xaxis_title='Amount (₹)')
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>',
                marker_line_width=0
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if 'transaction_type' in transactions.columns:
            type_data = (transactions.groupby('transaction_type')['amount_inr']
                         .sum().reset_index())
            fig2 = go.Figure(go.Pie(
                labels=type_data['transaction_type'],
                values=type_data['amount_inr'],
                hole=0.55,
                marker=dict(
                    colors=['#0066ff','#00e5a0','#7b2fff'],
                    line=dict(color='rgba(0,0,0,0)', width=0)
                ),
                hovertemplate='<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>',
                textfont=dict(color='#e0eaf8', size=12)
            ))
            fig2.update_layout(
                **CHART_THEME,
                title=dict(text='SIP vs Lumpsum vs Redemption',
                           font=dict(family='Space Grotesk', size=15, color='#c8d8f0'),
                           x=0.02),
                height=400,
                legend=dict(bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#c8d8f0', size=12))
            )
            # Centre annotation
            fig2.add_annotation(
                text='Split', x=0.5, y=0.5,
                font=dict(size=13, color='#7aa0c8', family='Space Grotesk'),
                showarrow=False
            )
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Age group
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if 'age_group' in transactions.columns:
        age_data = (transactions.groupby('age_group')['amount_inr']
                    .mean().reset_index())
        age_data.columns = ['age_group', 'avg_amount']
        fig3 = px.bar(age_data, x='age_group', y='avg_amount',
                      color='avg_amount',
                      color_continuous_scale=[[0,'#002a60'],[0.5,'#0066ff'],[1,'#00e5a0']])
        fig3.update_coloraxes(showscale=False)
        fig3 = style_fig(fig3, 'Average Transaction Amount by Age Group (₹)')
        fig3.update_traces(
            hovertemplate='<b>Age %{x}</b><br>Avg: ₹%{y:,.0f}<extra></extra>',
            marker_line_width=0
        )
        fig3.update_layout(height=320, xaxis_title='Age Group', yaxis_title='Avg Amount (₹)')
        st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# PAGE 4 — SIP & MARKET TRENDS
# ═══════════════════════════════════════════
elif "SIP" in page:
    st.markdown("""
    <div class="glow-badge">Market Intelligence</div>
    <h1>SIP & Market Trends</h1>
    <p style="color:#4a7090; font-size:0.95rem; margin-bottom:28px;">
        SIP inflow patterns · Category flows · Benchmark index performance
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if 'sip_inflow_crore' in sip.columns:
        fig = go.Figure()
        x_col = sip.columns[0]
        # Bar + Line combo
        fig.add_trace(go.Bar(
            x=sip[x_col], y=sip['sip_inflow_crore'],
            name='SIP Inflow',
            marker=dict(
                color=sip['sip_inflow_crore'],
                colorscale=[[0,'#002a60'],[0.5,'#0055cc'],[1,'#00e5a0']],
                line=dict(width=0)
            ),
            hovertemplate='<b>%{x}</b><br>SIP: ₹%{y:,.0f} Cr<extra></extra>'
        ))
        fig = style_fig(fig, 'Monthly SIP Inflows — 2022 to 2025 (₹ Crore)')
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Benchmark
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if 'index_name' in benchmark.columns:
        indices = benchmark['index_name'].unique().tolist()
        selected_indices = st.multiselect(
            "Select Benchmark Indices to Compare:",
            options=indices,
            default=indices[:3]
        )
        if selected_indices:
            bench_f = benchmark[benchmark['index_name'].isin(selected_indices)]
            fig3 = px.line(bench_f, x='date', y='close_value',
                           color='index_name',
                           color_discrete_sequence=COLOR_SEQ)
            fig3 = style_fig(fig3, 'Benchmark Index Performance Comparison')
            fig3.update_traces(line_width=2)
            fig3.update_layout(height=400,
                               xaxis_title='Date', yaxis_title='Index Value')
            st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════
# PAGE 5 — FUND RECOMMENDER
# ═══════════════════════════════════════════
elif "Recommender" in page:
    st.markdown("""
    <div class="glow-badge">AI-Powered Recommender</div>
    <h1>Smart Fund Recommender</h1>
    <p style="color:#4a7090; font-size:0.95rem; margin-bottom:28px;">
        Personalised fund recommendations based on your risk profile & investment goals
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.8])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">'
                    '<span class="section-icon">⚙️</span>'
                    '<span class="section-title">Your Profile</span>'
                    '</div>', unsafe_allow_html=True)

        risk = st.radio(
            "Risk Appetite",
            ["Low", "Moderate", "High"],
            help="Low = Debt/Liquid  |  Moderate = Hybrid  |  High = Equity"
        )

        invest_amount = st.number_input(
            "Monthly SIP Amount (₹)",
            min_value=500, max_value=500000,
            value=10000, step=500
        )

        years = st.slider("Investment Horizon (Years)", 1, 25, 7)

        btn = st.button("🔍  Get My Recommendations", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if btn:
            # filter funds
            if 'risk_grade' in performance.columns:
                f = performance[
                    performance['risk_grade'].str.lower() == risk.lower()
                ]
            else:
                f = performance
            if f.empty:
                f = performance

            top3 = f.nlargest(3, 'sharpe_ratio').reset_index(drop=True)

            medals = ['🥇', '🥈', '🥉']
            for i, row in top3.iterrows():
                st.markdown(f"""
                <div class="rank-card">
                    <div style="display:flex; align-items:center; gap:16px;">
                        <div class="rank-number">{medals[i]}</div>
                        <div>
                            <div class="fund-name">{row['scheme_name']}</div>
                            <div class="fund-meta">{row.get('category','—')} &nbsp;·&nbsp;
                                {row.get('fund_house','—')}</div>
                        </div>
                    </div>
                    <div style="margin-top:14px;">
                        <span class="stat-pill">3yr Return<span>{row['return_3yr_pct']:.1f}%</span></span>
                        <span class="stat-pill">Sharpe<span>{row['sharpe_ratio']:.2f}</span></span>
                        <span class="stat-pill">Alpha<span>{row.get('alpha', 0):.2f}</span></span>
                        <span class="stat-pill">Expense<span>{row.get('expense_ratio_pct', 0):.2f}%</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # SIP Projection
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">'
                        '<span class="section-icon">📈</span>'
                        '<span class="section-title">SIP Growth Projection</span>'
                        '</div>', unsafe_allow_html=True)

            avg_r      = top3['return_3yr_pct'].mean() / 100
            mrate      = avg_r / 12
            months     = years * 12
            fv         = invest_amount * (((1+mrate)**months - 1)/mrate) * (1+mrate)
            invested   = invest_amount * months
            gained     = fv - invested

            pc1, pc2, pc3 = st.columns(3)
            with pc1:
                st.markdown(f"""
                <div class="projection-card">
                    <div class="projection-label">Total Invested</div>
                    <div class="projection-value" style="color:#7ab8ff;">
                        ₹{invested/100000:.1f}L
                    </div>
                </div>""", unsafe_allow_html=True)
            with pc2:
                st.markdown(f"""
                <div class="projection-card">
                    <div class="projection-label">Wealth Gained</div>
                    <div class="projection-value" style="color:#ffd60a;">
                        ₹{gained/100000:.1f}L
                    </div>
                </div>""", unsafe_allow_html=True)
            with pc3:
                st.markdown(f"""
                <div class="projection-card">
                    <div class="projection-label">Future Value</div>
                    <div class="projection-value">
                        ₹{fv/100000:.1f}L
                    </div>
                </div>""", unsafe_allow_html=True)

            # Growth chart
            months_range = list(range(1, months + 1))
            cumulative   = [invest_amount * m for m in months_range]
            future_vals  = [invest_amount * (((1+mrate)**m - 1)/mrate) * (1+mrate)
                            for m in months_range]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months_range, y=cumulative,
                name='Amount Invested',
                line=dict(color='#4a7090', width=2, dash='dot'),
                fill='tozeroy', fillcolor='rgba(74,112,144,0.05)',
                hovertemplate='Month %{x}<br>Invested: ₹%{y:,.0f}<extra></extra>'
            ))
            fig.add_trace(go.Scatter(
                x=months_range, y=future_vals,
                name='Portfolio Value',
                line=dict(color='#00e5a0', width=2.5),
                fill='tozeroy', fillcolor='rgba(0,229,160,0.07)',
                hovertemplate='Month %{x}<br>Value: ₹%{y:,.0f}<extra></extra>'
            ))
            fig = style_fig(fig, f'SIP Growth Over {years} Years (₹{invest_amount:,}/month)')
            fig.update_layout(
                height=300,
                xaxis_title='Month',
                yaxis_title='Value (₹)',
                legend=dict(orientation='h', y=-0.15)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center;
                        justify-content:center; height:300px; opacity:0.4;">
                <div style="font-size:3rem;">🤖</div>
                <div style="font-family:'Space Grotesk',sans-serif; font-size:1rem;
                            color:#4a7090; margin-top:12px;">
                    Set your profile and click Get Recommendations
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div style="margin-top:40px; padding:16px 0;
            border-top:1px solid rgba(0,120,255,0.1);
            text-align:center; color:#273a52; font-size:0.72rem;
            letter-spacing:0.04em;">
    🏦 Bluestock Fintech Pvt. Ltd. &nbsp;·&nbsp;
    Mutual Fund Analytics Platform &nbsp;·&nbsp;
    Capstone Project June 2026 &nbsp;·&nbsp;
    Data: AMFI India &nbsp;·&nbsp;
    ⚠️ Educational purposes only — not financial advice
</div>
""", unsafe_allow_html=True)
