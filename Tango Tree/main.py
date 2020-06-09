from Tango import *
import random
import matplotlib.pyplot as plt

fn = 'input3.txt'
f = open(fn, 'r')
inputs = f.readlines()
f.close()

# inputs = [51, 21, 7, 532, 24, 651, 174, 34, 724, 12, 512, 192, 4012, 9282, 1982, 32981, 410, 1403, 810, 1480, 6582]

print('Inserting...')
for i in range(len(inputs)):
    inputs[i] = int(inputs[i])

tango = TangoTree(inputs)
# TangoTree.print_tree(tango)

print('Tango Searching...')
total_tango_search_time = 0
for i in range(len(inputs)):
    print('{} / {}'.format(i + 1, len(inputs)))
    num = random.randint(1, len(inputs))
    search_time = tango.tango_search(num)
    total_tango_search_time += search_time

print('Total Tango search time ({}) : {}'.format(len(inputs), total_tango_search_time))

# 20000 : 0.12161612510681152
# 40000 : 0.25716519355773926