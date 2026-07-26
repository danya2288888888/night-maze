import os
import pygame
from settings import SOUNDS_DIR, MUSIC_DIR

class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init()
        except Exception:
            self.enabled = False
        self.sounds = {}
        if self.enabled:
            self._load_sounds()

    def _try_load_sound(self, filename):
        path = os.path.join(SOUNDS_DIR, filename)
        try:
            if os.path.isfile(path):
                return pygame.mixer.Sound(path)
        except Exception:
            return None
        return None

    def _load_sounds(self):
        self.sounds["step"] = self._try_load_sound("step.wav")
        self.sounds["door"] = self._try_load_sound("door.wav")
        self.sounds["win"] = self._try_load_sound("win.wav")
        self.sounds["exit"] = self._try_load_sound("exit.wav")

    def play(self, name):
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except Exception:
                pass

    def play_music(self, filename, loop=True):
        if not self.enabled:
            return
        path = os.path.join(MUSIC_DIR, filename)
        try:
            if os.path.isfile(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(-1 if loop else 0)
        except Exception:
            pass

    def stop_music(self):
        if not self.enabled:
            return
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass