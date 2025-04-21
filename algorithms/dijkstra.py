import heapq
from utils.path_utils import reconstruct_path, get_neighbors

def dijkstra(start, end, grid):
    pq = [(0, start)]
    dist = {start: 0}
    came_from = {}
    visited = set()

    while pq:
        cost, current = heapq.heappop(pq)
        visited.add(current)

        if current == end:
            return reconstruct_path(came_from, current), visited

        for neighbor in get_neighbors(current, grid):
            new_cost = dist[current] + 1
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))
    return [], visited
