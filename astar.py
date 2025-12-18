import heapq

N = 3

def manhattan(state):
    dist = 0
    for i, v in enumerate(state):
        if v == 0: continue
        tr = (v - 1) // N
        tc = (v - 1) % N
        r, c = divmod(i, N) #r la row, c la column
        dist += abs(r - tr) + abs(c - tc)
    return dist

def neighbors(state):
    res = []
    z = state.index(0)
    r, c = divmod(z, N)
    moves = [(-1,0,'U'),(1,0,'D'),(0,-1,'L'),(0,1,'R')]
    for dr, dc, a in moves:
        nr, nc = r+dr, c+dc
        if 0 <= nr < N and 0 <= nc < N:
            s = list(state)
            nz = nr*N + nc
            s[z], s[nz] = s[nz], s[z]
            res.append((tuple(s), a))
    return res

def solve_astar(start):
    goal = tuple(range(1, N*N)) + (0,)

    # OPEN: (f, g, state)
    open_set = [(manhattan(start), 0, start)]
    
    # CLOSE: các trạng thái đã mở rộng
    closed = set()

    came = {}          # truy vết đường đi
    g = {start: 0}     # chi phí từ start → state

    while open_set:
        # Lấy trạng thái có f nhỏ nhất
        _, cost, cur = open_set.pop(0)

        # Nếu đã duyệt rồi → bỏ qua
        if cur in closed:
            continue

        # Đánh dấu đã duyệt
        closed.add(cur)

        # Đạt đích
        if cur == goal:
            path = []
            while cur in came:
                cur, act = came[cur]
                path.append(act)
            return path[::-1]

        # Duyệt hàng xóm
        for ns, act in neighbors(cur):
            if ns in closed:
                continue

            ng = g[cur] + 1

            # Nếu tìm được đường đi tốt hơn
            if ns not in g or ng < g[ns]:
                g[ns] = ng
                f = ng + manhattan(ns)
                open_set.append((f, ng, ns))
                open_set.sort(key=lambda x: x[0])
                came[ns] = (cur, act)

    # Không tìm được lời giải
    return []

