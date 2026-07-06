import streamlit as st
import random

# 1. App Configuration and Title
st.set_page_config(layout="centered", page_title="GD LUDO")

st.title("🎲 GD LUDO")
st.write("Welcome to GD LUDO")

# 2. Game State Setup (Ek hi phone par data maintain karne ke liye)
if 'ludo_perfect_state' not in st.session_state:
    st.session_state.ludo_perfect_state = {
        'players': ['🔴 Red', '🟢 Green', '🟡 Yellow', '🔵 Blue'],
        'turn': 0,
        'dice_value': 1,
        'has_rolled': False,
        # Har player ki 4 gotiyon ki position (0 = Ghar ke andar, 57 = Winner Home)
        'tokens': {
            '🔴 Red': [0, 0, 0, 0],
            '🟢 Green': [0, 0, 0, 0],
            '🟡 Yellow': [0, 0, 0, 0],
            '🔵 Blue': [0, 0, 0, 0]
        }
    }

state = st.session_state.ludo_perfect_state
current_player = state['players'][state['turn']]

# 3. Token Dots Generator (Base me bachi hui gotiyan dikhane ke liye)
red_dots = "".join(['<span class="goti g-red"></span>' for pos in state['tokens']['🔴 Red'] if pos == 0])
green_dots = "".join(['<span class="goti g-green"></span>' for pos in state['tokens']['🟢 Green'] if pos == 0])
blue_dots = "".join(['<span class="goti g-blue"></span>' for pos in state['tokens']['🔵 Blue'] if pos == 0])
yellow_dots = "".join(['<span class="goti g-yellow"></span>' for pos in state['tokens']['🟡 Yellow'] if pos == 0])

# 4. ADVANCED GRAPHICAL CSS GRID (Aapki photo jaisa layout)
ludo_board_html = f"""
<style>
    .ludo-board {{
        display: grid;
        grid-template-columns: repeat(15, 1fr);
        grid-template-rows: repeat(15, 1fr);
        width: 380px;
        height: 380px;
        margin: 0 auto;
        border: 4px solid #222;
        background-color: #fff;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
        border-radius: 10px;
        overflow: hidden;
    }}
    .cell {{
        border: 1px solid #ddd;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
    }}
    /* Home Quadrants */
    .quad {{
        grid-column: span 6;
        grid-row: span 6;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-family: sans-serif;
    }}
    .hq-red {{ background-color: #ff4d4d; }}
    .hq-green {{ background-color: #2ecc71; }}
    .hq-blue {{ background-color: #3498db; }}
    .hq-yellow {{ background-color: #f1c40f; color: black; }}
    
    /* Center Triangle Zone */
    .center-tri {{
        grid-column: span 3;
        grid-row: span 3;
        background: conic-gradient(#ff4d4d 0.25turn, #2ecc71 0.25turn 0.5turn, #f1c40f 0.5turn 0.75turn, #3498db 0.75turn);
        border: 1px solid #222;
    }}
    
    /* Paths & Safe Zones */
    .bg-red {{ background-color: #ff4d4d !important; }}
    .bg-green {{ background-color: #2ecc71 !important; }}
    .bg-blue {{ background-color: #3498db !important; }}
    .bg-yellow {{ background-color: #f1c40f !important; }}
    .star-cell {{ background-color: #f6e58d; font-weight: bold; }}

    /* Gotiyon ka Visual Design */
    .goti {{
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin: 2px;
        border: 2px solid white;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }}
    .g-red {{ background-color: red; }}
    .g-green {{ background-color: green; }}
    .g-blue {{ background-color: blue; }}
    .g-yellow {{ background-color: yellow; }}
</style>

<div class="ludo-board">
    <div class="quad hq-red">GD RED HOME<br><div style="margin-top:10px;">{red_dots}</div></div>
    <div class="cell"></div><div class="cell bg-green">⭐</div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
    <div class="quad hq-green">GD GREEN HOME<br><div style="margin-top:10px;">{green_dots}</div></div>
    
    <div class="cell"></div><div class="cell bg-red"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div>
    <div class="cell bg-red">⭐</div><div class="cell bg-red"></div><div class="cell bg-red"></div><div class="cell bg-red"></div><div class="cell bg-red"></div><div class="cell bg-red"></div>
    <div class="cell"></div><div class="cell bg-red"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div>
    
    <div class="center-tri"></div>
    
    <div class="cell"></div><div class="cell bg-yellow"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div>
    <div class="cell bg-yellow"></div><div class="cell bg-yellow"></div><div class="cell bg-yellow"></div><div class="cell bg-yellow"></div><div class="cell bg-yellow">⭐</div><div class="cell bg-yellow"></div>
    <div class="cell"></div><div class="cell bg-yellow"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div>

    <div class="quad hq-blue">GD BLUE HOME<br><div style="margin-top:10px;">{blue_dots}</div></div>
    <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
    <div class="cell">⭐</div><div class="cell bg-blue"></div><div class="cell"></div>
    <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
    <div class="quad hq-yellow">GD YELLOW HOME<br><div style="margin-top:10px;">{yellow_dots}</div></div>
</div>
"""

