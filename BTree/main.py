from btree import *
import random
import time
import matplotlib.pyplot as plt

fn = 'input.txt'
f = open(fn, 'r')
datas = f.readlines()
f.close()
N_data_list = []
for i in range(len(datas)):
    N_data_list.append(i + 1)
    datas[i] = int(datas[i])

_23tree, _234tree = BTree(3), BTree(4)

print('Inserting...')

_23_insert_time = []
start = time.time()
for data in datas:
    _23tree.insert(data)
    mid = time.time()
    _23_insert_time.append(mid - start)

_234_insert_time = []
start = time.time()
for data in datas:
    _234tree.insert(data)
    mid = time.time()
    _234_insert_time.append(mid - start)

print('Inserting done')

print('Searching...')

_23_search_time = []
start = time.time()
for i in range(len(datas)):
    data_search = random.randint(1, len(datas))
    _23tree.search(data_search)
    mid = time.time()
    _23_search_time.append(mid - start)

_234_search_time = []
start = time.time()
for i in range(len(datas)):
    data_search = random.randint(1, len(datas))
    _234tree.search(data_search)
    mid = time.time()
    _234_search_time.append(mid - start)

print('Searching done')

print('Deleting...')

_23_delete_time = []
start = time.time()
for i in range(len(datas) / 2):
    _23tree.delete(datas[-1])
    mid = time.time()
    _23_delete_time.append(mid - start)

N_delete_list = []
_234_delete_time = []
start = time.time()
for i in range(len(datas) / 2):
    _234tree.delete(datas[-1])
    mid = time.time()
    _234_delete_time.append(mid - start)
    N_delete_list.append(i + 1)

print('Deleting done')

print('[Insertion]')
print('23 Tree  : {}'.format(_23_insert_time[-1]))
print('234 Tree : {}'.format(_234_insert_time[-1]))

print('\n[Search]')
print('23 Tree  : {}'.format(_23_search_time[-1]))
print('234 Tree : {}'.format(_234_search_time[-1]))

print('\n[Deletion]')
print('23 Tree  : {}'.format(_23_delete_time[-1]))
print('234 Tree : {}'.format(_234_delete_time[-1]))

plt.figure(0)
plt.plot(N_data_list, _23_insert_time, 'r-', label='23 Tree')
plt.plot(N_data_list, _234_insert_time, 'b:', label='234 Tree')
plt.title('Insert time')
plt.legend()

plt.figure(1)
plt.plot(N_data_list, _23_search_time, 'r-', label='23 Tree')
plt.plot(N_data_list, _234_search_time, 'b:', label='234 Tree')
plt.title('Search time')
plt.legend()

plt.figure(2)
plt.plot(N_delete_list, _23_delete_time, 'r-', label='23 Tree')
plt.plot(N_delete_list, _234_delete_time, 'b:', label='234 Tree')
plt.title('Insert time')
plt.legend()

plt.show()
