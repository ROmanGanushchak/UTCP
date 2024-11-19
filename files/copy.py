n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
p, q = map(int, input().split())

if p == q:
    area = a[p-1]
else:
    if p < q:
        area = b[p-1] + a[q-1]
    else:
        area = b[q-1] + a[p-1]

print(area)

# x1, y1, r1, x2, y2, r2 = map(int, input().split())
# x21, y21 = x2 - x1, y2 - y1
#
# f = (r1**2 + x21**2 + y21**2 - r2**2) / 2
# d = (4 * f**2 * x21**2 - 4 * (x21**2 + y21**2) * (f**2 - y21**2 * r1**2))
#
# if abs(d) < 0.000001:
#     if y1 == y2:
#         if max(x1, x2) - min(x1, x2) == r1 + r2:
#             print(1)
#         else:
#             print(2)
#     else:
#         print(1)
# elif d > 0:
#     print(2)
# else:
#     print(0)

# n = int(input())
# mas = list(map(int, input().split()))
#
# # field = [[None] * (n-1) for _ in range(n)]
# rez = -1
# used = set()
#
# for i in range(n):
#     min1_i, min2_i = i, None
#     local_used = set()
#     for a in range(i+1, n, 1):
#         if mas[a] < mas[min1_i]:
#             min2_i, min1_i = min1_i, a
#         elif min2_i is None or mas[a] < mas[min2_i]:
#             min2_i = a
#
#         if (min1_i, min2_i) in used:
#             break
#         local_used.add((min1_i, min2_i))
#
#         q = (mas[min1_i] + mas[min2_i]) * (a - i + 1)
#         if rez < q:
#             rez = q
#     used.update(local_used)
#
# print(rez)

# def lcs(a, b):
#     n = len(a)
#     m = len(b)
#     f = [[0] * (m + 1) for _ in range(n + 1)]
#
#     for i in range(1, n + 1):
#         for j in range(1, m + 1):
#             if a[i-1] == b[j-1]:
#                 f[i][j] = f[i-1][j] + 1
#             else:
#                 f[i][j] = max(f[i-1][j], f[i][j-1])
#
#     return f[-1][-1]
#
#
# print(lcs("abcabaac", "baccbca"))

# s1 = "abffc"
# s2 = "afbc"
#
#
# def find_max_sub_line(line1, line2, i1, i2):
#     print(i1, i2)
#     if i1 == -1 or i2 == -1:
#         print(None)
#         return ""
#
#     if line1[i1] == line2[i2]:
#         q = find_max_sub_line(line1, line2, i1 - 1, i2-1) + line1[i1]
#         print(q)
#         return q
#
#     sub_line1 = find_max_sub_line(line1, line2, i1, i2-1)
#     sub_line2 = find_max_sub_line(line1, line2, i1-1, i2)
#
#     print(max([sub_line1, sub_line2], key=lambda x: len(x)))
#     return max([sub_line1, sub_line2], key=lambda x: len(x))
#
#
# print(find_max_sub_line(s1, s2, len(s1)-1, len(s2)-1), "printed")


# from math import ceil
#
#
# def get_multypliers(num: int, mult: dict, znak):
#     i = 2
#     edge = int(num) // 2 + 1
#
#     while i < edge and num > 1:
#         if num % i == 0:
#             if i in mult:
#                 mult[i] += znak
#             else:
#                 mult[i] = znak
#
#             num //= i
#             i -= 1
#
#         i += 1
#
#     if num != 1:
#         if num in mult:
#             mult[num] += znak
#         else:
#             mult[num] = znak
#
#
# n = int(input())
# mas1 = list(map(int, input().split()))
# mas2 = list(map(int, input().split()))
# p, q = map(int, input().split())
#
# mas = [mas1[i//2] if i % 2 == 0 else mas2[i//2] for i in range(n*2 - 1)]
#
# weights = [None] * (n*2)
# weights[0] = [1, 1]
# for i in range(n*2-1):
#     weights[i+1] = (mas[i] * weights[i][1], weights[i][0])
#
#
# mult = dict()
# get_multypliers(weights[(p-1) * 2][0] * weights[(q-1) * 2 + 1][0], mult, 1)
# get_multypliers(weights[(p-1) * 2][1] * weights[(q-1) * 2 + 1][1], mult, -1)
#
# is_printed = False
# for elem in sorted(list(mult)):
#     if mult[elem] != 0 and elem != 1:
#         print(elem, mult[elem])
#         is_printed = True
#
# if not is_printed:
#     print(1, 1)

