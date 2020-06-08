import random

fn1 = 'data_insert.txt'
fn2 = 'data_search.txt'

f = open(fn1, 'w')
for i in range(1, 100001):
    f.write(str(i) + '\n')
f.close()

f = open(fn2, 'w')
l2 = []
for i in range(70000):
    num = random.randint(1, 100000)
    while num in l2:
        num = random.randint(1, 100000)
    l2.append(num)

for n in l2:
    f.write(str(n) + '\n')

l3 = []
for i in range(30000):
    num = random.randint(100001, 200000)
    while num in l3:
        num = random.randint(100001, 200000)
    l3.append(num)

for n in l3:
    f.write(str(n) + '\n')

f.close()
