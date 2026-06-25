import streamlit as st
import pandas as pd
import numpy as np
import time
import math
import random as rnd
from pathlib import Path

# Page config
st.set_page_config(
    page_title="🎡 Raffle Draw",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .winner-box {
        background-color: #FFD700;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

WHEEL_COLORS = [
    "#e74c3c","#e67e22","#f39c12","#2ecc71","#1abc9c",
    "#3498db","#9b59b6","#e91e63","#ff5722","#00bcd4","#8bc34a","#ff9800"
]

def build_wheel_svg(display_nums, rotation=0):
    n = len(display_nums)
    cx, cy, r = 200, 200, 185
    paths = []
    for i, num in enumerate(display_nums):
        start_deg = i * 360 / n
        end_deg   = (i + 1) * 360 / n
        sa = math.radians(start_deg - 90)
        ea = math.radians(end_deg - 90)
        x1 = cx + r * math.cos(sa);  y1 = cy + r * math.sin(sa)
        x2 = cx + r * math.cos(ea);  y2 = cy + r * math.sin(ea)
        large_arc = 1 if (end_deg - start_deg) > 180 else 0
        color = WHEEL_COLORS[i % len(WHEEL_COLORS)]
        paths.append(
            f'<path d="M {cx},{cy} L {x1:.1f},{y1:.1f} A {r},{r} 0 {large_arc},1 {x2:.1f},{y2:.1f} Z" '
            f'fill="{color}" stroke="white" stroke-width="3"/>'
        )
        mid_rad = math.radians((start_deg + end_deg) / 2 - 90)
        tx = cx + r * 0.68 * math.cos(mid_rad)
        ty = cy + r * 0.68 * math.sin(mid_rad)
        rot = (start_deg + end_deg) / 2
        paths.append(
            f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" dominant-baseline="middle" '
            f'fill="white" font-weight="bold" font-size="17" font-family="Arial" '
            f'transform="rotate({rot:.1f},{tx:.1f},{ty:.1f})">{num}</text>'
        )
    segments = ''.join(paths)
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;">
        <div style="width:0;height:0;border-left:18px solid transparent;border-right:18px solid transparent;
                    border-top:36px solid #2c3e50;margin-bottom:-4px;z-index:10;position:relative;"></div>
        <svg width="400" height="400" viewBox="0 0 400 400">
            <circle cx="200" cy="200" r="196" fill="#2c3e50"/>
            <g transform="rotate({rotation:.2f}, 200, 200)">
                {segments}
                <circle cx="200" cy="200" r="22" fill="#2c3e50"/>
                <circle cx="200" cy="200" r="12" fill="#ecf0f1"/>
            </g>
        </svg>
    </div>
    """

# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def load_raffle_data():
    return pd.read_excel(Path(__file__).parent / "Raffle_26Jun26.xlsx")

@st.cache_data
def prepare_draw_pool(df):
    """Returns eligible people with their ticket numbers, plus a flat number list for the wheel display."""
    avg_tickets = pd.to_numeric(df['Raffle Tickets'], errors='coerce').dropna().mean()
    min_required_tickets = int(math.ceil(avg_tickets)) if pd.notna(avg_tickets) else 0

    people = []        # [{name, numbers}]
    weights = []       # ticket count per person
    all_nums = []      # flat list of all eligible numbers (for wheel display only)
    for _, row in df.iterrows():
        exclude = row.get('Exclude', 'N')
        if pd.notna(exclude) and str(exclude).strip().upper() == 'Y':
            continue

        ticket_count = pd.to_numeric(row.get('Raffle Tickets'), errors='coerce')
        ticket_count = int(ticket_count) if pd.notna(ticket_count) else 0
        if ticket_count < min_required_tickets:
            continue

        numbers_str = row['Number']
        if pd.isna(numbers_str):
            continue
        numbers = [int(x.strip()) for x in str(numbers_str).split(',')]
        people.append({'name': row['Name'], 'numbers': numbers})
        weights.append(len(numbers))
        all_nums.extend(numbers)
    total = sum(weights)
    probs = [w / total for w in weights] if total else []
    return people, probs, all_nums

def check_duplicates(df):
    seen = {}
    dups = {}
    for _, row in df.iterrows():
        if pd.isna(row['Number']):
            continue
        try:
            nums = [int(x.strip()) for x in str(row['Number']).split(',')]
        except:
            continue
        for n in nums:
            if n in seen:
                seen[n].append(row['Name'])
                dups[n] = seen[n]
            else:
                seen[n] = [row['Name']]
    return dups or None

# ── Session state ─────────────────────────────────────────────────────────────

for key, default in [('winner_number', None), ('winner_name', None), ('draw_history', [])]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Load data ─────────────────────────────────────────────────────────────────

df = load_raffle_data()
people, probs, all_nums = prepare_draw_pool(df)

if not people:
    st.error("No eligible participants after backend filtering. Adjust ticket data or exclusion rules.")
    st.stop()

dups = check_duplicates(df)
if dups:
    st.error("⚠️ **DUPLICATE TICKET NUMBERS DETECTED — please recheck the Excel file.**")
    for num, owners in sorted(dups.items()):
        st.write(f"**Number {num}**: {', '.join(owners)}")
    st.stop()

# ── Header & stats ────────────────────────────────────────────────────────────

_, mid, _ = st.columns([1, 2, 1])
with mid:
    st.markdown("# 🎡 Raffle Draw | Brian & Angel 🎡")
    st.markdown("### *Spin to reveal the lucky winner!*")

c1, c2, c3 = st.columns(3)
c1.metric("Participants",       len(df))
c2.metric("Total Tickets Sold", int(df['Raffle Tickets'].sum()))
c3.metric("Draws Made",         len(st.session_state.draw_history))

st.divider()

# ── Main section ──────────────────────────────────────────────────────────────

col1, col2 = st.columns([1, 1])

# Pick 12 numbers to display on wheel — fixed for this page load (gimmick)
wheel_display_nums = rnd.sample(all_nums, min(12, len(all_nums)))

with col1:
    st.markdown("## 🎯 THE WHEEL")

    # Wheel lives here — updated in place during spin
    wheel_placeholder = st.empty()
    wheel_placeholder.markdown(build_wheel_svg(wheel_display_nums, rotation=0), unsafe_allow_html=True)

    if st.button("🎰 SPIN THE WHEEL! 🎰", key="spin_btn", use_container_width=True):
        # Weighted draw: pick a PERSON based on relative ticket-count probability
        winner_idx     = int(np.random.choice(len(people), p=probs))
        winner_name    = people[winner_idx]['name']
        winning_ticket = rnd.choice(people[winner_idx]['numbers'])

        # Ease-out spin: ~10.5 full rotations over 60 frames (~18 s)
        total_rotation = 3600 + rnd.randint(0, 360)
        for i in range(60):
            t      = i / 59
            eased  = 1 - (1 - t) ** 3          # cubic ease-out
            angle  = total_rotation * eased
            wheel_placeholder.markdown(
                build_wheel_svg(wheel_display_nums, rotation=angle),
                unsafe_allow_html=True
            )
            time.sleep(0.3)

        # Store result and refresh
        st.session_state.winner_number = winning_ticket
        st.session_state.winner_name   = winner_name
        st.session_state.draw_history.append({
            'number': winning_ticket,
            'name':   winner_name,
            'time':   time.strftime("%H:%M:%S")
        })
        st.rerun()

with col2:
    st.markdown("## 🏆 THE WINNER")
    if st.session_state.winner_number is not None:
        st.markdown(f"""
            <div class='winner-box'>
                <p style='font-size:24px;margin:0;'>WINNING TICKET NUMBER</p>
                <p style='font-size:72px;margin:10px 0;color:#CC0000;'>
                    <strong>{st.session_state.winner_number}</strong>
                </p>
                <p style='font-size:36px;margin:5px 0;'>🎉</p>
                <p style='font-size:28px;margin:0;'><strong>{st.session_state.winner_name}</strong></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='border:3px dashed #ccc;padding:80px 20px;text-align:center;
                        border-radius:10px;color:#aaa;'>
                <p style='font-size:22px;'>👈 Spin the wheel to reveal the winner!</p>
            </div>
            """, unsafe_allow_html=True)

# ── Participants table ────────────────────────────────────────────────────────

st.divider()
st.markdown("## 📋 Participants")
st.dataframe(
    df[['#', 'Name', 'Raffle Tickets', 'Number']].copy(),
    width='stretch',
    hide_index=True
)

# ── Draw history ──────────────────────────────────────────────────────────────

if st.session_state.draw_history:
    st.markdown("## 📜 Draw History")
    st.dataframe(pd.DataFrame(st.session_state.draw_history), width='stretch', hide_index=True)
    if st.button("🗑️ Clear History"):
        st.session_state.draw_history = []
        st.rerun()

st.markdown("---")
st.markdown("<div style='text-align:center;color:#aaa;font-size:12px;'>🎡 Raffle Draw | Brian & Angel </div>",
            unsafe_allow_html=True)
