import pygame
from settings import PLAYER_SPEED, PLAYER_SIZE

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.rect.center = (x, y)
        self.speed = PLAYER_SPEED

    def handle_input(self, keys, dt, walls):
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        moved = dx != 0 or dy != 0
        move_x = dx * self.speed * dt
        move_y = dy * self.speed * dt
        self._move_axis(move_x, 0, walls)
        self._move_axis(0, move_y, walls)
        return moved

    def _move_axis(self, dx, dy, walls):
        self.rect.x += int(dx)
        self.rect.y += int(dy)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                elif dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                elif dy < 0:
                    self.rect.top = wall.rect.bottom

    def draw(self, surface, camera_offset):
        image_rect = self.image.get_rect(
            center=(self.rect.centerx - camera_offset[0], self.rect.centery - camera_offset[1])
        )
        surface.blit(self.image, image_rect)
        