# count = int(input())
#
# for _ in range(count):
#     n, t, p = map(int, input().split())
#     t -= n * p
#     print((n-1) * t + t)

# def get_count(n, coins, i):
#     if n == 5:
#         return 1
#
#     if n < 5:
#         return 1
#
#     if n == 0:
#         return 0
#
#     combinations_count = 0
#     for i in range(i, len(coins), 1):
#         if n - coins[i] >= 0:
#             combinations_count += get_count(n - coins[i], coins, i)
#
#     return combinations_count
#
#
# while True:
#     try:
#         n = int(input())
#     except:
#         exit()
#     coins = (50, 25, 10, 5, 1)
#     rez = 0
#
#     if n == 5:
#         print(2)
#     else:
#         print(get_count(n, coins, 0))

# used_sum = {n}
# check = deque([(n, 0)])
# while check:
#     deleten = check.pop()
#     print(deleten)
#
#     if deleten[0] == 0:
#         continue
#
#     if deleten[0] < 5:
#         rez += 1
#         continue
#
#     if deleten[0] == 5:
#         rez += 2
#         continue
#
#     if deleten[0] % 5 == 0:
#         check.append((deleten[0] // 5 * 5, deleten[1]))
#     else:
#         if deleten[0] > 5:
#             check.append((deleten[0] - 5, deleten[1]))
#
#     for i in range(deleten[1], len(coins), 1):
#         if coins[i] > deleten[0]:
#             continue
#
#         check.append((deleten[0] - coins[i], i))
# print(rez)

# from array import array
#
# n, k = map(int, input().split())
# mas = array("i", [0] * n)
# mas[0] = 1
#
# for i in range(n):
#     for a in range(i + 1, min(i + k + 1, n), 1):
#         mas[a] += mas[i]
#
# print(mas[-1])

# from itertools import combinations
#
# if True:
#     raws = [list(input()[:]) for _ in range(3)]
#     raws_set = [set(raw) for raw in raws]
#
#     rez = 0
#
#     letters = []
#     index_min_raw = raws.index(min(raws, key=lambda x: len(x)))
#     for i, letter in enumerate(raws[index_min_raw]):
#         if all([letter in raws_set[i] for i in range(3)]):
#             letters.append((letter, i))
#     rez += len(letters)
#     print(letters)
#
#     last_combinations = [letters[i][1] for i in range(len(letters))]
#     new_combinations = []
#
#     for i in range(2, len(letters)):
#         for combination in last_combinations:
#             for letter_i in range(combination+1, len(letters), 1):
#                 if all(letters[letter_i] in raw[combination+1:] for raw in raws):
#                     print(combination, letter_i, "fkfkkf")
#                     new_combinations.append(letter_i)
#                     rez += 1
#
#         last_combinations = new_combinations.copy()
#         new_combinations.clear()
#         print()
#
# print(rez)

# activates = combinations(range_mas, i)

# n, m = map(int, input().split())
# field = tuple([tuple(list(map(int, input().split()))) for _ in range(n)])
# mas = [list(elem) for elem in field]
#
# for i in range(1, n, 1):
#     mas[i][0] += mas[i-1][0]
#
# for a in range(1, m, 1):
#     mas[0][a] += mas[0][a-1]
#
# for i in range(1, n, 1):
#     for a in range(1, m, 1):
#         if mas[i-1][a] < mas[i][a-1]:
#             mas[i][a] += mas[i - 1][a]
#         else:
#             mas[i][a] += mas[i][a - 1]
#
# print(mas[-1][-1])
#
# cell = (n-1, m-1)
# way = []
# while cell != (0, 0):
#     way.append(cell)
#     if mas[cell[0]-1][cell[1]] < mas[cell[0]][cell[1]-1]:
#         cell = (cell[0] - 1, cell[1])
#     else:
#         cell = (cell[0], cell[1] - 1)
# way.append((0, 0))
#
# for cell in reversed(way):
#     print(cell[0] + 1, cell[1] + 1)

