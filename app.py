import streamlit as st
import random
from algorithms.astar import astar
from algorithms.dijkstra import dijkstra
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from utils.grid import create_grid, add_random_obstacles
from utils.path_utils import format_grid

st.set_page_config(layout="wide")
st.title("🧠 Pathfinding Visualizer")
st.sidebar.title("⚙️ Controls")

# Grid size controls
rows = st.sidebar.slider("Rows", 5, 20, 10)
cols = st.sidebar.slider("Columns", 5, 20, 10)
start = (0, 0)
end = (rows - 1, cols - 1)

# Initialize grid
if "grid" not in st.session_state or len(st.session_state.grid) != rows or len(st.session_state.grid[0]) != cols:
    st.session_state.grid = create_grid(rows, cols)

# Random obstacles
if st.sidebar.button("🔁 Random Obstacles"):
    st.session_state.grid = add_random_obstacles(rows, cols, start, end)

grid = st.session_state.grid

# Track algorithms used
if "algorithms_used" not in st.session_state:
    st.session_state.algorithms_used = []

# Choose algorithm
algorithm = st.sidebar.selectbox("Choose Algorithm", ["A*", "Dijkstra", "BFS", "DFS"])
run_button = st.sidebar.button("▶️ Run Algorithm")
details_button = st.sidebar.button("📜 Show Algorithm Details")

# Reset visualization state
if "step" not in st.session_state:
    st.session_state.step = 0
if "visited_list" not in st.session_state:
    st.session_state.visited_list = []
if "path_list" not in st.session_state:
    st.session_state.path_list = []
if "agent_step" not in st.session_state:
    st.session_state.agent_step = 0

# Suggest best algorithm based on grid
def suggest_best_algorithm(grid):
    actual_rows = len(grid)
    actual_cols = len(grid[0]) if actual_rows > 0 else 0
    num_obstacles = sum([1 for i in range(actual_rows) for j in range(actual_cols) if grid[i][j] == 1])
    total_cells = actual_rows * actual_cols
    obstacle_pct = num_obstacles / total_cells if total_cells > 0 else 0

    if obstacle_pct > 0.3:
        return "A*"
    elif total_cells < 100:
        return "BFS"
    elif obstacle_pct <= 0.3:
        return "Dijkstra"
    else:
        return "DFS"

suggested_algorithm = suggest_best_algorithm(grid)
st.sidebar.markdown(f"### 🤖 Suggested: `{suggested_algorithm}`")

# Run selected algorithm
if run_button or details_button:
    if algorithm == "A*":
        path, visited = astar(start, end, grid)
    elif algorithm == "Dijkstra":
        path, visited = dijkstra(start, end, grid)
    elif algorithm == "BFS":
        path, visited = bfs(start, end, grid)
    elif algorithm == "DFS":
        path, visited = dfs(start, end, grid)


    st.session_state.visited_list = list(visited)
    st.session_state.path_list = path
    st.session_state.step = len(st.session_state.visited_list)
    st.session_state.agent_step = 0
    st.session_state.algorithms_used.append(algorithm)

# Animation sliders
max_step = len(st.session_state.visited_list)
current_step = st.sidebar.slider("🎞 Visited Nodes Animation", 0, max_step if max_step > 0 else 1, max_step if max_step > 0 else 1)

# Agent animation slider
if st.session_state.path_list:
    agent_max_step = len(st.session_state.path_list) - 1
    agent_step = st.sidebar.slider("🚶 Agent Path Animation", 0, agent_max_step, 0)
    st.session_state.agent_step = agent_step
else:
    st.session_state.agent_step = None

# Render grid
st.subheader("🧭 Grid Visualization")
agent_pos = None
if st.session_state.path_list and st.session_state.agent_step is not None:
    if 0 <= st.session_state.agent_step < len(st.session_state.path_list):
        agent_pos = st.session_state.path_list[st.session_state.agent_step]

for i in range(rows):
    row_html = ""
    for j in range(cols):
        cell = (i, j)
        if cell == start:
            color = "#4caf50"
        elif cell == end:
            color = "#f44336"
        elif agent_pos and cell == agent_pos:
            # Use emoji to show agent
            row_html += f'<div style="width:20px; height:20px; display:inline-block; margin:1px; font-size:16px; text-align:center;">🤖</div>'
            continue
        elif i < len(grid) and j < len(grid[i]) and grid[i][j] == 1:
            color = "#000000"
        elif cell in st.session_state.path_list:
            color = "#2196f3"
        elif cell in st.session_state.visited_list[:current_step]:
            color = "#90caf9"
        else:
            color = "#ddd"
        row_html += f'<div style="background-color:{color}; width:20px; height:20px; display:inline-block; margin:1px;"></div>'
    st.markdown(row_html, unsafe_allow_html=True)

# Algorithm info section
if details_button:
    st.subheader("📜 Algorithm Details")

    definitions = {
        "A*": {
            "definition": "A* (A-star) uses cost + heuristic to find the shortest path.",
            "how": "Expands most promising node using priority queue with cost + estimated distance."
        },
        "Dijkstra": {
            "definition": "Dijkstra finds shortest path using uniform cost search.",
            "how": "Explores nodes in order of increasing distance from start."
        },
        "BFS": {
            "definition": "BFS finds the shortest path in unweighted graphs.",
            "how": "Explores neighbors level by level using a queue."
        },
        "DFS": {
            "definition": "DFS explores as far as possible along one branch before backtracking.",
            "how": "Uses a stack (recursion or explicit) and doesn’t guarantee the shortest path."
        }
    }

    info = definitions.get(algorithm, {})
    st.markdown(f"### 🔍 {algorithm}")
    st.markdown(f"**Definition**: {info['definition']}")
    st.markdown(f"**How It Works**: {info['how']}")
    st.markdown(f"**Start**: `{start}` | **End**: `{end}`")
    st.markdown(f"**Visited Nodes**: `{len(st.session_state.visited_list)}`")
    st.markdown(f"**Visited List**: `{st.session_state.visited_list}`")
    st.markdown(f"**Path Length**: `{len(st.session_state.path_list)}`")

    if st.session_state.path_list:
        st.markdown(f"**Optimal Path**: {st.session_state.path_list}")

    st.text("🧮 Final Grid:\n" + format_grid(
        grid,
        st.session_state.path_list,
        st.session_state.visited_list,
        start,
        end
    ))

# Show all used algorithms
st.sidebar.subheader("📈 Algorithms Used")
for algo in st.session_state.algorithms_used:
    st.sidebar.text(algo)
