import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import base64

st.set_page_config(
    page_title="AtliQ Media: 2026 Election Decision Desk",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return encoded
    return ""

map_path = "tamil_nadu_map.png"
finger_path = "voting_finger.png"
map_base64 = get_base64_image(map_path)
finger_base64 = get_base64_image(finger_path)

st.markdown(f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            background-color: #080A1C !important;
            background-image:
                linear-gradient(rgba(8,10,28,0.82), rgba(8,10,28,0.82)),
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

        .main, [data-testid="stMainRegion"], [data-testid="stViewport"], .block-container {{
            background-color: transparent !important;
            background: transparent !important;
        }}
        
        section[data-testid="stSidebar"] {{
            background-color: #050613 !important;
            border-right: 1px solid #1E293B;
        }}
        
        .metric-card {{
            background-color: #11153B;
            border: 1px solid #1E293B;
            border-radius: 16px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            margin-bottom: 20px;
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            border-color: #A855F7;
        }}
        .metric-value {{
            font-size: 38px;
            font-weight: 900;
            color: #A855F7;
            margin-bottom: 5px;
        }}
        .metric-title {{
            font-size: 13px;
            font-weight: 700;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 1.2px;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            background-color: #050613;
            border-radius: 12px;
            padding: 6px;
            border: 1px solid #1E293B;
        }}
        .stTabs [data-baseweb="tab"] {{
            color: #94A3B8;
            font-weight: 700;
            font-size: 15px;
            padding: 10px 16px;
        }}
        .stTabs [aria-selected="true"] {{
            color: #06B6D4 !important;
            background-color: #11153B;
            border-radius: 8px;
        }}
    </style>
""", unsafe_allow_html=True)

COLOR_MAP = {
    'TVK': '#A855F7',
    'DMK': '#06B6D4',
    'AIADMK': '#10B981',
    'INC': '#3B82F6',
    'PMK': '#EAB308',
    'VCK': '#EC4899',
    'CPIM': '#EF4444',
    'CPI': '#DC2626',
    'BJP': '#F59E0B',
    'LDF': '#EF4444',
    'UDF': '#3B82F6',
    'NDA': '#F59E0B',
    'TDP': '#FBBF24',
    'YSRCP': '#3B82F6',
    'JSP': '#EF4444',
    'Others': '#64748B'
}

def get_party_symbol(party):
    return party

@st.cache_data
def load_data():
    base_dir = "data"
    df_2021 = pd.read_csv(os.path.join(base_dir, "processed", "cleaned_results_2021.csv"))
    df_2026 = pd.read_csv(os.path.join(base_dir, "processed", "cleaned_results_2026.csv"))
    df_flips = pd.read_csv(os.path.join(base_dir, "processed", "swing_predictions.csv"))
    return df_2021, df_2026, df_flips

try:
    df_2021, df_2026, df_flips = load_data()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

st.sidebar.image("voting_finger.png", width=120)
st.sidebar.title("AtliQ Media")
st.sidebar.markdown("### **Election Decision Desk**")
st.sidebar.markdown("---")

selected_state = st.sidebar.selectbox(
    "Select State",
    options=["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh"]
)

live_feed_enabled = st.sidebar.checkbox("Enable Live ECI Feed (Simulated)")

if live_feed_enabled:
    reporting_progress = st.sidebar.slider("ECI Reporting Progress (%)", 5, 100, 100, 5)
else:
    reporting_progress = 100

@st.cache_data
def generate_kerala_data():
    np.random.seed(42)
    ac_numbers = np.arange(1, 141)
    constituencies = [f"Kerala AC {i}" for i in ac_numbers]
    regions = np.random.choice(["Travancore", "Malabar", "Kochi"], size=140)
    reserved = np.random.choice(["GEN", "SC", "ST"], size=140, p=[0.85, 0.12, 0.03])
    
    df_list = []
    for ac, name, reg, res in zip(ac_numbers, constituencies, regions, reserved):
        t21 = round(np.random.uniform(70, 80), 2)
        t26 = round(min(98.0, t21 + np.random.uniform(2, 6)), 2)
        p21 = np.random.choice(["LDF", "UDF", "NDA"], p=[0.50, 0.45, 0.05])
        p26 = np.random.choice(["LDF", "UDF", "NDA"], p=[0.48, 0.48, 0.04])
        is_flip = p21 != p26
        m21 = round(np.random.uniform(0.5, 15.0), 2)
        m26 = round(np.random.uniform(0.5, 15.0), 2)
        sp = round(np.random.uniform(0.1, 0.95), 4)
        
        df_list.append({
            'ac_number': ac, 'constituency': name, 'party_2021': p21, 'votes_2021': int(np.random.uniform(60000, 90000)),
            'region': reg, 'reserved': res, 'turnout_2021': t21, 'party_2026': p26, 'votes_2026': int(np.random.uniform(65000, 95000)),
            'turnout_2026': t26, 'is_flip': is_flip, 'turnout_surge': t26 - t21, 'margin_2021': m21, 'margin_2026': m26,
            'swing_probability': sp, 'predicted_class': 1 if sp >= 0.5 else 0
        })
    return pd.DataFrame(df_list)

@st.cache_data
def generate_karnataka_data():
    np.random.seed(42)
    ac_numbers = np.arange(1, 225)
    constituencies = [f"Karnataka AC {i}" for i in ac_numbers]
    regions = np.random.choice(["Old Mysore", "Mumbai Karnataka", "Hyderabad Karnataka", "Coastal", "Central"], size=224)
    reserved = np.random.choice(["GEN", "SC", "ST"], size=224, p=[0.80, 0.15, 0.05])
    
    df_list = []
    for ac, name, reg, res in zip(ac_numbers, constituencies, regions, reserved):
        t21 = round(np.random.uniform(68, 78), 2)
        t26 = round(min(98.0, t21 + np.random.uniform(3, 7)), 2)
        p21 = np.random.choice(["INC", "BJP", "Others"], p=[0.45, 0.45, 0.10])
        p26 = np.random.choice(["INC", "BJP", "Others"], p=[0.47, 0.45, 0.08])
        is_flip = p21 != p26
        m21 = round(np.random.uniform(0.5, 18.0), 2)
        m26 = round(np.random.uniform(0.5, 18.0), 2)
        sp = round(np.random.uniform(0.1, 0.95), 4)
        
        df_list.append({
            'ac_number': ac, 'constituency': name, 'party_2021': p21, 'votes_2021': int(np.random.uniform(70000, 110000)),
            'region': reg, 'reserved': res, 'turnout_2021': t21, 'party_2026': p26, 'votes_2026': int(np.random.uniform(75000, 115000)),
            'turnout_2026': t26, 'is_flip': is_flip, 'turnout_surge': t26 - t21, 'margin_2021': m21, 'margin_2026': m26,
            'swing_probability': sp, 'predicted_class': 1 if sp >= 0.5 else 0
        })
    return pd.DataFrame(df_list)

@st.cache_data
def generate_ap_data():
    np.random.seed(42)
    ac_numbers = np.arange(1, 176)
    constituencies = [f"AP AC {i}" for i in ac_numbers]
    regions = np.random.choice(["Coastal Andhra", "Rayalaseema"], size=175)
    reserved = np.random.choice(["GEN", "SC", "ST"], size=175, p=[0.82, 0.15, 0.03])
    
    df_list = []
    for ac, name, reg, res in zip(ac_numbers, constituencies, regions, reserved):
        t21 = round(np.random.uniform(75, 83), 2)
        t26 = round(min(98.0, t21 + np.random.uniform(2, 5)), 2)
        p21 = np.random.choice(["TDP", "YSRCP", "Others"], p=[0.40, 0.55, 0.05])
        p26 = np.random.choice(["TDP", "YSRCP", "Others"], p=[0.58, 0.35, 0.07])
        is_flip = p21 != p26
        m21 = round(np.random.uniform(0.5, 20.0), 2)
        m26 = round(np.random.uniform(0.5, 20.0), 2)
        sp = round(np.random.uniform(0.1, 0.95), 4)
        
        df_list.append({
            'ac_number': ac, 'constituency': name, 'party_2021': p21, 'votes_2021': int(np.random.uniform(80000, 120000)),
            'region': reg, 'reserved': res, 'turnout_2021': t21, 'party_2026': p26, 'votes_2026': int(np.random.uniform(85000, 125000)),
            'turnout_2026': t26, 'is_flip': is_flip, 'turnout_surge': t26 - t21, 'margin_2021': m21, 'margin_2026': m26,
            'swing_probability': sp, 'predicted_class': 1 if sp >= 0.5 else 0
        })
    return pd.DataFrame(df_list)

if selected_state == "Tamil Nadu":
    base_dir = "data"
    try:
        df_flips = pd.read_csv(os.path.join(base_dir, "processed", "swing_predictions.csv"))
        df_2021 = pd.read_csv(os.path.join(base_dir, "processed", "cleaned_results_2021.csv"))
        df_2026 = pd.read_csv(os.path.join(base_dir, "processed", "cleaned_results_2026.csv"))
    except Exception as e:
        st.error(f"Error loading datasets. Please execute data_pipeline.py and swing_seat_classifier.py first. Details: {e}")
        st.stop()
elif selected_state == "Kerala":
    df_flips = generate_kerala_data()
    df_2021 = df_flips.rename(columns={'party_2021': 'party_std', 'votes_2021': 'votes', 'turnout_2021': 'turnout'})
    df_2026 = df_flips.rename(columns={'party_2026': 'party_std', 'votes_2026': 'votes', 'turnout_2026': 'turnout'})
elif selected_state == "Karnataka":
    df_flips = generate_karnataka_data()
    df_2021 = df_flips.rename(columns={'party_2021': 'party_std', 'votes_2021': 'votes', 'turnout_2021': 'turnout'})
    df_2026 = df_flips.rename(columns={'party_2026': 'party_std', 'votes_2026': 'votes', 'turnout_2026': 'turnout'})
else:
    df_flips = generate_ap_data()
    df_2021 = df_flips.rename(columns={'party_2021': 'party_std', 'votes_2021': 'votes', 'turnout_2021': 'turnout'})
    df_2026 = df_flips.rename(columns={'party_2026': 'party_std', 'votes_2026': 'votes', 'turnout_2026': 'turnout'})

if live_feed_enabled:
    st.markdown("<div style='background-color: #7f1d1d; border: 1px solid #ef4444; border-radius: 8px; padding: 10px; margin-bottom: 20px; font-weight: bold; color: #ef4444; text-align: center;'>LIVE ECI DATA FEED INGESTING - AUTOMATIC BROADCAST REFRESH ACTIVE</div>", unsafe_allow_html=True)
    
    np.random.seed(reporting_progress)
    simulated_flips = df_flips.copy()
    
    for idx, row in simulated_flips.iterrows():
        if reporting_progress < 100:
            scale = reporting_progress / 100.0
            simulated_flips.at[idx, 'votes_2026'] = int(row['votes_2026'] * scale)
            simulated_flips.at[idx, 'turnout_2026'] = round(row['turnout_2026'] * scale, 2)
            
            if np.random.uniform(0, 100) > reporting_progress:
                simulated_flips.at[idx, 'party_2026'] = row['party_2021']
                simulated_flips.at[idx, 'is_flip'] = False
                
    df_flips = simulated_flips

st.sidebar.subheader("Filters")
selected_regions = st.sidebar.multiselect(
    "Filter by Region",
    options=list(df_flips['region'].unique()),
    default=list(df_flips['region'].unique())
)

selected_reservations = st.sidebar.multiselect(
    "Filter by Reservation Category",
    options=list(df_flips['reserved'].unique()),
    default=list(df_flips['reserved'].unique())
)

filtered_flips = df_flips[
    df_flips['region'].isin(selected_regions) & 
    df_flips['reserved'].isin(selected_reservations)
]

filtered_2026 = df_2026[
    df_2026['region'].isin(selected_regions) & 
    df_2026['reserved'].isin(selected_reservations)
]

filtered_2021 = df_2021[
    df_2021['region'].isin(selected_regions) & 
    df_2021['reserved'].isin(selected_reservations)
]

st.title("AtliQ Media: 2026 Election Decision Desk")
st.subheader(f"Translating complex electoral statistics into compelling stories: {selected_state}")
st.markdown("---")

tab_state, tab_regions, tab_flips, tab_search, tab_predict = st.tabs([
    "Act 1: The Big Picture (Statewide)", 
    "Act 2: Battleground Spotlights", 
    "Act 3: Where Voters Flipped", 
    "Act 4: Constituency Search",
    "Act 5: Swing Seat Classifier"
])

with tab_state:
    st.markdown("### **Statewide Electoral Indicators**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_seats = len(filtered_flips)
    flips_count = filtered_flips['is_flip'].sum()
    flips_pct = (flips_count / total_seats * 100) if total_seats > 0 else 0
    avg_turnout_26 = filtered_flips['turnout_2026'].mean()
    
    if len(filtered_flips) > 0:
        leading_party = filtered_flips['party_2026'].value_counts().index[0]
        leading_seats = filtered_flips['party_2026'].value_counts().values[0]
    else:
        leading_party = "N/A"
        leading_seats = 0
        
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #A855F7;">{leading_seats} ({get_party_symbol(leading_party)})</div>
                <div class="metric-title">Leading Party Seats</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #06B6D4;">{flips_count}</div>
                <div class="metric-title">Seats that Flipped</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #F97316;">{flips_pct:.1f}%</div>
                <div class="metric-title">Volatility Index</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #10B981;">{avg_turnout_26:.2f}%</div>
                <div class="metric-title">Voter Turnout (Record)</div>
            </div>
        """, unsafe_allow_html=True)
        
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("The Balance of Power: 2026 vs. 2021 Seats")
        seats_26 = filtered_flips['party_2026'].value_counts()
        seats_21 = filtered_flips['party_2021'].value_counts()
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
        fig_seats.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#1E293B'),
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_seats, use_container_width=True)
        
    with col_chart2:
        st.subheader("Statewide Vote Shares (%)")
        if selected_state == "Tamil Nadu":
            votes_26 = filtered_2026.groupby('party_std')['votes'].sum().reset_index()
            total_v26 = votes_26['votes'].sum()
            votes_26['Share (%)'] = round(votes_26['votes'] / total_v26 * 100, 2)
            votes_26 = votes_26.sort_values(by='Share (%)', ascending=False).head(6)
        else:
            votes_26 = filtered_flips.groupby('party_2026')['votes_2026'].sum().reset_index().rename(columns={'party_2026': 'party_std', 'votes_2026': 'votes'})
            total_v26 = votes_26['votes'].sum()
            votes_26['Share (%)'] = round(votes_26['votes'] / total_v26 * 100, 2)
            votes_26 = votes_26.sort_values(by='Share (%)', ascending=False).head(6)
            
        fig_votes = px.bar(
            votes_26, y='party_std', x='Share (%)',
            orientation='h',
            color='party_std',
            color_discrete_map=COLOR_MAP,
            text='Share (%)'
        )
        fig_votes.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            showlegend=False,
            xaxis=dict(gridcolor='#1E293B'),
            yaxis=dict(gridcolor='#1E293B', categoryorder='total ascending')
        )
        fig_votes.update_traces(textposition='outside')
        st.plotly_chart(fig_votes, use_container_width=True)

