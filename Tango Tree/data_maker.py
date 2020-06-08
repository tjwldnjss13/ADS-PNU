import random

k = 5
n = k * 2 * (10 ** 4)

fn = 'input' + str(k) + '.txt'
f = open(fn, 'w')
num_list = []
for i in range(n):
    num = random.randint(1, 2 * n)
    while num in num_list:
        num = random.randint(1, 2 * n)
    num_list.append(num)

for num in num_list:
    f.write(str(num) + '\n')
f.close()
