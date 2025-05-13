# NOTE: If running the game gives you an error, run either "sudo apt install python3-pygame" OR "pip install pygame" in the terminal.
import pygame
import threading
import time
import random
from collections import deque
from input_structure import Input
from joystick import Joystick

pygame.init()
JOYSTICK = Joystick()

# Set up the display
GRID_SIZE = 56
GRID_WIDTH, GRID_HEIGHT = 16, 15  # 16 columns x 15 rows
WIDTH, HEIGHT = GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Score: 0")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Snake and food sizes
SNAKE_SPEED = 8

# Input poll (ms)
INPUT_POLL = 20

# Fonts
FONT = pygame.font.SysFont(None, 25)

# Pause variable
PAUSED = False

# Input buffer
input_buffer = []

# Current direction (initialized to right)
current_direction = Input.RIGHT

# Function to draw snake
def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(WINDOW, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Function to display message
def message(msg, color):
    mesg = FONT.render(msg, True, color)
    WINDOW.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# Function to generate random food position
def generate_food():
    return random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT)

def check_input():
    global current_direction, JOYSTICK
    # TODO: Replace "False" with the correct method call to the joystick object you make
    # Can't double-back on your snake
    if JOYSTICK.get_direction() == "Left" and current_direction != Input.RIGHT:
        input_buffer.append(Input.LEFT)
    elif JOYSTICK.get_direction() == "Right" and current_direction != Input.LEFT:
        input_buffer.append(Input.RIGHT)
    elif JOYSTICK.get_direction() == "Up" and current_direction != Input.DOWN:
        input_buffer.append(Input.UP)
    elif JOYSTICK.get_direction() == "Down" and current_direction != Input.UP:
        input_buffer.append(Input.DOWN)
    
    if JOYSTICK.get_button_pressed(): # Pressing in on the joystick should pause the game
        input_buffer.append(Input.PRESS)

# Function to main loop
def game_loop():
    global PAUSED, current_direction
    game_over = False
    game_close = False

    while True:
        
        # Reset the title tab
        pygame.display.set_caption("Snake Game - Score: 0")
        
        # Initial snake position (// performs division and rounds down)
        snake_list = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        length_of_snake = 1

        # Food position
        food_x, food_y = generate_food()

        # Score
        score = 0

        # Main game loop
        while not game_over:
            
            inputs_queue = deque(input_buffer)
            input_buffer.clear()

            # Pause mechanism
            if PAUSED:
                WINDOW.fill(BLACK)
                message("Paused. Press in on the joystick to continue or [Escape] to quit.", WHITE)
                pygame.display.update()
                
                while inputs_queue:
                    input_item : Input = inputs_queue.popleft()
                    if input_item == Input.PRESS:
                        PAUSED = False
                        break

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Straight kill the game
                            pygame.quit() # Kill game
                            quit() # Kill program
                            
                continue

            # Input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # An attempt to close the window or program
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # Escape pauses the game
                        PAUSED = True
                        
            new_direction: Input = None
            
            while inputs_queue:
                input_item : Input = inputs_queue.popleft()
                
                if input_item != Input.PRESS:
                    new_direction = input_item
                else:
                    PAUSED = True
                              
            current_direction = new_direction if new_direction != None else current_direction
            
            if PAUSED == False:
                # Move the snake
                x, y = snake_list[0]
                if current_direction == Input.RIGHT:
                    x += 1
                elif current_direction == Input.LEFT:
                    x -= 1
                elif current_direction == Input.UP:
                    y -= 1
                elif current_direction == Input.DOWN:
                    y += 1

                # Check for collision with walls or self
                if x >= GRID_WIDTH or x < 0 or y >= GRID_HEIGHT or y < 0 or (x, y) in snake_list[1:]:
                    game_over = True
                    game_close = True

                # Check if snake eats food
                if x == food_x and y == food_y:
                    food_x, food_y = generate_food()
                    length_of_snake += 1
                    score += 1
                    pygame.display.set_caption(f"Snake Game - Score: {score}")
                else:
                    snake_list.pop()

                # Update snake position
                snake_list.insert(0, (x, y))

            # Drawing
            WINDOW.fill(BLACK)
            pygame.draw.rect(WINDOW, RED, (food_x * GRID_SIZE, food_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            draw_snake(snake_list)

            pygame.display.update()

            # Game speed
            pygame.time.Clock().tick(SNAKE_SPEED)

        # End game message
        while game_close:
            WINDOW.fill(BLACK)
            message("Game Over! Press in on the joystick to play again or [Escape] to quit.", WHITE)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # Kill game
                    quit() # Kill program
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_close = False
                        game_over = True
                        
            # TODO: Replace "False" with a call to the appropriate method in your joystick instance
            if JOYSTICK.get_button_pressed():
                game_close = False
                game_over = False

        if game_over:
            pygame.quit() # Kill game
            quit() # Kill program
            
def input_loop(interval_ms: int):
    while True:
        check_input() # Poll the input device
        time.sleep(interval_ms / 1000.0) # Convert ms to seconds

if __name__ == '__main__':
    print ('Program is starting ... ') # Program entrance
    try:
        threading.Thread(target=input_loop, args=(INPUT_POLL,), daemon=True).start()
        game_loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        pass
