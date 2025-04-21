def get_neighbors(pos, grid):
    rows, cols = len(grid), len(grid[0])
    x, y = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # Ensure that the neighbor is within the bounds of the grid
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 1:
            neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def format_grid(grid, path=None, visited=None, start=None, end=None):
    result = ""
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            pos = (i, j)
            if pos == start:
                result += "S "
            elif pos == end:
                result += "E "
            elif path and pos in path:
                result += "* "
            elif visited and pos in visited:
                result += ". "
            elif cell == 1:
                result += "# "
            else:
                result += "- "
        result += "\n"
    return result
