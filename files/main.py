import itertools

for i in range(20):
    values = '012345xx'
    combinations = list(set(itertools.permutations(values, 8)))

    naibors = {
        '0': ['1', '3', '4', '5'],
        '1': ['0', '2', '4', '5'],
        '2': ['1', '5'],
        '3': ['0'],
        '4': ['0', '1', '5'],
        '5': ['0', '1', '2', '4'],
        'x': []
    }

    moves = [-1, 1, -4, 4]
    maxNaiborCount = 0
    maxNaiborCombination = None
    for combination in combinations:
        naiborCount = 0
        for i in range(len(combination)):
            for move in moves:
                if 0 <= i + move < len(combination) and \
                        combination[i+move] in naibors[combination[i]]:
                    naiborCount += 1

        if naiborCount > maxNaiborCount:
            maxNaiborCount = naiborCount
            maxNaiborCombination = combination

    print(maxNaiborCount)
    print("".join(maxNaiborCombination[0:4]))
    print("".join(maxNaiborCombination[4:8]))






# from copy import copy
#
# n, m, k = map(int, input().split())
# masM = list(map(int, input().split()))
# masKDef = [list(map(int, input().split())) for _ in range(k)]
# masKI = [masKDef[i][0] for i in range(k)]
# masKCell = [masKDef[i][1]-1 for i in range(k)]
#
# isFree = [True] * n
# mPlace = [-1] * m
#
# for i in range(k):
#     isFree[masKCell[i]] = False
#     if masKI[i] in masM:
#         mPlace[masM.index(masKI[i])] = masKCell[i]
#
# print(isFree)
# index = masM[-1] - 1
#
# for i in range(m-1, -1, -1):
#     if mPlace[i] == -1:
#         while isFree[index] != True:
#             index -= 1
#
#         isFree[index] = False
#         mPlace[i] = index
#         index -= 1
#     else:
#         index = mPlace[i] - 1
#
# print(isFree)





# w = int(input())
# weights = [0] + list(map(int, input().split()))
# weights.sort()
#
# check = [array("i", [0, 0])]# weight, point
# final_weights = []
#
# while check:
#     deleten = check.pop()
#     point, weight = deleten[1], deleten[0]
#     edge_point = copy(point)
#     while edge_point < len(weights) and w - weight - weights[edge_point] >= 0:
#         edge_point += 1
#
#     if point == edge_point:
#         final_weights.append(weight)
#         continue
#
#     for i in range(point+1, edge_point, 1):
#         check.append(array("i", [weight+weights[i], i]))
#         if weight+weights[i] == w:
#             print(w)
#             exit()
#
# try:
#     print(max(final_weights))
# except Exception:
#     print(0)



# from collections import deque
# from array import array
#
# def find_rigth(mas, elem, right=None):
#     left=-1
#     if right is None:
#         right = len(mas)
#     while right - left > 1:
#         middle = (right + left) // 2
#         if mas[middle] > elem:
#             right = middle
#         else:
#             left = middle
#     return right
#
# max_w = int(input())
# weights = sorted(list(map(int, input().split())))
# right_edge = find_rigth(weights, max_w)
# weights = weights[:right_edge]
# if max_w in weights:
#     print(max_w)
#     exit()
#
#
# rez = set()
# check = deque([array("i", [weights[i], i]) for i in range(0, len(weights), 1)])
# while check:
#     w, i = check.pop()
#     print(w, i)
#     free_w = max_w - w
#     right_edge = find_rigth(weights, free_w, i-1)
#     if right_edge >= 0:
#         for a in range(min(right_edge+1, i)-1, -1, -1):
#             if max_w - (w+weights[a]) > 0:
#                 check.append(array("i", [w+weights[a], a]))
#
#             if w+weights[a] == max_w:
#                 print(max_w)
#                 exit()
#
#     rez.add(w)
# try:
#     print(max(list(rez)))
# except:
#     print(0)

# def get_len_number(i):
#     i += 1
#     len = i // 10 * 3
#     len += i // 100
#     i = i % 10
#
#     if i:
#         len += 1
#         if i > 7:
#             len += 2
#         elif i > 4:
#             len += 1
#
#     return len
#
# # n = int(input())
#
# for i in range(1000):
#     print(i, len(str(2**i)), get_len_number(i))

# n, g, y, r = map(int, input().split())
#
# n = n % (g + y + r)
# n -= 1
#
# print(line[n-1])


# print(bool(input() % 11))


# number = int(input())
#
# if number in [1, 2, 3, 5, 7]:
#     print("Yes")
#     exit()
#
# if any([not (number % i) for i in [2, 3, 5, 7]]):
#     print("No")
#     exit()
#
# for num in range(3, math.ceil(math.sqrt(number)), 1):
#     if number % num == 0:
#         print("No")
#         exit()
#
# print("Yes")



# mas = []
# bad_line = input()
# bad_line_without_space = bad_line.replace(" ", "")
# new_line = input()
#
# with open("input", "r") as f:
#     for line in f.readlines():
#         line = line.replace("\n", "")
#         mas.append(line.replace(bad_line_without_space, new_line)n1, n2: n1 + n2, "-": lambda n1, n2: n1 - n2}]
#
#         self.set_operation, self.set_function = set(), set(list(self.dict_function.keys()))
#         for i in self.dict_operation:
#             self.set_operation.update(list(i.keys()))
#
#     def find_closed_bracket(self, line, n):
#         line = line[n + 1:]
#         count_open_bracket, count_closed_bracket = 1, 0
#         i = 0
#         while count_closed_bracket != count_open_bracket:
#             if line[i] == "(":
#                 count_open_bracket += 1
#             elif line[i] == ")":
#                 count_closed_bracket += 1
#             i += 1
#         return i
#
#     def creating_negative_numbers(self, mas_number, mas_signs, line):
#         for i, sign in enumerate(mas_signs):
#             if len(sign) <= 1:
#                 continue
#             count_mines = sign.count("-")
#             if not sign.count("-"):
#                 continue
#             if count_mines % 2 != 0:
#                 mas_number[i + 1] = mas_number[i + 1] * -1
#                 mas_signs[i] = mas_signs[i].replace("-", "")
#             else:
#                 mas_signs[i] = mas_signs[i].replace("-", "")
#
#         if line[0] == "-":
#             mas_signs.pop(0)
#             mas_number[0] *= -1
#
#     def to_calculate(self, line: str):
#         if line.count("(") > 0:
#             i = 0
#             while i < len(line):
#                 if line[i] == "(":
#                     index_close = i + self.find_closed_bracket(line, i)
#                     line = line[:i] + str(self.to_calculate(line[i + 1:index_close])) + line[index_close + 1:]
#                 i += 1
#
#         if not line:
#             print("bracket can not by empty")
#             exit()
#
#         mas_number_default = re.split('[qwertyuiopasdfghjklzxcvbnm+*/#!-]', line)
#         mas_signs_default = list(re.split("[0123456789.]", line))
#         mas_signs, mas_number = [], array.array("d", [])
#         for number in mas_number_default:
#             if number != "":
#                 mas_number.append(float(number))
#
#         for sign in mas_signs_default:
#             if sign != '':
#                 mas_signs.append(sign)
#
#         self.creating_negative_numbers(mas_number, mas_signs, line)
#
#         a = 0
#         for sign in copy(mas_signs):
#             if len(sign) > 1:
#                 index_begining = 0
#                 if sign[0] in self.set_operation:
#                     a += 1
#                     index_begining = 1
#                 math_fanction = sign[index_begining:]
#                 sign = sign[0]
#                 if math_fanction in self.set_function:
#                     mas_number[a] = self.dict_function[math_fanction](mas_number[a])
#                 if sign in self.set_operation:
#                     mas_signs[a-1] = sign
#                 else:
#                     mas_signs.pop(a)
#
#         for layer_operation in range(len(self.dict_operation)):
#             number_index = 0
#             for sign in copy(mas_signs):
#                 if sign in self.dict_operation[layer_operation]:
#                     mas_number[number_index] = self.dict_operation[layer_operation][sign](mas_number[number_index],
#                                                                                           mas_number[number_index + 1])
#                     mas_number.pop(number_index + 1)
#                     mas_signs.pop(number_index)
#                 else:
#                     number_index += 1
#
#         if len(mas_number) > 1:
#             raise Exception("during calculatin formed 2 resalt numbers")
#         if math.floor(mas_number[0]) == math.ceil(mas_number[0]):
#             return int(mas_number[0])
#         return float(mas_number[0])
#
# calculator = Calculator()
# line = input()
# line = line.replace(" ", "")
# print(calculator.to_calculate(line))

# n = 0
# print(int(not 1))

# s = input()
# if len(s) == 1:
#     print(s if s == "8" else "-1")
# elif len(s) == 2:
#     if int(s) % 8 == 0:
#         print(s)
#     if s[1] != 0 and int(s[1] + s[0]) % 8 == 0:
#         print(s[1] + s[0])
#     else:
#         print(-1)
# elif s[-3] != 0 and int(s[-3: -1] + s[-1]) % 8 == 0 or s[-1] == s[-2] == s[-3] == 0:
#     print(s)
#     exit()
# mas = Counter(list(map(int, list(s))))
# mas2 = sorted(list(set(mas)), reverse = True)
# rez = ""
# for i in mas2:
#     if i:
#         for a in mas2:
#             for z in mas2:
#                 if int("{}{}{}".format(i, a, z)) % 8 == 0:
#                     mas[i] -= 1
#                     mas[a] -= 1
#                     mas[z] -= 1
#                     if mas[i] < 0 or mas[a] < 0 or mas[z] < 0:
#                         mas[i] += 1
#                         mas[a] += 1
#                         mas[z] += 1
 for a in range(10)}
# mas_can_move = [(0, 1), (1, 0), (1, 1)]
# f = False
# while check:
#     deleten = check.popleft()
#     for i in mas_can_move:
#         new_elem = (deleten[0] + i[0], deleten[1] + i[1])
#         if perents[new_elem] == None and 0 <= new_elem[0] < 10 and 0 <= new_elem[1] < 10:
#             if mas[new_elem[0]][new_elem[1]] == 1:
#                 perents[tuple(new_elem)] = deleten
#                 f = True
#                 break
#             check.append(new_elem)
#             perents[new_elem] = deleten
#     if f:
#         break
# last_elem = (4, 7)
# while last_elem != None:
#     mas_rez.append(last_elem)
#     last_elem = perents[last_elem]
# print(*mas_rez)

# def one(n, k, mas):
#     kil_par, rez = 0, 0
#     for i in range(n):
#         mas[i] -= 1
#         rez += 1
#     for i in range(len(mas)):
#         if kil_par == k:
#             break
#         while mas[i] > 0:
#             if mas[i] == 1:
#                 kil_par += 1
#                 rez += 1
#                 break
#             else:
#                 kil_par += 1
#                 rez += 2
#                 mas[i] -= 2
#             if kil_par == k:
#                 break
#     return rez
#
# def two(n, k, mas):
#     kil_par, rez = 0, 0
#     for i in range(n):
#         mas[i] -= 1
#         rez += 1
#     for i in range(len(mas)):
#         if kil_par == k:
#             break
#         while mas[i] > 1:
#             if kil_par == k - 1:
#                 break
#             kil_par += 1
#             rez += 2
#             mas[i] -= 2
#             if kil_par == k - 1:
#                 break
#     for i in range(n):
#         if kil_par == k:
#             break
#         mas[i] -= 1
#         kil_par += 1
#         rez += 1
#     return rez
#
# if __name__ == "__main__":
#     rez1, rez2 = 0, 0
#     n, k, mas = 0, 0, []
#     while rez1 == rez2:
#         n = random.randint(10, 20)
#         k = random.randint(1, 4)
#         mas = [random.randint(5, 10000) for i in range(n)]
#         rez1 = one(n, k, list(mas)) - 1
#         rez2 = two(n, k, list(mas))
#         print(1)
#     while mas.count(0) != n:
#         for i in range(n):
#             if mas[i]:
#                 print(1, end = " ")
#                 mas[i] -= 1
#             else:
#                 print(" ", end = " ")
#         print()
#     print(n, k)
#     print(mas)
#     print(rez1, "rez1", rez2, "res2")

# n = int(input())
# for i in range(n):
#     m = int(input())
#     mas = list(map(int, list(input())))
#     if mas[0] == 0:
#         print("Anton")
#     else:
#         print("Archi")

# s = input()
# last_elem, rez, mas_elem, mas_kil_elem = None, 0, [], []
# for i, elem in enumerate(s):
#     if elem != last_elem:
#         mas_elem.append(elem)
#         mas_kil_elem.append(1)
#         last_elem = elem
#     else:
#         mas_kil_elem[-1] += 1
# for i in range(0, len(mas_elem), 1):
#     if i >= 1 and mas_kil_elem[i - 1] > 1:
#         rez += mas_kil_elem[i - 1] - 1
#     if i < len(mas_elem) - 1 and mas_kil_elem[i + 1] > 1:
#         rez += mas_kil_elem[i + 1] - 1
#     if i < len(mas_elem) - 1 and i >= 1 and mas_kil_elem[i] == 1 and mas_elem[i - 1] == mas_elem[i + 1]:
#         rez += mas_kil_elem[i - 1] * mas_kil_elem[i + 1]
# print(rez)

# n, m = map(int, input().split())
# mas, mas_sum_line, mas_sum_column, mas_column = [], [], [], []
# for i in range(n):
#     mas.append(list(map(int, input().split())))
#     mas_sum_line.append(sum(mas[i]))
# for i in range(m):
#     mas_column.append([])
#     for a in range(n):
#         mas_column[i].append(mas[a][i])
#     mas_sum_column.append(sum(mas_column[i]))
#
# mas_elem= []
# mas_elem.extend(mas_sum_line)
# mas_elem.extend(mas_sum_column)
# set_mas_elem = list(set(mas_elem))
# if len(set_mas_elem) > 2:
#     print("No")
# else:
#     print("Yes")

# n, k = map(int, input().split())
# mas = sorted(list(map(int, input().split())))
# sum_mas = sum(mas)
# need_borel = math.ceil(sum_mas / k)
# sum_l = sum(mas[0:len(mas)-need_borel])
# print(need_borel, sum_l)

# n, k = map(int, input().split())
# mas = list(map(int, input().split()))
# for i in range(len(mas)):
#     if mas[i] % 2 != 0:
#         mas[i] -= 1
# print(sum(mas))

