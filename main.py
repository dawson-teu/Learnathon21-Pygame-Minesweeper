import pygame
import random

from pygame.constants import *
from pygame.locals import *


def neighbours(pos, width, height):
    output = []
    for x_offset in range(-1, 2):
        for y_offset in range(-1, 2):
            if x_offset == 0 and y_offset == 0:
                continue
            new_x = pos[0] + x_offset
            new_y = pos[1] + y_offset
            if 0 <= new_x < width and 0 <= new_y < height:
                output.append((new_x, new_y))
    return output


def setup():
    mines_setup = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for _ in range(NUM_MINES):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        while mines_setup[y][x]:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
        mines_setup[y][x] = True

    mine_count_setup = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for i_setup in range(GRID_HEIGHT):
        for j_setup in range(GRID_WIDTH):
            count = 0
            for neighbour_setup in neighbours((j_setup, i_setup), GRID_WIDTH, GRID_HEIGHT):
                if mines_setup[neighbour_setup[1]][neighbour_setup[0]]:
                    count += 1
            mine_count_setup[i_setup][j_setup] = count

    is_uncovered_setup = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    is_flagged_setup = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    return mines_setup, mine_count_setup, is_uncovered_setup, is_flagged_setup


def start_game():
    mines, mine_count, is_uncovered, is_flagged = setup()

    is_game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if event.button == 1 and not is_flagged[y_pos][x_pos]:
                    if mines[y_pos][x_pos]:
                        print('GAME OVER')
                        return
                    elif mine_count[y_pos][x_pos] > 0:
                        is_uncovered[y_pos][x_pos] = True
                    else:
                        queue = [(x_pos, y_pos)]
                        is_uncovered[y_pos][x_pos] = True
                        while len(queue) > 0:
                            cur_pos = queue.pop(0)
                            for neighbour in neighbours(cur_pos, GRID_WIDTH, GRID_HEIGHT):
                                if not mines[neighbour[1]][neighbour[0]] and not is_uncovered[neighbour[1]][neighbour[0]]:
                                    is_uncovered[neighbour[1]][neighbour[0]] = True
                                    if mine_count[neighbour[1]][neighbour[0]] == 0:
                                        queue.append(neighbour)
                elif event.button == 3:
                    is_flagged[y_pos][x_pos] = not is_flagged[y_pos][x_pos]
            elif event.type == QUIT:
                return 'QUIT'
        if is_game_over:
            continue
        screen.blit(background, (0, 0))
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if not is_uncovered[i][j]:
                    pygame.draw.rect(screen, (255, 168, 54), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif mine_count[i][j] > 0:
                    txt_w, txt_h = text.size(str(mine_count[i][j]))
                    text_pos = j * CELL_SIZE + CELL_SIZE // 2 - txt_w // 2, i * CELL_SIZE + CELL_SIZE // 2 - txt_h // 2
                    screen.blit(text.render(str(mine_count[i][j]), False, num_color[mine_count[i][j]]), text_pos)
                if is_flagged[i][j]:
                    pygame.draw.rect(screen, (255, 50, 50), (j * CELL_SIZE + 10, i * CELL_SIZE + 10, 55, 30))
                    pygame.draw.rect(screen, (255, 50, 50), (j * CELL_SIZE + 10, i * CELL_SIZE + 40, 10, 30))

        screen.blit(grid_lines, (0, 0))
        pygame.display.flip()


pygame.init()

CELL_SIZE = 75
GRID_WIDTH = 8
GRID_HEIGHT = 8
NUM_MINES = 10

text = pygame.font.SysFont('sans-serif', 75)

screen = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))

background = pygame.Surface((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
background.fill((43, 255, 96))

num_color = {1: (38, 53, 255), 2: (0, 66, 4), 3: (255, 31, 31), 4: (175, 56, 255), 5: (252, 98, 50), 6: (0, 87, 78), 7: (153, 133, 0), 8: (0, 0, 0)}

grid_lines = pygame.Surface((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT), flags=SRCALPHA)
for index in range(1, GRID_WIDTH + 1):
    pygame.draw.line(grid_lines, (50, 50, 50), (index * CELL_SIZE, 0), (index * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), width=2)

for index in range(1, GRID_HEIGHT + 1):
    pygame.draw.line(grid_lines, (50, 50, 50), (0, index * CELL_SIZE), (GRID_WIDTH * CELL_SIZE, index * CELL_SIZE), width=2)

start_game()
