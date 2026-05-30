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

def tp_box(cue_text):
    return f"""
    <div class="tp-box">
        <span class="tp-badge">Presenter Cue</span>
        <p class="tp-text">{cue_text}</p>
    </div>"""

def story_ctx(text):
    return f"""
    <div class="story-ctx"><p>{text}</p></div>"""

def section_hdr(title, sub=""):
    sub_html = f'<p class="section-hdr-sub">{sub}</p>' if sub else ""
    return f"""
    <div class="section-hdr">
        <p class="section-hdr-title">{title}</p>
        {sub_html}
    </div>"""

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

st.markdown(f"""
<div style="margin-bottom:6px;">
    <span style="font-size:28px;font-weight:900;color:#FFFFFF;letter-spacing:-0.8px;">
        AtliQ Media: {selected_state} Decision Desk
    </span>
</div>
<p style="font-size:14px;color:#64748B;margin:0 0 6px;font-style:italic;">
    Translating 234 constituencies of raw data into the story only the numbers can tell.
</p>
<div class="editorial-rule"></div>
""", unsafe_allow_html=True)

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
    "Act 4: Deep Dive Explorer",
    "Act 5: The Predictive Engine",
])

with tab_state:
    st.markdown(section_hdr(
        "The Pulse of Tamil Nadu — Big Picture at a Glance",
        "Statewide seat count, volatility, and turnout stripped down to what matters on air."
    ), unsafe_allow_html=True)

    st.markdown(tp_box(
        "Open with the 84.69% turnout headline — then immediately pause and ask: "
        "'But here is the question no one asked on election night.' The 20-Lakh reality check is "
        "your prime-time hook. The viewer already knows who won. Make them understand how the "
        "arithmetic actually works. This cognitive dissonance is your Act 1."
    ), unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#A855F7;">{leading_seats}</div>
            <div class="metric-title">Who's Leading the House</div>
            <div class="metric-sub">{get_party_symbol(leading_party)} holds the plurality</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#06B6D4;">{flips_count}</div>
            <div class="metric-title">Incumbents Sent Packing</div>
            <div class="metric-sub">Seats that changed hands since 2021</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#F59E0B;">{flips_pct:.1f}%</div>
            <div class="metric-title">Electoral Churn Index</div>
            <div class="metric-sub">Share of constituencies that flipped</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#10B981;">{avg_turnout_26:.2f}%</div>
            <div class="metric-title">Turnout — A Record High</div>
            <div class="metric-sub">Boosted partly by a 46-Lakh voter-list clean</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="editorial-rule"></div>', unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown(story_ctx(
            "This chart tells the five-year story at a glance. What was a clear two-party "
            "state in 2021 — with DMK's absolute majority of 133 — is now a tri-polar contest. "
            "TVK entered with 0 seats. It leaves with 108."
        ), unsafe_allow_html=True)

        seats_26   = filtered_flips['party_2026'].value_counts()
        seats_21   = filtered_flips['party_2021'].value_counts()
        seats_comp = pd.concat([seats_21, seats_26], axis=1, keys=['2021', '2026']).fillna(0)
        seats_comp.index.name = 'Party'
        seats_comp = seats_comp.reset_index().sort_values(by='2026', ascending=False)

        fig_seats = go.Figure()
        fig_seats.add_trace(go.Bar(
            x=seats_comp['Party'], y=seats_comp['2021'], name='2021 (Outgoing)',
            marker_color='#475569', opacity=0.45
        ))
        fig_seats.add_trace(go.Bar(
            x=seats_comp['Party'], y=seats_comp['2026'], name='2026 (Current)',
            marker_color=[COLOR_MAP.get(p, COLOR_MAP['Others']) for p in seats_comp['Party']]
        ))
        chart_style(fig_seats, "The Balance of Power: Seats Won — 2021 vs 2026", height=380)
        fig_seats.update_layout(barmode='group')
        st.plotly_chart(fig_seats, use_container_width=True)

    with col_c2:
        st.markdown(story_ctx(
            "Seat counts can be deceiving — a party can win many seats on razor-thin margins. "
            "Vote share anchors the seat story in actual voter preference. The gap between "
            "TVK's seat count and its raw vote share is the editorial sub-story worth exploring."
        ), unsafe_allow_html=True)

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
        chart_style(fig_votes, "Statewide Vote Share — Who Won the Raw Ballot", height=380)
        fig_votes.update_layout(showlegend=False,
                                yaxis=dict(gridcolor='#1E293B', categoryorder='total ascending'))
        fig_votes.update_traces(textposition='outside', textfont=dict(size=11))
        st.plotly_chart(fig_votes, use_container_width=True)