# def get_distance(cell, field, mas, moves) -> int:
#     if not (field[cell[0]][cell[1]] is None):
#         return field[cell[0]][cell[1]]
#
#     distances = [0] * 2
#     for i, move in enumerate(moves):
#         distances[i] = get_distance((cell[0] + move[0], cell[1] + move[1]), field, mas, moves)
#
#     field[cell[0]][cell[1]] = min(distances) + mas[cell[0]][cell[1]]
#     return field[cell[0]][cell[1]]
#
#
# n, m = map(int, input().split())
# mas = tuple([tuple(list(map(int, input().split()))) for _ in range(n)])
#
# field = [[None] * m for _ in range(n)]
# field[0][0] = mas[0][0]
# for i in range(1, m, 1):
#     field[0][i] = field[0][i-1] + mas[0][i]
#
# for j in range(1, n, 1):
#     field[j][0] = field[j-1][0] + mas[j][0]
#
# moves = ((-1, 0), (0, -1))
#
# print(get_distance([n-1, m-1], field, mas, moves))

# from collections import deque
# from queue import PriorityQueue
#
# n, m = map(int, input().split())
# mas = tuple([tuple(list(map(int, input().split()))) for _ in range(n)])
#
# if n == m == 1:
#     print(1)
#     exit()
#
# check = PriorityQueue()
# check.put((mas[0][0], 0, 0))
# new_mas = [[None] * m for _ in range(n)]
# new_mas[0][0] = mas[0][0]
# possible_moves = ((0, 1), (1, 0))
#
# while True:
#     current_cell = check.get()
#
#     for move in possible_moves:
#         cell = (current_cell[1] + move[0], current_cell[2] + move[1])
#         if 0 <= cell[0] < n and 0 <= cell[1] < m and cell != current_cell:
#             length = current_cell[0] + mas[cell[0]][cell[1]]
#             if new_mas[cell[0]][cell[1]] is None or new_mas[cell[0]][cell[1]] > length:
#                 check.put((length, cell[0], cell[1]))
#                 new_mas[cell[0]][cell[1]] = length
#
#             if cell == (n-1, m-1):
#                 print(length)
#                 exit()

# num_loop = int(input())
#
# for _ in range(num_loop):
#     n, t, p = map(int, input().split())
#     t = t - p * n
#     print(t)
#     print((t+1) ** (n-1))

# from collections import deque
#
#
# def find_left(mas, elem):
#     left = -1
#     right = len(mas)
#     while right - left > 1:
#         middle = (right + left) // 2
#         if elem < mas[middle]:
#             left = middle
#         else:
#             right = middle
#
#     return left + 1
#
#
# weight, n = map(int, input().split())
# cons = sorted([list(map(int, input().split())) for _ in range(n)], key=lambda x: x[0], reverse=True)
#
# # удаляю повтори ваги
# indexs_to_delete = []
# for i in range(n-1):
#     if cons[i][0] == cons[i+1][0]:
#         indexs_to_delete.append(i)
#         cons[i+1][1] = max(cons[i][1], cons[i+1][1])
#
# for i in reversed(indexs_to_delete):
#     cons.pop(i)
#
# n = len(cons)
#
#
# cons_weights = [cons[i][0] for i in range(n)]
# cons_prizes = [cons[i][1] for i in range(n)]
#
# check = deque([(weight, 0)])  # free_weight, current_prize
# max_prize = 0
# used_weights = {weight}  # множина ваг комбінацій які вже перевірені
# used_weights_d = {weight: 0}  # словник використаних сум ваг і їх максимальною утвореною ціною
#
# while check:
#     deleten = check.pop()
#
#     left_edge = find_left(cons_weights, deleten[0])
#     if left_edge == n and deleten[1] > max_prize:
#         max_prize = deleten[1]
#
#     for i in range(left_edge, n, 1):
#         new = (deleten[0] - cons_weights[i], deleten[1] + cons_prizes[i])
#         if new[0] not in used_weights:
#             check.append(new)
#             used_weights.add(new[0])
#             used_weights_d[new[0]] = new[1]
#         else:
#             if used_weights_d[new[0]] < new[1]:
#                 check.append(new)
#                 used_weights_d[new[0]] = new[1]
#
# print(max_prize)

