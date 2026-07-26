import pygame
from settings import FONT_SIZE_SMALL, WHITE, TOTAL_LEVELS
from utils import load_font

class HUD:
    def __init__(self):
        self.font = load_font(FONT_SIZE_SMALL)

    def draw(self, surface, level_index, elapsed_time):
        level_text = self.font.render(f"Рівень: {level_index} / {TOTAL_LEVELS}", True, WHITE)
        minutes = int(elapsed_time) // 60
        seconds = int(elapsed_time) % 60
        time_text = self.font.render(f"Час: {minutes:02d}:{seconds:02d}", True, WHITE)
        controls_text = self.font.render("WASD / Стрілки - рух, ESC - пауза, R - рестарт", True, WHITE)
        surface.blit(level_text, (10, 10))
        surface.blit(time_text, (10, 36))
        surface.blit(controls_text, (10, 62))