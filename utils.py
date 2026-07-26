import random
import pygame
from collections import deque

def generate_maze(cols, rows):
    grid = [[1 for _ in range(cols * 2 + 1)] for _ in range(rows * 2 + 1)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    stack = [(0, 0)]
    visited[0][0] = True
    grid[1][1] = 0
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    while stack:
        cx, cy = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                neighbors.append((nx, ny, dx, dy))
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            visited[ny][nx] = True
            grid[cy * 2 + 1 + dy][cx * 2 + 1 + dx] = 0
            grid[ny * 2 + 1][nx * 2 + 1] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    return grid

def find_farthest_cell(grid, start):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([start])
    visited[start[1]][start[0]] = True
    farthest = start
    while queue:
        x, y = queue.popleft()
        farthest = (x, y)
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx] and grid[ny][nx] == 0:
                visited[ny][nx] = True
                queue.append((nx, ny))
    return farthest

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def load_font(size):
    try:
        font = pygame.font.SysFont("dejavusans", size)
        if font:
            return font
    except Exception:
        pass
    return pygame.font.Font(None, size)