from btree import *
import random

fn = './input1.txt'
f = open(fn, 'r')
data_list = f.readlines()
for i in range(len(data_list)):
    data_list[i] = int(data_list[i])

tree = BTree(3)
for data in data_list:
    print('[Insert {}]'.format(data))
    tree.insert(data)
    # if tree.search(data) is None:
        # print('Something is wrong....')
    # BTree.print_tree(tree)
    # print('----------------------------------')

BTree.print_tree(tree)

print('---------------------------------------')

del_cnt = 0
for del_i in range(int(len(data_list))):
# for del_i in range(50):
    data_del = data_list[del_i]
    print('[Delete {}]'.format(data_del))
    if data_del == 95:
        BTree.print_tree(tree)
    tree.delete(data_del)
    # BTree.print_tree(tree)
    del_cnt += 1
    # print('-----------------------------------')

print('Total insertion : {}'.format(len(data_list)))
print('Total deletion : {}'.format(del_cnt))
print('Duplicated data (insertion denied) : {}'.format(tree.N_dup))
print('# of nodes : {}'.format(tree.N_key))

BTree.print_tree(tree)
print('Done')
