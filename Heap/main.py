from binomial_heap import *
from time import *

# Declare heap object
heap = BinomialHeap()

# Read data file
fn = 'dataI_10_8.txt'
f = open(fn, 'r')
lines = f.readlines()
f.close()

# Insert all datas
start = time()
for line in lines:
    heap.insert(float(line))
heap.insert(int(line[0]) + 1)
end = time()
print('Insert {} data : {} sec'.format(heap.total_node, end - start))

total = heap.total_node

# Decrease key
# cur = heap.trees[-1]
# while cur.child is not None:
#     cur = cur.child
# start = time()
# for i in range(total):
#     heap.decrease_key(cur, cur.key - 1)
# end = time()
# print('Decrease key {} times (last tree\'s deepest child) : {} sec'.format(total, end - start))

# Delete minimum data
total = heap.total_node

# for i in range(1, total + 1):
# start = time()
# _, min_node = heap.find_min()
# min = min_node.key
# heap.delete_min()
# end = time()
# print('Delete minimum data {} times : {} sec'.format(total, end - start))