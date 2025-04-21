import heapq
from utils.path_utils import reconstruct_path, get_neighbors

def astar(start, end, grid):
    open_set = [(0, start)]
    came_from = {}
    g = {start: 0}
    f = {start: heuristic(start, end)}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        visited.add(current)

        if current == end:
            return reconstruct_path(came_from, current), visited

        for neighbor in get_neighbors(current, grid):
            tentative_g = g[current] + 1
            if tentative_g < g.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g[neighbor] = tentative_g
                f[neighbor] = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (f[neighbor], neighbor))
    return [], visited

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
