import streamlit as st
import streamlit.components.v1 as components
import random

# 1. App Configuration and Title
st.set_page_config(layout="centered", page_title="GD LUDO")

st.title("🎲 GD LUDO")
st.write("Welcome to GD LUDO")

# 2. Game State Setup
if 'ludo_perfect_state' not in st.session_state:
    st.session_state.ludo_perfect_state = {
        'players': ['🔴 Red', '🟢 Green', '🟡 Yellow', '🔵 Blue'],
        'turn': 0,
        'dice_value': 1,
        'has_rolled': False,
        'tokens': {
            '🔴 Red': [0, 0, 0, 0],
            '🟢 Green': [0, 0, 0, 0],
            '🟡 Yellow': [0, 0, 0, 0],
            '🔵 Blue': [0, 0, 0, 0]
        }
    }

state = st.session_state.ludo_perfect_state
current_player = state['players'][state['turn']]

# Callbacks for stable button state handling
def roll_dice_callback():
    st.session_state.ludo_perfect_state['dice_value'] = random.randint(1, 6)
    st.session_state.ludo_perfect_state['has_rolled'] = True

def confirm_move_callback(token_idx):
    dice = st.session_state.ludo_perfect_state['dice_value']
    c_player = st.session_state.ludo_perfect_state['players'][st.session_state.ludo_perfect_state['turn']]
    current_pos = st.session_state.ludo_perfect_state['tokens'][c_player][token_idx]
    
    if current_pos == 0 and dice == 6:
        st.session_state.ludo_perfect_state['tokens'][c_player][token_idx] = 1
    elif current_pos > 0 and current_pos + dice <= 57:
        st.session_state.ludo_perfect_state['tokens'][c_player][token_idx] += dice
        
    st.session_state.ludo_perfect_state['turn'] = (st.session_state.ludo_perfect_state['turn'] + 1) % 4
    st.session_state.ludo_perfect_state['has_rolled'] = False

def restart_game_callback():
    if 'ludo_perfect_state' in st.session_state:
        del st.session_state.ludo_perfect_state

# 3. Token Dots Generator
red_dots = "".join(['<span style="display:inline-block;width:10px;height:10px;border-radius:50%;margin:2px;border:2px solid white;background-color:red;"></span>' for pos in state['tokens']['🔴 Red'] if pos == 0])
green_dots = "".join(['<span style="display:inline-block;width:10px;height:10px;border-radius:50%;margin:2px;border:2px solid white;background-color:green;"></span>' for pos in state['tokens']['🟢 Green'] if pos == 0])
blue_dots = "".join(['<span style="display:inline-block;width:10px;height:10px;border-radius:50%;margin:2px;border:2px solid white;background-color:blue;"></span>' for pos in state['tokens']['🔵 Blue'] if pos == 0])
yellow_dots = "".join(['<span style="display:inline-block;width:10px;height:10px;border-radius:50%;margin:2px;border:2px solid white;background-color:yellow;"></span>' for pos in state['tokens']['🟡 Yellow'] if pos == 0])

# 4. FIXED MATHEMATICAL 15x15 GRID LAYOUT
html_style = """
<style>
    .ludo-container {
        display: flex;
        justify-content: center;
        margin: 20px auto;
    }
    .ludo-board {
        display: grid;
        grid-template-columns: repeat(15, 1fr);
        grid-template-rows: repeat(15, 1fr);
        width: 360px;
        height: 360px;
        border: 4px solid #333;
        background-color: #fff;
    }
    .cell {
        border: 1px solid #ccc;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 9px;
    }
    .home-box {
        grid-column: span 6;
        grid-row: span 6;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-family: Arial, sans-serif;
        font-size: 12px;
    }
    .center-triangle {
        grid-column: span 3;
        grid-row: span 3;
        background: conic-gradient(#ff4d4d 0.25turn, #2ecc71 0.25turn 0.5turn, #f1c40f 0.5turn 0.75turn, #3498db 0.75turn);
        border: 1px solid #333;
    }
    /* Colors */
    .bg-red { background-color: #ff4d4d; }
    .bg-green { background-color: #2ecc71; }
    .bg-yellow { background-color: #f1c40f; color: black; }
    .bg-blue { background-color: #3498db; }
    .star { font-size: 10px; }
</style>
"""

