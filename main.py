import pygame
import random
from arrow import Arrow
from settings import *
from game import Game
import sys


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Undyne")
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = Game(self)

    def update(self):
        self.game.update()
        self.clock.tick(FPS)
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.game.draw()
        pygame.display.flip()
    
    def check_events(self):
        self.game.check_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
    
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()

# graphs


"""
def generate_arrow():
    x = random.randint(1,4)
    arrows.append(Arrow(x, arrow_speed))


pygame.display.flip()

def basic_graphics():
    screen.fill((0, 0, 0))
    screen.blit(cat, (580,100))
    screen.blit(box, (580,330))
    barrier_side()

def barrier_side():
    if direc == "left":
        screen.blit(left_barrier, (580,330))
    elif direc == "right":
        screen.blit(right_barrier, (580,330))
    elif direc == "up":
        screen.blit(upper_barrier, (580,330))
    elif direc == "down":
        screen.blit(down_barrier, (580,330))

while running:
    t = pygame.time.get_ticks()
    deltaTime = (t-lastFrame)/1000.0
    lastFrame = t

    for arr in arrows:
        arr.update(deltaTime, arrow_speed)
        screen.blit(arr.sprite, arr.pos)       

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direc = "left"
            if event.key == pygame.K_RIGHT:
                direc = "right"
            if event.key == pygame.K_UP:
                direc = "up"
            if event.key == pygame.K_DOWN:
                direc = "down"
            print(direc)
        if event.type == timer_event:
            generate_arrow()

        if event.type == pygame.QUIT:
            running = False

    basic_graphics()

    pygame.display.update()

pygame.quit()"""