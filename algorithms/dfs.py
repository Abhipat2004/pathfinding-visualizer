from utils.path_utils import reconstruct_path, get_neighbors

def dfs(start, end, grid):
    stack = [start]
    came_from = {start: None}
    visited = set([start])

    while stack:
        current = stack.pop()

        if current == end:
            return reconstruct_path(came_from, current), visited

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
    return [], visited