# 15x15 blocks sequentially sorted
html_body = f"""
<div class="ludo-container">
    <div class="ludo-board">
        <div class="home-box bg-red">RED HOME<br><div>{red_dots}</div></div>
        
        <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
        <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
        <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
        <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
        <div class="cell bg-blue">⭐</div><div class="cell bg-green"></div><div class="cell"></div>
        <div class="cell"></div><div class="cell bg-green"></div><div class="cell"></div>
        
        <div class="home-box bg-green">GREEN HOME<br><div>{green_dots}</div></div>
        
        <div class="cell"></div><div class="cell bg-red"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div>
        <div class="cell bg-red"></div><div class="cell bg-red"></div><div class="cell bg-red"></div><div class="cell bg-red"></div><div class="cell bg-red"></div><div class="cell bg-red"></div>
        <div class="cell"></div><div class="cell bg-red">⭐</div><div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div>
        
        <div class="center-triangle"></div>
        
        <div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell bg-yellow">⭐</div><div class="cell"></div><div class="cell"></div>
        <div class="cell bg-yellow"></div><div class="cell bg-yellow"></div><div class="cell bg-yellow"></div><div class="cell bg-yellow"></div><div class="cell bg-yellow"></div><div class="cell bg-yellow"></div>
        <div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell bg-yellow"></div><div class="cell"></div><div class="cell"></div>
        
        <div class="home-box bg-blue">BLUE HOME<br><div>{blue_dots}</div></div>
        
        <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
        <div class="cell"></div><div class="cell bg-blue"></div><div class="cell bg-yellow">⭐</div>
        <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
        <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
        <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
        <div class="cell"></div><div class="cell bg-blue"></div><div class="cell"></div>
        
        <div class="home-box bg-yellow" style="color:black;">YELLOW HOME<br><div>{yellow_dots}</div></div>
    </div>
</div>
"""

components.html(html_style + html_body, height=390)
st.markdown("---")

# 5. CONTROLS LOGIC
st.info(f"### 🎯 Current Turn: {current_player}")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 🎲 Dice Roll: **{state['dice_value']}**")
    if not state['has_rolled']:
        st.button("Roll Dice 🎲", type="primary", use_container_width=True, on_click=roll_dice_callback)

with col2:
    if state['has_rolled']:
        dice = state['dice_value']
        player_tokens = state['tokens'][current_player]
        
        moves_options = {}
        for idx, pos in enumerate(player_tokens):
            if pos == 0 and dice == 6:
                moves_options[idx] = f"🔓 Goti {idx+1} ko Bahar Nikalein"
            elif pos > 0 and pos + dice <= 57:
                moves_options[idx] = f"🏃 Goti {idx+1} ko Chalayein (Pos: {pos} -> {pos+dice})"
            else:
                moves_options[idx] = f"🏠 Goti {idx+1} (Locked/No Move)"

        selected_token_idx = st.selectbox("Apni kaunsi goti chalani hai?", list(moves_options.keys()), format_func=lambda x: moves_options[x])
        
        st.button("Confirm Move ➡️", use_container_width=True, on_click=confirm_move_callback, args=(selected_token_idx,))

# 6. LIVE SCOREBOARD DATA TRACKER
st.markdown("### 📊 GD LUDO Live Scoreboard")
for p_name, t_list in state['tokens'].items():
    st.write(f"**{p_name}** ➡️ Goti 1: `{t_list[0]}`, Goti 2: `{t_list[1]}`, Goti 3: `{t_list[2]}`, Goti 4: `{t_list[3]}`")

st.sidebar.button("🔄 Restart GD LUDO", on_click=restart_game_callback)
