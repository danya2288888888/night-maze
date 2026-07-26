import sys
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, TOTAL_LEVELS, LEVEL_SIZES,
    VISION_RADIUS, BLACK, WHITE, GREEN, FONT_SIZE_LARGE, FONT_SIZE_MEDIUM
)
from assets import Assets
from sound import SoundManager
from hud import HUD
from level import Level
from player import Player
from utils import clamp, load_font

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_WIN = "win"

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        self.sound = SoundManager()
        self.hud = HUD()
        self.font_large = load_font(FONT_SIZE_LARGE)
        self.font_medium = load_font(FONT_SIZE_MEDIUM)
        self.state = STATE_MENU
        self.current_level_index = 1
        self.level = None
        self.player = None
        self.camera_offset = [0, 0]
        self.elapsed_time = 0
        self.step_timer = 0
        self.running = True
        self.darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.sound.play_music("str.mp3")

    def start_level(self, index):
        cols, rows = LEVEL_SIZES[index - 1]
        is_final = index == TOTAL_LEVELS
        self.level = Level(index, cols, rows, self.assets, is_final)
        self.player = Player(self.level.start_pos[0], self.level.start_pos[1], self.assets.get("player"))
        self.elapsed_time = 0
        self.step_timer = 0
        self.state = STATE_PLAYING
        self.update_camera()

    def restart_level(self):
        self.start_level(self.current_level_index)

    def start_new_game(self):
        self.current_level_index = 1
        self.start_level(self.current_level_index)

    def update_camera(self):
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        target_y = self.player.rect.centery - SCREEN_HEIGHT // 2
        max_x = max(0, self.level.width - SCREEN_WIDTH)
        max_y = max(0, self.level.height - SCREEN_HEIGHT)
        self.camera_offset[0] = clamp(target_x, 0, max_x)
        self.camera_offset[1] = clamp(target_y, 0, max_y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                    elif self.state == STATE_PAUSED:
                        self.state = STATE_PLAYING
                    elif self.state == STATE_WIN:
                        self.running = False
                elif event.key == pygame.K_r:
                    if self.state in (STATE_PLAYING, STATE_PAUSED):
                        self.restart_level()
                elif event.key == pygame.K_RETURN:
                    if self.state == STATE_MENU:
                        self.start_new_game()
                    elif self.state == STATE_WIN:
                        self.start_new_game()

    def update(self, dt):
        if self.state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            moved = self.player.handle_input(keys, dt, self.level.walls)
            if moved:
                self.step_timer += dt
                if self.step_timer >= 0.3:
                    self.sound.play("step")
                    self.step_timer = 0
            else:
                self.step_timer = 0
            self.elapsed_time += dt
            self.update_camera()
            if self.player.rect.colliderect(self.level.get_target_rect()):
                self.on_level_complete()

    def on_level_complete(self):
        if self.level.is_final:
            self.sound.play("win")
            self.state = STATE_WIN
        else:
            self.sound.play("door")
            self.current_level_index += 1
            self.start_level(self.current_level_index)

    def draw_lighting(self):
        self.darkness.fill((0, 0, 0, 255))
        px = self.player.rect.centerx - self.camera_offset[0]
        py = self.player.rect.centery - self.camera_offset[1]
        radius = VISION_RADIUS
        for r in range(radius, 0, -4):
            alpha = int(255 * (r / radius))
            pygame.draw.circle(self.darkness, (0, 0, 0, alpha), (px, py), r)
        pygame.draw.circle(self.darkness, (0, 0, 0, 0), (px, py), max(1, radius // 6))
        self.screen.blit(self.darkness, (0, 0))

    def draw_background_tile(self):
        background = self.assets.get("background")
        if background:
            w, h = background.get_size()
            for y in range(0, SCREEN_HEIGHT, h):
                for x in range(0, SCREEN_WIDTH, w):
                    self.screen.blit(background, (x, y))

    def draw_menu(self):
        self.screen.fill(BLACK)
        self.draw_background_tile()
        title = self.font_large.render(TITLE, True, WHITE)
        hint = self.font_medium.render("Натисніть ENTER, щоб почати", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        text = self.font_large.render("ПАУЗА", True, WHITE)
        hint = self.font_medium.render("ESC - продовжити, R - рестарт рівня", True, WHITE)
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))

    def draw_win(self):
        self.screen.fill(BLACK)
        self.draw_background_tile()
        text = self.font_large.render("ПЕРЕМОГА!", True, GREEN)
        hint1 = self.font_medium.render("ENTER - зіграти знову", True, WHITE)
        hint2 = self.font_medium.render("ESC - вийти", True, WHITE)
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
        self.screen.blit(hint1, hint1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))
        self.screen.blit(hint2, hint2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

    def draw_playing(self):
        self.screen.fill(BLACK)
        self.level.draw(self.screen, self.camera_offset)
        self.player.draw(self.screen, self.camera_offset)
        self.draw_lighting()
        self.hud.draw(self.screen, self.current_level_index, self.elapsed_time)

    def draw(self):
        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state in (STATE_PLAYING, STATE_PAUSED):
            self.draw_playing()
            if self.state == STATE_PAUSED:
                self.draw_pause()
        elif self.state == STATE_WIN:
            self.draw_win()
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()