# n, m = map(int, input().split())
# mas = sorted(list(map(int, input().split())), reverse=True)
#
# begin = 0
# rez = 0
# while mas[0] != 0:
#     for i in range(begin, min(begin + m, len(mas)), 1):
#         mas[i] -= 1
#     mas.sort(reverse=True)
#
#     rez += 1
#
# print(rez)

# from math import ceil
#
# n, m = map(int, input().split())
# mas = sorted(list(map(int, input().split())), reverse=True)
# print(mas)
#
# rez = 0
# begin, end = 0, min(m, len(mas))
# while end < len(mas):
#     rez += 1
#     for i in range(begin, end, 1):
#         mas[i] -= 1
#
#     a = m - 1
#     count_zero = 0
#     while mas[begin+a] == 0 and a >= 0:
#         count_zero += 1
#         a -= 1
#
#     begin += count_zero
#     end = min(end + count_zero, len(mas))
#     print(mas)
#
# rez += mas[-1]
# print(rez)

# from math import ceil
#
# n, m = map(int, input().split())
# mas = sorted(list(map(int, input().split())), reverse=True)
#
# rez = 0
# for i in range(ceil(n / m)):
#     rez += mas[i*m]
#
# print(rez)

# n, m = map(int, input().split())
# b = sorted(list(map(int, input().split())))
# g = sorted(list(map(int, input().split())))
#
# rez = 0
# i, a = 0, 0
# while i != len(b) and a != len(g):
#     if b[i] >= g[a]:
#         rez += 1
#         i += 1
#         a += 1
#     else:
#         i += 1
#
# print(rez)


# n = int(input())
# months_lens = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#
# sum_months = months_lens[0]
# i = 1
# while sum_months < n:
#     sum_months += months_lens[i]
#     i += 1
#
# print(months_lens[i-1] - (sum_months - n), i)

# from math import ceil
#
# n = int(input())
# mas = sorted(list(map(int, input().split())), reverse=True)
# avenger_mas = sum(mas) / n
#
# if int(avenger_mas) == ceil(avenger_mas):
#     avenger_mas_int = int(avenger_mas)
#     rez = 0
#     i = 0
#     while mas[i] > int(avenger_mas):
#         rez += mas[i] - avenger_mas_int
#         i += 1
#         if i == len(mas):
#             break
#
#     print(rez)
# else:
#     print(-1)

# n = int(input()) - 1
# if n == 0:
#     print(1)
#     exit()
#
# tops = [0]
# current_top = 2
# while current_top + tops[-1] < n:
#     tops.append(current_top + tops[-1])
#     current_top *= 2
# tops.append(current_top + tops[-1])
#
# local_i = n - tops[-2]
# product = 1
# for i in range(len(tops)-1, 0, -1):
#     if local_i > (tops[i] - tops[i-1]) / 2:
#         local_i -= (tops[i] - tops[i-1]) // 2
#         product *= 2
#
# print(product * local_i)

# n = int(input()) - 1
# if n == 0:
#     print(1)
#     exit()
#
# len_mas = 2
# mas = [1, 2]
# index_start = 0
# while len(mas) < n - index_start:
#     index_start += len(mas)
#     mas.extend([elem * 2 for elem in mas])
#
# print(mas[n-index_start-1])

# n = int(input())
# if n > 14:
#     n = 27 - n
#
# print(int((1 + (n+1)) / 2 * (n+1)))
# print(n, int((1 + (n+1)) / 2 * (n+1)) ** 2, end=" ")

# n = int(input())
# rez = 0
# for i in range(0, min(9, n)+1):
#     rez += max(9 - abs(n - i - 9) + 1, 0)
#
# print(rez ** 2)

# n = int(input())
# if n == 1:
#     print(3)
#     exit()
#
# if n % 5 == 0:
#     print(n // 5)
#     exit()
#
# rez = []
# num_i = n // 5
# for i in [-5, 5]:
#     q = num_i * 5 if i < 0 else (num_i + 1) * 5
#     while 0 <= q <= 100:
#         if abs(n - q) % 3 == 0:
#             rez.append(q // 5 + abs(n - q) // 3)
#             break
#         q += i
#
# print(min(rez))