# f = open("input.txt", "r")
# f1 = open("output.txt", "a")
# n = int(f.readline())
# for i in range(n):
#     m = int(f.readline())
#     field, winner = list(f.readline()), 0
#     if field[-1] == "\n":
#         field.pop()
#     if len(field) == 1:
#         if field[0] == "1":
#             f1.write("Archi")
#             f1.write("\n")
#         else:
#             f1.write("Anton")
#             f1.write("\n")
#         continue
#     while field[0] == "1" or len(set(field)) != 1:
#         numbre_1 = m
#         for a in    rez += 1
#         dict_elem = dict()
#         for a in list_s[i:i+3]:
#             if a not in dict_elem:
#                 dict_elem[a] = 1
#             else:
#                 dict_elem[a] += 1
#         for a in range(i+3, len(s), 1):
#             if list_s[a] in set_line and dict_elem[list_s[a]] != 1:
#                 rez += 1
#             else:
#                 break
# print(rez)

# n, m = map(int, input().split())
# mas, mas_sum_line, mas_sum_column, mas_column = [], [], [], []
# for i in range(n):
#     mas.append(list(map(int, input().split())))
#     mas_sum_line.append(sum(mas[i]))
# for i in range(m):
#     mas_column.append([])
#     for a in range(n):
#         mas_column[i].append(mas[a][i])
#     mas_sum_column.append(sum(mas_column[i]))
#
# mas_elem= []
# mas_elem.extend(mas_sum_line)
# mas_elem.extend(mas_sum_column)
# set_mas_elem = list(set(mas_elem))
# if len(set_mas_elem) > 3:
#     print("No")
#     exit()
# if len(set_mas_elem) == 1:
#     print("Yes")
#     exit()
# mas_count_elem = [mas_elem.count(i) for i in set_mas_elem]
# need_elem = set_mas_elem[mas_count_elem.index(max(mas_count_elem))]
# mas_num_bad_elem = []
# for i in mas_sum_line, mas_sum_column:
#     index = 0
#     for a in i:
#         if a != need_elem:
#             break
#         index += 1
#     if index == len(i):
#         print("No")
#         exit()
#     mas_num_bad_elem.append(index)
# need_elem_line = need_elem - mas_sum_line[mas_num_bad_elem[0]] + mas[mas_num_bad_elem[0]][mas_num_bad_elem[1]]
# need_elem_column = need_elem - mas_sum_column[mas_num_bad_elem[1]] + mas[mas_num_bad_elem[0]][mas_num_bad_elem[1]]
# if need_elem_line == need_elem_column:
#     print("Yes")
# else:
#     print("No")


# n, k, m = map(int, input().split())
# last_num, mas_rez = k, []
# if m != 0:
#     for i in range(2 ** (m - 1)):
#         if last_num <= 1:
#             print(-1)
#             exit()
#         mas_rez.extend([last_num, last_num - 1])
#         last_num -= 2
# mas_not_use_num = [i for i in range(2**n, k, -1)]
# mas_not_use_num.extend([i for i in range(last_num, 0, -1)])
# len_mas_not_use_num = len(mas_not_use_num)
# for i in range(0, len_mas_not_use_num // 2, 1):
#     mas_rez.extend([mas_not_use_num[i], mas_not_use_num[len_mas_not_use_num - i-1]])
# print(*mas_rez)

# n, m = map(int, input().split())
# mas, mas_sum_line, mas_sum_column, mas_colum, mas_elem = [], [], [], [], []
# for i in range(n):
#     mas.append(list(map(int, input().split())))
#     mas_sum_line.append(sum(mas[i]))
#
# for i in range(m):
#     mas_colum.append([])
#     for a in range(n):
#         mas_colum[i].append(mas[a][i])
#     mas_sum_column.append(sum(mas_colum[i]))
#
# mas_elem.extend(mas_sum_line)
# mas_elem.extend(mas_sum_column)
# set_mas_elem = set(mas_elem)
# if len(set_mas_elem) == 1:
#     print("Yes")
#     exit()
# if len(set_mas_elem) > 3:
#     print("No")
#     exit()
# mas_znach_elem = list(set_mas_elem)
# mas_count_elem = [mas_elem.count(i) for i in mas_znach_elem]
# more_elem = max(mas_count_elem)
# mas_index_bad_line = [i for i in range(len(mas_znach_elem)) if mas_count_elem[i] != more_elem]
# print("Yes")

# n = int(input())
# mas = list(map(int, input().split()))
# need_point, mas_index_1, rez = n - 1, [i for i in range(len(mas)) if mas[i] == 1], 0
# mas_index_1.reverse()
# for i in mas_index_1:
#     rez += need_point - i
#     need_point -= 1
# print(rez)

# n = int(input())
# mas = list(map(int, input().split()))
# kil = 0
# for i in range(0, n-1, 1):
#     for a in range(0, n-1-i, 1):
#         if mas[a] > mas[a+1]:
#             mas[a], mas[a+1] = mas[a+1], mas[a]
#             kil += 1
# print(kil)

# def found_len_way(n):
#     check= deque([[0, n]])
#     set_elem = {n}
#
#     while check:
#         mas_num = check.popleft()
#         num, k = mas_num[1], mas_num[0]
#         for i in num + 1, num - 1, num // 3 if num % 3 == 0 else None:
#             if i:
#                 if i == 1:
#                     return k
#                 if i not in set_elem:
#                     check.append([k+1, i])
#                     set_elem.add(i)
# n = int(input())
# for i in range(2, n, 1):
#     print(found_len_way(i) + 1)

# n, k = map(int, input().split())
# print(n // (k + 1) * k + n % (k + 1))

# def recurse(elem, set_check_elem, set_print_elem):
#     set_uze_number = set()
#     for z in range(1, len(elem), 1):
#         if elem[z] not in set_uze_number:
#             set_uze_number.add(elem[z])
#             for i in range(1, elem[z] // 2 + 1, 1):
#                 kil_1 = elem[0]
#                 new_number = [i, elem[z] - i]
#                 use_number = []
#                 for a in new_number:
#                     if a == 1:
#                         kil_1 += 1
#                     else:
#  in range(1, len(number_del), 1):
#         for i in range(1, number_del[z] // 2 + 1, 1):
#             number = [i, number_del[z] - i]
#             new_number = [number_del[0]]
#             new_number.extend(number_del[1:z])
#             for a in number:
#                 if a == 1:
#                     new_number[0] += 1
#                 else:
#                     new_number.append(a)
#             new_number.extend(number_del[z+1:])
#             if tuple(new_number) not in set_elem:
#                 sorted_elem = [new_number[0]]
#                 sorted_elem.extend(sorted(new_number[1:]))
#                 if tuple(sorted_elem) not in set_expresion:
#                     expresion = "1" if new_number[0] else ""
#                     expresion += "+1" * (new_number[0] - 1)
#                     for a in range(1, len(new_number), 1):
#                         expresion += "+" if expresion else ""
#                         expresion += str(new_number[a])
#                     f.write(expresion)
#                     f.write('\n')
#                     set_expresion.add(tuple(sorted_elem))
#                 set_elem.add(tuple(new_number))
#                 check.append(new_number)
#                 print(1)
# f.close()

# n = int(input())
# check = [[0, n]]
# set_elem, set_expresion = {str(n)}, {str(n)}
# while check:
#     deleten = check.pop()
#     if deleten[0] == n:
#         continue
#     for z in range(1, len(deleten)):
#         print("djjdjd", deleten)
#         for i in range(1, deleten[z] // 2 + 1):
#             kil_1, num = 0, [i, deleten[z] - i]
#             new_mas = [deleten[0]]
#             for a in range(2):
#                 if num[a] == 1:
#                     kil_1 += 1
#                 else:
#                     new_mas.append(num[a])
#             new_mas[0] += kil_1
#             new_mas.extend(deleten[1:z])
#             new_mas.extend(deleten[z+1:])
#             if tuple(new_mas) not in set_elem:
#                 set_elem.add(tuple(new_mas))
#                 check.append(new_mas)
#                 expresion = "1" + "+1" * (new_mas[0] - 1) if new_mas[0] else ""
#                 for a in new_mas[1:]:
#                     expresion += "+" if expresion else ""
#                     expresion += str(a)
#                 sort_expresion = sorted(expresion)
#                 sort_expresion = "".join(sort_expresion)
#                 if sort_expresion not in set_expresion:
#                     print(expresion)
#                     set_expresion.add(sort_expresion)

# for i in list(set_expresion):
#     print(i)

# d1, m1, y1 = map(int, input().split())
# d2, m2, y2 = map(int, input().split())
# mas_len_mounce = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# len_year = sum(mas_len_mounce)
# rez = 1
#
# if (y1 > y2) or (m1 > m2 and y1 == y2) or (d1 > d2 and y1 == y2 and m1 == m2):
#     d1, d2 = d2, d1
#     m1, m2 = m2, m1
#     y1, y2 = y2, y1
#
# for i in range(y1 + 1, y2, 1):
#     if i % 4 == 0:
#         rez += 1
#     rez += len_year
#
# if y1 != y2:
#     if y1 % 4 == 0 and m1 <= 2:
#         rez += 1
#     if y2 % 4 == 0 and m2 > 2:
#         rez += 1
#     rez += abs(mas_len_mounce[m1] - d1) + sum(mas_len_mounce[m1 + 1:])
#     rez += sum(mas_len_mounce[:m2]) + d2
# else:
#     print(0/0)
#     if y1 % 4 == 0 and m1 <= 2 < m2:
#         rez += 1
#     rez += sum(mas_len_mounce[m1+1: m2]) + mas_len_mounce[m1] - d1 + d2 - 1 if m1 != m2 else d2 - d1
# print(rez)

# def found_quarter(x1, y1, x2, y2):
#     x = x1 if x1 != 0 else x2
#     y = y1 if y1 != 0 else y2
#     if x == 0:
#         return None
#     elif y == 0:
#         return None
#     if x > 0 and y > 0:
#         return 1
#     elif x < 0 and y > 0:
#         return 2
#     elif x < 0 and y < 0:
#         return 3
#     elif x > 0 and y < 0:
#         return 4
#
# x1, y1, x2, y2 = map(int, input().split())
# if x1 == x2 == 0 or y1 == y2 == 0:
#     print(0)
#     exit()
# k = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else 0
# p = y1 - k*x1
# edge_y = p if y1 < p < y2 or y2 < p < y1 else None
# if k == 0:
#     edge_x = 0
# else:
#     edge_x = -p/k if x1 < -p/k < x2 or x2 < -p/k < x1 else None
# set_quarter = {found_quarter(x1, y1, x2, y2), found_quarter(x2, y2, x1, y1)}
# if edge_y:
#     if edge_y < 0:
#         set_quarter.update({3, 4})
#     elif edge_y > 0:
#         set_quarter.update({1, 2})
# if edge_x:
#     if edge_x < 0:
#         set_quarter.update({2, 3})
#     elif edge_x > 0:
#         set_quarter.update({1, 4})
#
# for i in set_quarter:
#     print(i)


# def found_quarter(x1, y1, x2, y2):
#     x = x1 if x1 != 0 else x2
#     y = y1 if y1 != 0 else y2
#     if x == 0:
#         return None
#     elif y == 0:
#         return None
#     elif x > 0 and y > 0:
#         return 1
#     elif x < arter:
#         print(i)


# x1, y1, x2, y2 = map(int, input().split())
# if x2 - x1 == 0:
#     k = 0
# else:
#     k = (y2 - y1) / (x2 - x1)
# p = y1 - k * x1
# edge_x = k*x + p
# edge_y = p


# d1, m1, y1 = map(int, input().split())
# d2, m2, y2 = map(int, input().split())
# mas_len_mounce = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# len_year = sum(mas_len_mounce)
# rez = 1
#
# if (y1 > y2) or (m1 > m2 and y1 == y2) or (d1 > d2 and y1 == y2 and m1 == m2):
#     d1, d2 = d2, d1
#     m1, m2 = m2, m1
#     y1, y2 = y2, y1
#
# for i in range(y1 + 1, y2, 1):
#     if i % 4 == 0:
#         rez += 1
#     rez += len_year
#
# if y1 != y2:
#     if y1 % 4 == 0 and m1 <= 2:
#         rez += 1
#     if y2 % 4 == 0 and m2 > 2:
#         rez += 1
#     rez += abs(mas_len_mounce[m1] - d1) + sum(mas_len_mounce[m1 + 1:])
#     rez += sum(mas_len_mounce[:m2]) + d2
# else:
#     if y1 % 4 == 0 and m1 <= 2 < m2:
#         rez += 1
#     rez += sum(mas_len_mounce[m1+1: m2]) + mas_len_mounce[m1] - d1 + d2 - 1 if m1 != m2 else d2 - d1
# print(rez)

# d1, m1, y1 = map(int, input().split())
# d2, m2, y2 = map(int, input().split())
#
# if y1 == y2:
#     print(0/0)
#
# if (y1 > y2) or (y1 == y2 and m1 > m2) or (y1 == y2 and m1 == m2 and d1 > d2):
#     d1, d2 = d2, d1
#     m1, m2 = m2, m1
#     y1, y2 = y2, y1
#
# mas_len_mounce = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# len_year = sum(mas_len_mounce)
# rez = 1
# for i in range(y1 + 1, y2, 1):
#     if i % 4 == 0:
#         rez += 1
#     rez += len_year
# if y1 != y2:
#     if y1 % 4 == 0 and m1 <= 2:
#         rez += 1
#     if y2 % 4 == 0 and m2 > 2:
#         rez += 1
#     rez += sum(mas_len_mounce[m1:]) - d1
#     rez += sum(mas_len_mounce[:m2]) + d2
# else:
#     if y1 % 4 == 0 and m1 <= 2 < m2:
#         rez += 1
#     if m1 == m2:
#         rez += d2 - d1
#     else:
#         sum_mounce = 0
#         for i in range(m1 + 1, m2):
#             sum_mounce += mas_len_mounce[i]
#         rez += mas_len_mounce[m1] - d1 + d2
#
# print(rez)


