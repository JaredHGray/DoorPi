import pygame
from pygame import mixer

file = 'musicFiles/NINTENDO Mii THEME (TRAP REMIX) - VANDER.mp3'
mixer.init()
mixer.music.set_volume(10.0)
sound = pygame.mixer.Sound(file)
sound.play()
# mixer.music.load(file)
# mixer.music.play()
# clock = pygame.time.Clock()
while mixer.music.get_busy():
    clock.tick(10)
#pygame.event.wait()