import heapq
N = 3


def build_goal_pos(goal):
    pos = {}
    for idx, v in enumerate(goal):
        pos[v] = divmod(idx, N)   # v -> (row, col) #Ví dụ goal:(1,2,3,4,0,5,6,7,8)
                                  # thì pos[5] = divmod(4,3) = (1,1) (hàng 1,cột 1)=>gán với tr,tc ở manhattan
    return pos


# Hàm tính toán khoảng cách Manhattan là hàm ưngs dụng phổ biến trong thuật toán A* để đánh giá chi phí ước lượng từ trạng thái hiện tại đến trạng thái đích.
# Manhattan distance là tổng khoảng cách theo hàng và cột từ vị trí hiện tại của mỗi ô đến vị trí đích của nó.
# Manhattan = |x1 - x2| + |y1 - y2|
# vdu ô số 5 đang ở vị trí (1,2) mà vị trí đích của nó là (1,1)
# thì khoảng cách Manhattan của ô số 5 là |1-1| + |2-1| = 1
def manhattan(state, goal_pos):
    dist = 0
    for i, v in enumerate(state): #i là index, v là giá trị tại index đó
                                  #enumerate(state) duyệt qua từng ô trong mảng 1 chiều
        if v == 0: 
            continue

        # nhưng nếu goal bất kì thì phải tra vị trí đích từ goal_pos
        tr, tc = goal_pos[v]      # tr là target row (hàng đích) của ô v
                                  # tc là target column (cột đích) của ô v

        r, c = divmod(i, N)       # r la row, c la column hàm divmod(i,N) trả về (i//N, i%N)
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

def reconstruct_path(start, goal, came, verbose=True): #verbose là để in chi tiết đường đi nếu = True
    if start == goal:
        if verbose:
            print("Tổng bước: 0")
        return []

    if goal not in came:
        if verbose:
            print("Không có đường đi (goal không truy vết được).")
        return []

    path = []
    cur = goal # bắt đầu từ goal và truy ngược về start
    while cur != start:
        parent, act = came[cur]
        path.append(act)
        cur = parent

    path.reverse()

    if verbose:
        for i, m in enumerate(path, start=1): #i là số bước, m là hành động di chuyển
                                              # start=1 để đánh số bước từ 1
            print(f"{i}-{m}")
        print(f"Tổng bước: {len(path)}")

    return path


def solve_astar(start, goal, verbose=False):
    # goal được truyền vào từ game.py (goal bất kì)
    goal_pos = build_goal_pos(goal)

    # OPEN: (f, g, state)
    # dùng heapq để lấy f nhỏ nhất nhanh hơn
    open_set = []
    heapq.heappush(open_set, (manhattan(start, goal_pos), 0, start)) 
    
    # CLOSE: các trạng thái đã mở rộng
    closed = set()

    came = {}          # truy vết đường đi
    g = {start: 0}     # chi phí từ start → state

    while open_set:
        # Lấy trạng thái có f nhỏ nhất
        _, cost, cur = heapq.heappop(open_set)

        # Nếu đã duyệt rồi → bỏ qua
        if cur in closed:
            continue

        # Đánh dấu đã duyệt
        closed.add(cur)

        # Đạt đích
        if cur == goal:
            return reconstruct_path(start, goal, came, verbose=verbose)

        # Duyệt hàng xóm
        for ns, act in neighbors(cur): # ns là trạng thái hàng xóm, act là hành động di chuyển
            if ns in closed: 
                continue

            ng = g[cur] + 1 # chi phí từ start → ns

            # Nếu tìm được đường đi tốt hơn
            if ns not in g or ng < g[ns]: 
                g[ns] = ng
                f = ng + manhattan(ns, goal_pos) # f = g + h
                heapq.heappush(open_set, (f, ng, ns)) # Đưa ns vào OPEN
                came[ns] = (cur, act) # Lưu lại đường đi

    # Không tìm được lời giải
    return []