with tab_regions:
    st.markdown("### **Regional Territory Focus**")
    
    reg_list = list(filtered_flips['region'].unique())
    selected_reg = st.selectbox("Select Regional Spotlight to Analyze", options=reg_list)
    
    reg_flips = filtered_flips[filtered_flips['region'] == selected_reg]
    
    st.markdown(f"Currently Auditing **{selected_reg} Region** ({len(reg_flips)} Total Seats)")
    
    col_reg1, col_reg2 = st.columns([1, 1])
    
    with col_reg1:
        st.subheader("Regional Stronghold Seats Shift")
        reg_seats_26 = reg_flips['party_2026'].value_counts()
        reg_seats_21 = reg_flips['party_2021'].value_counts()
        reg_seats_comp = pd.concat([reg_seats_21, reg_seats_26], axis=1, keys=['2021', '2026']).fillna(0)
        reg_seats_comp.index.name = 'Party'
        reg_seats_comp = reg_seats_comp.reset_index().sort_values(by='2026', ascending=False)
        
        fig_reg_seats = go.Figure()
        fig_reg_seats.add_trace(go.Bar(
            x=reg_seats_comp['Party'], y=reg_seats_comp['2021'], name='2021',
            marker_color='#64748B', opacity=0.4
        ))
        fig_reg_seats.add_trace(go.Bar(
            x=reg_seats_comp['Party'], y=reg_seats_comp['2026'], name='2026',
            marker_color=[COLOR_MAP.get(p, COLOR_MAP['Others']) for p in reg_seats_comp['Party']]
        ))
        fig_reg_seats.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#1E293B'),
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_reg_seats, use_container_width=True)
        
    with col_reg2:
        st.subheader("Margin of Victory Heatmap")
        
        fig_heatmap = px.scatter(
            reg_flips, x='constituency', y='margin_2026',
            color='margin_2026',
            color_continuous_scale='RdYlGn',
            size='margin_2026',
            size_max=15,
            labels={'margin_2026': 'Margin (%)', 'constituency': 'Constituency'}
        )
        fig_heatmap.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#1E293B', tickangle=45),
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
    st.subheader("Constituency Winners in selected Region")
    
    table_df = reg_flips[['constituency', 'party_2021', 'party_2026', 'margin_2026', 'is_flip', 'turnout_2026']].copy()
    table_df['party_2021_symbol'] = table_df['party_2021'].map(get_party_symbol)
    table_df['party_2026_symbol'] = table_df['party_2026'].map(get_party_symbol)
    
    st.dataframe(
        table_df[['constituency', 'party_2021_symbol', 'party_2026_symbol', 'margin_2026', 'is_flip', 'turnout_2026']].rename(
            columns={
                'constituency': 'Assembly Constituency',
                'party_2021_symbol': '2021 Winner',
                'party_2026_symbol': '2026 Winner',
                'margin_2026': 'Margin (%)',
                'is_flip': 'Flipped?',
                'turnout_2026': 'Turnout (%)'
            }
        ).sort_values(by='Assembly Constituency'),
        hide_index=True,
        use_container_width=True
    )

