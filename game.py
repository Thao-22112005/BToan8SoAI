import pygame
import random
import time
from astar import solve_astar

# ================= CONFIG =================
N = 3
TILE = 100
MARGIN = 5
AI_DELAY = 0.2
# ==========================================


def shuffle_state(state, steps=100):
    import astar
    cur = list(state)
    for _ in range(steps):
        cur = list(random.choice(astar.neighbors(tuple(cur)))[0])
    return tuple(cur)


def apply_move(state, move):
    z = state.index(0)
    r, c = divmod(z, N) # r = z // N  (hàng)
                        # c = z % N   (cột) N =3, z là vị trí index = 0, ví dụ index của số 0 là
                        # 4 thì z//N=4//3=1 (hàng 1) và z%N=4%3=1 (cột 1) 
                        # luu ý hàng và cột đều tính từ 0
    s = list(state)

    if move == 'U': nr, nc = r - 1, c
    elif move == 'D': nr, nc = r + 1, c
    elif move == 'L': nr, nc = r, c - 1
    elif move == 'R': nr, nc = r, c + 1
    else: return state
    #nr, nc là tọa độ “new row, new col” của ô mà ô trống sẽ đổi chỗ với nó.
    #Nếu move không hợp lệ (khác U/D/L/R) thì trả về y nguyên state.

    nz = nr * N + nc
    s[z], s[nz] = s[nz], s[z]
    return tuple(s)


def is_goal(state):
    return state == tuple(range(1, N * N)) + (0,)  #N=3 => range(1,9)+0 => số chạy từ 1 đến 8 và 0 ở cuối


def run_game(screen, font, mode, tiles=None):
    state = shuffle_state(tuple(range(1, N * N)) + (0,))
    ai_moves = []
    idx = 0
    solving = False
    last = time.time()

    access_message = ""   # 🔥 MESSAGE TRẠNG THÁI

    clock = pygame.time.Clock()

    # -------- CANH GIỮA BOARD --------
    W, H = screen.get_size()
    BOARD_SIZE = N * TILE + (N + 1) * MARGIN
    OFFSET_X = (W - BOARD_SIZE) // 2
    OFFSET_Y = 40

    # ================= GAME LOOP =================
    while True:
        clock.tick(30)
        screen.fill((40, 40, 40))

        # ---------- DRAW BOARD ----------
        for i, v in enumerate(state):
            if v == 0: continue
            r, c = divmod(i, N)

            x = OFFSET_X + c * TILE + (c + 1) * MARGIN
            y = OFFSET_Y + r * TILE + (r + 1) * MARGIN
            rect = pygame.Rect(x, y, TILE, TILE)

            if mode == "number":
                pygame.draw.rect(screen, (245, 245, 245), rect)
                t = font.render(str(v), True, (0, 0, 0))
                screen.blit(t, t.get_rect(center=rect.center))
            else:
                screen.blit(tiles[v - 1], rect)

            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # ---------- TEXT ----------
        info = font.render("K_A:AI   K_R:Reset   ESC:Menu", True, (255, 255, 255))
        screen.blit(
            info,
            (W // 2 - info.get_width() // 2,
             OFFSET_Y + BOARD_SIZE + 20)
        )

        # 🔥 MESSAGE DƯỚI HƯỚNG DẪN
        if access_message:
            msg = font.render(access_message, True, (255, 200, 0))
            screen.blit(
                msg,
                (W // 2 - msg.get_width() // 2,
                 OFFSET_Y + BOARD_SIZE + 55)
            )

        pygame.display.flip()

        # ================= EVENTS =================
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return

                if e.key == pygame.K_r:
                    state = shuffle_state(tuple(range(1, N * N)) + (0,))
                    solving = False
                    access_message = "Game has been reset"

                if e.key == pygame.K_a:
                    access_message = "The AI ​is calculating..."
                    pygame.display.flip()

                    ai_moves = solve_astar(state)
                    if not ai_moves:
                        access_message = "AI could not find the solution"
                        solving = False
                    else:
                        idx = 0
                        solving = True

            # ---------- MOUSE ----------
            if e.type == pygame.MOUSEBUTTONDOWN and not solving:
                mx, my = e.pos
                mx -= OFFSET_X
                my -= OFFSET_Y

                if 0 <= mx < BOARD_SIZE and 0 <= my < BOARD_SIZE:
                    c = mx // (TILE + MARGIN)
                    r = my // (TILE + MARGIN)

                    z = state.index(0)
                    zr, zc = divmod(z, N)

                    if abs(zr - r) + abs(zc - c) == 1:
                        s = list(state)
                        s[z], s[r * N + c] = s[r * N + c], s[z]
                        state = tuple(s)

                        if is_goal(state):
                            access_message = "YOU'VE DONE! Congratulations!"

        # ================= AI MOVE =================
        if solving and idx < len(ai_moves):
            if time.time() - last > AI_DELAY:
                state = apply_move(state, ai_moves[idx])
                idx += 1
                last = time.time()

                if is_goal(state):
                    access_message = " AI SUCCESSFULLY SOLVED!"
                    solving = False
