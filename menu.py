# menu.py
import pygame

BG_IMAGE = None

TITLE_COLOR = (55, 78, 112)

TEXT_COLOR = (255,255,255)
TEXT_HOVER =  (220, 80, 80)


def init_menu_background(screen):
    global BG_IMAGE
    BG_IMAGE = pygame.image.load("menu2.jpg").convert()
    BG_IMAGE = pygame.transform.scale(
        BG_IMAGE,
        (screen.get_width(), screen.get_height())
    )

def draw_menu(screen, font):
    # ----- DRAW BACKGROUND -----
    if BG_IMAGE:
        screen.blit(BG_IMAGE, (0, 0))
    else:
        screen.fill((25, 25, 25))

    W, H = screen.get_size()
    mouse=pygame.mouse.get_pos()

    # ----- TITLE -----
    title_font = pygame.font.SysFont(None, 47)
    title = title_font.render("Welcome To Our Game (8 Puzzle - A*)", True, TITLE_COLOR)
    screen.blit(title, title.get_rect(center=(W//2, H//2 - 140)))

    # ----- BUTTONS -----
    btn_w, btn_h = 400, 80
    gap = 20

    btn1 = pygame.Rect(
        W//2 - btn_w//2,
        H//2 - btn_h - gap//2,
        btn_w, btn_h
    )
    btn2 = pygame.Rect(
        W//2 - btn_w//2,
        H//2 + gap//2,
        btn_w, btn_h
    )

    pygame.draw.rect(screen, (70, 130, 180), btn1, border_radius=20)
    pygame.draw.rect(screen, (100, 180, 100), btn2, border_radius=20)

    # ----- TEXT HOVER -----
    t1_color = TEXT_HOVER if btn1.collidepoint(mouse) else TEXT_COLOR
    t2_color = TEXT_HOVER if btn2.collidepoint(mouse) else TEXT_COLOR

    t1 = font.render("Play Puzzle With Numbers", True, t1_color)
    t2 = font.render("Play Puzzle With Images", True, t2_color)

    screen.blit(t1, t1.get_rect(center=btn1.center))
    screen.blit(t2, t2.get_rect(center=btn2.center))

    return btn1, btn2
