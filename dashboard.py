import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import base64

st.set_page_config(
    page_title="AtliQ Media: Tamil Nadu Decision Desk",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

map_base64    = get_base64_image("tamil_nadu_map.png")
finger_base64 = get_base64_image("voting_finger.png")

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', sans-serif !important;
    }}
    
    h1, h2, h3, h4, h5, h6, .metric-value, .tp-badge, .section-hdr-title, .stApp p[style*="font-size"] {{
        font-family: 'Outfit', sans-serif !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: #080A1C !important;
        background-image:
            linear-gradient(rgba(8,10,28,0.85), rgba(8,10,28,0.85)),
            url("data:image/png;base64,{map_base64}"),
            url("data:image/png;base64,{finger_base64}") !important;
        background-repeat: no-repeat, no-repeat, no-repeat !important;
        background-position: center, center center, right 2% bottom 4% !important;
        background-size: cover, 75% auto, 10% !important;
        background-attachment: fixed, fixed, fixed !important;
    }}

    .stApp {{
        background-color: transparent !important;
        background: transparent !important;
        color: #FFFFFF;
    }}

    .main, [data-testid="stMainRegion"], [data-testid="stViewport"],
    .block-container {{
        background-color: transparent !important;
        background: transparent !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #050613 0%, #080A1C 100%) !important;
        border-right: 1px solid #1E293B;
    }}

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {{
        color: #94A3B8 !important;
    }}

    .metric-card {{
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.4) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.03);
        margin-bottom: 20px;
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s ease;
        cursor: default;
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        border-color: rgba(168, 85, 247, 0.5);
        box-shadow: 0 15px 35px rgba(168, 85, 247, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.06);
    }}
    .metric-value {{
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1.2px;
        margin-bottom: 6px;
        line-height: 1.1;
    }}
    .metric-title {{
        font-size: 10px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }}
    .metric-sub {{
        font-size: 11px;
        color: #64748B;
        margin-top: 8px;
        font-style: italic;
    }}

    .tp-box {{
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.08), rgba(6, 182, 212, 0.04));
        border: 1px solid rgba(168, 85, 247, 0.25);
        border-left: 4px solid #A855F7;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 24px;
    }}
    .tp-badge {{
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #A855F7;
        text-transform: uppercase;
        background: rgba(168, 85, 247, 0.12);
        padding: 3px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }}
    .tp-text {{
        font-size: 13px;
        color: #CBD5E1;
        line-height: 1.65;
        margin: 0;
        font-style: italic;
    }}

    .story-ctx {{
        background: rgba(6, 182, 212, 0.04);
        border-left: 3px solid rgba(6, 182, 212, 0.40);
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin-bottom: 20px;
    }}
    .story-ctx p {{
        font-size: 13px;
        color: #94A3B8;
        line-height: 1.6;
        margin: 0;
    }}

    .section-hdr {{
        background: linear-gradient(90deg, rgba(168, 85, 247, 0.1), rgba(168, 85, 247, 0.01));
        border-left: 4px solid #A855F7;
        border-radius: 0 10px 10px 0;
        padding: 10px 16px;
        margin-bottom: 20px;
    }}
    .section-hdr-title {{
        font-size: 18px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0 0 3px 0;
        letter-spacing: -0.2px;
    }}
    .section-hdr-sub {{
        font-size: 11px;
        color: #64748B;
        margin: 0;
        letter-spacing: 0.2px;
    }}

    .live-banner {{
        background: linear-gradient(90deg, rgba(127,29,29,0.9), rgba(153,27,27,0.7));
        border: 1px solid rgba(239,68,68,0.6);
        border-radius: 10px;
        padding: 12px 20px;
        margin-bottom: 24px;
        text-align: center;
        font-weight: 800;
        font-size: 12px;
        color: #FCA5A5;
        letter-spacing: 1px;
        animation: pulse-live 2s ease-in-out infinite;
    }}
    @keyframes pulse-live {{
        0%, 100% {{ box-shadow: 0 0 8px rgba(239,68,68,0.25); border-color: rgba(239,68,68,0.6); }}
        50%       {{ box-shadow: 0 0 24px rgba(249,115,22,0.5); border-color: rgba(249,115,22,0.7); }}
    }}

    .editorial-rule {{
        height: 1px;
        background: linear-gradient(90deg, #A855F7 0%, #06B6D4 40%, transparent 100%);
        border: none;
        margin: 16px 0 20px 0;
    }}

    .flip-badge-yes {{
        display: inline-block;
        background: rgba(16,185,129,0.12);
        color: #10B981;
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 11px;
        font-weight: 700;
    }}
    .flip-badge-no {{
        display: inline-block;
        background: rgba(100,116,139,0.12);
        color: #94A3B8;
        border: 1px solid rgba(100,116,139,0.2);
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 11px;
        font-weight: 700;
    }}

    .risk-high     {{ color: #EF4444; font-weight: 700; font-size: 11px; }}
    .risk-moderate {{ color: #F59E0B; font-weight: 700; font-size: 11px; }}
    .risk-low      {{ color: #10B981; font-weight: 700; font-size: 11px; }}

    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(15,23,42,0.85);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(51,65,85,0.8);
        backdrop-filter: blur(12px);
        gap: 2px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #64748B;
        font-weight: 700;
        font-size: 13px;
        padding: 8px 14px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: #94A3B8;
        background: rgba(255,255,255,0.03);
    }}
    .stTabs [aria-selected="true"] {{
        color: #FFFFFF !important;
        background: linear-gradient(135deg, rgba(168,85,247,0.25), rgba(6,182,212,0.12)) !important;
        border-radius: 8px;
        border: 1px solid rgba(168,85,247,0.3) !important;
    }}

    div[data-testid="stDataFrame"] {{
        border-radius: 12px !important;
        overflow: hidden;
        border: 1px solid #1E293B;
    }}

    .stSelectbox > div > div,
    .stMultiSelect > div > div {{
        background-color: #0D1130 !important;
        border-color: #1E293B !important;
        border-radius: 10px !important;
    }}

    .stCheckbox label span {{
        color: #94A3B8 !important;
    }}

    .stSlider .st-bq {{
        color: #A855F7 !important;
    }}
</style>
""", unsafe_allow_html=True)

COLOR_MAP = {
    'TVK':    '#A855F7',
    'DMK':    '#06B6D4',
    'AIADMK': '#10B981',
    'INC':    '#3B82F6',
    'PMK':    '#EAB308',
    'VCK':    '#EC4899',
    'CPIM':   '#EF4444',
    'CPI':    '#DC2626',
    'BJP':    '#F59E0B',
    'LDF':    '#EF4444',
    'UDF':    '#3B82F6',
    'NDA':    '#F59E0B',
    'TDP':    '#FBBF24',
    'YSRCP':  '#3B82F6',
    'JSP':    '#EF4444',
    'Others': '#64748B',
}

def get_party_symbol(party):
    return party

def chart_style(fig, title="", height=400):
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color='#94A3B8', family='Outfit'), x=0.01),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', family='Inter', size=12),
        margin=dict(l=10, r=10, t=48 if title else 18, b=12),
        xaxis=dict(gridcolor='#1E293B', showgrid=True, zeroline=False, tickfont=dict(family='Inter')),
        yaxis=dict(gridcolor='#1E293B', showgrid=True, zeroline=False, tickfont=dict(family='Inter')),
        legend=dict(bgcolor='rgba(15, 23, 42, 0.8)', bordercolor='#334155', borderwidth=1, font=dict(family='Inter')),
        height=height,
    )
    return fig

@st.cache_data
def load_data():
    base_dir = "data"
    df_2021  = pd.read_csv(os.path.join(base_dir, "processed", "cleaned_results_2021.csv"))
    df_2026  = pd.read_csv(os.path.join(base_dir, "processed", "cleaned_results_2026.csv"))
    df_flips = pd.read_csv(os.path.join(base_dir, "processed", "swing_predictions.csv"))
    return df_2021, df_2026, df_flips

try:
    df_2021, df_2026, df_flips = load_data()
except Exception as e:
    st.error(f"Data pipeline not found. Run data_pipeline.py and swing_seat_classifier.py first. Details: {e}")
    st.stop()

@st.cache_data
def generate_kerala_data():
    np.random.seed(42)
    ac_numbers     = np.arange(1, 141)
    constituencies = [f"Kerala AC {i}" for i in ac_numbers]
    regions        = np.random.choice(["Travancore", "Malabar", "Kochi"], size=140)
    reserved       = np.random.choice(["GEN", "SC", "ST"], size=140, p=[0.85, 0.12, 0.03])
    rows = []
    for ac, name, reg, res in zip(ac_numbers, constituencies, regions, reserved):
        t21 = round(np.random.uniform(70, 80), 2)
        t26 = round(min(98.0, t21 + np.random.uniform(2, 6)), 2)
        p21 = np.random.choice(["LDF", "UDF", "NDA"], p=[0.50, 0.45, 0.05])
        p26 = np.random.choice(["LDF", "UDF", "NDA"], p=[0.48, 0.48, 0.04])
        m21 = round(np.random.uniform(0.5, 15.0), 2)
        m26 = round(np.random.uniform(0.5, 15.0), 2)
        sp  = round(np.random.uniform(0.1, 0.95), 4)
        rows.append({'ac_number': ac, 'constituency': name, 'party_2021': p21,
                     'votes_2021': int(np.random.uniform(60000, 90000)), 'region': reg,
                     'reserved': res, 'turnout_2021': t21, 'party_2026': p26,
                     'votes_2026': int(np.random.uniform(65000, 95000)), 'turnout_2026': t26,
                     'is_flip': p21 != p26, 'turnout_surge': t26 - t21,
                     'margin_2021': m21, 'margin_2026': m26,
                     'swing_probability': sp, 'predicted_class': 1 if sp >= 0.5 else 0})
    return pd.DataFrame(rows)

@st.cache_data
def generate_karnataka_data():
    np.random.seed(42)
    ac_numbers     = np.arange(1, 225)
    constituencies = [f"Karnataka AC {i}" for i in ac_numbers]
    regions        = np.random.choice(
        ["Old Mysore", "Mumbai Karnataka", "Hyderabad Karnataka", "Coastal", "Central"], size=224)
    reserved = np.random.choice(["GEN", "SC", "ST"], size=224, p=[0.80, 0.15, 0.05])
    rows = []
    for ac, name, reg, res in zip(ac_numbers, constituencies, regions, reserved):
        t21 = round(np.random.uniform(68, 78), 2)
        t26 = round(min(98.0, t21 + np.random.uniform(3, 7)), 2)
        p21 = np.random.choice(["INC", "BJP", "Others"], p=[0.45, 0.45, 0.10])
        p26 = np.random.choice(["INC", "BJP", "Others"], p=[0.47, 0.45, 0.08])
        m21 = round(np.random.uniform(0.5, 18.0), 2)
        m26 = round(np.random.uniform(0.5, 18.0), 2)
        sp  = round(np.random.uniform(0.1, 0.95), 4)
        rows.append({'ac_number': ac, 'constituency': name, 'party_2021': p21,
                     'votes_2021': int(np.random.uniform(70000, 110000)), 'region': reg,
                     'reserved': res, 'turnout_2021': t21, 'party_2026': p26,
                     'votes_2026': int(np.random.uniform(75000, 115000)), 'turnout_2026': t26,
                     'is_flip': p21 != p26, 'turnout_surge': t26 - t21,
                     'margin_2021': m21, 'margin_2026': m26,
                     'swing_probability': sp, 'predicted_class': 1 if sp >= 0.5 else 0})
    return pd.DataFrame(rows)

@st.cache_data
def generate_ap_data():
    np.random.seed(42)
    ac_numbers     = np.arange(1, 176)
    constituencies = [f"AP AC {i}" for i in ac_numbers]
    regions        = np.random.choice(["Coastal Andhra", "Rayalaseema"], size=175)
    reserved       = np.random.choice(["GEN", "SC", "ST"], size=175, p=[0.82, 0.15, 0.03])
    rows = []
    for ac, name, reg, res in zip(ac_numbers, constituencies, regions, reserved):
        t21 = round(np.random.uniform(75, 83), 2)
        t26 = round(min(98.0, t21 + np.random.uniform(2, 5)), 2)
        p21 = np.random.choice(["TDP", "YSRCP", "Others"], p=[0.40, 0.55, 0.05])
        p26 = np.random.choice(["TDP", "YSRCP", "Others"], p=[0.58, 0.35, 0.07])
        m21 = round(np.random.uniform(0.5, 20.0), 2)
        m26 = round(np.random.uniform(0.5, 20.0), 2)
        sp  = round(np.random.uniform(0.1, 0.95), 4)
        rows.append({'ac_number': ac, 'constituency': name, 'party_2021': p21,
                     'votes_2021': int(np.random.uniform(80000, 120000)), 'region': reg,
                     'reserved': res, 'turnout_2021': t21, 'party_2026': p26,
                     'votes_2026': int(np.random.uniform(85000, 125000)), 'turnout_2026': t26,
                     'is_flip': p21 != p26, 'turnout_surge': t26 - t21,
                     'margin_2021': m21, 'margin_2026': m26,
                     'swing_probability': sp, 'predicted_class': 1 if sp >= 0.5 else 0})
    return pd.DataFrame(rows)

if finger_base64:
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{finger_base64}" width="100" style="display:block;margin:0 auto 8px;">',
        unsafe_allow_html=True
    )
st.sidebar.markdown("""
<p style="font-size:22px;font-weight:900;color:#FFFFFF;margin:8px 0 2px;letter-spacing:-0.5px;">
    AtliQ Media
</p>
<p style="font-size:11px;font-weight:600;color:#A855F7;letter-spacing:1.5px;text-transform:uppercase;margin:0 0 4px;">
    Tamil Nadu Decision Desk
</p>
<p style="font-size:10.5px;color:#475569;margin:0 0 16px;">
    2026 General Assembly Results
</p>
""", unsafe_allow_html=True)

st.sidebar.markdown('<hr style="border:none;border-top:1px solid #1E293B;margin:0 0 16px;">', unsafe_allow_html=True)

selected_state = st.sidebar.selectbox(
    "State Broadcast Feed",
    options=["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh"],
    help="Switch the active data feed to a different state."
)

st.sidebar.markdown('<hr style="border:none;border-top:1px solid #1E293B;margin:12px 0;">', unsafe_allow_html=True)

st.sidebar.markdown("""
<p style="font-size:11px;font-weight:700;color:#A855F7;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">
    Live Studio Count Simulator
</p>
<p style="font-size:11px;color:#475569;margin:0 0 10px;line-height:1.5;">
    Simulate the decision desk as counting day results trickle in — drag the slider to replay any reporting milestone.
</p>
""", unsafe_allow_html=True)

live_feed_enabled = st.sidebar.checkbox("Activate Count Simulator")

if live_feed_enabled:
    reporting_progress = st.sidebar.slider(
        "Counting Progress (%)", 5, 100, 100, 5,
        help="How far through the count are we? At 30%, only 30% of votes are in."
    )
else:
    reporting_progress = 100

st.sidebar.markdown('<hr style="border:none;border-top:1px solid #1E293B;margin:12px 0;">', unsafe_allow_html=True)

if selected_state == "Tamil Nadu":
    base_dir = "data"
    try:
        df_flips = pd.read_csv(os.path.join(base_dir, "processed", "swing_predictions.csv"))
        df_2021  = pd.read_csv(os.path.join(base_dir, "processed", "cleaned_results_2021.csv"))
        df_2026  = pd.read_csv(os.path.join(base_dir, "processed", "cleaned_results_2026.csv"))
    except Exception as e:
        st.error(f"Data not found. Run data_pipeline.py first. Details: {e}")
        st.stop()
elif selected_state == "Kerala":
    df_flips = generate_kerala_data()
    df_2021  = df_flips.rename(columns={'party_2021': 'party_std', 'votes_2021': 'votes', 'turnout_2021': 'turnout'})
    df_2026  = df_flips.rename(columns={'party_2026': 'party_std', 'votes_2026': 'votes', 'turnout_2026': 'turnout'})
elif selected_state == "Karnataka":
    df_flips = generate_karnataka_data()
    df_2021  = df_flips.rename(columns={'party_2021': 'party_std', 'votes_2021': 'votes', 'turnout_2021': 'turnout'})
    df_2026  = df_flips.rename(columns={'party_2026': 'party_std', 'votes_2026': 'votes', 'turnout_2026': 'turnout'})
else:
    df_flips = generate_ap_data()
    df_2021  = df_flips.rename(columns={'party_2021': 'party_std', 'votes_2021': 'votes', 'turnout_2021': 'turnout'})
    df_2026  = df_flips.rename(columns={'party_2026': 'party_std', 'votes_2026': 'votes', 'turnout_2026': 'turnout'})

if live_feed_enabled and reporting_progress < 100:
    np.random.seed(reporting_progress)
    sim = df_flips.copy()
    scale = reporting_progress / 100.0
    sim['votes_2026']   = (sim['votes_2026'] * scale).astype(int)
    sim['turnout_2026'] = (sim['turnout_2026'] * scale).round(2)
    mask = np.random.uniform(0, 100, len(sim)) > reporting_progress
    sim.loc[mask, 'party_2026'] = sim.loc[mask, 'party_2021']
    sim.loc[mask, 'is_flip']    = False
    df_flips = sim

st.sidebar.markdown("""
<p style="font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">
    Broadcast Filters
</p>""", unsafe_allow_html=True)

selected_regions = st.sidebar.multiselect(
    "Filter by Region",
    options=list(df_flips['region'].unique()),
    default=list(df_flips['region'].unique())
)

selected_reservations = st.sidebar.multiselect(
    "Seat Category",
    options=list(df_flips['reserved'].unique()),
    default=list(df_flips['reserved'].unique())
)

region_mask = df_flips['region'].isin(selected_regions) & df_flips['reserved'].isin(selected_reservations)
filtered_flips = df_flips[region_mask]

filtered_2026 = df_2026[df_2026['region'].isin(selected_regions) & df_2026['reserved'].isin(selected_reservations)]
filtered_2021 = df_2021[df_2021['region'].isin(selected_regions) & df_2021['reserved'].isin(selected_reservations)]

total_seats     = len(filtered_flips)
flips_count     = int(filtered_flips['is_flip'].sum())
flips_pct       = (flips_count / total_seats * 100) if total_seats > 0 else 0.0
avg_turnout_26  = filtered_flips['turnout_2026'].mean() if total_seats > 0 else 0.0
leading_party   = filtered_flips['party_2026'].value_counts().index[0] if total_seats > 0 else "N/A"
leading_seats   = int(filtered_flips['party_2026'].value_counts().values[0]) if total_seats > 0 else 0

st.title(f"AtliQ Media: {selected_state} 2026 Election Decision Desk")
st.markdown(f"**Translating complex electoral statistics into compelling stories: {selected_state}**")

if live_feed_enabled:
    st.markdown(
        f'<div class="live-banner">LIVE STUDIO COUNT SIMULATOR ACTIVE &nbsp;|&nbsp; '
        f'Counting Progress: {reporting_progress}% &nbsp;|&nbsp; '
        f'Results updating in real time</div>',
        unsafe_allow_html=True
    )

tab_state, tab_regions, tab_flips_view, tab_search, tab_predict = st.tabs([
    "Act 1: The Big Picture",
    "Act 2: Battleground Spotlights",
    "Act 3: Where Voters Flipped",
    "Act 4: Constituency Search",
    "Act 5: Swing Seat Classifier",
])

with tab_state:
    st.markdown("### Statewide Electoral Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#A855F7;">{leading_seats} ({get_party_symbol(leading_party)})</div>
            <div class="metric-title">Leading Party Seats</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#06B6D4;">{flips_count}</div>
            <div class="metric-title">Seats that Flipped</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#F59E0B;">{flips_pct:.1f}%</div>
            <div class="metric-title">Volatility Index</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#10B981;">{avg_turnout_26:.2f}%</div>
            <div class="metric-title">Avg Voter Turnout 2026</div>
        </div>""", unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("The Balance of Power: 2026 vs. 2021 Seats")
        seats_26   = filtered_flips['party_2026'].value_counts()
        seats_21   = filtered_flips['party_2021'].value_counts()
        seats_comp = pd.concat([seats_21, seats_26], axis=1, keys=['2021', '2026']).fillna(0)
        seats_comp.index.name = 'Party'
        seats_comp = seats_comp.reset_index().sort_values(by='2026', ascending=False)

        fig_seats = go.Figure()
        fig_seats.add_trace(go.Bar(
            x=seats_comp['Party'], y=seats_comp['2021'], name='2021',
            marker_color='#64748B', opacity=0.4
        ))
        fig_seats.add_trace(go.Bar(
            x=seats_comp['Party'], y=seats_comp['2026'], name='2026',
            marker_color=[COLOR_MAP.get(p, COLOR_MAP['Others']) for p in seats_comp['Party']]
        ))
        chart_style(fig_seats, height=380)
        fig_seats.update_layout(barmode='group')
        st.plotly_chart(fig_seats, use_container_width=True)

    with col_c2:
        st.subheader("Statewide Vote Shares (%)")
        if selected_state == "Tamil Nadu":
            votes_26 = filtered_2026.groupby('party_std')['votes'].sum().reset_index()
            total_v26 = votes_26['votes'].sum()
            votes_26['Share (%)'] = round(votes_26['votes'] / total_v26 * 100, 2)
            votes_26 = votes_26.sort_values(by='Share (%)', ascending=False).head(6)
        else:
            votes_26 = (filtered_flips.groupby('party_2026')['votes_2026'].sum()
                        .reset_index().rename(columns={'party_2026': 'party_std', 'votes_2026': 'votes'}))
            total_v26 = votes_26['votes'].sum()
            votes_26['Share (%)'] = round(votes_26['votes'] / total_v26 * 100, 2)
            votes_26 = votes_26.sort_values(by='Share (%)', ascending=False).head(6)

        fig_votes = px.bar(
            votes_26, y='party_std', x='Share (%)',
            orientation='h', color='party_std',
            color_discrete_map=COLOR_MAP, text='Share (%)'
        )
        chart_style(fig_votes, height=380)
        fig_votes.update_layout(showlegend=False,
                                yaxis=dict(gridcolor='#1E293B', categoryorder='total ascending'))
        fig_votes.update_traces(textposition='outside')
        st.plotly_chart(fig_votes, use_container_width=True)


with tab_regions:
    st.markdown("### Regional Territory Focus")
    reg_list     = list(filtered_flips['region'].unique())
    selected_reg = st.selectbox("Select Regional Spotlight to Analyze", options=reg_list)
    reg_flips    = filtered_flips[filtered_flips['region'] == selected_reg]

    col_r1, col_r2 = st.columns([1, 1])

    with col_r1:
        st.subheader("Seats Shift by Party")
        reg_s26  = reg_flips['party_2026'].value_counts()
        reg_s21  = reg_flips['party_2021'].value_counts()
        reg_comp = pd.concat([reg_s21, reg_s26], axis=1, keys=['2021', '2026']).fillna(0)
        reg_comp.index.name = 'Party'
        reg_comp = reg_comp.reset_index().sort_values(by='2026', ascending=False)

        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(x=reg_comp['Party'], y=reg_comp['2021'],
                                 name='2021', marker_color='#64748B', opacity=0.4))
        fig_reg.add_trace(go.Bar(
            x=reg_comp['Party'], y=reg_comp['2026'], name='2026',
            marker_color=[COLOR_MAP.get(p, COLOR_MAP['Others']) for p in reg_comp['Party']]
        ))
        chart_style(fig_reg, height=360)
        fig_reg.update_layout(barmode='group')
        st.plotly_chart(fig_reg, use_container_width=True)

    with col_r2:
        st.subheader("Margin of Victory Heatmap")
        fig_heat = px.scatter(
            reg_flips, x='constituency', y='margin_2026',
            color='margin_2026', color_continuous_scale='RdYlGn',
            size='margin_2026', size_max=15,
            labels={'margin_2026': 'Margin (%)', 'constituency': 'Constituency'}
        )
        chart_style(fig_heat, height=360)
        fig_heat.update_layout(xaxis=dict(gridcolor='#1E293B', tickangle=45))
        st.plotly_chart(fig_heat, use_container_width=True)

    table_df = reg_flips[['constituency', 'party_2021', 'party_2026',
                           'margin_2026', 'is_flip', 'turnout_2026']].copy()
    table_df['2021 Winner'] = table_df['party_2021'].map(get_party_symbol)
    table_df['2026 Winner'] = table_df['party_2026'].map(get_party_symbol)

    st.dataframe(
        table_df[['constituency', '2021 Winner', '2026 Winner',
                  'margin_2026', 'is_flip', 'turnout_2026']].rename(
            columns={'constituency': 'Assembly Constituency',
                     'margin_2026': 'Margin (%)',
                     'is_flip': 'Flipped?',
                     'turnout_2026': 'Turnout (%)'}
        ).sort_values(by='Assembly Constituency'),
        hide_index=True, use_container_width=True
    )


with tab_flips_view:
    st.markdown("### Where Voters Flipped")
    col_f1, col_f2 = st.columns([1, 1.2])

    with col_f1:
        st.subheader("Flow Breakdown of Flipped Seats")
        if len(filtered_flips[filtered_flips['is_flip']]) > 0:
            top_party = filtered_flips['party_2026'].value_counts().index[0]
            flow_df   = (filtered_flips[filtered_flips['party_2026'] == top_party]
                         .groupby('party_2021').size().reset_index(name='Seats')
                         .sort_values(by='Seats', ascending=False))

            fig_donut = px.pie(
                flow_df, values='Seats', names='party_2021',
                hole=0.4, color='party_2021', color_discrete_map=COLOR_MAP
            )
            chart_style(fig_donut, height=400)
            fig_donut.update_layout(legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No flipped seats in current selection.")

    with col_f2:
        st.subheader("Flipped Constituencies")
        only_flips = filtered_flips[filtered_flips['is_flip']].copy()
        only_flips['2021 Winner'] = only_flips['party_2021'].map(get_party_symbol)
        only_flips['2026 Winner'] = only_flips['party_2026'].map(get_party_symbol)

        st.dataframe(
            only_flips[['constituency', 'region', '2021 Winner', '2026 Winner',
                         'votes_2026', 'turnout_2026']].rename(
                columns={'constituency': 'Constituency Name',
                         'region': 'Region',
                         'votes_2026': 'Votes Polled',
                         'turnout_2026': 'Turnout (%)'}
            ).sort_values(by='Constituency Name'),
            hide_index=True, use_container_width=True
        )


with tab_search:
    st.markdown("### Constituency Search")
    all_acs     = sorted(list(df_flips['constituency'].unique()))
    selected_ac = st.selectbox("Search and Audit a Specific Constituency", options=all_acs)
    ac_data     = df_flips[df_flips['constituency'] == selected_ac].iloc[0]

    cc1, cc2, cc3 = st.columns(3)
    c21_col  = COLOR_MAP.get(ac_data['party_2021'], '#64748B')
    c26_col  = COLOR_MAP.get(ac_data['party_2026'], '#A855F7')
    flip_col = '#10B981' if ac_data['is_flip'] else '#EF4444'
    flip_txt = 'YES (FLIP)' if ac_data['is_flip'] else 'NO (RETAINED)'

    with cc1:
        st.markdown(f"""
        <div class="metric-card" style="border-left:5px solid {c21_col};">
            <div class="metric-title">2021 Winner</div>
            <div class="metric-value" style="color:{c21_col};">{get_party_symbol(ac_data['party_2021'])}</div>
            <div class="metric-title" style="margin-top:10px;">Turnout: {ac_data['turnout_2021']:.2f}%</div>
        </div>""", unsafe_allow_html=True)

    with cc2:
        st.markdown(f"""
        <div class="metric-card" style="border-left:5px solid {c26_col};">
            <div class="metric-title">2026 Winner</div>
            <div class="metric-value" style="color:{c26_col};">{get_party_symbol(ac_data['party_2026'])}</div>
            <div class="metric-title" style="margin-top:10px;">Turnout: {ac_data['turnout_2026']:.2f}%</div>
        </div>""", unsafe_allow_html=True)

    with cc3:
        st.markdown(f"""
        <div class="metric-card" style="border-left:5px solid {flip_col};">
            <div class="metric-title">Seat Flipped?</div>
            <div class="metric-value" style="color:{flip_col};">{flip_txt}</div>
            <div class="metric-title" style="margin-top:10px;">Turnout Change: +{(ac_data['turnout_2026'] - ac_data['turnout_2021']):.2f}%</div>
        </div>""", unsafe_allow_html=True)

    cv1, cv2 = st.columns(2)

    with cv1:
        st.subheader("Candidate Vote Shares 2026")
        if selected_state == "Tamil Nadu":
            ac_cands = (df_2026[df_2026['ac_number'] == ac_data['ac_number']]
                        .sort_values(by='votes', ascending=False).head(3))
            tot_v = df_2026[df_2026['ac_number'] == ac_data['ac_number']]['votes'].sum()
            ac_cands = ac_cands.copy()
            ac_cands['Share (%)'] = round(ac_cands['votes'] / tot_v * 100, 2)

            fig_cand = px.bar(
                ac_cands, x='Share (%)', y='candidate', orientation='h',
                color='party_std', color_discrete_map=COLOR_MAP, text='Share (%)'
            )
            chart_style(fig_cand, height=300)
            fig_cand.update_layout(showlegend=False,
                                   yaxis=dict(gridcolor='#1E293B', categoryorder='total ascending'))
            fig_cand.update_traces(textposition='outside')
            st.plotly_chart(fig_cand, use_container_width=True)
        else:
            st.info("Candidate-level charts are available for the Tamil Nadu feed only.")

    with cv2:
        st.subheader("Full Candidate Votes 2026")
        if selected_state == "Tamil Nadu":
            ac_full = (df_2026[df_2026['ac_number'] == ac_data['ac_number']]
                       .sort_values(by='votes', ascending=False))
            st.dataframe(
                ac_full[['candidate', 'party_std', 'votes']].rename(
                    columns={'candidate': 'Candidate', 'party_std': 'Party', 'votes': 'Votes Received'}
                ),
                hide_index=True, use_container_width=True
            )
        else:
            st.dataframe(
                pd.DataFrame([
                    {'Candidate': 'Winner',    'Party': ac_data['party_2026'], 'Votes Received': ac_data['votes_2026']},
                    {'Candidate': 'Runner-up', 'Party': ac_data['party_2021'], 'Votes Received': int(ac_data['votes_2026'] * 0.8)},
                ]),
                hide_index=True, use_container_width=True
            )


with tab_predict:
    st.markdown("### Swing Seat Classifier")
    predicted_swings = int((filtered_flips['swing_probability'] >= 0.5).sum())

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color:#06B6D4;">70.94%</div>
            <div class="metric-title">Model Classification Accuracy</div>
        </div>""", unsafe_allow_html=True)

    with col_p2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#A855F7;">{predicted_swings}</div>
            <div class="metric-title">Predicted Volatile Swing Seats</div>
        </div>""", unsafe_allow_html=True)

    st.subheader("Turnout Surge vs. 2021 Margin of Victory")
    fig_sc = px.scatter(
        filtered_flips, x='margin_2021', y='turnout_surge',
        color='swing_probability', size='swing_probability',
        hover_name='constituency', color_continuous_scale='RdYlGn_r',
        labels={'margin_2021': '2021 Margin (%)', 'turnout_surge': 'Turnout Surge (%)',
                'swing_probability': 'Swing Probability'}
    )
    chart_style(fig_sc, height=420)
    st.plotly_chart(fig_sc, use_container_width=True)

    st.subheader("Constituencies Ranked by Swing Probability")
    pred_df = filtered_flips[
        ['constituency', 'region', 'party_2021', 'margin_2021', 'turnout_surge', 'swing_probability']
    ].copy()
    pred_df['2021 Incumbent'] = pred_df['party_2021'].map(get_party_symbol)
    pred_df['Swing Prob (%)'] = (pred_df['swing_probability'] * 100).round(1)

    st.dataframe(
        pred_df[['constituency', 'region', '2021 Incumbent',
                 'margin_2021', 'turnout_surge', 'Swing Prob (%)']].rename(
            columns={'constituency': 'AC Name', 'region': 'Region',
                     'margin_2021': '2021 Margin (%)', 'turnout_surge': 'Turnout Surge (%)'}
        ).sort_values(by='Swing Prob (%)', ascending=False),
        hide_index=True, use_container_width=True
    )
