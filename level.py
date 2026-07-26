import pygame
from settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from utils import generate_maze, find_farthest_cell
from wall import Wall
from door import Door
from exit import Exit

class Level:
    def __init__(self, index, cols, rows, assets, is_final):
        self.index = index
        self.cols = cols
        self.rows = rows
        self.assets = assets
        self.is_final = is_final
        self.grid = generate_maze(cols, rows)
        self.grid_rows = len(self.grid)
        self.grid_cols = len(self.grid[0])
        self.width = self.grid_cols * TILE_SIZE
        self.height = self.grid_rows * TILE_SIZE
        self.walls = []
        self._build_tiles()

        start_cell = (1, 1)
        farthest_cell = find_farthest_cell(self.grid, start_cell)
        self.start_pos = (
            start_cell[0] * TILE_SIZE + TILE_SIZE // 2,
            start_cell[1] * TILE_SIZE + TILE_SIZE // 2,
        )
        target_pos = (farthest_cell[0] * TILE_SIZE, farthest_cell[1] * TILE_SIZE)

        if is_final:
            self.target = Exit(target_pos[0], target_pos[1], assets.get("exit"))
        else:
            self.target = Door(target_pos[0], target_pos[1], assets.get("door"))

    def _build_tiles(self):
        wall_image = self.assets.get("wall")
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                if self.grid[y][x] == 1:
                    self.walls.append(Wall(x * TILE_SIZE, y * TILE_SIZE, wall_image))

    def get_target_rect(self):
        return self.target.rect

    def draw(self, surface, camera_offset):
        floor_image = self.assets.get("floor")
        start_x = max(0, camera_offset[0] // TILE_SIZE - 1)
        start_y = max(0, camera_offset[1] // TILE_SIZE - 1)
        end_x = min(self.grid_cols, (camera_offset[0] + SCREEN_WIDTH) // TILE_SIZE + 2)
        end_y = min(self.grid_rows, (camera_offset[1] + SCREEN_HEIGHT) // TILE_SIZE + 2)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                px = x * TILE_SIZE
                py = y * TILE_SIZE
                pos = (px - camera_offset[0], py - camera_offset[1])
                surface.blit(floor_image, pos)

        for wall in self.walls:
            wx, wy = wall.rect.x, wall.rect.y
            if start_x * TILE_SIZE <= wx <= end_x * TILE_SIZE and start_y * TILE_SIZE <= wy <= end_y * TILE_SIZE:
                wall.draw(surface, camera_offset)

        self.target.draw(surface, camera_offset)