# n = int(input())
#
# rez = 0
# for i in range(0, min(9, n)+1):
#     for a in range(0, min(9, n)+1):
#         if 0 <= n - (i + a) <= 9:
#             print(f"{i}{a}")
#             rez += 1
#
# print(rez ** 2)

# n = int(input())
# if n % 5 == 0:
#     print(n // 5)
#     exit()
#
# rez = []
# num_i = n // 5
# for i in [-5, 5]:
#     q = num_i * 5
#     while 0 <= q <= 100:
#         if abs(n - q) % 3 == 0:
#             rez.append(q // 5 + abs(n - q) // 3)
#             break
#         q += i
#
# print(min(rez))


# from collections import Counter
#
# n = int(input())
# mas = list(map(int, input().split()))
# max_count = Counter(mas).most_common(1)[0][1]
# print(n - max_count)

# from math import ceil
# n = ceil(int(input()) / 60)
# mas = [2 ** i for i in range(6, max(6-n, 0), -1)]
# print(sum(mas) + max(0, n-6) + 1)

# n, k = map(int, input().split())
# mas = list(map(int, input().split()))
# rez = n - (sum(mas) + 1 - k)
# print(0 if rez < 0 else rez)

# n = int(input())
# mas1 = list(map(int, input().split()))
# m = int(input())
# mas2_set = set(list(map(int, input().split())))
#
# rez = []
# for i in range(n):
#     if not (mas1[i] in mas2_set):
#         rez.append(mas1[i])
# print(len(rez))
# print(*rez)

# def get_distance(cell1, cell2) -> float:
#     return sqrt((cell2[0] - cell1[0]) ** 2 + (cell2[1] - cell1[1]) ** 2)
#
#
# def a(field: list[list], start: list[int], final: list[int]):
#     possible_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
#     check = [start]
#     distances: list[list] = [[[None, None, None]] * len(field[0]) for _ in range(len(field))]
#     distances[start[0]][start[1]] = [0, get_distance(start, final), get_distance(start, final)]
#     current_cell = start
#
#     while current_cell != final:
#         check.remove(current_cell)
#         print(current_cell)
#         for move in possible_moves:
#             new_cell = [current_cell[0] + move[0], current_cell[1] + move[1]]
#             if not(0 <= new_cell[0] < len(field) and 0 <= new_cell[1] < len(field[0])) \
#                                                           or field[new_cell[0]][new_cell[1]] == 1:
#                 continue
#
#             if distances[new_cell[0]][new_cell[1]][2] is None:
#                 distance_to_final = get_distance(new_cell, final)
#                 distances[new_cell[0]][new_cell[1]] = [distances[current_cell[0]][current_cell[1]][0] + 1, \
#                                             distance_to_final*10,
#                                             distances[current_cell[0]][current_cell[1]][0] + distance_to_final*10 + 1]
#                 check.append(new_cell)
#
#         if check:
#             current_cell = min(check, key=lambda x: distances[x[0]][x[1]][2])
#         else:
#             break
#
#     return distances
#
#
# field = [
#     [0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0]
# ]
# start_pos = [0, 0]
# final_pos = [4, 4]
# for raw in a(field, start_pos, final_pos):
#     for elem in raw:
#         if elem[2]:
#             print("%0.3f" % elem[2], end=" ")
#         else:
#             print("None", end=" ")
#     print()


# from math import log, ceil
# print(ceil(log(int(input()), 3)))

# n = int(input())
#
# plus, negs = [], []
# for num in list(map(int, input().split())):
#     if num < 0:
#         negs.append(num)
#     else:
#         plus.append(num)
# plus.sort(reverse=True)
# negs.sort()
#
# if n == 3:
#     rez = 1
#     for a in negs + plus:
#         rez *= a
#     print(rez)
# elif len(plus) == 0:
#     print(negs[-1] * negs[-2] * negs[-3])
# elif len(negs) <= 1:
#     print(plus[0] * plus[1] * plus[2])
# elif len(plus) <= 2:
#     print(plus[0] * negs[0] * negs[1])
# else:
#     if plus[0] * plus[1] * plus[2] > negs[0] * negs[1] * plus[0]:
#         print(plus[0] * plus[1] * plus[2])
#     else:
#         print(negs[0] * negs[1] * plus[0])

# n = int(input())
#
# count = 0
# while n != 1:
#     if n % 3 == 0:
#         n //= 3
#     else:
#         n //= 2
#     count += 1
# print(count)

