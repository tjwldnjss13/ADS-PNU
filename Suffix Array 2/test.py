
a_list = [[2, 1, 1, 2, 4], [2, 1, 1, 1], [2, 1, 1, 3, 5]]

for i in range(len(a_list) - 1):
    if a_list[i] in a_list[i + 1:]:
        a_list.pop(i)

a_list.sort()

print(a_list)