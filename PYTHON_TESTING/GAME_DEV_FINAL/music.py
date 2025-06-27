# MUSIC MANAGEMENT SYSTEM

import pygame as pg

class Music:

    def __init__(self):
        # Initialize all mixer modules inside the pygame.
        pg.mixer.init()

        # Set the volume
        self.music_volume = 0.5
        pg.mixer.music.set_volume(self.music_volume)

        # Set background music path file.
        self.background_music_path = 'GAME_DEV_FINAL/assets/sound/Relaxing Music with Nature Sounds.mp3' 

    def play_background_music(self, loop=-1):
        # Starts playing the background music track. loop=-1 means it will repeat indefinitely.
        if not pg.mixer.music.get_busy() or pg.mixer.music.get_file() != self.background_music_path:
            pg.mixer.music.load(self.background_music_path)
            pg.mixer.music.play(loop)

    def stop_music(self):
        # Stops any currently playing music.
        pg.mixer.music.stop()

    def set_music_volume(self, volume):
        # Sets the music volume from 0.0 to 1.0.
        self.music_volume = max(0.0, min(1.0, volume))
        pg.mixer.music.set_volume(self.music_volume)

    def quit_mixer(self):
        # Uninitializes the mixer module.
        pg.mixer.quit()