# n = int(input())
#
# check = [["", n]]
# set_elem = {n}
#
# while check:
#     deleten = check.pop()
#     if len(deleten) > 1:
#         number = deleten[1]
#     else:
#         continue
#     for i in range(1, number // 2 + 1, 1):
#         kil_1, mas_num = 0, []
#         for a in [i, number - i]:
#             if a == 1:
#                 kil_1 += 1
#             else:
#                 mas_num.append(a)
#         expresion1 = expresion = deleten[0] + "+1" * kil_1
#         if expresion and expresion[0] == "+":
#             expresion = expresion[1:]
#         if expresion1 and expresion1[0] == "+":
#             expresion1 = expresion1[1:]
#         for a in mas_num, deleten[2:]:
#             for z in a:
#                 if expresion:
#                     expresion += "+"
#                 expresion += str(z)
#         if expresion not in set_elem:
#             check.append([expresion1, *mas_num, *deleten[2:]])
#             set_elem.add(expresion)
#             print(expresion)


# def add_points(x1, y1, x2, y2):
#     if ((x1 > 0 and y1 > 0) or (x2 > 0 and y2 > 0)):
#         set_pice.add(1)
#     if ((x1 < 0 and y1 > 0) or (x2 < 0 and y2 > 0)) or ((x1 == 0 and x2 < 0) or x2 == 0 and x1 < 0):
#         set_pice.add(2)
#     if ((x1 < 0 and y1 < 0) or (x2 < 0 and y2 < 0)):
#         set_pice.add(3)
#     if ((x1 > 0 and y1 < 0) or (x2 > 0 and y2 < 0)):
#         set_pice.add(4)
#
# def add_points_line(x1, y1, x2, y2, set_pice):
#     if x1 == x2:
#         k = 0
#     else:
#         k = (y2 - y1) / (x2 - x1)
#     p = y1 - k * x1
#     if k == 0:
#         zero_line_x = 0
#     else:
#         zero_line_x = (-p) / k
#     zero_line_y = p
#     if x1 < zero_line_x < x2 or x2 < zero_line_x < x1:
#         if zero_line_x < 0:
#             set_pice.update(set([2, 3]))
#         elif zero_line_x > 0:
#             set_pice.update(set([1, 4]))
#     if y1 < zero_line_y < y1 or y2 < zero_line_y < y1:
#         if zero_line_y < 0:
#             set_pice.update(set([3, 4]))
#         elif zero_line_y > 0:
#             set_pice.update(set([1, 2]))
#
# x1, y1, x2, y2 = map(int, input().split())
# set_pice = set()
# mas_rules = [(x1 > 0 and y1 > 0) or (x2 > 0 and y2 > 0)]
# add_points(x1, y1, x2, y2)
# add_points_line(x1, y1, x2, y2, set_pice)
# for i in set_pice:
#     print(i)

# def add_points(x1, y1, x2, y2):
#     if ((x1 > 0 and y1 > 0) or (x2 > 0 and y2 > 0)) or (x1 == 0 and x2 > 0):
#         set_pice.add(1)
#     if (x1 < 0 and y1 > 0) or (x2 < 0 and y2 > 0):
#         set_pice.add(2)
#     if (x1 < 0 and y1 < 0) or (x2 < 0 and y2 < 0):
#         set_pice.add(3)
#     if (x1 > 0 and y1 < 0) or (x2 > 0 and y2 < 0):
#         set_pice.add(4)
#
# def add_points_line(x1, y1, x2, y2, set_pice= input()
# if expression[4] == "x":
#     if expression[1] == "-":
#         print(int(expression[0]) - int(expression[2]))
#     else:
#         print(int(expression[0]) + int(expression[2]))
# elif expression[0] == "x":
#     if expression[1] == "-":
#         print(int(expression[4]) + int(expression[2]))
#     else:
#         print(int(expression[4]) - int(expression[2]))
# else:
#     if expression[1] == "-":
#         print(int(expression[0]) - int(expression[4]))
#     else:
#         print(int(expression[4]) - int(expression[0]))

# m = n = int(input())
# mas_kupur = [500, 200, 100, 50, 20, 10]
# i, kil = 0, 0
# while m:
#     if m < mas_kupur[-1]:
#         print(-1)
#         exit()
#     kil += m // mas_kupur[i]
#     m = m % mas_kupur[i]
#     i += 1
# print(kil)

# d, m, y = map(int, input().split())
# mas_len_mounce = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# point_x, point_y, x1, y1, x2, y2 = map(int, input().split())
# if x2 == x1:
#     if (point_x == x2) and (y1 <= point_y <= y2 or y2 <= point_y <= y1):
#         print("YES")
#     else:
#         print("NO")
#     exit()
# if x1 <= point_x <= x2 or x2 <= point_x <= x1:
#     k = (y2 - y1) / (x2 - x1)
#     p = y1 - k * x1
#     if k * point_x + p == point_y:
#         print("YES")
#     else:
#         print("NO")
# else:
#     print("NO")

# x1, y1, x2, y2 = map(int, input().split())
# set_pice = set()
# if (x1 > 0 and y1 > 0) or (x2 > 0 and y2 > 0):
#     set_pice.add(1)
# if (x1 > 0 and y1 < 0) or (x2 > 0 and y2 < 0):
#     set_pice.add(4)
# if (x1 < 0 and y1 < 0) or (x2 < 0 and y2 < 0):
#     set_pice.add(3)
# if (x1 < 0 and y1 > 0) or (x2 < 0 and y2 > 0):
#     set_pice.add(2)
#
# k = (y2 - y1) / (x2 - x1)
# p = y1 - k*x1
# if (x1 < 0 and x2 > 0) or (x1 > 0 and x2 < 0):
#     zero_line_y = p
#     if zero_line_y > 0:
#         set_pice.add(1)
#         set_pice.add(2)
#     elif zero_line_y < 0:
#         set_pice.add(3)
#         set_pice.add(4)
# if (y1 < 0 and y2 > 0) or (y1 > 0 and y2 < 0):
#     zero_line_x = -p / k
#     if zero_line_x > 0:
#         set_pice.add(1)
#         set_pice.add(4)
#     elif zero_line_x < 0:
#         set_pice.add(2)
#         set_pice.add(3)
# for i in set_pice:
#     print(i)



# point_x, point_y, x1, y1, x2, y2 = map(int, input().split())
# if x2 - x1 == 0:
#     if point_x == x2:
#         print("YES")
#     else:
#         print("NO")
#     exit()
# k = (y2 - y1) / (x2 - x1)
# p = y1 - k*x1
# if k * point_x + p == point_y:
#     print("YES")
# else:
#     print("NO")

# number = bin(int(input()))
# print(number[2:])

# m, n1 = map(int, input().split())
# mas_a = [array('H', list(map(int, input().split()))) for i in range(m)]
# n2, q = map(int, input().split())
# if n1 == n2:
#     n = n1
# else:
#     print(-1)
#     exit()
# mas_b = [array('H', list(map(int, input().split()))) for i in range(n)]
# mas_b_reflected = [[mas_b[a][i] for a in range(n)] for i in range(q)]
# mas_c = [array("H", [0] * q) for i in range(m)]
#
# for i in range(m):
#     for a in range(q):
#         sum = 0
#         for z in range(n):
#             sum += mas_a[i][z] * mas_b_reflected[a][z]
#         mas_c[i][a] = sum
# print(m, q)
# for i in mas_c:
#     print(*i)

# s, k, a, b = map(int, input().split())
# kil_s, kil_d = a - k, 1
# while True:
#     if kil_s <= 0:
#         print(-1)
#         exit()
#     if int((b - kil_s * s) / kil_d) == math.ceil((b - kil_s * s) / kil_d) and kil_s >= 0 and (b - kil_s * s) / kil_d >= 0:
#         break
#     kil_s -= k
#     kil_d += 1
#
# print(int((b - kil_s * s) / kil_d))

# n, s = map(int, input().split())
# print(math.ceil(s / n))


# s, k, a, b = map(int, input().split())
# kil_s, kil_d = b // s + 1, 0
# print(kil_s)
# while True:
#     if kil_s < 0:
#         print("exit")
#         exit()
#     if a == kil_s + kil_d * k:
#         print(kil_s, kil_d)
#         print((b + kil_s * s) / kil_d)
#         break
#     else:
#         kil_s -= k
#         kil_d += 1

# def program(e, f, c):
#     kil_boler = e + f
#     rez = 0
#     while kil_boler >= c:
#         peref = kil_boler // c
#         kil_boler = peref + kil_boler % c
#         rez += peref
#     return rez
#
# e, f, c = map(int, input().split())
# print(program(e, f, c))

# n = int(input())
# if n <= 9:
#     print(n)
#     exit()
# len_number, min_number, max_number = 1, 1, 9
# while n >= max_number:
#     len_number += 1
#     min_number = max_number
#     max_number = int("9" + "0" * (len_number - 1)) * len_number + max_number
#
# m = (n - min_number) / len_number + int("9" * (len_number - 1))
# if int(m) == math.ceil(m):
#     print(int(m))
# else:
#     print(0)

# mas_n, znak_sort, kil_zero, mas_number = list(input()), False, 0, []
# if mas_n[0] == "-":
#     znak_s + y2
#
# def give_scalar_multiply(x1, y1, x2, y2):
#     return x1 * x2 + y1 * y2
#
# def give_vector_multiply(x1, y1, x2, y2):
#     return x1 * y2 - x2 * y1
#
# def give_s_trigle(vector_mult):
#     return abs(vector_mult / 2)
#
#
#
# v1_x1, v1_y1, v1_x2, v1_y2 = map(int, input().split())
# v2_x1, v2_y1, v2_x2, v2_y2 = map(int, input().split())
# x1, y1 = give_vector(v1_x1, v1_y1, v1_x2, v1_y2)
# x2, y2 = give_vector(v2_x1, v2_y1, v2_x2, v2_y2)
# len_vec_1, len_vec_2 = give_len_vector(v1_x1, v1_y1, v1_x2, v1_y2), give_len_vector(v2_x1, v2_y1, v2_x2, v2_y2)
# cos_angle = give_cos_angle(x1, y1, x2, y2)
# sum_vec_x, sum_vec_y = give_sum_vectors(x1, y1, x2, y2)
# scalar_mult = give_scalar_multiply(x1, y1, x2, y2)
# vector_mult = give_vector_multiply(x1, y1, x2, y2)
# trigle_s = give_s_trigle(vector_mult)
# print("{:.9f} {:.9f}".format(len_vec_1, len_vec_2))
# print("{:.9f} {:.9f}".format(sum_vec_x, sum_vec_y))
# print("{:.9f} {:.9f}".format(scalar_mult, vector_mult))
# print("{:.9f}".format(trigle_s))


# n = int(input())
# letter = {"a", "o", "e", "u"}
# mas_vidnos, mas_len, mas_index_min = [], [], []
# for i in range(n):
#     s = input().lower()
#     kil = 0
#     for a in letter:
#         kil += s.count(a)
#     s = " ".join(s.split())
#     kil_verd = len(s.split(" "))
#     mas_vidnos.append(kil / kil_verd)
#     mas_len.append(kil_verd)
# min_elem = min(mas_vidnos)
# if mas_vidnos.count(min_elem) > 1:
#     for i in range(len(mas_vidnos)):
#         if mas_vidnos[i] == min_elem:
#             mas_index_min.append(i)
#     index_max, max_elem, count_max = 0, 0, 0
#     for i in mas_index_min:
#         if mas_len[i] > max_elem:
#             max_elem = mas_len[i]
#             index_max = i
#     for i in mas_index_min:
#         if mas_len[i] == max_elem:
#             count_max += 1
#     if count_max > 1:
#         print("O-o-o-rks...")
#     else:
#         print(index_max + 1)
# else:
#     print(mas_vidnos.index(min_elem) + 1)


# n = int(input())
# letter = {"a", "o", "e", "u"}
# mas_vidnow, mas_len, mas_index_min_vidmow = [], [], []
# for i in range(n):
#     s = input()
#     s = s.lower()
#     s_gol = ""
#     s = ' '.join(s.split())
#     for let in range(len(s)):
#         if s[let] in letter and s[let - 1] not in letter and s[let - 1] != " " and let != 0: #s[let] in letter
#             s_gol += s[let]
#     mas_vidnow.append(len(s_gol) / len(s.split(" ")))
#     mas_len.append(len(s))
#
# min_vidnow = min(mas_vidnow)
# if mas_vidnow.count(min_vidnow) == 1:
#     print(mas_vidnow.index(min_vidnow) + 1)
# else:
#     for i in range(len(mas_vidnow)):
#         if mas_vidnow[i] == min_vidnow:
#             mas_index_min_vidmow.append(i)
#     max_elem = 0
#     index_max = 0
#     for i in mas_index_min_vidmow:
#         if mas_len[i] > max_elem:
#             max_elem = mas_len[i]
#             index_max = i
#     print(index_max + 1)


# def give_vector(x11, y11, x12, y12, x21, y21, x22, y22):
#     return x12 - x11, y12 - y11, x22 - x21, y22 - y21
#
# def give_sum_vector(x1, y1, x2, y2):
#     return x1 + x2, y1 + y2
#
# def give_angle(x1, y1, x2, y2):
#     return (x1 * x2 + y1 * y2) / (math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2))
#
# def give_scalar_mult(x1, y1, x2, y2, angle):
#     return math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2) * angle
#
# def give_s_trigle(len_vec_1, len_vec_2, sum_vector_x, sum_vector_y, angle):
#     # return 0.5 * len_vec_1 * len_vec_2 * math.sin(angle)
#     len_vec_3 = math.sqrt(len_vec_1 ** 2 + len_vec_2 ** 2 - 2 * len_vec_2 * len_vec_1 * angle)
#     y_len_vec_3 = math.sqrt((sum_vector_x) ** 2 + (sum_vector_y) ** 2)
#     p = (len_vec_1 + len_vec_2 + len_vec_3) / 2
#     return math.sqrt(p * (p - len_vec_1) * (p - len_vec_2) * (p - len_vec_3))
#
# def give_vector_multiply(x1, y1, x2, y2):
#     return x1 * y2 - x2 * y1
#
# x11, y11, x12, y12 = map(int, input().split())
# x21, y21, x22, y22 = map(int, input().split())
# x1, y1, x2, y2 = give_vector(x11, y11, x12, y12, x21, y21, x22, y22)
# # print(x1, y1, x2, y2)
#
# len_vec_1 = math.sqrt((x12 - x11) ** 2 + (y12 - y11) ** 2)
# len_vec_2 = math.sqrt((x22 - x21) ** 2 + (y22 - y21) ** 2)
# angle = give_angle(x1, y1, x2, y2)
# sum_vector_x, sum_vector_y = give_sum_vector(x1, y1, x2, y2)
#
# print("{:.9f}".format(len_vec_1), "{:.9f}".format(len_vec_2))
# print("{:.9f}".format(sum_vector_x), "{:.9f}".format(sum_vector_y))
# print("{:.9f}".format(give_scalar_mult(x1, y1, x2, y2, angle)),
#       "{:.9f}".format(give_vector_multiply(x1, y1, x2, y2)))
# print("{:.9f}".format(give_s_trigle(len_vec_1, len_vec_2, sum_vector_x, sum_vector_y, angle)))


