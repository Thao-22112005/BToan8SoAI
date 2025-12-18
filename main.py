import pygame
from game import run_game, GOAL_DEFAULT
from menu import draw_menu, init_menu_background

# -------- CONFIG --------
N = 3
TILE = 100
MARGIN = 5

BOARD_SIZE = N*TILE + (N+1)*MARGIN  # 320

SCREEN_W = 600
SCREEN_H = 500
IMAGE_PATH = "icon.png"
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("8 Puzzle A*")
pygame.display.set_icon(pygame.image.load(IMAGE_PATH))
font = pygame.font.SysFont(None, 40)
init_menu_background(screen)

# -------- LOAD IMAGE PUZZLE --------
IMAGE = pygame.image.load("bg.jpg").convert()
IMAGE = pygame.transform.scale(IMAGE, (BOARD_SIZE, BOARD_SIZE))

tiles = []
for i in range(N * N):
    r, c = divmod(i, N)
    x = c * TILE + (c + 1) * MARGIN
    y = r * TILE + (r + 1) * MARGIN
    rect = pygame.Rect(x, y, TILE, TILE)
    tiles.append(IMAGE.subsurface(rect))

# -------- MAIN LOOP --------
while True:
    screen.fill((30, 30, 30))
    btn1, btn2 = draw_menu(screen, font)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

        if e.type == pygame.MOUSEBUTTONDOWN:
            if btn1.collidepoint(e.pos):
                run_game(screen, font, "number", goal=GOAL_DEFAULT)
            if btn2.collidepoint(e.pos):
                run_game(screen, font, "image", tiles, goal=GOAL_DEFAULT)

    pygame.display.flip()
