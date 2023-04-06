import pygame
import random
from settings import *
from level import *

class Catdyne:
    def __init__(self):
        name_level = input("Enter the level name: ")

        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen.fill(background_color)
        pygame.display.set_caption("Catdyne")
        self.font = pygame.font.SysFont(None, 30)

        self.clock = pygame.time.Clock()

        self.score = 0
        self.direction_input = ""
        self.speed = 2

        self.current_time = 0
        self.last_spawn_time = 0
        self.last_speed_increase_time = 0

        self.squares = []

        self.lives = 3

        self.center_square = pygame.Rect(screen_width/2 - square_size, screen_height/2 - square_size, 100, 100)

        self.loadimages()

        ### sound

        pygame.mixer.init()
        music = pygame.mixer.Channel(0)
        self.sfx = pygame.mixer.Channel(1)

        self.bpm, self.lvl_arrows, bgm, cat_sprite = loadlevel(name_level)
        self.cat = pygame.image.load(cat_sprite).convert_alpha()
        self.cat = pygame.transform.scale(self.cat, (128, 128))

        self.spawning_time = (int(self.bpm)/60)*1000

        self.arrow_index = 0

        undyne = pygame.mixer.Sound(bgm)
        music.play(undyne, -1) # -1 for looping

    def loadimages(self):
        self.box = pygame.image.load("Imgs/box.png").convert_alpha()
        self.box = pygame.transform.scale(self.box, (128, 128))

        self.left_barrier = pygame.image.load("Imgs/leftbar.png").convert_alpha()
        self.left_barrier = pygame.transform.scale(self.left_barrier, (128,128))

        self.right_barrier = pygame.image.load("Imgs/rightbar.png").convert_alpha()
        self.right_barrier = pygame.transform.scale(self.right_barrier, (128,128))

        self.upper_barrier = pygame.image.load("Imgs/upperbar.png").convert_alpha()
        self.upper_barrier = pygame.transform.scale(self.upper_barrier, (128,128))

        self.down_barrier = pygame.image.load("Imgs/downbar.png").convert_alpha()
        self.down_barrier = pygame.transform.scale(self.down_barrier, (128,128))

        self.heart0 = pygame.image.load("Imgs/heart0.png").convert_alpha()
        self.heart0 = pygame.transform.scale(self.heart0, (128,128))
        self.heart1 = pygame.image.load("Imgs/heart1.png").convert_alpha()
        self.heart1 = pygame.transform.scale(self.heart1, (128,128))
        self.heart2 = pygame.image.load("Imgs/heart2.png").convert_alpha()
        self.heart2 = pygame.transform.scale(self.heart2, (128,128))
        self.heart3 = pygame.image.load("Imgs/heart3.png").convert_alpha()
        self.heart3 = pygame.transform.scale(self.heart3, (128,128))

    def barrier_side(self, spawn):
        if self.direction_input == "left":
            self.screen.blit(self.left_barrier, spawn)
        elif self.direction_input == "right":
            self.screen.blit(self.right_barrier, spawn)
        elif self.direction_input == "up":
            self.screen.blit(self.upper_barrier, spawn)
        elif self.direction_input == "down":
            self.screen.blit(self.down_barrier, spawn)

    def increase_difficulty(self):
        self.last_speed_increase_time = self.current_time
        self.spawning_time = (self.spawning_time * 3)/4
        print("increasing speed")
        self.speed += 1

    def spawn_arrow(self):
        queue = []
        while(True):
            if  (self.arrow_index >= len(self.lvl_arrows)) or self.lvl_arrows[self.arrow_index] == ' ': break
            if(self.lvl_arrows[self.arrow_index] == '.'):
                self.increase_difficulty()
            else: 
                queue.append(self.lvl_arrows[self.arrow_index])
            self.arrow_index += 1
        
        if queue == []: return

        print("queue:",queue, '  index:', self.arrow_index)

        initial_size = len(queue)
        distance = 40

        while(len(queue) != 0):
            x = 0
            y = 0
            dx = 0
            dy = 0
            side = int(queue.pop())
            print("side:",side)

            if side == 1:       # Top
                x = screen_width/2 - square_size/2
                y = -square_size - len(queue)*distance
                print(y)
                dx = 0
                dy = self.speed
            elif side == 2:     # Bottom
                x = screen_width/2 - square_size/2
                y = screen_height + len(queue)*distance
                dx = 0
                dy = -self.speed
            elif side == 3:     # Right
                x = screen_width + len(queue)*distance
                y = screen_height/2 - square_size/2
                dx = -self.speed
                dy = 0
            elif side == 4:     # Left
                x = -square_size - len(queue)*distance
                y = screen_height/2 - square_size/2
                dx = self.speed
                dy = 0

            new_square = pygame.Rect(x, y, square_size, square_size)
            self.squares.append((new_square, dx, dy))

        self.arrow_index += 1

    def spawn_squares(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_spawn_time > self.spawning_time:
            self.last_spawn_time = self.current_time
            self.spawn_arrow()

    def draw(self):
        score_text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))               # Draw Score

        fps = f"{self.clock.get_fps():2.0f} FPS"
        fps_t = self.font.render(fps , 1, (255,255,255))
        self.screen.blit(fps_t, (650, 10))

                                                        # Draw center heart
        if self.lives == 3: self.screen.blit(self.heart0, (screen_width/2-64, screen_height/2-64))
        elif self.lives == 2: self.screen.blit(self.heart1, (screen_width/2-64, screen_height/2-64))
        elif self.lives == 1: self.screen.blit(self.heart2, (screen_width/2-64, screen_height/2-64))
        elif self.lives == 0: self.screen.blit(self.heart3, (screen_width/2-64, screen_height/2-64))

        self.screen.blit(self.box, self.center_square)                 # Draw Central Box
        self.screen.blit(self.cat, (screen_width/2-64, 100))      # Draw Cat
        self.barrier_side(self.center_square)                     # Draw Barrier

        pygame.display.update()                         # Update the display

        self.screen.fill(background_color)                   # Clear screen

    def update(self):
        for square in self.squares:
            square_rect, dx, dy = square
            square_rect.move_ip(dx, dy)
                                                # Check for collision with the center square
            if square_rect.colliderect(self.center_square): 
                if (dx > 0 and self.direction_input != "right") or (dx < 0 and self.direction_input != "left") or (dy > 0 and self.direction_input != "down") or (dy < 0 and self.direction_input != "up"):
                    self.score += 1
                    ping = pygame.mixer.Sound('./audio/ping sfx.mp3')
                    self.sfx.play(ping)

                else: 
                    self.lives-=1
                    dmg = pygame.mixer.Sound('./audio/damage sfx.mp3')
                    self.sfx.play(dmg)

                self.squares.remove(square)
                                                # Remove the square if it goes off screen

            self.square_image = pygame.image.load("Imgs/right.png").convert_alpha()
                                                # Draw the square
            if dx > 0: self.square_image = pygame.image.load("Imgs/right.png").convert_alpha()
            elif dx < 0: self.square_image = pygame.image.load("Imgs/left.png").convert_alpha()
            elif dy > 0: self.square_image = pygame.image.load("Imgs/down.png").convert_alpha()
            elif dy < 0: self.square_image = pygame.image.load("Imgs/upper.png").convert_alpha()

            self.square_image = pygame.transform.scale(self.square_image, (square_size, square_size))
            self.screen.blit(self.square_image, square_rect)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction_input = "left"
                if event.key == pygame.K_RIGHT:
                    self.direction_input = "right"
                if event.key == pygame.K_UP:
                    self.direction_input = "up"
                if event.key == pygame.K_DOWN:
                    self.direction_input = "down"
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def run(self):
        while True:
            self.clock.tick(60)
            self.check_events()
            self.spawn_squares()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Catdyne()
    game.run()