# n = int(input())
# letter = {"a", "o", "e", "u"}
# mas_vidnow, mas_len, mas_index_min_vidmow = [], [], []
# for i in range(n):
#     s = input()
#     slen(s.split(" "))
#     mas_vidnos.append(kil / kil_verd)
#     mas_len.append(kil_verd)
# min_elem = min(mas_vidnos)
# if mas_vidnos.count(min_elem) > 1:
#     mas_index = []
#     for i in range(len(mas_vidnos)):
#         if mas_vidnos[i] == min_elem:
#             mas_index.append(i)
#     min, min_index = 0, 0
#     for i in mas_index:
#         if mas_vidnos[i] < min:
#             min = mas_vidnos[i]
#             min_index = i
#     print(min_index + 1)
# else:
#     print(mas_vidnos.index(min_elem) + 1)




# x1, y1, x2, y2 = map(int, input().split())
#
# angle = (x1 * x2 + y1 * y2) / (math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2))
# scalar_multiply = math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2) * angle
# print(int(scalar_multiply))
# print(math.acos(angle))


# def give_sum_vector(x11, y11, x12, y12, x21, y21, x22, y22):
#     x1, y1 = x12 - x11, y12 - y11
#     h, w = y22 - y21, x22 - x21
#     sum_vector = [x1 + w, y1 + h]
#     return sum_vector
#
# def give_diference_vector(x11, y11, x12, y12, x21, y21, x22, y22):
#
#     pass
#
# x11, y11, x12, y12 = map(int, input().split())
# x21, y21, x22, y22 = map(int, input().split())
#
# len_vec_1 = math.sqrt((x12 - x11) ** 2 + (y12 - y11) ** 2)
# len_vec_2 = math.sqrt((x22 - x21) ** 2 + (y22 - y21) ** 2)
#
# print(give_sum_vector(x11, y11, x12, y12, x21, y21, x22, y22))


# n = int(input())
# min = 0
# number_min = 0
# for i in range(n):
#     s = input()
#     if min > len(s):
#         min = len(s)
#         number_min = i
# print(i)


# n = int(input())
# s = input()
# set_s = set(s)
# for i in set_s:
#     if s.count(i) % 2 != 0:
#         print(i)
#         exit()
# print("Ok")


# n = list(map(int, list(input())))
# dict_number = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
# rez = 0
# for i in n:
#     rez += dict_number[i]
# print(rez)


# n = int(input())
# for i in range(n):
#     s1, s2 = input().split()
#     s1, s2 = s1.lower(), s2.lower()
#     s1, s2 = sorted(s1), sorted(s2)
#     if s1 == s2:
#         print("Yes")
#     else:
#         print("No")


# n = int(input())
# for i in range(n):
#     f = True
#     s = list(input().split())
#     for i in range(len(s)):
#         s[i] = s[i].lower()
#     mas_dict_s = [dict(), dict()]
#     for z in range(len(s)):
#         for letter in s[z]:
#             if letter not in mas_dict_s[z]:
#                 mas_dict_s[z][letter] = 1
#             else:
#                 mas_dict_s[z][letter] += 1
#     if len(mas_dict_s[0]) != len(mas_dict_s[1]):
#         print("No")
#         continue
#     for a in mas_dict_s[0]:
#         if a not in mas_dict_s[1] or mas_dict_s[0][a] != mas_dict_s[1][a]:
#             print("No")
#             f = False
#             break
#     if f:
#         print("Yes")


# x1, y1 = map(int, input().split())
# x2, y2 = map(int, input().split())
# x = int(input())
#
# len_vector = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
# delta = x / len_vector
#
# vector = [float(x2 - x1), float(y2 - y1)]
# normal_vector = [vector[0] / len_vector, vector[1] / len_vector]
# spiv_napr = [vector[0] * delta, vector[1] * delta]
# vec_pov90 = [vector[1], -vector[0]]
# vec_pov_90 = [-vector[1], vector[0]]
#
# print('{:.10f}'.format(vector[0]), '{:.10f}'.format(vector[1]))
# print('{:.10f}'.format(normal_vector[0]), '{:.10f}'.format(normal_vector[1]))
# print('{:.10f}'.format(spiv_napr[0]), '{:.10f}'.format(spiv_napr[1]))
# print('{:.10f}'.format(vec_pov90[0]), '{:.10f}'.format(vec_pov90[1]))
# print('{:.10f}'.format(vec_pov_90[0]), '{:.10f}'.format(vec_pov_90[1]))


# start = 2
# n = int(input())
# give, eat, dolg = 0, start, start
# num = 2
# for i in range(n - 1):
#     num *= 2
#     give = int((dolg + num) / 2)
#     eat = num - give
#     dolg = math.ceil((dolg + num) / 2)
#
# print(eat, dolg)


# n = int(input())
# mas_S = input()
# mas_S  = mas_S.replace(" ", "")
# kil = 0
# for i in list(set(mas_S)):
#     p = mas_S.count(i)
#     # print(i, "i")
#     if p > kil:
#         kil = p
# print(len(mas_S) - kil)

# x1, y1, x2, y2 = map(int, input().split())
# print(round(math.acos((x1 * x2 + y1 * y2) / (math.sqrt(x1 ** 2 + y1 ** 2) * math.sqrt(x2 ** 2 + y2 ** 2))), 5))

# x1, y1, x2, y2 = map(int, input().split())
# print(round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 6))

# n = int(input())
# kil = 0
# for i in list(map(float, input().split())):
#     if i < 30:
#         kil += 1
#
# print(math.ceil(kil * 0.2 / 0.9), kil)


# n = int(input())
#
# sum_progres = 1
# i = 0
# while sum_progres < n:
#     sum_progres *= 2
#     i += 1
#
# print(i)

# s = input()
# letter = "f"
# if s.count(letter) == 0:
#     exit()
# first_index = s.index(letter)
# if s.count(letter) == 1:
#     print(first_index)
#     exit()
# s = s[::-1]
# last_ia in range(i, len(mas_time), 1):
#             if (mas_time[i][1] > mas_time[a][0] and mas_time[i][1] < mas_time[a][1]) or (mas_time[a][1] > mas_time[i][0] and mas_time[a][1] < mas_time[i][1]):
#                 mas_rez.append([mas_time[i], mas_time[a]])
#     for i in mas_time:
#         if i not in mas_rez:
#             mas_returned.append(i)
#     return mas_rez, mas_returned
#
# def found_repite(mas):
#     dict_kil, mas_delet, new_mas, mas_rez = {0: 0}, [], [], []
#     for i in mas:
#         for a in i:
#             if tuple(a) not in dict_kil:
#                 dict_kil[tuple(a)] = 1
#             else:
#                 # dict_kil[tuple(a)] += 1
#                 mas.pop(mas.index(i))
#     print(mas, "mas")
#     # keys = list(dict_kil)
#     # for i in keys:
#     #     if dict_kil[i] != 1:
#     #         mas_delet.append(i)
#     #
#     # for z in mas:
#     #     for i in z:
#     #         f = True
#     #         for a in i:
#     #             if dict_kil[a] != 1:
#     #                 f = False
#     #         if f:
#     #             mas_rez.append(i[0])
#
#     return mas_rez
#
# n, k = map(int, input().split())
# mas_times = []
# for i in range(k):
#     mas_times.append(input().split("-"))
#     mas_times[i] = [mas_times[i][a].split(":") for a in range(2)]
#     for a in range(2):
#         mas_times[i][a] = int(mas_times[i][a][0]) * 60 + int(mas_times[i][a][1])
#         if a == 1:
#             mas_times[i][a] += 30
#
# mas_times.sort(key = lambda x: x[0], reverse = True)
# not_use_time = list(mas_times)
# print(not_use_time)
# mas_rez = dict()
# mas_rooms = [[] for i in range(n)]
# mas_rooms[0] = mas_times[0]
# time = 0
# dict_time_action = dict()
# dict_number_room = dict()
# for i, elem in enumerate(mas_times):
#     dict_number_room[tuple(elem)] = i + 1
# max_kil_room = 0
#
# while not_use_time:
#     deleten = not_use_time.pop()
#     dict_time_action[dict_number_room[tuple(deleten)]] = time + 1
#     less_new_times, best_new_times = [], []
#     for i in not_use_time:
#         if i[1] <= deleten[0]:
#             less_new_times.append(i)
#         elif deleten[1] <= i[0]:
#             best_new_times.append(i)
#     left, delet1 = found_times(less_new_times)
#     rigth, delet2 = found_times(best_new_times)
#     peref1 = found_repite(left)
#     peref2 = found_repite(rigth)
#     for i in peref1, peref2, delet1, delet2:
#         for a in i:
#             if a and a in not_use_time:
#                 dict_time_action[dict_number_room[tuple(not_use_time.pop(not_use_time.index(list(a))))]] = time + 1
#     time += 1
#     if time > n:
#         k = k - len(not_use_time)
#         break
#
# print(k, time)
# for i in dict_time_action:
#     print(i, dict_time_action[i])
#
# for i in mas_times:
#     print(i)

# a, b, c, d, n, k = map(int, input().split())
# if a < b:
#     a, b = b, a
#     c, d = d, c
#
# for i in range(k):
#     z = 0
#     mas_plus_num = []
#     while n - z * a >= 0:
#         mas_plus_num.append(z * c + (n - z * a) // b * d)
#         z += 1
#     n += max(mas_plus_num)
#
# print(n)



# def found_more(mas_map, n, h, w, point, can_move, perents):
#     if n <= 1:
#         # print(mas_map[point[0]][point[1]])
#         # print("1", point, mas_map[point[0]][point[1]], perents)
#         return mas_map[point[0]][point[1]]
#     mas_points, mas_rez = [], []
#     f = False
#     for i in can_move:
#         check_point = [point[0] + i[0], point[1] + i[1]]
#         if 0 <= check_point[0] < h and 0 <= check_point[1] < w and check_point[0] * w + check_point[1] not in perents:
#             mas_points.append(check_point)
#
#     for i in range(len(mas_points)):
#         add_perent = mas_points[i][0] * w + mas_points[i][1]
#         mas_rez.append(found_more(mas_map, n - 1, h, w, mas_points[i], can_move, perents.union({add_perent})))
#         for a in range(i, len(mas_points) - 1, 1):
#             f = True
#             add_perent = mas_points[i][0] * w + mas_points[i][1]
#             peref = found_more(mas_map, n - 2, h, w, mas_points[i], can_move, perents.union({add_perent}))
#             peref += found_more(mas_map, n - 2, h, w, mas_points[a], can_move, perents.union({add_perent}))
#             mas_rez.append(peref)
#     if mas_rez == []:
#         return 0
#     print(point, max(mas_rez) + mas_map[point[0]][point[1]], n, mas_rez, "ff",  mas_points, f)
#     return max(mas_rez) + mas_map[point[0]][point[1]]
#
#
# n, h, w = map(int, input().split())
# mas_map = []
# for i in range(h):
#     mas_map.append(list(map(int, input().split())))
#
# can_move = [(0, 1), (0, -1), (1, 0), (-1, 0)]
# print(found_more(mas_map, n, h, w, [0, 0], can_move, {0}))

# def found_left(mas, elem):
#     left = -1
#     rigth = len(mas)
#     while rigth - left > 1:
#         middle =    check_index.insert(left, block_pos)
#     mas[index[0]][index[1]] = None
#     rez += num
# print(rez)

# def found_left(mas, elem):
#     left = -1
#     rigth = len(mas)
#     while rigth - left > 1:
#         middle = (rigth + left) // 2
#         if elem > mas[middle]:
#             left = middle
#         else:
#             rigth = middle
#     return left + 1
#
# n, h, w = map(int, input().split())
# mas = []
# for i in range(h):
#     mas.append(list(map(int, input().split())))
#
# mas.reverse()
# dict_elem = sorted(zip(mas[0], [[0, i] for i in range(w)]), key = lambda i: i[0])
# check_num = [i[0] for i in dict_elem]
# check_index = [i[1] for i in dict_elem]
# mas[0] = [None for i in range(w)]
#
# mas_can_make = [(0, -1), (1, 0), (0, 1)]
# rez = 0
#
# for i in range(n):
#     num = check_num.pop()
#     print(num)
#     index = check_index.pop()
#     for a in mas_can_make:
#         block_pos = [index[0] + a[0], index[1] + a[1]]
#         if 0 <= block_pos[0] < h and 0 <= block_pos[1] < w and mas[block_pos[0]][block_pos[1]] != None:
#             left = found_left(check_num, mas[block_pos[0]][block_pos[1]])
#             check_num.insert(left, mas[block_pos[0]][block_pos[1]])
#             check_index.insert(left, block_pos)
#     mas[index[0]][index[1]] = None
#     rez += num
# print(check_num)
# print(rez)

# while check:


# x0, n = map(int, input().split())
# masx, masy = [], []
# for i in range(n):
#     x1, y1, x2, y2 = map(int, input().split())
#     masx.append(x1)
#     masx.append(x2)
#     masy.append(y1)
#     masy.append(y2)
#
# mas = [array('B', [0 for a in range(max(masx) + 2)]) for i in range(max(masy) + 2)]
# num_pipe = 1
# final_pipes = dict()
#
# for i in range(0, n * 2, 2):
#     x1, y1, x2, y2 = masx[i], masy[i], masx[i + 1], masy[i + 1]
#     k = (y2 - y1) / (x2 - x1)
#     p = y1 - k * x1
#     for x in range(x1, x2 + 1, 1):
#         y = k * x + p
#         mas[math.ceil(y)][int(x)] = num_pipe
#     if y1 > y2:
#         final_pipes[num_pipe] = [y2 - 1, x2]
#     else:
#         final_pipes[num_pipe] = [y1 - 1, x1]
#     num_pipe += 1
#
#
# check = deque([[len(mas) - 1, x0]])
# # check = None
# rez = 0
# while check:
#     deleten = check.popleft()
#     # print(deleten)
#     if deleten[0] == 0:
#         rez = deleten[1]
#         break
#     if mas[deleten[0] - 1][deleten[1]] == 0:
#         peref = [deleten[0] - 1, deleten[1]]
#         check.append(peref)
#         # mas[deleten[0]][deleten[1]] = 7
#         continue
#     num_pipe = mas[deleten[0] - 1][deleten[1]]
#     if final_pipes[num_pipe][0] == -1 or final_pipes[num_pipe][0] == 0:
#         rez = final_pipes[num_pipe][1]
#         break
#     check.append(final_pipes[num_pipe])
#     # mas[deleten[0]][deleten[1]] = 7
#
# # mas.reverse()
# # for i in range(len(mas)):
# #     print(*mas[i], "number", i)
#
# print(rez)


