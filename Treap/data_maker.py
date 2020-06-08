import random

n = 1000000
fn = 'data_10_6.txt'
f = open(fn, 'w')
for i in range(n):
    f.write(str(random.randint(1, n)) + '\n')
f.close()
