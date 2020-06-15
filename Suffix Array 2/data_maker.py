import random

f = open('input_long.txt', 'w')
for i in range(1000000):
    num = random.randint(1, 4)
    if num == 1:
        f.write('a')
    elif num == 2:
        f.write('c')
    elif num == 3:
        f.write('g')
    elif num == 4:
        f.write('t')

f.write('$')
f.close()