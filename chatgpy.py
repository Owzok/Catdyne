import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the background color
background_color = (0, 0, 0)
screen.fill(background_color)

# Set the title of the window
pygame.display.set_caption("Undyne")

font = pygame.font.SysFont(None, 30)

# Set the font for displaying text
font = pygame.font.SysFont(None, 30)

score = 0

# Set the square size
square_size = 64

direction_input = ""

# Set the initial speed
speed = 1

# Set the time variables
current_time = 0
last_spawn_time = 0
last_speed_increase_time = 0

# Create a list to store the squares
squares = []

cat = pygame.image.load("Imgs/cat.png").convert_alpha()
cat = pygame.transform.scale(cat, (128, 128))
box = pygame.image.load("Imgs/box.png").convert_alpha()
box = pygame.transform.scale(box, (128, 128))

left_barrier = pygame.image.load("Imgs/leftbar.png").convert_alpha()
left_barrier = pygame.transform.scale(left_barrier, (128,128))

right_barrier = pygame.image.load("Imgs/rightbar.png").convert_alpha()
right_barrier = pygame.transform.scale(right_barrier, (128,128))

upper_barrier = pygame.image.load("Imgs/upperbar.png").convert_alpha()
upper_barrier = pygame.transform.scale(upper_barrier, (128,128))

down_barrier = pygame.image.load("Imgs/downbar.png").convert_alpha()
down_barrier = pygame.transform.scale(down_barrier, (128,128))

heart0 = pygame.image.load("Imgs/heart0.png").convert_alpha()
heart0 = pygame.transform.scale(heart0, (128,128))
heart1 = pygame.image.load("Imgs/heart1.png").convert_alpha()
heart1 = pygame.transform.scale(heart1, (128,128))
heart2 = pygame.image.load("Imgs/heart2.png").convert_alpha()
heart2 = pygame.transform.scale(heart2, (128,128))
heart3 = pygame.image.load("Imgs/heart3.png").convert_alpha()
heart3 = pygame.transform.scale(heart3, (128,128))

lives = 3

# Create the center square
center_square = pygame.Rect(screen_width/2 - square_size, screen_height/2 - square_size, 100, 100)

def barrier_side(spawn):
    if direction_input == "left":
        screen.blit(left_barrier, spawn)
    elif direction_input == "right":
        screen.blit(right_barrier, spawn)
    elif direction_input == "up":
        screen.blit(upper_barrier, spawn)
    elif direction_input == "down":
        screen.blit(down_barrier, spawn)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction_input = "left"
            if event.key == pygame.K_RIGHT:
                direction_input = "right"
            if event.key == pygame.K_UP:
                direction_input = "up"
            if event.key == pygame.K_DOWN:
                direction_input = "down"
            print(direction_input)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Spawn a square every second
    

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > 2000:
        last_spawn_time = current_time

        # Choose a random side to spawn the square
        side = random.randint(1, 4)
        if side == 1:
            # Top
            x = screen_width/2 - square_size/2
            y = -square_size
            dx = 0
            dy = speed
        elif side == 2:
            # Bottom
            x = screen_width/2 - square_size/2
            y = screen_height
            dx = 0
            dy = -speed
        elif side == 3:
            # Right
            x = screen_width
            y = screen_height/2 - square_size/2
            dx = -speed
            dy = 0
        elif side == 4:
            # Left
            x = -square_size
            y = screen_height/2 - square_size/2
            dx = speed
            dy = 0

        # Create a new square and add it to the list
        new_square = pygame.Rect(x, y, square_size, square_size)
        squares.append((new_square, dx, dy))

    # Increase the speed every 30 seconds
    if current_time - last_speed_increase_time > 30000:
        last_speed_increase_time = current_time
        print("increasing speed")
        speed += 1

    # Move the squares
    for square in squares:
        square_rect, dx, dy = square
        square_rect.move_ip(dx, dy)

        # Check for collision with the center square
        if square_rect.colliderect(center_square):
            if (dx > 0 and direction_input != "right") or (dx < 0 and direction_input != "left") or (dy > 0 and direction_input != "down") or (dy < 0 and direction_input != "up"):
                score += 1
                print("Score:", score)
            else:
                lives-=1
            squares.remove(square)

        # Remove the square if it goes off screen
        if square_rect.left > screen_width or square_rect.right < 0 or square_rect.top > screen_height or square_rect.bottom < 0:
            squares.remove(square)

        # Draw the square
        if dx > 0:
            square_image = pygame.image.load("Imgs/right.png").convert_alpha()
        elif dx < 0:
            square_image = pygame.image.load("Imgs/left.png").convert_alpha()
        elif dy > 0:
            square_image = pygame.image.load("Imgs/down.png").convert_alpha()
        elif dy < 0:
            square_image = pygame.image.load("Imgs/upper.png").convert_alpha()

        square_image = pygame.transform.scale(square_image, (square_size, square_size))
        screen.blit(square_image, square_rect)

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


    if lives == 3:
        screen.blit(heart0, (screen_width/2-64, screen_height/2-64))
    elif lives == 2:
        screen.blit(heart1, (screen_width/2-64, screen_height/2-64))
    elif lives == 1:
        screen.blit(heart2, (screen_width/2-64, screen_height/2-64))
    elif lives == 0:
        screen.blit(heart3, (screen_width/2-64, screen_height/2-64))

    # Draw the center square
    screen.blit(box, center_square)
    screen.blit(cat, (screen_width/2-64, 100))
    barrier_side(center_square)

    # Update the display
    pygame.display.update()
    pygame.time.delay(5)

    # Clear the screen to avoid leaving a trail
    screen.fill(background_color)