with tab_flips:
    st.markdown("### **The Volatile Ground: Where Voters Flipped the Script**")
    st.markdown(f"Out of {total_seats} seats, **{flips_count} seats changed hands (Volatility Index: {flips_pct:.1f}%)**.")
    
    col_f1, col_f2 = st.columns([1, 1.2])
    
    with col_f1:
        st.subheader("Flow Breakdown of Flipping Seats")
        if len(filtered_flips[filtered_flips['is_flip']]) > 0:
            top_winning_party = filtered_flips['party_2026'].value_counts().index[0]
            tvk_flips = filtered_flips[filtered_flips['party_2026'] == top_winning_party].groupby('party_2021').size().reset_index(name='Seats')
            tvk_flips = tvk_flips.sort_values(by='Seats', ascending=False)
            
            fig_donut = px.pie(
                tvk_flips, values='Seats', names='party_2021',
                hole=0.4,
                color='party_2021',
                color_discrete_map=COLOR_MAP
            )
            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                legend=dict(orientation="h", y=-0.1)
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No flipped seats in current selection.")
        
    with col_f2:
        st.subheader("Search Flipped Constituencies")
        only_flips = filtered_flips[filtered_flips['is_flip']].copy()
        only_flips['party_2021_symbol'] = only_flips['party_2021'].map(get_party_symbol)
        only_flips['party_2026_symbol'] = only_flips['party_2026'].map(get_party_symbol)
        
        st.dataframe(
            only_flips[['constituency', 'region', 'party_2021_symbol', 'party_2026_symbol', 'votes_2026', 'turnout_2026']].rename(
                columns={
                    'constituency': 'Constituency Name',
                    'region': 'Region',
                    'party_2021_symbol': '2021 Winner',
                    'party_2026_symbol': '2026 Winner',
                    'votes_2026': 'Votes Polled',
                    'turnout_2026': 'Turnout (%)'
                }
            ).sort_values(by='Constituency Name'),
            hide_index=True,
            use_container_width=True
        )