# print("y = {}x + {}".format(k, p1))


# message = list(input())
# key = list(input())
# mas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
# tranclator = {" ": " "}
#
# for i in range(len(key)):
#     tranclator[mas[i]] = key[i]
#
# for i in range(len(message)):
#     print(tranclator[message[i]], end = "")


# mas = list(input())
#
# open_bracked = {"{", "[", "("}
# closed_bracked = {"}": "{", "]": "[", ")": "("}
#
# check = [mas[0]]
# rez = 0
#
# for i in range(len(mas)):
#     if mas[i] in open_bracked:
#         check.append(mas[i])
#         continue
#     if closed_bracked[mas[i]] == check[-1]:
#         check.pop()
#     else:
#         rez += 1
#         check.pop()
#
# print(rez)

# s, k, a, b = map(int, input().split())
#
# mas = [i for i in range(0, a, k)]
# mas.pop(0)
# rez = -1
#
# for i in mas:
#     kil_lap_drag = b - ((a - i) * s)
#     if kil_lap_drag % (i // k) == 0 and kil_lap_drag > 0:
#         rez = kil_lap_drag // (i // k)
#         break
# if rez == -1 and b == s * a:
#     rez = 0
# print(rez)


# def creat_graph(mas_prize, mas_road, n):
#     graph = {i: dict() for i in range(1, n + 1, 1)}
#     for i in range(0, len(mas_road), 2):
#         v1, v2 = mas_road[i], mas_road[i + 1]
#         graph[v1][v2] = mas_prize[v1]
#         graph[v2][v1] = mas_prize[v2]
#     return graph
#
# def dicstra(graph, mas_prize, n, m):
#     start = 1
#     finish = n
#     check = deque([start])
#     distance = {start: 0}
#
#     while check:
#         deleten = check.popleft()
#         for i in graph[deleten]:
#             if i not in distance or distance[deleten] + graph[deleten][i] < distance[i]:
#                 check.append(i)
#                 distance[i] = distance[deleten] + graph[deleten][i]
#     return distance
#
#
# if __name__ == "__main__":
#     f = open("inp math.ceil(s):
#     print(int(s))
# else:
#     print(s)

# def creat_graph(mas_prize, mas_road, n):
#     graph = {i: dict() for i in range(1, n + 1, 1)}
#     for i in range(0, len(mas_road), 2):
#         v1, v2 = mas_road[i], mas_road[i + 1]
#         graph[v1][v2] = mas_prize[v1]
#         graph[v2][v1] = mas_prize[v2]
#     return graph
#
# def dicstra(graph, mas_prize, n, m):
#     start = 1
#     finish = n
#     check = deque([start])
#     distance = {start: 0}
#
#     while check:
#         deleten = check.popleft()
#         for i in graph[deleten]:
#             if i not in distance or distance[deleten] + graph[deleten][i] < distance[i]:
#                 check.append(i)
#                 distance[i] = distance[deleten] + graph[deleten][i]
#     return distance
#
#
# if __name__ == "__main__":
#     n = int(input())
#     mas_prize = [None]
#     mas_prize.extend(list(map(int, input().split())))
#     m = int(input())
#     if m == 0:
#         print(-1)
#         exit()
#     mas_road = list(map(int, input().split()))
#     graph = creat_graph(mas_prize, mas_road, n)
#     distances = dicstra(graph, mas_prize, n, m)
#     if n not in distances:
#         print(-1)
#     else:
#         print(distances[n])

# def creat_graph(mas_prize, mas_road, city_prizes, n, m):
#     graph = {i: dict() for i in range(1, n + 1, 1)}
#     # try:
#     mas_par = [mas_road[i] for i in range(len(mas_road)) if i % 2 == 0]
#     mas_no_par = [mas_road[i] for i in range(len(mas_road)) if i % 2 != 0]
#     # except:
#     #     print(1)
#     #     exit()
#     for i in range(len(mas_road) // 2):
#         v1, v2 = mas_par[i], mas_no_par[i]
#         graph[v1][v2] = city_prizes[v1]
#         graph[v2][v1] = city_prizes[v2]
#     return graph
#
#
# def dicstra(graph, start, final):
#     check = deque([start])
#     mas_weigth = {start: 0}
#
#     while check:
#         deleten = check.popleft()
#         for i in graph[deleten]:
#             if i not in mas_weigth or mas_weigth[deleten] + graph[deleten][i] < mas_weigth[i]:
#                 mas_weigth[i] = mas_weigth[deleten] + graph[deleten][i]
#                 check.append(i)
#     return mas_weigth
#
# def found_path(mas_weigth, start, final, city_prizes):
#     check = deque([final])
#     rez = 0
#     mas_path = []
#
#     while check:
#         deleten = check.popleft()
#         for i in graph[deleten]:
#             if mas_weigth[deleten] - graph[i][deleten] == mas_weigth[i]:
#                 rez += graph[i][deleten]
#                 mas_path.append(deleten)
#                 check.append(i)
#                 if i == start:
#                     return rez
#     return "path is not defined"
#
# if __name__ == "__main__":
#     n = int(input())
#     if n == 0:
#         print(-1)
#         exit()
#     mas_prize = list(map(int, input().split()))
#     city_prizes = {i: mas_prize[i - 1] for i in range(1, n + 1, 1)}
#     m = int(input())
#     if m == 0:
#         print(-1)
#         exit()
#     start = 1
#     final = n
#     mas_road = list(map(int, input().split()))
#     graph = creat_graph(mas_prize, mas_road, city_prizes, n, m)
#     mas_weigth = dicstra(graph, start, final)
#     print(graph, "graph")
#     # print(mas_weigth, "mas_weigth")
#     rez = found_path(mas_weigth, start, final, city_prizes)
#     if rez == "path is not defined":
#         print(-1)
#     else:
#         print(rez)

# def dicstart(graph, start, final):
#
#     check = deque([start])
#     dictance = {start: 0}
#
#     while check:
#         deleten = check.popleft()
#         for i in graph[deleten]:
#             if i not in dictance or dictance[deleten] + graph[deleten][i] < dictance[i]:
#                 check.append(i)
#                 dictance[i] = dictance[deleten] + graph[deleten][i]
#     return dictance
#
# def found_all_path(graph, mas_distance, start, final):
#     check = deque([final])
#     mas_path = []
#
#     while check:
#         deleten = check.popleft()
#         for i in graph[deleten]:
#             if mas_distance[deleten] == mas_distance[i] + graph[deleten][i]:
#                 if i == start:
#                     mas_path.append(i)
#                     continue
#                 check.append(i)
#                 mas_path.append(i)
#     mas_path.insert(0, final)
#     return mas_path
#
#
# if __name__ == "__main__":
#     f = open("input.txt", 'r')
#     n, m, k = map(int, f.readline().split())
#     mas_quick_path = list(map(int, f.readline().split()))
#     graph = {i: dict() for i in range(1, n + 1, 1)}
#     start = 1
#     final = n
#     for i in range(m):
#         v1, v2, weigth = map(int, f.readline().split())
#         if v2 in graph[v1] and graph[v1][v2] > weigth:
#             pass
#         else:
#             graph[v1][v2] = weheck.popleft()
#         for i in graph[deleten]:
#             if i not in mas_weigth or mas_weigth[deleten] + graph[deleten][i] < mas_weigth[i]:
#                 mas_weigth[i] = mas_weigth[deleten] + graph[deleten][i]
#                 check.append(i)
#     return mas_weigth
#
# def found_path(mas_weigth, start, final):
#     check = deque([final])
#     mas_path = []
#
#     while check:
#         deleten = check.popleft()
#         for i in graph[deleten]:
#             if mas_weigth[deleten] - graph[deleten][i] == mas_weigth[i]:
#                 mas_path.append(deleten)
#                 check.append(i)
#                 if i == start:
#                     mas_path.append(start)
#                     mas_path.reverse()
#                     return mas_path
#     return "path is not defined"
#
# if __name__ == "__main__":
#     n = int(input())
#     mas_prize = list(map(int, input().split()))
#     m = int(input())
#     if m == 0:
#         print(-1)
#         exit()
#     mas_road = list(map(int, input().split()))
#     graph = creat_graph(mas_prize, mas_road, m)
#     start = 1
#     final = n
#     mas_weigth = dicstra(graph, start, final)
#     path = found_path(mas_weigth, start, final)
#     if path == "path is not defined":
#         print(-1)
#         exit()
#     print(len(path))


# def bfs(n, m, translator, can_move, start, final):
#     check = deque([start])
#     distance = [[None for a in range(8)] for i in range(8)]
#     distance[start[0]][start[1]] = 0
#     perents = [[None for a in range(8)] for i in range(8)]
#
#     while check:
#         deleten = check.popleft()
#         for i in can_move:
#             # print(deleten[0])
#             # print(i[1])
#             peref = [deleten[0] + i[0], deleten[1] + i[1]]
#             if 0 <= peref[0] < 8 and 0 <= peref[1] < 8 and distance[peref[0]][peref[1]] == None:
#                 check.append(peref)
#                 distance[peref[0]][peref[1]] = distance[deleten[0]][deleten[1]] + 1
#                 perents[peref[0]][peref[1]] = [deleten[0], deleten[1]]
#                 if final == peref:
#                     return distance
#     return "not find path"
#
# def foundpath(n, m):
#     translator = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
#     can_move = [(1, 2), (2, 1), (-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, -2), (2, -1)]
#
#     start = list(n)
#     final = list(m)
#     start = [translator[start[0]], int(start[1]) - 1]
#     final = [translator[final[0]], int(final[1]) - 1]
#
#     mas_distance = bfs(n, m, translator, can_move, start, final)
#     if mas_distance == "not find path":
#         return 0
#     return mas_distance[final[0]][final[1]]
#
# if __name__ == "__main__":
#     f = open("input.txt", "r")
#     q = open("output.txt", "w")
#     q.close()
#     q = open("output.txt", "a")
#     s = f.readline()
#     while s != "":
#         n, m = s.split()
#         s = f.readline()
#         q.write("To get from {} to {} takes {} knight moves.\n".format(n, m, foundpath(n, m)))
#     q.close()



# def bfs(n, m):
#     check = deque([n])
#     use_numeric = set([n])
#     perents = {n: "start"}
#
#     while check:
#         num = check.popleft()
#         for i in (num + 1000 if num + 1000 < 10000 else None), (num // 10 * 10 + num % 10 - 1 if num % 10 - 1 > 0 else None), (num // 10 + num % 10 * 1000), (num % 1000 * 10 + num // 1000):
#             if i and i not in use_numeric:
#                 check.append(i)
#                 use_numeric.add(i)
#                 perents[i] = num
#                 if i == m:
#                     return perents
#
# def found_path(n, m, perents):
#     mas_path = []
#     num_now = m
#     while perents[num_now] != "start":
#         mas_path.append(num_now)
#         num_now = perents[num_now]
#     mas_path.append(n)
#     mas_path.reverse()
#     return mas_path
#
# if __name__ == "__main__":
#     n = int(input())
#     m = int(input())
#     perents = bfs(n, m)
#     mas_path = found_path(n, m, perents)
#     for i in mas_path:
#         print(i)


# def bfs(a, b):
#     rez = 0
#     check = deque([a])
#     use_nameric = set([a])
#     perents = {a: "start"}
#
#     while check:
#         nam = check.popleft()
#         for i in (nam - 2), (nam * 3), (nam + sum(list(map(int, list(str(nam)))))):
#             if 1 <= i < 9999 and i not in use_nameric:
#                 check.append(i)
#                 use_nameric.add(i)
#                 perents[i] = nam
#                 if i == b:
#                     return perents
#
#
# def found_path(perents, b):
#     mas_path = []
#     num_now = b
#     while num_now != "start":
#         mas_path.append(num_now)
#         num_now = perents[num_now]
#     return mas_path
#
# if __name__ == "__main__":
#     a                 check.append(peref)
#                     distance[peref[0]][peref[1]] = distance[deleten[0]][deleten[1]] + 1
#                     perents[peref[0]][peref[1]] = deleten
#                     if peref == final:
#                         return perents
#     return "way is not find"
#
#
# def found_path(perents, n, start, final):
#     mas_path = []
#     point_now = final
#     while point_now != "start":
#         mas_path.append(point_now)
#         point_now = perents[point_now[0]][point_now[1]]
#     return mas_path
#
#
# def chenge_map(mas_path, _map, start, final):
#     for i in mas_path:
#         _map[i[0]][i[1]] = "+"
#     _map[start[0]][start[1]] = "@"
#
#
# def found_way(n):
#     wall = "O"
#
#     start = found_points("@")
#     final = found_points("X")
#
#     perents = bfs(start, final, n, _map, wall)
#     if perents == "way is not find":
#         return "N"
#     mas_path = found_path(perents, n, start, final)
#     chenge_map(mas_path, _map, start, final)
#     return "Y"
#
#
# if __name__ == "__main__":
#     n = int(input())
#     _map = []
#     for i in range(n):
#         _map.append(list(input()))
#
#     rez = found_way(n)
#     if rez == "N":
#         print(rez)
#         exit()
#     print(rez)
#     for i in _map:
#         for a in i:
#             print(a, end = "")
#         print()



