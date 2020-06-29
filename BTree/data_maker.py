import random

f = open('input1.txt', 'w')
n = 100000
data_list = []
for i in range(n):
    print(i + 1)
    temp = random.randint(1, 100 * n)
    while temp in data_list:
        temp = random.randint(1, 100 * n)
    data_list.append(temp)

for data in data_list:
    f.write(str(data) + '\n')

f.close()