# m, k = map(int, input().split())
#
# num = 2 ** m * 5 ** k
# count_zero = 0
# while num % 10 == 0:
#     count_zero += 1
#     num //= 10
#
# print(count_zero)

# n, k = map(int, input().split())
# if k > n:
#     print(-1)
#     exit()
# print(sorted(list(map(int, input().split())), reverse=True)[k-1])

# from math import sqrt
#
# def get_vector(point1, point2) -> list:
#     return [point2[i] - point1[i] for i in range(2)]
#
# def get_vec_len(vec: list) -> int:
#     return sqrt(vec[0]**2 + vec[1]**2)
#
# points = [list(map(int, input().split())) for _ in range(4)]
# dig1_vec = get_vector(points[0], points[2])
# dig2_vec = get_vector(points[1], points[3])
#
# print(*["%.3f" % (points[0][i] + dig1_vec[i] / 2) for i in range(2)])
# print(*["%.3f" % (get_vec_len(a)) for a in [dig1_vec, dig2_vec]])


# def get_vector(point1, point2) -> list:
#     return [point2[i] - point1[i] for i in range(2)]

# def get_vec_len(vec: list) -> int:
#     return sqrt(vec[0]**2 + vec[1]**2)

# def add_vectors(vec1, vec2) -> list:
#     return [vec1[i] + vec2[i] for i in range(2)]
#
# points = [list(map(float, input().split())) for i in range(4)]
#
# for i in range(1, 4, 1):
#     if add_vectors(get_vector(points[0], points[(i+1)%4]), get_vector(points[0], \
#                               points[(i+2)%4])) == get_vector(points[0], points[i]):
#

# n = int(input())
# if n == 1:
#     print(1)
#     exit()
#
# mas = sorted(list(map(int, input().split())))
#
# for i, elem in enumerate(mas):
#     if i+1 != elem:
#         print(i+1)
#         exit()
# print(n)

# print(int(math.log(int(input()), 2)))

# print(1 / math.tan(10 / 180 * math.pi))

# import bpy
# from copy import copy
#
# numbers = {"x": 5, "y": 5, "z": 1}
# object_name = "Main_cphere"
# sphere = bpy.data.objects[object_name]
# s = sphere.scale[0] * 2.2
# off_sets = {"x": s, "y": s, "z": s}
#
# for x in range(numbers["x"]):
#     for y in range(numbers["y"]):
#         for z in range(numbers["z"]):
#             if x == y == z == 0:
#                 continue
#             i = 1
#             name = object_name + "0" * (3-len(str(i))) + str(i)
#             new_sphere = bpy.data.objects.new(name=name, object_data=sphere.data)
#             new_sphere.location = sphere.location.copy()
#
#             new_sphere.location.x += x * off_sets["x"]
#             new_sphere.location.y += y * off_sets["y"]
#             new_sphere.location.z += z * off_sets["z"]
#
#             new_sphere.scale = copy(sphere.scale)
#
#             bpy.data.collections["Spheres"].objects.link(new_sphere)
#             bpy.data.scenes['Scene'].rigidbody_world.collection.objects.link(new_sphere)

# max_w = int(input())
# weights = sorted(list(map(int, input().split())), reverse=True)
# if max_w in weights:
#     print(max_w)
#     exit()
#
# left_i = 0
# while left_i < len(weights) and weights[left_i] > max_w:
#     left_i += 1
# weights = weights[left_i:]
#
# check = deque([array("i", [weights[i], i]) for i in range(len(weights))])
# used = set()
# rez = set()
#
# while check:
#     w, i = check.pop()
#     rez.add(w)
#     free_w = max_w - w
#     r_i = len(weights) - 1
#
#     while r_i > i and free_w > weights[r_i]:
#         if not ((w+weights[r_i], r_i) in used):
#             check.append(array("i", [w+weights[r_i], r_i]))
#             used.add((w+weights[r_i], r_i))
#         r_i -= 1
#
#     if r_i != i and r_i < len(weights) and free_w == weights[r_i]:
#         print(max_w)
#         exit()
#
# try:
#     print(max(rez))
# except:
#     print(0)

