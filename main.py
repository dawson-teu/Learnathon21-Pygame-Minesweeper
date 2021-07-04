import pygame
import random

from pygame.constants import *
from pygame.locals import *

pygame.init()

CELL_SIZE = 75
GRID_WIDTH = 8
GRID_HEIGHT = 10
NUM_MINES = 10

screen = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))

background = pygame.Surface((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
background.fill((43, 255, 96))

grid_lines = pygame.Surface((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT), flags=SRCALPHA)
for i in range(1, GRID_WIDTH + 1):
    pygame.draw.line(grid_lines, (50, 50, 50), (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), width=2)

for i in range(1, GRID_HEIGHT + 1):
    pygame.draw.line(grid_lines, (50, 50, 50), (0, i * CELL_SIZE), (GRID_WIDTH * CELL_SIZE, i * CELL_SIZE), width=2)

is_quit = False
mines = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
for i in range(NUM_MINES):
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    while mines[y][x]:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
    mines[y][x] = True
for i in range(GRID_HEIGHT):
    output = ""
    for j in range(GRID_WIDTH):
        if mines[i][j]:
            output += "#"
        else:
            output += "."
    print(output)
while not is_quit:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            print(event.pos, event.button)
        elif event.type == QUIT:
            is_quit = True
    screen.blit(background, (0, 0))
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if mines[i][j]:
                pygame.draw.rect(screen, (255, 168, 54), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    screen.blit(grid_lines, (0, 0))
    pygame.display.flip()
