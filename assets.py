import os
import math
import pygame
from settings import (
    TILE_SIZE, WALL_COLOR, FLOOR_COLOR, DOOR_COLOR, EXIT_COLOR,
    PLAYER_COLOR, IMAGES_DIR
)

class Assets:
    def __init__(self):
        self.images = {}
        self._load_all()

    def _try_load(self, filename, size):
        path = os.path.join(IMAGES_DIR, filename)
        try:
            if os.path.isfile(path):
                image = pygame.image.load(path).convert_alpha()
                return pygame.transform.smoothscale(image, size)
        except Exception:
            return None
        return None

    def _fallback_rect(self, size, color, border_color=None):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill(color)
        if border_color:
            pygame.draw.rect(surface, border_color, surface.get_rect(), 2)
        return surface

    def _fallback_circle(self, size, color, border_color=None):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        radius = min(size) // 2
        center = (size[0] // 2, size[1] // 2)
        pygame.draw.circle(surface, color, center, radius)
        if border_color:
            pygame.draw.circle(surface, border_color, center, radius, 2)
        return surface

    def _fallback_star(self, size, color):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        cx, cy = size[0] // 2, size[1] // 2
        outer = min(size) // 2
        inner = outer // 2
        points = []
        for i in range(10):
            angle = math.pi / 5 * i - math.pi / 2
            radius = outer if i % 2 == 0 else inner
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        pygame.draw.polygon(surface, color, points)
        return surface

    def _load_all(self):
        size = (TILE_SIZE, TILE_SIZE)

        wall = self._try_load("wall.png", size)
        self.images["wall"] = wall if wall else self._fallback_rect(size, WALL_COLOR, (10, 10, 10))

        floor = self._try_load("floor.png", size)
        self.images["floor"] = floor if floor else self._fallback_rect(size, FLOOR_COLOR)

        door = self._try_load("door.png", size)
        self.images["door"] = door if door else self._fallback_rect(size, DOOR_COLOR, (30, 15, 5))

        exit_img = self._try_load("exit.png", size)
        self.images["exit"] = exit_img if exit_img else self._fallback_star(size, EXIT_COLOR)

        player_size = (int(TILE_SIZE * 0.7), int(TILE_SIZE * 0.7))
        player = self._try_load("player.png", player_size)
        self.images["player"] = player if player else self._fallback_circle(player_size, PLAYER_COLOR, (10, 40, 90))

        background = self._try_load("background.png", size)
        self.images["background"] = background if background else self._fallback_rect(size, (15, 15, 20))

    def get(self, name):
        return self.images.get(name)