# from array import array
#
# max_w = int(input())
# weights = sorted(list(map(int, input().split())))
# if max_w in weights:
#     print(max_w)
#     exit()
#
# left = 0
# while left < len(weights) and max_w < weights[left]:
#     left += 1
# weights = weights[left:]
#
# mas = array("i", [])
# for i in range(len(weights)):
#     mas.append(weights[i])
#     for a in range(len(mas)-1):
#         if mas[a] + weights[i] > max_w:
#             continue
#         if mas[a] + weights[i] == max_w:
#             print(max_w)
#             exit()
#         mas.append(mas[a] + weights[i])
#
# try:
#     print(max(mas))
# except:
#     print(0)


# from collections import deque
# from random import randint
# from copy import copy
#
# max_w = int(input())
# # weights = sorted([randint(1, 5) for i in range(30)], reverse=True) #list(map(int, input().split()))
# weights = sorted(list(map(int, input().split())), reverse=True)
# if max_w in weights:
#     print(max_w)
#     exit()
#
# left_i = 0
# while left_i < len(weights) and weights[left_i] > max_w:
#     left_i += 1
# weights = weights[left_i:]
#
# check = deque([[weights[i], i] for i in range(len(weights))])
# used = set()
# rez = set()
#
# while check:
#     w, i = check.pop()
#     rez.add(w)
#     free_w = max_w - w
#     r_i = len(weights) - 1
#
#     while r_i > i and free_w > weights[r_i]:
#         if not ((w+weights[r_i], r_i) in used):
#             check.append([w+weights[r_i], copy(r_i)])
#             used.add((w+weights[r_i], r_i))
#         r_i -= 1
#
#     if r_i != i and r_i < len(weights) and free_w == weights[r_i]:
#         print(max_w)
#         exit()
#
# try:
#     print(max(rez))
# except:
#     print(0)

# from collections import deque
# from random import randint
# import time
#
# def find_left(mas, elem):
#     lo, up = -1, len(mas)
#     while lo < up:
#         mid = (lo + up) // 2
#         if mas[mid] <= elem:
#             up = mid
#         else:
#             lo = mid + 1
#     return up
#
# max_w = 199
# weights = sorted([randint(1, 5) for i in range(20)], reverse=True)
# print(weights)
# print(sum(weights))
#
# check = deque([[weights[i], i] for i in range(len(weights))])
# rez = set()
# while check:
#     w, i = check.popleft()
#     rez.add(w)
#     if i == 0:
#         continue
#     free_w = max_w - w
#     left_edge = find_left(weights, free_w)
#     for a in range(max(left_edge, i+1), len(weights), 1):
#         if w + weights[a] < max_w:
#             check.append([w + weights[a], a])
#
#         if w+weights[a] == max_w:
#             print(max_w)
#             exit()
#
# print(max(rez), "rez")


# from collections import deque
# from array import array
# from random import randint
# from copy import copy
#
# def find_rigth(mas, elem, right=None):
#     left=-1
#     if right is None:
#         right = len(mas)
#     while right - left > 1:
#         middle = (right + left) // 2
#         if mas[middle] >= elem:
#             right = middle
#         else:
#             left = middle
#     if 0 <= right < len(mas) and mas[right] == elem:
#         return right - 1
#     return right
# print(find_rigth([0, 1, 2, 2, 3, 3], 3))
# max_w = 100
# weights = sorted([randint(1, 5) for i in range(10)])
# right_edge = find_rigth(weights, max_w)
# weights = weights[:right_edge]
# if max_w in weights:
#     print(max_w)
#     exit()
#
#
# rez = set()
# check = deque([[weights[i], i] for i in range(len(weights))])
# print(check)
# q = 0
# while check:
#     w, i = check.popleft()
#     free_w = max_w - w
#     right_edge = find_rigth(weights, free_w, i+1)
#     print(w, i, right_edge)
#     if right_edge > 0:
#         for a in range(0, min(right_edge+1, i),  1):
#             if max_w - (w+weights[a]) >= 0:
#                 check.append([w+weights[a], copy(a)])
#
#             if w+weights[a] == max_w:
#                 print(max_w)
#                 exit()
#
#     rez.add(w)
#
#     # q+=1
#     # if q == 10000:
#     #     break
# try:
#     print(max(list(rez)))
# except:
#     print(0)
