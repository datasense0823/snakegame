import streamlit as st
import random

# Streamlit page config
st.set_page_config(page_title="DataSense Python Game", layout="centered")

# CSS Styling
st.markdown("""
    <style>
        .snake-cell {
            background-color: #39FF14;
            border: 1px solid #000;
            width: 20px;
            height: 20px;
            display: inline-block;
        }
        .food-cell {
            background-color: #FF4136;
            border: 1px solid #000;
            width: 20px;
            height: 20px;
            display: inline-block;
        }
        .empty-cell {
            background-color: #F0F0F0;
            border: 1px solid #CCC;
            width: 20px;
            height: 20px;
            display: inline-block;
        }
        .center-text {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🐍 DataSense Python Game")

# Get player name
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if not st.session_state.player_name:
    name_input = st.text_input("Enter your name to start playing:")
    if name_input:
        st.session_state.player_name = name_input
        st.session_state.snake = [(0, 0)]
        st.session_state.food = (random.randint(0, 9), random.randint(0, 9))
        st.session_state.direction = (0, 1)
        st.session_state.alive = True
        st.session_state.score = 0
        st.session_state.best_score = 0
    else:
        st.stop()

# Initialize game state
if "snake" not in st.session_state:
    st.session_state.snake = [(0, 0)]
    st.session_state.food = (random.randint(0, 9), random.randint(0, 9))
    st.session_state.direction = (0, 1)
    st.session_state.alive = True
    st.session_state.score = 0
    st.session_state.best_score = 0

GRID_SIZE = 10

def draw_grid():
    html = ""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i, j) in st.session_state.snake:
                html += '<div class="snake-cell"></div>'
            elif (i, j) == st.session_state.food:
                html += '<div class="food-cell"></div>'
            else:
                html += '<div class="empty-cell"></div>'
        html += "<br>"
    return html

def move_snake():
    if not st.session_state.alive:
        return

    head = st.session_state.snake[-1]
    dx, dy = st.session_state.direction
    new_head = (head[0] + dx, head[1] + dy)

    # Check for collisions
    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or
        new_head in st.session_state.snake):
        st.session_state.alive = False
        return

    # Eating food
    if new_head == st.session_state.food:
        st.session_state.snake.append(new_head)
        st.session_state.score += 1
        while True:
            new_food = (random.randint(0, 9), random.randint(0, 9))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    else:
        st.session_state.snake.append(new_head)
        st.session_state.snake.pop(0)

# Show player name
st.markdown(f"### 🎮 Player: `{st.session_state.player_name}`")

# Direction controls
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️"):
        st.session_state.direction = (-1, 0)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️"):
        st.session_state.direction = (0, -1)
with col3:
    if st.button("➡️"):
        st.session_state.direction = (0, 1)
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬇️"):
        st.session_state.direction = (1, 0)

# Run game logic
move_snake()

# Draw game grid
st.markdown(draw_grid(), unsafe_allow_html=True)

# Show score
st.markdown(f"### 🧮 Score: `{st.session_state.score}`")

# Best score tracking
if st.session_state.score > st.session_state.best_score:
    st.session_state.best_score = st.session_state.score

st.markdown(f"### 🏆 Best Score: `{st.session_state.best_score}`")

# Game over message
if not st.session_state.alive:
    st.error("💀 Game Over! Refresh the page to restart.")
else:
    st.success("🚀 Keep going!")