# def bfs(n, m, translator, can_move, start, final):
#     check = deque([start])
#     distance = [[None for a in range(8)] for i in range(8)]
#     distance[start[0]][start[1]] = 0
#     perents = [[None for a in range(8)] for i in range(8)]
#
#     while check:
#         deleten = check.popleft()
#         for i in can_move:
#             # print(deleten[0])
#             # print(i[1])
#             peref = [deleten[0] + i[0], deleten[1] + i[1]]
#             if 0 <= peref[0] < 8 and 0 <= peref[1] < 8 and distance[peref[0]][peref[1]] == None:
#                 check.append(peref)
#                 distance[peref[0]][peref[1]] = distance[deleten[0]][deleten[1]] + 1
#                 perents[peref[0]][peref[1]] = [deleten[0], deleten[1]]
#                 if final == peref:
#                     return distance
#     return "not find path"
#
# def foundpath(n, m):
#     translator = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
#     can_move = [(1, 2), (2, 1), (-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, -2), (2, -1)]
#
#     start = list(n)
#     final = list(m)
#     start = [translator[start[0]], int(start[1]) - 1]
#     final = [translator[final[0]], int(final[1]) - 1]
#
#     mas_distance = bfs(n, m, translator, can_move, start, final)
#     if mas_distance == "not find path":
#         return 0
#     return mas_distance[final[0]][final[1]]
#
# while True:
#     n, m = input().split()
#     print("To get from {} to {} takes {} knight moves.".format(n, m, foundpath(n, m)))



# def bfs(start, wall, door, can_move, map_maze, l, r, c):
#     check = deque([start])
#     distance = [[[None for z in range(c)] for a in range(r)] for i in range(l)]
#     distance[start[0]][start[1]][start[2]] = 0
#
#     while check:
#         deleten = check.popleft()
#         for i in can_move:
#             # print(deleten, i)
#             a, b, f = deleten[0] + i[0], deleten[1] + i[1], deleten[2] + i[2]
#             # print(a, b, f, 0 <= a < l, 0 <= b < r, 0 <= f < c)
#             if 0 <= a < l and 0 <= b < r and 0 <= f < c:
#                 # print(1)
#                 if map_maze[a][b][f] != wall and distance[a][b][f] == None:
#                     # print(a, b, f)
#                     peref = [a, b, f]
#                     check.append(peref)
#                     distance[a][b][f] = distance[deleten[0]][deleten[1]][deleten[2]] + 1
#                     if map_maze[a][b][f] == door:
#                         # print("finish", a, b, f)
#                         return [a, b, f, distance[a][b][f]]
#     return "Trapped!"
#
# def scan():
#     l, r, c = map(int, input().split())
#     if l == 0 and r == 0 and c == 0:
#         exit()
#     start = [0, 0, 0]
#
#     map_maze = []
#
#     for i in range(l):
#         map_maze.append(list())
#         for a in range(r):
#             map_maze[-1].append(list(input()))
#         if i == l - 1:
#             break
#         input()
#
#     can_move = [(0, 0, 1), (0, 1, 0), (0, 0, -1), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
#     wall = "#"
#     door = "E"
#     start = foundstart(map_maze)
#
#     return bfs(start, wall, door, can_move, map_maze, l, r, c)
#
#
# def foundstart(map_maze):
#     for i in range(len(map_maze)):
#         for a in range(len(map_maze[i])):
#             for z in range(len(map_maze[i][a])):
#                 if map_maze[i][a][z] == 'S':
#                     start = [i, a, z]
#                     breaph[v1][v2] = int(distance)
#     graph[v2][v1] = int(distance)
#
# start = "A"
# check = deque(start)
# mas_dictance = {start: 0}
#
# while check:
#     deleten = check.popleft()
#     for i in graph[deleten]:
#         if i not in mas_dictance or mas_dictance[deleten] + graph[deleten][i] < mas_dictance[i]:
#             check.append(i)
#             mas_dictance[i] = mas_dictance[deleten] + graph[deleten][i]
#
# path = foundpath()
# print(graph)
# print(mas_dictance)
# print(path)

# def found_left(mas, elem):
#     left = -1
#     rigth = len(mas)
#     while rigth - left > 1:
#         middle = (rigth + left) // 2
#         if mas[middle] < elem:
#             left = middle
#         else:
#             rigth = middle
#     return left + 1
#
# def found_rigth(mas, elem):
#     left = -1
#     rigth = len(mas)
#     while rigth - left > 1:
#         middle = (rigth + left) // 2
#         if mas[middle] > elem:
#             rigth = middle
#         else:
#             left = middle
#     return rigth
#
# def found_point(mas, elem):
#     left = found_left(mas, elem)
#     rigth = found_rigth(mas, elem)
#
#
# mas = list(map(int, input().split()))
# elem = int(input())
# print(found_left(mas, elem), found_rigth(mas, elem))

# def larg_list(x, y):
#     map_L = [[0] * (len(y)) for i in range(len(x))]
#     mas_path = []
#
#     for x_i, x_elem in enumerate(x):
#         for y_i, y_elem in enumerate(y):
#             if x_elem == y_elem:
#                 map_L[x_i][y_i] = map_L[x_i - 1][y_i - 1] + 1
#                 mas_path.append(x_i)
#             else:
#                 map_L[x_i][y_i] = max(map_L[x_i - 1][y_i], map_L[x_i][y_i - 1])
#     return map_L, mas_path
#
#
#
# mas1 = list(map(int, input().split()))
# mas2 = list(map(int, input().split()))
#
# map_l, mas_path = larg_list(mas1, mas2)
#
# print(mas_path)
# for i in map_l:
#     print(i)

# n, m = map(int, input().split())
# finish = list(map(int, input().split()))
#
# chess_map = [[0] * m for i in range(n)]
# chess_map[0] = [1] * m
# for i in range(n):
#     chess_map[i][0] = 1
#
# for i in range(1, n):
#     for a in range(1, m):
#         chess_map[i][a] = chess_map[i - 1][a] + chess_map[i][a - 1]
#
# # start = [0, 0]
# # check = deque([start])
# # mas_can_go = [(0, 1), (1, 0), (1, 1)]
# # destance = [[None] * m for i in range(n)]
# #
# # while check:
# #     deleten = check.popleft()
# #     for i in range(len(mas_can_go)):
# #         # print(deleten[0] - mas_can_go[i][0], deleten[1] - mas_can_go[i][1])
# #         if deleten[0] - mas_can_go[i][0] >= 0 and deleten[1] - mas_can_go[i][1] >= 0:
# #             chess_map[deleten[0]][deleten[1]] += chess_map[deleten[0] - mas_can_go[i][0]][deleten[1] - mas_can_go[i][1]]
# #     # print(deleten, chess_map[deleten[0]][deleten[1]])
# #     for i in range(len(mas_can_go)):
# #         peref = [deleten[0] + mas_can_go[i][0], deleten[1] + mas_can_go[i][1]]
# #         if peref[0] < m and peref[1] < n and destance[peref[0]][peref[1]] == None :
# #             destance[deleten[0] + mas_can_go[i][0]][deleten[1] + mas_can_go[i][1]] = 1
# #             check.append([peref[0], peref[1]])
#
# for i in chess_map:
#     print(i)




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
#
# def blab_sort(mas):
#     for i in range(len(mas) - 1):
#         for a in range(len(mas) - i - 1):
#             if mas[a] > mas[a + 1]:
#                 peref = mas[a]
#                 mas[a] = mas[a + 1]
#                 mas[a + 1] = peref
# n = int(input())
# mas1, mas2 = [], []
# for i in range(n):
#     peref = randint(-10000, 10000)
#     mas1.append(peref)
#     mas2.append(peref)
# time1 = time()
# blab_sort(mas1)
# time2 = time()
# print(time2 - time1)
# quick_sort(mas2)
# print(time() - time2)

# n = int(input())
# mas = []
#
# for i in range(2, int(n ** 0.5) + 1, 1):
#     if n % i == 0:
#         mas.append(i)
#         mas.append(n // i)
# print(mas)

# def quick_sort(mas):
#     if len(mas) <= 1:
#         return
#     main_element = mas[0]
#     left, right, middle = [], [], []
#     for x in mas:
#         if x < main_element:
#             left.append(x)
#         elif x == main_element:
#             middle.append(x)
#         else:
#             right.append(x)
#     quick_sort(left)
#     quick_sort(right)
#     k = 0
#     for x in left + middle + right:
#         mas[k] = x
#         k += 1
#
# mas = [mas1 < len_mas1 and left_index_mas2 < len_mas2:
#     min_element_index = 0
#     if mas1[left_index_mas1] <= mas2[left_index_mas2]:
#         masrez.append(mas1[left_index_mas1])
#         left_index_mas1 += 1
#     else:
#         masrez.append(mas2[left_index_mas2])
#         left_index_mas2 += 1
#
# if left_index_mas1 != len_mas1:
#     masrez.extend(mas1[left_index_mas1: len_mas1])
# else:
#     masrez.extend(mas2[left_index_mas2: len_mas2])
#
# print(masrez)

# def bfs(startpoint):
#     check = deque([startpoint])
#     peref = 0
#     while check:
#         deleten = check.popleft()
#         for i in mascross:
#             if deleten[0] + i[0] < kil and deleten[0] + i[0] >= 0 and deleten[1] + i[1] < n and deleten[1] + i[1] >= 0:
#                 check.append((deleten[0] + i[0], deleten[1] + i[1]))
#                 map[deleten[0] + i[0]][deleten[1] + i[1]] += 1
#
# n = int(input())
# if n == 1:
#     print(10)
#     exit()
#
# kil = 10
# mascross = [[0, 1], [1, 1], [-1, 1]]
# startpoints = [(i, 0) for i in range(kil)]
# res = 0
#
# map = [[0 for i in range(n)] for a in range(kil)]
#
# for i in startpoints:
#     bfs(i)
# for i in range(kil):
#     res += map[i][-1]
# print(res)

# map = [[2], [3], [3] ,[3] ,[3] ,[3] ,[3] ,[3] ,[3] ,[2]]
# n = int(input())
# if n == 1:
#     print(10)
#     exit()
# kil = 10
# res = 0
#
# for i in range(n - 2):
#     map[0].append(map[0][i] + map[1][i])
#     map[kil - 1].append(map[kil - 1][i] + map[kil - 2][i])
#     for a in range(1, kil - 1, 1):
#         map[a].append(map[a - 1][i] + map[a][i] + map[a + 1][i])
# for i in map:
# #    print(i)
#     res += i[n - 2]
# print(res)

# n = int(input())
#
# masbool = [True] * n
# for i in range(2, int(n ** 0.5)):
#     if masbool[i]:
#         for a in range(i ** 2, n, i):
#             masbool = False


# n = int(input())
# masdil = [1, n]
# for i in range(2, int(math.sqrt(n)) + 1):
#     if n % i == 0:
#         masdil.append(i)
#         masdil.append(n // i)
# print(*set(masdil))

# a, b = map(int, input().split())
# while a != 0 and b != 0:
#     if a > b:
#         a = a % b
#     else:
#         b = b % a
# print(max(a, b))

# n = int(input())
# masbool = [True] * n
# for i in range(2, int(n ** 0.5) + 1):
#     if masbool[i]:
#         for a in range(i ** 2, n, i):
#             masbool[a] = False
# maseazychyslo = [i for i in range(n) if masbool[i] == True]
# print(maseazychyslo)


# n = int(input())
# masbool = [True for i in range(n)]
# for i in range(2, int(n ** 0.5) + 1):
#     if masbool[i]:
#         for a in range(i ** 2, n, i):
#             masbool[a] = False
# maseasyschyslo = [i for i in range(n) if masbool[i] == True]
# print(maseasyschyslo)


# n, m, c = map(int, input().split())
# # masfigure = [list(map(int, input().split())) for i in range(c)]
# for i in range(c):
#     masfigure = randomizator(c, 1, min(n, m))
#
# cart = [array('b', [0 for i in range(m)]) for i in range(n)]
#
# def best():
#     masdobavgor = set()
#     dictfigurex = defaultdict(list)
#     dictfigurey = defaultdict(list)
#
#     res = 0
#     gor = n
#     ver = m
#
#     for i in range(c):
#         for a in range(2):
#             masfigure[i][a] -= 1
#
#     masfigurex = array('i', [masfigure[i][0] for i in range(c)])
#     masfigurey = array('i', [masfigure[i][1] for i in range(c)])
#
#     for i, item in enumerate(masfigurex):
#         dictfigurex[item].append(masfigurey[i])
#     for i, item in enumerate(masfigurey):
#         dictfigurey[item].append(masfigurex[i])
#
#     for i in range(len(dictfigurex)):
#         dictfigurex[i].sort()
#     for i in range(len(dictfigurey)):
#         dictfigurey[i].sort()
#
#     if dictfigurey[0] != []:
#         gor = dictfigurey[0][0]
#     if dictfigurex[0] != []:
#         ver = dictfigurex[0][0]
#
#     for i in range(gor):
#         if dictfigurex[i] == []:
#             res += m
#         else:
#             res += dictfigurex[i][0]
#
#     for i in range(ver):
#         if dictfigurey[i] == []:
#             res += len(masdobavgor) + (n - gor)
#         else:
#             if dictfigurey[i][0] < gor:
#                 maselementless = [a for a in list(masdobavgor) if a < dictfigurey[i][0]]
#                 masdobavgor.union(set(maselementless))
#                 res += len(maselementless)
#             else:
#                 res += len(masdobavgor)
#                 res += (dictfigurey[i][0] - gor)
#             masdobavgor.update(set([i for i in dictfigurey[i] if i < gor]))
#     return res - 1
#
# def lose():
#     gor = n
#     ver = m
#     res = -1
#     for i in range(len(masfigure)):
#         for a in range(2):
#             masfigure[i][a] -= 1
#         cart[masfigure[i][0]][masfigure[i][1]] = 3
#     for i in range(m):
#         if cart[0ange(len(masfigure)):
#     for a in range(2):
#         masfigure[i][a] -= 1
#     cart[masfigure[i][0]][masfigure[i][1]] = 3
# for i in range(m):
#     if cart[0][i] == 3:
#         ver = i
#         break
# for i in range(n):
#     if cart[i][0] == 3:
#         gor = i
#         break
#
# for i in range(gor):
#     for a in range(m):
#         if cart[i][a] == 3:
#             break
#         cart[i][a] = 1
#
# for i in range(ver):
#     for a in range(n):
#         if cart[a][i] == 3:
#             break
#         cart[a][i] = 1
#
# for i in cart:
#     print(*i)
#     res += i.count(1)
# print(res)