# HTML Board ko render karna
st.markdown(ludo_board_html, unsafe_allow_html=True)
st.markdown("---")

# 5. CONTROLS FOR ONE PHONE PLAYERS
st.info(f"### 🎯 Current Turn: {current_player}")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 🎲 Dice Roll: **{state['dice_value']}**")
    if not state['has_rolled']:
        if st.button("Roll Dice 🎲", type="primary", use_container_width=True):
            state['dice_value'] = random.randint(1, 6)
            state['has_rolled'] = True
            st.rerun()

with col2:
    if state['has_rolled']:
        dice = state['dice_value']
        player_tokens = state['tokens'][current_player]
        
        # Valid moves filter karna dropdown ke liye
        moves_options = {}
        for idx, pos in enumerate(player_tokens):
            if pos == 0 and dice == 6:
                moves_options[f"Token {idx+1}"] = f"🔓 Token {idx+1} ko Ghar se Bahar Nikalein"
            elif pos > 0 and pos + dice <= 57:
                moves_options[f"Token {idx+1}"] = f"🏃 Token {idx+1} ko Chalayein (Pos: {pos} -> {pos+dice})"
            else:
                moves_options[f"Token {idx+1}"] = f"🏠 Token {idx+1} (Abhi locked hai ya move possible nahi)"

        selected_token = st.selectbox("Apni kaunsi goti aage badhani hai?", list(moves_options.keys()), format_func=lambda x: moves_options[x])
        token_index = int(selected_token.split(" ")[1]) - 1
        
        if st.button("Confirm Move & Pass Phone ➡️", use_container_width=True):
            current_pos = player_tokens[token_index]
            if current_pos == 0 and dice == 6:
                state['tokens'][current_player][token_index] = 1
            elif current_pos > 0 and current_pos + dice <= 57:
                state['tokens'][current_player][token_index] += dice
                
            # strict turn change (Agle bande ki baari)
            state['turn'] = (state['turn'] + 1) % 4
            state['has_rolled'] = False
            st.rerun()

# 6. LIVE SCOREBOARD DATA TRACKER (Niche track karne ke liye)
st.markdown("### 📊 GD LUDO Live Scoreboard")
for p_name, t_list in state['tokens'].items():
    st.write(f"**{p_name}** ➡️ Goti 1: `{t_list[0]}`, Goti 2: `{t_list[1]}`, Goti 3: `{t_list[2]}`, Goti 4: `{t_list[3]}`")

# Reset options in sidebar
if st.sidebar.button("🔄 Restart GD LUDO"):
    del st.session_state.ludo_perfect_state
    st.rerun()