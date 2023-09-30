import pygame
pygame.mixer.init()
pygame.mixer.music.load("mix.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pass
