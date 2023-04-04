import pygame
from settings import *

class Arrow:
    def __init__(self, direction, speed):
        self.direction = direction
        self.speed = speed
        self.sprite = pygame.image.load("Imgs/left.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (128, 128))
        self.pos = (100,100)

    def is_alive(self):
        if not self.alive:
            self.kill()

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        self.pos += move_direction

    def update(self):
        self.move(direction='right')
        
