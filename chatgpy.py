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

# Set the font for displaying text
font = pygame.font.SysFont(None, 30)

# Set the square size
square_size = 64

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


# Create the center square
center_square = pygame.Rect(screen_width/2 - square_size, screen_height/2 - square_size, 100, 100)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
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
            print(dx, dy)
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

    # Draw the center square
    screen.blit(box, center_square)
    screen.blit(cat, (screen_width/2-64, 100))

    # Update the display
    pygame.display.update()
    pygame.time.delay(5)

    # Clear the screen to avoid leaving a trail
    screen.fill(background_color)