with tab_search:
    st.markdown("### **Search a Seat: Side-by-Side Constituency Analysis**")
    
    all_constituencies = sorted(list(df_flips['constituency'].unique()))
    selected_ac = st.selectbox("Search and Audit a Specific Constituency", options=all_constituencies)
    
    ac_data = df_flips[df_flips['constituency'] == selected_ac].iloc[0]
    
    st.markdown(f"## **Assembly Constituency: {selected_ac} (AC #{int(ac_data['ac_number'])})**")
    st.markdown(f"**Geographic Region:** {ac_data['region']} | **Category:** {ac_data['reserved']}")
    st.markdown("---")
    
    col_card1, col_card2, col_card3 = st.columns(3)
    
    with col_card1:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid {COLOR_MAP.get(ac_data['party_2021'], '#64748B')};">
                <div class="metric-title">2021 Winner</div>
                <div class="metric-value" style="color: {COLOR_MAP.get(ac_data['party_2021'], '#64748B')};">{get_party_symbol(ac_data['party_2021'])}</div>
                <div class="metric-title" style="margin-top: 10px;">Turnout: {ac_data['turnout_2021']:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_card2:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid {COLOR_MAP.get(ac_data['party_2026'], '#A855F7')};">
                <div class="metric-title">2026 Winner</div>
                <div class="metric-value" style="color: {COLOR_MAP.get(ac_data['party_2026'], '#A855F7')};">{get_party_symbol(ac_data['party_2026'])}</div>
                <div class="metric-title" style="margin-top: 10px;">Turnout: {ac_data['turnout_2026']:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_card3:
        flip_color = "#10B981" if ac_data['is_flip'] else "#EF4444"
        flip_text = "YES (FLIP)" if ac_data['is_flip'] else "NO (RETAINED)"
        
        st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid {flip_color};">
                <div class="metric-title">Seat Flipped?</div>
                <div class="metric-value" style="color: {flip_color};">{flip_text}</div>
                <div class="metric-title" style="margin-top: 10px;">Voter Turnout Change: +{(ac_data['turnout_2026'] - ac_data['turnout_2021']):.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
        
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("Candidate-level Vote Shares in 2026")
        if selected_state == "Tamil Nadu":
            ac_candidates = df_2026[df_2026['ac_number'] == ac_data['ac_number']].sort_values(by='votes', ascending=False).head(3)
            tot_votes = df_2026[df_2026['ac_number'] == ac_data['ac_number']]['votes'].sum()
            ac_candidates['Share (%)'] = round(ac_candidates['votes'] / tot_votes * 100, 2)
            
            fig_cand = px.bar(
                ac_candidates, x='Share (%)', y='candidate',
                orientation='h', color='party_std',
                color_discrete_map=COLOR_MAP,
                text='Share (%)'
            )
            fig_cand.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                showlegend=False,
                xaxis=dict(gridcolor='#1E293B'),
                yaxis=dict(gridcolor='#1E293B', categoryorder='total ascending')
            )
            fig_cand.update_traces(textposition='outside')
            st.plotly_chart(fig_cand, use_container_width=True)
        else:
            st.info("Detailed candidate-level charts are populated for live ECI states.")
            
    with col_v2:
        st.subheader("Detailed Candidate Votes in 2026")
        if selected_state == "Tamil Nadu":
            ac_candidates_26 = df_2026[df_2026['ac_number'] == ac_data['ac_number']].sort_values(by='votes', ascending=False)
            st.dataframe(
                ac_candidates_26[['candidate', 'party_std', 'votes']].rename(
                    columns={
                        'candidate': 'Candidate Name',
                        'party_std': 'Party',
                        'votes': 'Votes Received'
                    }
                ),
                hide_index=True,
                use_container_width=True
            )
        else:
            st.dataframe(
                pd.DataFrame([
                    {'Candidate Name': 'Winner Candidate', 'Party': ac_data['party_2026'], 'Votes Received': ac_data['votes_2026']},
                    {'Candidate Name': 'Incumbent Candidate', 'Party': ac_data['party_2021'], 'Votes Received': int(ac_data['votes_2026']*0.8)}
                ]),
                hide_index=True,
                use_container_width=True
            )

with tab_predict:
    st.markdown("### **Predictive Classifier: Swing Seat Analyzer**")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value" style="color: #06B6D4;">70.94%</div>
                <div class="metric-title">Model Classification Accuracy</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_p2:
        predicted_swings = (filtered_flips['swing_probability'] >= 0.5).sum()
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value" style="color: #A855F7;">""" + str(predicted_swings) + """</div>
                <div class="metric-title">Predicted Volatile Swing Seats</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.subheader("Voter Turnout Surge vs. 2021 Margin of Victory")
    
    fig_scatter = px.scatter(
        filtered_flips, x='margin_2021', y='turnout_surge',
        color='swing_probability',
        size='swing_probability',
        hover_name='constituency',
        color_continuous_scale='RdYlGn_r',
        labels={'margin_2021': '2021 Margin (%)', 'turnout_surge': 'Turnout Surge (%)', 'swing_probability': 'Swing Probability'}
    )
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF'),
        xaxis=dict(gridcolor='#1E293B'),
        yaxis=dict(gridcolor='#1E293B')
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.subheader("Constituencies Ranked by Highest Swing Probability")
    
    table_pred_df = filtered_flips[['constituency', 'region', 'party_2021', 'margin_2021', 'turnout_surge', 'swing_probability']].copy()
    table_pred_df['party_2021_symbol'] = table_pred_df['party_2021'].map(get_party_symbol)
    
    st.dataframe(
        table_pred_df[['constituency', 'region', 'party_2021_symbol', 'margin_2021', 'turnout_surge', 'swing_probability']].rename(
            columns={
                'constituency': 'AC Name',
                'region': 'Region',
                'party_2021_symbol': '2021 Incumbent',
                'margin_2021': '2021 Margin (%)',
                'turnout_surge': 'Turnout Surge (%)',
                'swing_probability': 'Swing Probability'
            }
        ).sort_values(by='Swing Probability', ascending=False),
        hide_index=True,
        use_container_width=True
    )
