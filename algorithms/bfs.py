from collections import deque
from utils.path_utils import reconstruct_path, get_neighbors

def bfs(start, end, grid):
    queue = deque([start])
    came_from = {start: None}
    visited = set([start])

    while queue:
        current = queue.popleft()

        if current == end:
            return reconstruct_path(came_from, current), visited

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    return [], visited