with tab_regions:
    st.markdown(section_hdr(
        "Battleground Spotlights — Tamil Nadu's Six Electoral Theatres",
        "Each region has its own political DNA. This is where the real swings happened — and where old loyalties held firm."
    ), unsafe_allow_html=True)

    st.markdown(tp_box(
        "Walk the audience through each region as if you're narrating a battle map. "
        "Chennai Metro is your opening salvo — TVK swept 29 of 32 seats. "
        "In Kongu, show the AIADMK bastion crumbling from 19 seats to 7. "
        "The regional contrast drives the editorial tension in your Act 2 segment."
    ), unsafe_allow_html=True)

    reg_list   = list(filtered_flips['region'].unique())
    selected_reg = st.selectbox(
        "Select Regional Theatre to Spotlight",
        options=reg_list,
        help="Each region tells a different political story."
    )

    reg_flips = filtered_flips[filtered_flips['region'] == selected_reg]

    r_total      = len(reg_flips)
    r_flips      = int(reg_flips['is_flip'].sum())
    r_flip_pct   = (r_flips / r_total * 100) if r_total > 0 else 0
    r_avg_margin = reg_flips['margin_2026'].mean() if r_total > 0 else 0

    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#A855F7;">{r_total}</div>
            <div class="metric-title">Total Seats in Region</div>
        </div>""", unsafe_allow_html=True)
    with rc2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#06B6D4;">{r_flips}</div>
            <div class="metric-title">Seats that Changed Hands</div>
        </div>""", unsafe_allow_html=True)
    with rc3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#F59E0B;">{r_flip_pct:.1f}%</div>
            <div class="metric-title">Regional Churn Rate</div>
        </div>""", unsafe_allow_html=True)
    with rc4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#10B981;">{r_avg_margin:.1f}%</div>
            <div class="metric-title">Average Victory Margin</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="editorial-rule"></div>', unsafe_allow_html=True)

    col_r1, col_r2 = st.columns([1, 1])

    with col_r1:
        st.markdown(story_ctx(
            f"The grouped bar shows the full seat shift in {selected_reg} — compare the "
            f"muted 2021 bars against the current 2026 results. Look for parties that "
            f"gained or lost dramatically. That contrast is your on-air talking point."
        ), unsafe_allow_html=True)

        reg_s26   = reg_flips['party_2026'].value_counts()
        reg_s21   = reg_flips['party_2021'].value_counts()
        reg_comp  = pd.concat([reg_s21, reg_s26], axis=1, keys=['2021', '2026']).fillna(0)
        reg_comp.index.name = 'Party'
        reg_comp  = reg_comp.reset_index().sort_values(by='2026', ascending=False)

        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(x=reg_comp['Party'], y=reg_comp['2021'],
                                 name='2021', marker_color='#475569', opacity=0.45))
        fig_reg.add_trace(go.Bar(
            x=reg_comp['Party'], y=reg_comp['2026'], name='2026',
            marker_color=[COLOR_MAP.get(p, COLOR_MAP['Others']) for p in reg_comp['Party']]
        ))
        chart_style(fig_reg, f"{selected_reg} — Seat Shift 2021 vs 2026", height=360)
        fig_reg.update_layout(barmode='group')
        st.plotly_chart(fig_reg, use_container_width=True)

    with col_r2:
        st.markdown(story_ctx(
            "The margin heatmap separates comfortable wins from nail-biters. Green dots are "
            "decisive victories; red dots are constituencies that could have swung the other "
            "way with a few thousand votes. These thin-margin seats are your live drama moments."
        ), unsafe_allow_html=True)

        fig_heat = px.scatter(
            reg_flips, x='constituency', y='margin_2026',
            color='margin_2026', color_continuous_scale='RdYlGn',
            size='margin_2026', size_max=16,
            labels={'margin_2026': 'Victory Margin (%)', 'constituency': 'Constituency'},
            hover_name='constituency',
            hover_data={'party_2026': True, 'margin_2026': ':.2f'}
        )
        chart_style(fig_heat, "Victory Margin Heatmap — Thin Wins vs Safe Holds", height=360)
        fig_heat.update_layout(xaxis=dict(gridcolor='#1E293B', tickangle=45))
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown(section_hdr(
        f"Full Scorecard — {selected_reg} Region",
        f"All {r_total} constituencies: who held, who flipped, and by how much."
    ), unsafe_allow_html=True)

    table_df = reg_flips[['constituency', 'party_2021', 'party_2026',
                           'margin_2026', 'is_flip', 'turnout_2026']].copy()
    table_df['2021 Winner'] = table_df['party_2021'].map(get_party_symbol)
    table_df['2026 Winner'] = table_df['party_2026'].map(get_party_symbol)

    st.dataframe(
        table_df[['constituency', '2021 Winner', '2026 Winner',
                  'margin_2026', 'is_flip', 'turnout_2026']].rename(
            columns={'constituency': 'Assembly Constituency',
                     'margin_2026': 'Victory Margin (%)',
                     'is_flip': 'Seat Flipped?',
                     'turnout_2026': 'Turnout 2026 (%)'}
        ).sort_values(by='Victory Margin (%)'),
        hide_index=True, use_container_width=True, height=360
    )


with tab_flips_view:
    st.markdown(section_hdr(
        "Where Voters Flipped the Script",
        f"Out of {total_seats} seats — {flips_count} incumbents were voted out. Volatility Index: {flips_pct:.1f}%"
    ), unsafe_allow_html=True)

    st.markdown(tp_box(
        "This is the 'churn segment' of your show. Lead with the raw number — "
        f"{flips_count} of {total_seats} seats changed hands. Then bring up the donut chart: "
        "it reveals exactly *who* the leading party took those seats from. "
        "If it's Tamil Nadu, 60% came directly from DMK. That single stat is your Act 3 hook — "
        "it tells you this was not just a new wave, it was a direct transfer of mandate."
    ), unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1, 1.15])

    with col_f1:
        st.markdown(story_ctx(
            "The donut chart shows the anatomy of the leading party's victory — "
            "specifically which parties it took seats from. "
            "A large single slice means one party was the main donor. "
            "That relationship is your editorial thread for the transfer-of-mandate story."
        ), unsafe_allow_html=True)

        flip_data = filtered_flips[filtered_flips['is_flip']]
        if len(flip_data) > 0:
            top_party  = filtered_flips['party_2026'].value_counts().index[0]
            flow_df    = (filtered_flips[filtered_flips['party_2026'] == top_party]
                          .groupby('party_2021').size().reset_index(name='Seats')
                          .sort_values(by='Seats', ascending=False))

            fig_donut = px.pie(
                flow_df, values='Seats', names='party_2021',
                hole=0.42, color='party_2021', color_discrete_map=COLOR_MAP
            )
            chart_style(fig_donut, f"{top_party}'s Seat Gains — Which Party Donated Them?", height=400)
            fig_donut.update_layout(legend=dict(orientation="h", y=-0.12))
            fig_donut.update_traces(textposition='outside', textinfo='label+percent')
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No flipped seats in the current filter selection.")

    with col_f2:
        st.markdown(story_ctx(
            "Every row in this table is a constituency where the electorate actively "
            "chose to change its representative. Sort by turnout to find where new voter "
            "mobilisation drove the flip — or sort by region for a geographic narrative arc."
        ), unsafe_allow_html=True)

        only_flips = filtered_flips[filtered_flips['is_flip']].copy()
        only_flips['2021 Winner'] = only_flips['party_2021'].map(get_party_symbol)
        only_flips['2026 Winner'] = only_flips['party_2026'].map(get_party_symbol)

        st.dataframe(
            only_flips[['constituency', 'region', '2021 Winner', '2026 Winner',
                         'votes_2026', 'turnout_2026']].rename(
                columns={'constituency': 'Constituency',
                         'region': 'Region',
                         'votes_2026': 'Votes Polled',
                         'turnout_2026': 'Turnout (%)'}
            ).sort_values(by='Constituency'),
            hide_index=True, use_container_width=True, height=430
        )


with tab_search:
    st.markdown(section_hdr(
        "Deep Dive Explorer — One Constituency at a Time",
        "Search any seat to get the full before-and-after picture, candidate breakdown, and swing context."
    ), unsafe_allow_html=True)

    st.markdown(tp_box(
        "Use this during counting day for live constituency call-outs. Pick a specific "
        "battleground — Chepauk, Coimbatore South, or Madurai Central — and walk the viewer "
        "through the 2021 vs 2026 winner cards side-by-side. The candidate vote bar chart is "
        "your live B-roll visual. Narrate the margin of victory to humanise the data."
    ), unsafe_allow_html=True)

    all_acs    = sorted(list(df_flips['constituency'].unique()))
    selected_ac = st.selectbox(
        "Search and Select a Constituency",
        options=all_acs,
        help="Type to search any of the 234 assembly constituencies."
    )

    ac_data = df_flips[df_flips['constituency'] == selected_ac].iloc[0]

    st.markdown(f"""
    <div style="margin-bottom:6px;">
        <span style="font-size:22px;font-weight:900;color:#FFFFFF;">
            {selected_ac}
        </span>
        <span style="font-size:13px;color:#64748B;margin-left:10px;">
            AC #{int(ac_data['ac_number'])}
        </span>
    </div>
    <p style="font-size:13px;color:#64748B;margin:0 0 4px;">
        Region: <strong style="color:#94A3B8;">{ac_data['region']}</strong>
        &nbsp;|&nbsp; Category: <strong style="color:#94A3B8;">{ac_data['reserved']}</strong>
        &nbsp;|&nbsp; Turnout Shift:
        <strong style="color:#10B981;">+{(ac_data['turnout_2026'] - ac_data['turnout_2021']):.2f}%</strong>
    </p>
    <div class="editorial-rule"></div>
    """, unsafe_allow_html=True)

    cc1, cc2, cc3 = st.columns(3)
    c21_col   = COLOR_MAP.get(ac_data['party_2021'], '#64748B')
    c26_col   = COLOR_MAP.get(ac_data['party_2026'], '#A855F7')
    flip_col  = '#10B981' if ac_data['is_flip'] else '#64748B'
    flip_text = 'SEAT FLIPPED' if ac_data['is_flip'] else 'SEAT RETAINED'

    with cc1:
        st.markdown(f"""
        <div class="metric-card" style="border-left:5px solid {c21_col};">
            <div class="metric-title">2021 Incumbent</div>
            <div class="metric-value" style="color:{c21_col};font-size:32px;">
                {get_party_symbol(ac_data['party_2021'])}
            </div>
            <div class="metric-sub">Turnout: {ac_data['turnout_2021']:.2f}%</div>
            <div class="metric-sub">Margin: {ac_data['margin_2021']:.2f}%</div>
        </div>""", unsafe_allow_html=True)

    with cc2:
        st.markdown(f"""
        <div class="metric-card" style="border-left:5px solid {c26_col};">
            <div class="metric-title">2026 Winner</div>
            <div class="metric-value" style="color:{c26_col};font-size:32px;">
                {get_party_symbol(ac_data['party_2026'])}
            </div>
            <div class="metric-sub">Turnout: {ac_data['turnout_2026']:.2f}%</div>
            <div class="metric-sub">Margin: {ac_data['margin_2026']:.2f}%</div>
        </div>""", unsafe_allow_html=True)

    with cc3:
        st.markdown(f"""
        <div class="metric-card" style="border-left:5px solid {flip_col};">
            <div class="metric-title">Verdict</div>
            <div class="metric-value" style="color:{flip_col};font-size:26px;">
                {flip_text}
            </div>
            <div class="metric-sub">
                Swing Probability: {ac_data['swing_probability']*100:.1f} out of 100
            </div>
        </div>""", unsafe_allow_html=True)

    cv1, cv2 = st.columns(2)

    with cv1:
        st.markdown(story_ctx(
            "The candidate bar gives a ground-level view of the race — not just who won, "
            "but by how much, and who the closest challenger was. "
            "A candidate with under 35% share in a three-cornered contest may have won "
            "on pure vote-split, not genuine majority support."
        ), unsafe_allow_html=True)

        if selected_state == "Tamil Nadu":
            ac_cands = (df_2026[df_2026['ac_number'] == ac_data['ac_number']]
                        .sort_values(by='votes', ascending=False).head(4))
            tot_v = df_2026[df_2026['ac_number'] == ac_data['ac_number']]['votes'].sum()
            ac_cands = ac_cands.copy()
            ac_cands['Share (%)'] = round(ac_cands['votes'] / tot_v * 100, 2)

            fig_cand = px.bar(
                ac_cands, x='Share (%)', y='candidate', orientation='h',
                color='party_std', color_discrete_map=COLOR_MAP, text='Share (%)'
            )
            chart_style(fig_cand, "How the Vote Split — Top 4 Candidates", height=300)
            fig_cand.update_layout(showlegend=False,
                                   yaxis=dict(gridcolor='#1E293B', categoryorder='total ascending'))
            fig_cand.update_traces(textposition='outside', textfont=dict(size=11))
            st.plotly_chart(fig_cand, use_container_width=True)
        else:
            st.info("Candidate-level detail is available for the Tamil Nadu live feed only.")

    with cv2:
        st.markdown(story_ctx(
            "The full candidate vote table is your reference during a live broadcast — "
            "read out the winner's exact vote count, the runner-up's tally, and the margin "
            "to give the viewer the human-scale sense of how close or decisive this result was."
        ), unsafe_allow_html=True)

        if selected_state == "Tamil Nadu":
            ac_full = (df_2026[df_2026['ac_number'] == ac_data['ac_number']]
                       .sort_values(by='votes', ascending=False))
            st.dataframe(
                ac_full[['candidate', 'party_std', 'votes']].rename(
                    columns={'candidate': 'Candidate', 'party_std': 'Party', 'votes': 'Votes Received'}
                ),
                hide_index=True, use_container_width=True, height=300
            )
        else:
            st.dataframe(
                pd.DataFrame([
                    {'Candidate': 'Winner Candidate',    'Party': ac_data['party_2026'],
                     'Votes Received': ac_data['votes_2026']},
                    {'Candidate': 'Runner-up Candidate', 'Party': ac_data['party_2021'],
                     'Votes Received': int(ac_data['votes_2026'] * 0.80)},
                ]),
                hide_index=True, use_container_width=True, height=300
            )


with tab_predict:
    st.markdown(section_hdr(
        "The Predictive Engine — Decoding Swing Seat Probability",
        "Our decision desk model scored every constituency on flip likelihood before counting day."
    ), unsafe_allow_html=True)

    st.markdown(tp_box(
        "Do NOT say 'logistic regression classifier' on air. Instead say: "
        "'Our decision desk ran every constituency through a flip-likelihood score from 0 to 100. "
        "Any seat scoring above 50 was flagged as active swing territory.' "
        "The model called the TVK plurality before 6 PM. Lead with that — it is your "
        "data credibility moment and the backbone of your Act 5 segment."
    ), unsafe_allow_html=True)

    predicted_swings = int((filtered_flips['swing_probability'] >= 0.5).sum())
    avg_sp           = filtered_flips['swing_probability'].mean() * 100

    pm1, pm2, pm3 = st.columns(3)

    with pm1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color:#06B6D4;">70.94%</div>
            <div class="metric-title">Model Accuracy</div>
            <div class="metric-sub">Correctly called 7 in 10 seat outcomes</div>
        </div>""", unsafe_allow_html=True)

    with pm2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#A855F7;">{predicted_swings}</div>
            <div class="metric-title">Active Swing Seats Flagged</div>
            <div class="metric-sub">Scored above 50 out of 100 pre-election</div>
        </div>""", unsafe_allow_html=True)

    with pm3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#F59E0B;">{avg_sp:.1f}</div>
            <div class="metric-title">Average Swing Score</div>
            <div class="metric-sub">Out of 100 across all filtered seats</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="editorial-rule"></div>', unsafe_allow_html=True)

    st.markdown(story_ctx(
        "The scatter plot maps two inputs: how safe the 2021 winner was (x-axis, their margin) "
        "and how much the electorate changed (y-axis, turnout surge). "
        "Red dots are high-flip-probability seats. The pattern is clear — low margin plus "
        "high surge equals near-certain flip. It is electoral physics."
    ), unsafe_allow_html=True)

    fig_sc = px.scatter(
        filtered_flips, x='margin_2021', y='turnout_surge',
        color='swing_probability', size='swing_probability',
        hover_name='constituency', color_continuous_scale='RdYlGn_r',
        labels={
            'margin_2021':       'Safety Margin — How Comfortable Was the 2021 Winner (%)',
            'turnout_surge':     'Bootup Surge — Clean Rolls Shifted the Math (%)',
            'swing_probability': 'Flip Score (0-100)'
        }
    )
    chart_style(fig_sc,
                "Turnout Bootup Surge vs 2021 Safety Margin — The Swing Probability Map",
                height=440)
    fig_sc.update_layout(
        coloraxis_colorbar=dict(
            title='Flip Score',
            tickvals=[0.0, 0.25, 0.5, 0.75, 1.0],
            ticktext=['0', '25', '50', '75', '100'],
            tickfont=dict(color='#94A3B8')
        )
    )
    st.plotly_chart(fig_sc, use_container_width=True)

    st.markdown(section_hdr(
        "Swing Seat Watchlist — Ranked by Flip Score",
        "Seats are sorted from most to least volatile. Use this as your 'seats to watch' list during your broadcast."
    ), unsafe_allow_html=True)

    pred_df = filtered_flips[
        ['constituency', 'region', 'party_2021', 'margin_2021', 'turnout_surge', 'swing_probability']
    ].copy()
    pred_df['2021 Incumbent'] = pred_df['party_2021'].map(get_party_symbol)

    def risk_label(p):
        if p >= 0.75: return "HIGH RISK"
        if p >= 0.50: return "ON THE EDGE"
        return "LIKELY SAFE"

    pred_df['Flip Score (0-100)'] = (pred_df['swing_probability'] * 100).round(1)
    pred_df['Risk Rating']        = pred_df['swing_probability'].apply(risk_label)

    st.dataframe(
        pred_df[['constituency', 'region', '2021 Incumbent',
                 'margin_2021', 'turnout_surge', 'Flip Score (0-100)', 'Risk Rating']].rename(
            columns={
                'constituency':  'Constituency',
                'region':        'Region',
                'margin_2021':   'Safety Margin 2021 (%)',
                'turnout_surge': 'Bootup Surge (%)',
            }
        ).sort_values(by='Flip Score (0-100)', ascending=False),
        hide_index=True, use_container_width=True, height=440
    )
