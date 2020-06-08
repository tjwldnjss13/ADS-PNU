
from random import *

seed()

fn = 'dataI_10_8.txt'
f = open(fn, 'w')
for i in range(10000000):
    f.write(str(int(uniform(1, 10000000))) + '\n')

f.close()
