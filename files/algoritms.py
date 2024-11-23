from math import ceil
from copy import copy

a, b, n, m, k = map(int, input().split())
len_loop = a + b
rez = 0

if k >= len_loop:
    if k % len_loop > 0:
        if 0 < k % len_loop <= a:
            rez += k % len_loop
        else:
            rez += a
    rez += k // len_loop * a
else:
    rez += min(a, k)

for i in range(1, k // n + 1, 1):
    n_pos = n * i
    if i * n > k:
        break
    pos = n_pos % len_loop
    if 0 < pos <= a:
        rez -= 1

for i in range(1, k // m + 1, 1):
    m_pos = m * i
    if i * m > k:
        break
    pos = m_pos % len_loop
    if 0 < pos <= a:
        rez += 1

print(rez)



# from copy import copy
#
# def check_in_board(cell):
#     if 0 <= cell[0] < 8 and 0 <= cell[1] < 8:
#         return True
#
# def get_kingdom(cell):
#     posible_cells = []
#     moves = [[-1, -1], [1, 1], [-1, 1], [1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
#     for move in moves:
#         new_cell = [cell[0]+move[0], cell[1]+move[1]]
#         if check_in_board(new_cell):
#             posible_cells.append(new_cell)
#
#     return posible_cells
#
# def get_line_move(board, board2, cell, move):
#     is_check = False
#     board2[cell[0]][cell[1]] = 1
#     cell[0] += move[0]
#     cell[1] += move[1]
#     while check_in_board(cell):
#         if board[cell[0]][cell[1]] == "K":
#             is_check = True
#         elif board[cell[0]][cell[1]] != ".":
#             board2[cell[0]][cell[1]] = 1
#             break
#         board2[cell[0]][cell[1]] = 1
#         cell[0] += move[0]
#         cell[1] += move[1]
#
#     return is_check
#
# def get_rook(board, board2, cell):
#     is_check = False
#     moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
#     for move in moves:
#         if get_line_move(board, board2, copy(cell), move):
#             is_check = True
#
#     return is_check
#
# def get_bishop(board, board2, cell):
#     is_check = False
#     moves = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
#     for move in moves:
#         if get_line_move(board, board2, copy(cell), move):
#             is_check = True
#
#     return is_check
#
# def get_queen(board, board2, cell):
#     is_check = False
#     if get_rook(board, board2, copy(cell)):
#         is_check = True
#     if get_bishop(board, board2, copy(cell)):
#         is_check = True
#
#     return is_check
#
#
# def get_horse(board, board2, cell):
#     is_check = False
#     moves = [[2, 1], [2, -1], [1, 2], [1, -2], [-1, -2], [-1, 2], [-2, 1], [-2, -1]]
#     for move in moves:
#         new_cell = [cell[0]+move[0], cell[1]+move[1]]
#         if check_in_board(new_cell):
#             board2[new_cell[0]][new_cell[1]] = 1
#             if board[new_cell[0]][new_cell[1]] == "K":
#                 is_check = True
#
#     return is_check
#
# def get_pawn(board, board2, cell):
#     is_check = False
#     cell1, cell2 = [cell[0]-1, cell[1]+1], [cell[0]-1, cell[1]-1]
#     for new_cell in [cell1, cell2]:
#         if check_in_board(new_cell):
#             board2[new_cell[0]][new_cell[1]] = 1
#             if board[new_cell[0]][new_cell[1]] == "K":
#                 is_check = True
#
#     return is_check
#
# board = [list(input()) for _ in range(8)]
# board2 = [[0] * 8 for _ in range(8)]
#
# figures = {
#     ".": None,
#     "r": get_rook,
#     "b": get_bishop,
#     "n": get_horse,
#     "Q": get_queen,
#     "p": get_pawn,
#     "K": None
# }
#
# columns = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
#
# k_cell = None
# check_figures = []
# for i, raw in enumerate(board):
#     for a, cell in enumerate(raw):
#         if cell == "K":
#             k_cell = [i, a]
#
#         func = figures[cell]
#         if func:
#             if func(board, board2, [i, a]):
#                 check_figures.append([i, a])
#
# posivle_moves = []
# for cell in get_kingdom(k_cell):
#     if board2[cell[0]][cell[1]] == 0:
#         posivle_moves.append(cell)
#
# if check_figures and len(posivle_moves) == 0:
#     print("Checkmate")
#     for check in check_figures:
#         print(f"{columns[check[1]]}{8-check[0]}")
# elif not (check_figures) and len(posivle_moves) == 0:
#     print("Stalemate")
# else:
#     print("Continue")
#     for cell in posivle_moves:
#         print(f"{columns[cell[1]]}{8-cell[0]}")
#
#
# for raw in board2:
#     print(raw)

# d, w = map(int, input().split())
# n = int(input())
# c = list(map(int, input().split()))
# x = list(map(int, input().split()))
# zaprs = list(zip(x, c))
# zaprs.sort(key=lambda x:x[0])
#
# index_remove = set()
# for i in range(1, len(zaprs), 1):
#     if zaprs[i][0] == zaprs[i-1][0]:
#         if zaprs[i][1] < zaprs[i-1][1]:
#             index_remove.add(i-1)
#         else:
#             index_remove.add(i)
#
# for i in sorted(list(index_remove), reverse=True):
#     zaprs.pop(i)
#
# n = len(zaprs)
# c = [zapr[1] for zapr in zaprs]
# x = [zapr[0] for zapr in zaprs]
#
# zapr_que_num = [0]
# prize = c[0]
# for i in range(1, n, 1):
#     if c[i] < prize:
#         zapr_que_num.append(i)
#         prize = c[i]
#
# distances = []
# for i in range(1, len(zapr_que_num), 1):
#     distances.append(x[i]-x[i-1])
# distances.append(d-x[zapr_que_num[-1]])
#
# print(max(distances) * w)


# n, m = map(int, input().split())
# a = list(map(int, input().split()))
# b = list(map(int, input().split()))
# e = int(input())
# max_exs = int((1 + e) / 2 * e)
# rez1 = 0
# rez2 = 0
#
# for a_i in a:
#     if a_i > max_exs:
#         rez1 += max_exs
#         break
#     rez1 += a_i
#
# for b_i in b:
#     if b_i > max_exs:
#         rez2 += max_exs
#         break
#     rez2 += b_i
#
#
# if rez1 > rez2:
#     print("Danya")
# elif rez2 > rez1:
#     print("Diana")
# else:
#     print("Draw")
# print(f"{max(rez1, rez2)}:{min(rez1, rez2)}")

# from math import ceil
# from copy import copy
#
# a, b, n, m, k = map(int, input().split())
# len_loop = a + b
# rez = 0
#
# if k >= len_loop:
#     if k % len_loop > 0:
#         if 0 < k % len_loop <= a:
#             rez += k % len_loop
#         else:
#             rez += a
#     rez += k // len_loop * a
# else:
#     rez += min(a, k)
#
# for i in range(1, k // n + 1, 1):
#     n_pos = n * i
#     pos = n_pos - (n_pos // len_loop) * len_loop
#     if 0 <= pos <= a:
#         rez -= 1
#
# for i in range(1, k // m + 1, 1):
#     m_pos = m * i
#     pos = m_pos - (m_pos // len_loop) * len_loop
#     if 0 <= pos <= a:
#         rez += 1
#
# print(rez)

# da, ta, wa = map(int, input().split())
# dm, tm, wm = map(int, input().split())
# dt, tt = map(int, input().split())
#
# bus = da + ta + wa
# metro = dm + tm + wm
# taxy = dt + tt
#
# if bus <= metro and bus <= taxy:
#     print("Bus")
# elif metro <= bus and metro <= taxy:
#     print("Metro")
# else:
#     print("Taxi")



# a, b, x, y = map(int, input().split())
# ease, hard = a-x, b-y
# points = ease + 2 * hard
# max_points = a + b * 2
# procent = points * 100 / max_points
# if procent >= 51:
#     print("YES")
# else:
#     print("NO")


# a = int(input())
# b = int(input())
# c = int(input())
# d = int(input())
#
# print(a+b+c-d)









# # diextra
# from collections import deque
#
# def diextra(graph: dict, start) -> dict:
#     check = deque([[start, 0]])
#     perents = {point: None for point in graph.keys()}
#     distances = {point: None for point in graph.keys()}
#     distances[start] = 0
#
#     while check:
#         deleten = check.popleft()
#         for point in graph[deleten[0]].keys():
#             distance = graph[deleten[0]][point]
#             if distances[point] is None or distances[point] > deleten[1] + distance:
#                 distances[point] = deleten[1] + distance
#                 perents[point] = deleten[0]
#                 check.append([point, distances[point]])
#
#     return perents
#     # return distances
#
# def get_way(graph, start, final) -> list:
#     perents = diextra(graph, start)
#     point = final
#     way = []
#     while point != start:
#         way.append(point)
#         point = perents[point]
#
#     way.append(start)
#     way.reverse()
#
#     return way
#
# graph = dict()
# n = int(input())
# for i in range(n):
#     a1, b1, distance = input().split()
#     distance = int(distance)
#     for a, b in [[a1, b1], [b1, a1]]:
#         if a in graph.keys():
#             graph[a][b] = distance
#         else:
#             graph[a] = {b: distance}
#
# print(get_way(graph, "A", "F"))



# # bfs
# from collections import deque
#
# def bfs(graph: dict, start, final) -> dict:
#     check = deque([start])
#     points_set = {start}
#     perents = {start: None}
#     while check:
#         deleten = check.popleft()
#         for point in graph[deleten]:
#             if not (point in points_set):
#                 check.append(point)
#                 points_set.add(point)
#                 perents[point] = deleten
#                 if point == final:
#                     return perents
#
#     return perents
#
# graph = dict()
# n = int(input())
# for i in range(n):
#     a1, b1 = input().split()
#     for a, b in [[a1, b1], [b1, a1]]:
#         if a in graph.keys():
#             graph[a].append(b)
#         else:
#             graph[a] = [b]
#
# print(bfs(graph, "A", "D"))




# # визначення n числа каталана
# (math.factorial(2 * n)) // (math.factorial(n)* math.factorial(n+1))

# # бінарний пошук
# def binary_search(mas: list, elem: int) -> int:
#     left, right = 0, len(mas)-1
#     while right >= left:
#         middle = (left + right) // 2
#         if mas[middle] == elem:
#             return middle
#         elif mas[middle] > elem:
#             right = middle - 1
#         else:
#             left = middle + 1
#     return left - 1



# # бінарний пошук
# def found_left(mas, elem):
#    left = -1
#    rigth = len(mas)
#    while rigth - left > 1:
#        middle = (rigth + left) // 2
#        if mas[middle] < elem:
#            left = middle
#        else:
#            rigth = middle
#    return left + 1
#
# def found_rigth(mas, elem):
#    left = -1
#    rigth = len(mas)
#    while rigth - left > 1:
#        middle = (rigth + left) // 2
#        if mas[middle] > elem:
#            rigth = middle
#        else:
#            left = middle
#    return rigth


# # найбільший спільний підмасив
# def best_pise_mas(mas1, mas2, returned = False):
#    mas_path = []
#    map_1 = [[0] * (len(mas2)) for i in range(len(mas1))]
#    for i in range(len(mas1)):
#        for a in range(len(mas2)):
#            if mas1[i - 1] == mas2[a - 1]:
#                map_1[i][a] = map_1[i - 1][a - 1] + 1
#                mas_path.append(i)
#            else:
#                map_1[i][a] = max(map_1[i][a - 1], map_1[i - 1][a])
#    if returned == False:
#        return map_1
#    return mas_path


# # швидка сортировка
# def quick_sort(mas):
#    if len(mas) <= 1:
#        return
#    main_element = mas[0]
#    left, right, middle = [], [], []
#    for x in mas:
#        if x < main_element:
#            left.append(x)
#        elif x == main_element:
#            middle.append(x)
#        else:
#            right.append(x)
#    quick_sort(left)
#    quick_sort(right)
#    k = 0
#    for x in left + middle + right:
#        mas[k] = x
#        k += 1


# # сортировка сливанням
# def marge_two_list(mas):
#    if len(mas) == 1:
#        return
#    midle = len(mas) // 2
#    mas1 = marge_two_list(mas[: midle])
#    mas2 = marge_two_list(mas[midle:])
#    masrez = []
#    left_index_mas1, left_index_mas2 = 0, 0
#    len_mas1, len_mas2 = len(mas1), len(mas2)
#    while left_index_mas1 < len_mas1 and left_index_mas2 < len_mas2:
#        if mas1[left_index_mas1] <= mas2[left_index_mas2]:
#            masrez.append(mas1[left_index_mas1])
#            left_index_mas1 += 1
#        else:
#            masrez.append(mas2[left_index_mas2])
#            left_index_mas2 += 1
#    if left_index_mas1 == len_mas1:
#        masrez.extend(mas2[left_index_mas2:])
#    else:
#        masrez.extend(mas1[left_index_mas1:])
#    return masrez



# # прості числа:
# n = int(input())
# masbool = [True for i in range(n)]
# for i in range(2, int(n ** 0.5) + 1):
#     if masbool[i]:
#         for a in range(i ** 2, n, i):
#             masbool[a] = False
# maseasyschyslo = [i for i in range(n) if masbool[i] == True]
# print(maseasyschyslo)


# # найбільше спільне кратне:
# a, b = map(int, input().split())
#
# while a != 0 and b != 0:
#    if a > b:
#        a = a % b
#    else:
#        b = b % a
# print(max(a, b))

# # дільники числа
# n = int(input())
# masdil = [1, n]
# for i in range(2, int(math.sqrt(n)) + 1):
#    if n % i == 0:
#        masdil.append(i)
#        masdil.append(n // i)
# print(*set(masdil))
