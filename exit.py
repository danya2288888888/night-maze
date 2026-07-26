import pygame
from settings import TILE_SIZE

class Exit:
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

    def draw(self, surface, camera_offset):
        pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        surface.blit(self.image, pos)
        