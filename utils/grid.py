import random

def create_grid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def add_random_obstacles(rows, cols, start, end, obstacle_pct=0.2):
    grid = create_grid(rows, cols)
    obstacle_count = int(rows * cols * obstacle_pct)
    obstacles = 0
    while obstacles < obstacle_count:
        x, y = random.randint(0, rows-1), random.randint(0, cols-1)
        if (x, y) != start and (x, y) != end and grid[x][y] != 1:
            grid[x][y] = 1
            obstacles += 1
    return grid