# from randomizayor import *
# n, m, c = map(int, input().split())
# masfigure = [list(map(int, input().split())) for i in range(c)]
#
# map = [[0 for a in range(m)] for i in range(n)] #fffff
#
# dictfigurex = defaultdict(list)
# dictfigurey = defaultdict(list)
#
# res = 0
# ver = n
# gor = m
#
# for i in range(c):
#     for a in range(2):
#         masfigure[i][a] -= 1
#
#
#
# masfigurex = array('i', [masfigure[i][0] for i in range(c)])
# masfigurey = array('i', [masfigure[i][1] for i in range(c)])
# #
# # setfigurex = set(masfigurex)
# # setfigurey = set(masfigurey)
#
# for i, item in enumerate(masfigurex):
#     dictfigurex[item].append(masfigurey[i])
# for i, item in enumerate(masfigurey):
#     dictfigurey[item].append(masfigurex[i])
#
# if dictfigurey[0] != []:
#     gor = min(dictfigurey[0])
# if dictfigurex[0] != []:
#     ver = min(dictfigurex[0])
#
# masdorobutuver = []
# masdorobutugor = []
# check = deque([[0, 0]])
# visited = []
# mascango = [[1, 0], [0, 1]]
# print(ver, gor)
# while check:
#     deleten = check.popleft()
#     for i in range(len(mascango)):
#         clit = [deleten[1] + mascango[i][0], deleten[0] + mascango[i][1]]
#         print(clit, "clit")
#         if clit not in masfigure:
#             if clit[0] > ver:
#                 masdorobutuver.append(clit)
#                 continue
#             elif clit[1] >= gor:
#                 masdorobutugor.append(clit)
#                 continue
#             check.append(clit)
#             res += 1
#             map[clit[0]][clit[1]] = 1
#
# for i in map:
#     print(i)
# print(res)
# print(masfigure)


# for i in range(n):
#     peref = m
    # if masfigurex.count(i):
        # peref =

# n = int(input())
# mas = list(map(int, input().split()))
# i = 0
# peref = mas[i]
# while peref <= n and i < 4:
#     i += 1
#     peref += mas[i]
# print(i)

# n, m, c = map(int, input().split())
# gor = n
# ver = m
# res = -1
# # masfigure = randomizator(c, 1, min(n, m))
# masfigure = [array('H', list(map(int, input().split()))) for i in range(c)]
# cart = [array('b', [0 for i in range(m)]) for i in range(n)]
# for i in range(len(masfigure)):
#     for a in range(2):
#         masfigure[i][a] -= 1
#     cart[masfigure[i][0]][masfigure[i][1]] = 3
# for i in range(m):
#     if cart[0][i] == 3:
#         ver = i
#         break
# for i in range(n):
#     if cart[i][0] == 3:
#         gor = i
#         break
#
# for i in range(gor):
#     for a in range(m):
#         if cart[i][a] == 3:
#             break
#         cart[i][a] = 1
#
# for i in range(ver):
#     for a in range(n):
#         if cart[a][i] == 3:
#             break
#         cart[a][i] = 1
#
# for i in cart:
#     # print(*i)
#     res += i.count(1)
# print(res)


# n, q = map(int, input().split())
# mas = list(map(int, input().split()))
# for i in range(q):
#     print(mas.count(int(input())))

# n, m = map(int, input().split())
# k = 0
# last = 0
# mas1 = array('i', [])
# mas2 = array('i', [])
# res = 0
# for i in range(m):
#     peref = list(map(int, input().split()))
#     mas1.append(peref[0])
#     mas2.append(peref[1])
# mas3 = list(zip(mas1, mas2))
# mas3.sort(key = lambda x : x[1], reverse = True)
# i = 0
# while k < n and i < m:
#     res += mas3[i][0] * mas3[i][1]
#     k += mas3[i][0]
#     i += 1
# if k - n > 0:
#     res -= mas3[i - 1][1] * abs(n - k)
# print(res)

# n, m, c = map(int, input().split())
# gor = n
# ver = m
# res = -1
# masfigure = randomizator(c, 1, min(n, m))
# # masfigure = [list(map(int, input().split())) for i in range(c)]
# for i in range(len(masfigure)):
#     for a in range(2):
#         masfigure[i][a] -= 1
# masfigurex = array('i', [masfigure[i][0] for i in range(c)])
# masfigurey = array('i', [masfigure[i][1] for i in range(c)])
# cart = [array('i', [0 for i in range(m)]) for i in range(n)]
# for i in masfigure:
#     cart[i[0]][i[1]] = 3
# for i in range(m):
#     if cart[0][i] == 3:
#         ver = i
#         break
# for i in range(n):
#     if cart[i][0] == 3:
#         gor = i
#         break
#
# # for i in range(gor):
# #     for a in range(m):
# #         if cart[i][a] == 3:
# #             break
#     if cart[0][i] == 3:
#         ver = i
#         break
# for i in range(n):
#     if cart[i][0] == 3:
#         gor = i
#         break
#
# for i in range(gor):
#     for a in range(m):
#         if cart[i][a] == 3:
#             break
#         cart[i][a] = 1
# for i in range(ver):
#     for a in range(n):
#         if cart[a][i] == 3:
#             break
#         cart[a][i] = 1
#
# for i in cart:
#     # print(*i)
#     res += i.count(1)
# print(res)

# n, m, c = map(int, input().split())
# cart = [array('i', [0 for a in range(m)]) for i in range(n)]
# gor = n
# ver = m
# res = 0
# masfigure = randomizator(c, 1, min(n, m))
# for i in range(c):
#     for a in range(2):
#         masfigure[i][a] -= 1
# print(masfigure)
# masfigurex = array('i', [masfigure[i][0] for i in range(c)])
# masfigurey = array('i', [masfigure[i][1] for i in range(c)])
# print(masfigurey)
# for i in masfigure:
#     cart[i[0]][i[1]] = 3
# if masfigurey.count(0) != 0:
#     for i in range(m):
#         if cart[0][i] == 3:
#             gor = i
#             break
# if masfigurex.count(0) != 0:
#     for i in range(m):
#         if cart[i][0] == 3:
#             ver = i
#             break
# print(gor, ver)
# for i in range(gor):
#     for a in range(n):
#         if cart[i][a] == 3:
#             break
#         cart[i][a] = 1
# for i in range(ver):
#     for a in range(m):
#         if cart[a][i] == 3:
#             break
#         cart[a][i] = 1
# for i in range(len(cart)):
#     print(*cart[i])
#     res += cart[i].count(1)
# print(res - 1)

# n, m, c = map(int, input().split())
# masfigure = randomizator(c, 0, min(n, m))
# masfigurex = array('i', [masfigure[i][0] for i in range(len(masfigure))])
# masfigurey = array('i', [masfigure[i][1] for i in range(len(masfigure))])
# if masfigurex.count(0) != -1:


# n, m, c = map(int, input().split())
# cart = [[0 for a in range(m)] for i in range(n)]
# gor = n
# ver = m
# res = 0
# masfigure = [list(map(int, input().split())) for i in range(c)]
# for i in range(c):
#     for a in range(2):
#         masfigure[i][a] -= 1
# masfigurex = [masfigure[i][0] for i in range(c)]
# masfigurey = [masfigure[i][1] for i in range(c)]
# for i in masfigure:
#     cart[i[0]][i[1]] = 3
# if masfigurey.count(0) != 0:
#     peref = masfigurey.index(0)
#     gor = masfigurex[peref]
# if masfigurex.count(0) != 0:
#     peref = masfigurex.index(0)
#     ver = masfigurey[peref]
# for i in range(gor):
#     for a in range(m):
#         if cart[i][a] == 3:
#             break
#         cart[i][a] = 1
# for i in range(ver):
#     for a in range(n):
#         if cart[a][i] == 3:
#             break
#         cart[a][i] = 1
# for i in range(len(cart)):
# #    print(cart[i])
#     res += cart[i].count(1)
# print(res - 1)

# n = int(input())
# mas = list(map(int, input().split()))
# a = []
# for i in range(n - 1):
#     if mas[i] < mas[i + 1]:
#         a.append(mas[i])
#     else:
#         a.append(mas[i + 1])
# print(sum(a) + mas[0] + mas[len(mas) - 1])

# for i in range(1, n - 1):
#     if mas[i - 1] < mas[i]:
#         mas[i] = max(mas[i - 1], mas[i + 1])
# c = list(set(mas))
# c.sort(reverse = True)
# if len(c) == 1:
#     print(sum(mas) + c[0])
# else:
#     print(sum(mas) + c[1])


# n, m, c = map(int, input().split())
# cart = [[0 for a in range(m)] for i in range(n)]
# gor = n
# ver = m
# res = 0
# masfigure = [list(map(int, input().split())) for i in range(c)]
# masfigurex = [masfigure[i][0] for i in range(c)]
# masfigurey = [masfigure[i][1] for i in range(c)]
# for i in masfigure:
#     cart[i[0]][i[1]] = 3
# if masfigurey.count(0) != 0:
#     peref = masfigurey.index(0)
#     gor = masfigurex[peref]
# if masfigurex.count(0) != 0:
#     peref = masfigurex.index(0)
#     ver = masfigurey[peref]
# for i in range(gor):
#     for a in range(n):
#         if cart[i][a] == 3:
#             break
#         cart[i][a] = 1
# for i in range(ver):
#     for a in range(m):
#         if cart[a][i] == 3:
#             break
#         cart[a][i] = 1
# for i in range(len(cart)):
#     print(cart[i])
#     res += cart[i].count(0)
# print(res - 1)


# def rizsum(mas1, mas2):
#     return sum(mas1) - sum(mas2)
# mas1 = list(map(int, input("Введіть дані 10 А класу ").split()))
# mas2 = list(map(int, input("Введіть дані 10 Б класу ").split()))
#
# peref = rizsum(mas1, mas2)
# if peref > 0:
#     print(peref, "в користь 10 А")
# elif peref < 0:
#     print(abs(peref), "в користь 10 В")
# else:
#     print("нічія")

# def firstvuras(mas):
#     return mas[0] * mas[1]
# def second(mas):
#     res = 1
#     for i in range(len(mas)):
#         res *= mas[i]
#     return res
#
# mas1 = list(map(int, input("введіть 1 список ").split())- ", ser(mas, n))

# n = 3
# diapazon = [3, 8]
# def vuras(diapazon):
#     mas = []
#     res = 0
#     for i in range(n):
#         res += (random.randint(diapazon[0], diapazon[1])) ** 2
#     return res
# print(vuras(diapazon))

# def vuras(mas):
#     return mas[0] * mas[1] - mas[2] / mas[3]
# mas = [3, 5, 2, 7]
# cor = (4, 1, 5, 6)
# print(vuras(mas))
# print(vuras(cor))

# n = 5
# mas = [1, 6]
#
# def everange(mas, n):
#     res = []
#     for i in range(n):
#         res.append(random.randint(mas[0], mas[1]))
#     return round(sum(res) / len(res), 3)
#
# print(everange(mas, n))

# start, endway = input().split()
# letter = 'abcdefgh'
# number = '12345678'
# graph = dict()
# for i in letter:
#     for a in number:
#         graph[i + a] = set()
# lenlet = len(letter)
# for i in range(8):
#     for a in range(8):
#         v1 = letter[i] + number[a]
#         if 0 <= i + 2 < lenlet and 0 <= a + 1 < lenlet:
#             v2 = letter[i + 2] + number[a + 1]
#             graph[v1].add(v2)
#             graph[v2].add(v1)
#         if 0 <= i + 1 < lenlet and 0 <= a + 2 < lenlet:
#             v2 = letter[i + 1] + number[a + 2]
#             graph[v1].add(v2)
#             graph[v2].add(v1)
#         if 0 <= i - 2 < lenlet and 0 <= a + 1 < lenlet:
#             v2 = letter[i - 2] + number[a + 1]
#             graph[v1].add(v2)
#             graph[v2].add(v1)
#         if 0 <= i + 2 < lenlet and 0 <= a - 1 < lenlet:
#             v2 = letter[i + 2] + number[a - 1]
#             graph[v1].add(v2)
#             graph[v2].add(v1)
#         if 0 <= i - 2 < lenlet and 0 <= a - 1 < lenlet:
#             v2 = letter[i - 2] + number[a - 1]
#             graph[v1].add(v2)
#             graph[v2].add(v1)
#         if 0 <= i - 1 < lenlet and 0 <= a - 2 < lenlet:
#             v2 = letter[i - 1] + number[a - 2]
#             graph[v1].add(v2)
#             graph[v2].add(v1)
#         if 0 <= i + 1 < lenlet and 0 <= a - 2 < lenlet:
#             v2 = letter[i + 1] + number[a - 2]
#             graph[v1].add(v2)
#             graph[v2].add(v1)
#         if 0 <= i - 1 < lenlet and 0 <= a + 2 < lenlet:
#             v2 = letter[i - 1] + number[a + 2]
#             graph[v1].add(v2)
#             graph[v2].add(v1)
#
# distance = {i: None for i in graph}
# check = [start]
# distance[start] = 0
# perents = {i: None for i in graph}
#
# while check:
#     deleten = check.pop(0)
#     for a in graph[deleten]:
#         if distance[a] is None:
#             distance[a] = distance[deleten] + 1
#             perents[a] = deleten
#             check.append(a)
#
# perent = perents[endway]
# way = [endway]
# while not perent is None:
#     way.append(perent)
#     perent = perents[perent]
# print(way[::-1])

# k1 = k2 = int(input())
# mas = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
# max1, min1 = 0, 0
# if k1 % 2 == 0:
#     max1 = '1' * (k1 // 2)
# else:
#     max1 = '7' + ('1' * (k1 // 2 - 1))
# if k1 < len(mas):
#     print(mas.index(k1), max1)
#     exit()
# dil7 = k2 % 7
# if dil7 == 0:
#     min1 = '8' * (k2 // 7)
# elif dil7 == 1:
#     min1 = '10' + str('8' * (k2 // 7 - 1))
# elif dil7 == 2:
#     min1 = '18' + str('8' * (k2 // 7 - 1))
# elif dil7 == 3:
#     min1 = 0
# elif dil7 == 4:
#     min1 = '20' + str('8' * (k2 // 7 - 1))
# elif dil7 == 5:
#     min1 = '28' + str('8' * (k2 // 7 - 1))
# else:
#     min1 = '68' + str('8' * (k2 // 7 - 1))
# print(min1, max1)

# m, n = map(int, input().split())
# v = []
# a = [[0] * n for i in range(n)]
# for i in range(m):
#     v1, v2 = input().split()
#     for c in v1, v2:
#         if c not in v:
#             v.append(c)
#     c1 = v.index(v1)
#     c2 = v.index(v2)
#     a[c1][c2] = 1
#     a[c2][c1] = 1
# for i in range(len(a)):
#     print(*a[i])

