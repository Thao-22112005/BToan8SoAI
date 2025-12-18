import pygame
import random
import time
from astar import solve_astar, neighbors

# ================= CONFIG =================
N = 3
TILE = 100
MARGIN = 5
AI_DELAY = 0.2

# GOAL DEFAULT (bạn tự set ở đây - goal bất kì)
# VD goal chuẩn: (1,2,3,4,5,6,7,8,0)
# VD goal 0 ở giữa: (1,2,3,4,0,5,6,7,8)
GOAL_DEFAULT = (1, 2, 3,
                4, 5, 6,
                7, 8, 0)

# GOAL_DEFAULT = (1, 2, 3,
#                 4, 0, 5,
#                 6, 7, 8)
# ==========================================


def shuffle_state(state, steps=100):
    # state sẽ được xáo bằng các bước hợp lệ từ goal -> đảm bảo luôn giải được về goal
    cur = list(state)
    for _ in range(steps):
        cur = list(random.choice(neighbors(tuple(cur)))[0])
    return tuple(cur)


def remap_tiles_for_goal(tiles, goal):
    """
    remap ảnh theo goal
    tiles đang cắt theo "vị trí ảnh gốc" (pos 0..8).
    Nhưng khi goal thay đổi, ta muốn khi state==goal thì ảnh vẫn "đúng theo goal".

    Trả về tiles_by_value sao cho:
    tiles_by_value[v-1] là mảnh ảnh đúng dành cho tile số v theo goal.
    """
    tiles_by_value = [None] * (N * N - 1)  # cho 1..8
    for pos, v in enumerate(goal):
        if v == 0:
            continue
        tiles_by_value[v - 1] = tiles[pos]  # mảnh ảnh đúng của vị trí pos trong ảnh gốc
    return tiles_by_value


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

    # thêm check biên để tránh đi ra ngoài
    if not (0 <= nr < N and 0 <= nc < N):
        return state

    nz = nr * N + nc
    s[z], s[nz] = s[nz], s[z]
    return tuple(s)


def is_goal(state, goal=GOAL_DEFAULT):
    return state == goal  


def run_game(screen, font, mode, tiles=None, goal=GOAL_DEFAULT):
    # start được shuffle từ goal -> luôn đảm bảo có lời giải về goal
    state = shuffle_state(goal)
    # state = (1, 2, 3,
    #          4, 0, 6,
    #          7, 5, 8)

    ai_moves = []
    idx = 0
    solving = False
    last = time.time()

    access_message = ""   # MESSAGE TRẠNG THÁI

    clock = pygame.time.Clock()

    # -------- CANH GIỮA BOARD --------
    W, H = screen.get_size()
    BOARD_SIZE = N * TILE + (N + 1) * MARGIN
    OFFSET_X = (W - BOARD_SIZE) // 2
    OFFSET_Y = 40

    # remap ảnh theo goal 
    tiles_by_value = None
    if mode == "image" and tiles is not None:
        tiles_by_value = remap_tiles_for_goal(tiles, goal)

    # ================= GAME LOOP =================
    while True:
        clock.tick(30) # GIỚI HẠN 30 FPS
        # ================= DRAW =================
        screen.fill((40, 40, 40)) # DARK BACKGROUND

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
                # dùng tiles_by_value để ảnh đúng theo goal
                screen.blit(tiles_by_value[v - 1], rect)

            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # ---------- TEXT ----------
        info = font.render("K_A:AI   K_R:Reset   ESC:Menu", True, (255, 255, 255))
        screen.blit(
            info,
            (W // 2 - info.get_width() // 2,
             OFFSET_Y + BOARD_SIZE + 20)
        )

        # MESSAGE DƯỚI HƯỚNG DẪN
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
                    state = shuffle_state(goal)
                    solving = False
                    access_message = "Game has been reset"

                if e.key == pygame.K_a:
                    access_message = "The AI ​is calculating..."
                    pygame.display.flip()

                    ai_moves = solve_astar(state, goal, verbose=True)
                    if not ai_moves:
                        access_message = "AI could not find the solution"
                        solving = False
                    else:
                        idx = 0
                        solving = True

            # ---------- MOUSE ----------
            if e.type == pygame.MOUSEBUTTONDOWN and not solving: # CHỈ CHƠI KHI KHÔNG ĐANG GIẢI BẰNG AI
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

                        if is_goal(state, goal):
                            access_message = "YOU'VE DONE! Congratulations!"

        # ================= AI MOVE =================
        if solving and idx < len(ai_moves):
            if time.time() - last > AI_DELAY:
                state = apply_move(state, ai_moves[idx])
                idx += 1
                last = time.time()

                if is_goal(state, goal):
                    access_message = " AI SUCCESSFULLY SOLVED!"
                    solving = False
