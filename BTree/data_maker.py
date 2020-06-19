import random

f = open('input.txt', 'w')
n = 100000
data_list = []
for i in range(n):
    temp = random.randint(1, 2 * n)
    while temp in data_list:
        temp = random.randint(1, 2 * n)
    data_list.append(temp)

for data in data_list:
    f.write(str(data) + '\n')

f.close()
