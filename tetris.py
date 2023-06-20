import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the dimensions of the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

# Set the dimensions of the game board
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

# Define the shapes of the blocks
SHAPES = [
    [(0, 1, 0), (1, 1, 1), (0, 0, 0)],  # L-shape
    [(1, 1), (1, 1)],  # Square
    [(0, 0, 1), (1, 1, 1), (0, 0, 0)],  # T-shape
    [(1, 1, 0), (0, 1, 1), (0, 0, 0)],  # S-shape
    [(0, 1, 1), (1, 1, 0), (0, 0, 0)],  # Z-shape
    [(0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0)],  # I-shape
    [(1, 1, 1), (0, 1, 0), (0, 0, 0)]  # J-shape
]

# Define a class for the blocks
class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice([RED, GREEN, BLUE])

    def draw(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        pygame.Rect(
                            (self.x + j) * BLOCK_SIZE,
                            (self.y + i) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE
                        )
                    )

# Define a class for the game board
class Board:
    def __init__(self):
        self.grid = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_block = None

    def add_block(self):
        shape = random.choice(SHAPES)
        x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        y = 0
        self.current_block = Block(x, y, shape)

    def move_block_down(self):
        if self.current_block:
            self.current_block.y += 1
            if self.collides():
                self.current_block.y -= 1
                self.add_to_grid()

    def move_block_left(self):
        if self.current_block:
            self.current_block.x -= 1
            if self.collides():
                self.current_block.x += 1

    def move_block_right(self):
        if self.current_block:
            self.current_block.x += 1
            if self.collides():
                self.current_block.x -= 1

    def rotate_block(self):
        if self.current_block:
            old_shape = self.current_block.shape
            new_shape = [[0] * len(old_shape) for _ in range(len(old_shape[0]))]
            for i in range(len(old_shape)):
                for j in range(len(old_shape[0])):
                    new_shape[j][len(old_shape)-1-i] = old_shape[i][j]
            self.current_block.shape = new_shape
            if self.collides():
                self.current_block.shape = old_shape

    def collides(self):
        if self.current_block:
            for i in range(len(self.current_block.shape)):
                for j in range(len(self.current_block.shape[i])):
                    if (
                        self.current_block.shape[i][j] == 1 and
                        (self.current_block.y + i >= BOARD_HEIGHT or
                         self.current_block.x + j < 0 or
                         self.current_block.x + j >= BOARD_WIDTH or
                         self.grid[self.current_block.y + i][self.current_block.x + j] != 0)
                    ):
                        return True
        return False

    def add_to_grid(self):
        fori in range(len(self.current_block.shape)):
            for j in range(len(self.current_block.shape[i])):
                if self.current_block.shape[i][j] == 1:
                    self.grid[self.current_block.y + i][self.current_block.x + j] = self.current_block.color
        self.current_block = None

    def draw(self):
        # Draw the grid
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        pygame.Rect(
                            j * BLOCK_SIZE,
                            i * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE
                        )
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        self.grid[i][j],
                        pygame.Rect(
                            j * BLOCK_SIZE,
                            i * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE
                        )
                    )

        # Draw the current block
        if self.current_block:
            self.current_block.draw()

# Create a new game board
board = Board()

# Set up the game loop
clock = pygame.time.Clock()
game_over = False

# Start the game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                board.move_block_left()
            elif event.key == pygame.K_RIGHT:
                board.move_block_right()
            elif event.key == pygame.K_DOWN:
                board.move_block_down()
            elif event.key == pygame.K_UP:
                board.rotate_block()

    # Move the block down
    board.move_block_down()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the game board
    board.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)

# Quit Pygame
pygame.quit()
