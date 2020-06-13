
a_list = [[3, 2, 1], [1, 2, 3], [2, 4, 4], [1, 2, 3]]

for i in range(len(a_list) - 1):
    if a_list[i] in a_list[i + 1:]:
        a_list.pop(i)

print(a_list)