# уровень вершины 2

# n = int(input())
# mas = []
# for i in range(n):
#     mas.append(list(map(int, input().split())))
# peref1 = 0
# res = []
# for i in range(1, n):
#    peref1 = 0
#    for a in range(i, n):
#        res.append(mas[a][n - peref1 - 1])
#        peref1 += 1
# print(max(res))#len(mas) - mas[::-1].index(mas) - 1

# n = int(input())
# mas = [list(map(int, input().split())) for i in range(n)]
# peref = 0
# peref1 = 0
# res = []
# for i in range(1, n):
#     peref1 = 0
#     for a in range(i, n):
#         res.append(mas[a][n - peref1 - 1])
#         peref1 += 1
#     peref += 1
# print(max(res))

# n = int(input())
# mas = []
# res = []
# for c in range(n):
#     mas.append(list(map(int, input().split())))
# for i in range(n - 1, -1, -1):
#     for a in range(n - i, n, 1):
#         print(a, n - i - 1, i, mas[a][n - i - 1])
#         res.append(mas[a][n - i - 1])
# print(mas[0][0])
# print(res)

# n = int(input())
# masperef = []
# for i in range(n):
#    peref = list(map(int, input().split()))ppend([random.uniform(-79, 90) for c in range(m)])
#     for a in range(m):
#         if mas[i][a] > 0:
#             massum += mas[i][a]
#             kil += 1
# print(round(massum / kil, 3))

# n, m = map(int, input().split())
# mas = []
# res = []
# for i in range(n):
#     peref = [random.randint(-100, 100) for a in range(m)]
#     perefmas = []
#     mas.append(peref)
#     for a in range(m):
#         perefmas.append(peref[a] * (-1))
#     res.append(perefmas)
# print(*mas)
# print()
# print(*res)

# n = int(input())
# mas = []
# res = []
# for c in range(n):
#     mas.append(list(map(int, input().split())))
# for i in range(3):
#     a = n - i
#     print(a)
#     for a in range(3):
#         print(a)
#         #print(res)
#         res.append(mas[a][n - i - 1])
#     print()
# print(res)

# n = int(input())
# mas = []
# masperef = []
# for i in range(n):
#     peref = list(map(int, input().split()))
#     mas.append(peref)
#     masperef.append(peref[n - 1 - i])
# print(masperef)

# n, m = map(int, input().split())
# mas = []
# massum = []
# for i in range(n):
#    mas.append(list(map(int, input().split())))
# for i in range(m):
#    peref = 0
#    for a in range(n):
#        peref += mas[a][i]
#    massum.append(peref)
# mini = massum.index(min(massum))
# for i in range(n):
#    print(mas[i][mini], end = ' ')

# n, m = map(int, input().split())
# mas = []
# massum = [[0] for i in range(m)]
# for i in range(n):
#    mas.append(list(map(int, input().split())))
# for i in range(m):
#    peref = 0
#    for a in range(n):
#        peref += mas[a][i]
#    massum[i] = peref
# print(*massum)
# print(max(massum))

# n = int(input())
# mas = []
# max1 = []
# min1 = []
# for i in range(n):
#     mas.append(list(map(int, input().split())))
#     max1.append(max(mas[len(mas) - 1]))
#     min1.append(min(mas[len(mas) - 1]))
# masmin = min1.index(min(min1))
# masmax = max1.index(max(max1))
# perefmin = mas[masmin].index(min(mas[masmin]))
# perefmax = mas[masmax].index(max(mas[masmax]))
# peref = mas[masmin][perefmin]
# mas[masmin][perefmin] = mas[masmax][perefmax]
# mas[masmax][perefmax] = peref
# print(mas)

# n, m = map(int, input().split())
# mas = []
# massum = []
# for i in range(n):
#     mas.append(list(map(int, input().split())))
# for i in range(n):
#     peref = 0
#     for a in range(m):
#         peref += mas[a][i]
#     massum.append(peref)
# maxi = massum.index(max(massum))
# for i in range(n):
#     print(mas[i][maxi], end = ' ')
# print(mas[massum.index(max(massum))])

# n = int(input())
# mas = []
# for i in range(n):
#     mas.append(min(list(map(int, input().split()))))
# print(*mas)
#
# mas = []
# for i in range(10):
#     mas.append(random.randint(4, 11))
# print(*mas)

# n = int(input())
# mas = []
# for i in range(n):
#     mas.append(sum(list(map(int, input().split()))))
# print(min(mas))

# mas = []
# n = int(input())
# for i in range(n):
#     mas.append(list(map(int, input().split())))
# res = 0
# for i in range(n):
#     for a in range(len(mas[i])):
#         res += mas[i][a]
# print(res)

# n = int(input())
# kil = 10 ** (n - 1)
# res = 0
# peref = 0
# for i in range(kil, kil * 10 - 1):
#     mas = list(map(int, list(str(i))))
#     chyslo = 1
#     if mas[1] == 0:
#         res += 9
#     for a in range(len(mas)):
#         peref = (10 - mas[a])
#         if a == 0:
#             chyslo *= peref - 1
#         else:
#             chyslo *= peref
#     res += chyslo
# mines = 0
# for i in range(2, len(str(kil))+1):
#     mines += 9 ** (i)
# print(res - mines)

# kil = 1000
# res = 0
# peref = 0
# for i in range(kil, kil * 10 - 1):
#     mas1 = list(map(int, list(str(i))))
#     for a in range(kil, kil * 10 - 1):
#         mas2 = list(map(int, list(str(a))))
#         if mas1[0] + mas2[0] < 10 and mas1[1] + mas2[1] < 10 and mas1[2] + mas2[2] < 10 and mas1[3] + mas2[3] < 10:
#             res += 1
#             print(mas1, mas2)
# print(res)

# kil = 100
# res = 0
# peref = 0
# for i in range(kil, kil * 10 - 1):
#     mas1 = list(map(int, list(str(i))))
#     for a in range(kil, kil * 10 - 1):
#         mas2 = list(map(int, list(str(a))))
#         if mas1[0] + mas2[0] < 10 and mas1[1] + mas2[1] < 10 and mas1[2] + mas2[2] < 10:
#             res += 1
#             print(mas1, mas2)
# print(res)

# mas = [2, 1]
# peref = 0
# res = 0
# maschyslo = []
# chyslo = 1
# for a in range(len(mas)):
#     peref = (10 - mas[a])
#     maschyslo.append(peref)
#     chyslo *= peref
# res += chyslo
# print(res-1)

# n = int(input())
# res = 0
# while n != 1:
#     if n == 2:
#         res += 1
#         n -= 1
#     elif n % 3 != 0:
#         if n % 3 == 1:
#             n -= 1
#             res += 1
#         else:
#             n += 1
#             res += ange(len(mas)-1):
#     if mas[i] == mas[i + 1]:
#         mas.sort()
#         for i in range(len(mas) - 2):
#             if mas[i] == mas[i + 1] == mas[i + 2]:
#                 print("Yes")
#                 exit()
#         break
# print("No")

# n = int(input())
# x = []
# y = []
# for i in range(n):
#     mas = input().split(" ")
#     if i % 2 == 0:
#         x.append(mas[i])
#     else:
#         y.append(mas[i])
# for i in range(len(x)*2-3):

# s = list(map(str, input().split()))
# for i in range(len(s)):
#     peref = s[i].find("a")
#     if peref != -1:
#         s[i] = "о"
# a = s.replace("a", "")
# print(a)

# a = list(input())
# b = list(input())
# c = list(input())
# a1 = set(a)
# b1 = set(b)
# c1 = set(c)
# for i in range(len(a)):
#     if a[i] not in b1 and a[i] not in c1:
#         print(a[i], end=" ")
# for i in range(len(b)):
#     if b[i] not in a1 and b[i] not in c1:
#         print(b[i], end=" ")
# for i in range(len(c)):
#     if c[i] not in b1 and c[i] not in a1:
#         print(c[i], end=" ")

# n1 = list(input())
# n2 = set(n1)
# res = []
# for i in range(len(n1)):
#     if n1[i] in n2:
#         n2.discard(n1[i])
#     else:
#         res.append(n1[i])
# print(*res)

# n1 = set(input())
# print(len(n1))

# n1 = list(input())
# peref = 0
# res = 0
# for i in range(len(n1)):
#     peref = n1.count(n1[i])
#     if peref > 1:
#         if n1[i] == n1[i-1] or n1[i] == n1[i+1]:
#             res += 1
# print(res)

# s = list(input())
# res = 0
# peref = 1
# per = 0
# for i in range(1, len(s)):
#     if s[i] == " " and s[i] == s[i - 1]:
#         per += 1
#         peref += 1
#     elif s[i] != " ":
#         if peref > res:
#             res = peref
# if per == 0:
#     print(0)
# else:
#     print(res)


# n = int(input())
# mas = list(map(int, input().split()))
# peref1 = 0
# if mas == sorted(mas):
#     print(0)
# else:
#     peref1 = 0
#     while True:
#         i = mas.index(min(mas))
#         if peref1 <= i:
#             mas.pop(i)
#             peref1 = i
#         else:
#             break
#     print(len(mas))

# mas = []
# mas.append(list(map(int, input().split())))
# mas.append(list(map(int, input().split())))
# mas.append(list(map(int, input().split())))
# print(min(mas[0]), min(mas[1]), min(mas[2]))

# mas = []
# n = 10
# for i in range(n):
#     mas.append(random.randint(4, 11))
# print(mas)

# mas = [(9, 5), (9, 6)]
# x = 0
# y = 0
# mas.append((x, y))
# print(mas)


# n = int(input())
# mas1 = list(map(int, input().split()))
# while True:
#     if len(mas1) < n:
#         mas1.append(int(input()))
#     else:
#         break
# mas2 = []
# for i in range(n):
#     mas2.append(mas1[i] % 10)
# for i in range(n):
#     for a in range(1, n):
#         if mas2[a-1] > mas2[a]:
#             per1 = mas2[a-1]
#             mas2[a-1] = mas2[a]
#             mas2[a] = per1
#             per2 = mas1[a-1]
#             mas1[a-1] = mas1[a]
#             mas1[a] = per2
#         elif mas2[a-1] == mas2[a] and mas1[a-1] > mas1[a]:
#             per2 = mas1[a-1]
#             mas1[a-1] = mas1[a]
#             mas1[a] = per2
# print(*mas1)

# n = int(input())
# peref = 1
# res = 1
# for i in range(1, n):
#     res = (peref * 8) + (10 ** i)
#     peref += res
# print(res)


# a, b, c = map(int, input().split())
# if a + b < c:
#     print((a + b) * 2)
# elif a + c < b:
#     print((a + c) * 2)
# elif c + b < a:
#     print((b + c) * 2)
# else:
#     print(a + b + c)


# a, b = map(int, input().split())
# if a % 2 == 0 and b % 2 == 0:
#     print(1)
# elif a % 2 != 0 and b % 2 != 0:
#     print(1)
# else:
#     print(0)

# mas = list(input())
# max = list(sorted(mas, reverse = True))
# min = list(sorted(mas, reverse = False))
# if min[0] == '0':
#     a = 0
#     while min[a] == '0':
#         a += 1
#     else:
#         min.insert(0, min[a])
#         min.pop(a+1)
# maxstr = max[0] + max[1] + max[2]
# minstr = min[0] + min[1] + min[2]
# res = int(maxstr) + int(minstr)
# print(res)


# mas = list(map(int, input().split()))
# mas.sort(reverse = True)
# print(mas[0] + mas[2])

# n = int(input())
# balans = list(map(int, input().split()))
# res = 0
# z = 0#в кого зараз др
# for i in range(n):
#     for a in range(i):
#         maxindex = balans.index(max(balans))
#         balans[maxindex] -= 1
#         balans[z] += 1
#     for a in range(len(balans)):
#         if a == z:
#             continue
#         balans[a] -= 1
#         balans[z] += 1
#         if balans[a] < 0:
#             res += abs(balans[a])
#             balans[a] = 0
#     z += 1
#     if z == 4:
#         z = 0
# print(res)

# n = int(input())
# mas = list(map(int, input().split()))
# x, y = list(map(int, input().split()))
# noparmas = 0
# fo  print(res + n3 * 30 + n4 * 2)

# mas = list(map(int, input().split()))
# t1 = mas[0] * 60 + mas[1]
# t2 = mas[2] * 60 + mas[3]
# t3 = mas[4] * 60 + mas[5]
# t4 = mas[6] * 60 + mas[7]
# res = 0
# if t3 < t2 and t2 > t4:
#     print("yes")
# else:
#     print("no")

# n > len(mas) or

# n = int(input())
# mas = list(map(int, input().split()))
# x, y = list(map(int, input().split()))
# noparmas = 0
# for i in range(len(mas)):
#     if mas[i] % 2 != 0:
#         noparmas+=1
# kilpar = len(mas) - noparmas
# if n > len(mas) or noparmas < y or kilpar + (y - noparmas)//2 < x:
#     print("no")
# else:
#     print("yes")


# mas = list(map(int, input().split()))
# a = mas[0]; b = mas[1]; c = mas[2]; d = mas[3]; n = mas[4]; k = mas[5]
# peref = 0
# res = n
# if a/c > b/d:
#     a1 = b
#     c1 = d
# else:
#     a1 = a
#     c1 = c
# for i in range(k):
#     res += int(res * c1/a1)
# print(res)

# mas = list(map(int, input().split()))
# t1 = mas[0] * 60 + mas[1]
# t2 = mas[2] * 60 + mas[3]
# t3 = mas[4] * 60 + mas[5]
# t4 = mas[6] * 60 + mas[7]
# t5 = mas[8] * 60 + mas[9]
# res = 0
# if t1 < t5 < t2:
#     res += 1
# if t3 < t5 < t4:
#     res += 1
# print(res)

# n = int(input())
# print((n+1) * (n+1))

# mas = list(map(int, input().split()))
# print(((mas[1]-1) * (mas[0]-1)+1))

# n = int(input())
#
# mas = []
# for i in range(n):
#     per = []
#     for a in range(n):
#         per.append(0)
#     mas.append(per)
# for i in range(2):
#     if i == 0:
#         peref = [1, n - 1]
#     else:
#         peref = [1-1, n - 1 - 2]
#     while peref[0] <= n - 1:
#         mas[peref[0]][peref[1]] = 1
#         peref[0] += 2
#         peref[1] -= 1
# for i in range(n):
#     print(*mas[i])
