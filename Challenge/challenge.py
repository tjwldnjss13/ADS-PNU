# from BinarySearchTree import *
from RedBlackTree import *
# from BTree import *
# from MergeSort import *
import copy
import time

POINT_DICT = dict()


def read_file(fp):
    f = open(fp, 'r')
    lines = f.readlines()
    f.close()

    return lines


def range_search(range_tree_x, pnt_center, radius):
    x_min, x_max = pnt_center[0] - radius, pnt_center[0] + radius
    y_min, y_max = pnt_center[1] - radius, pnt_center[1] + radius

    range_x, range_y = (x_min, x_max), (y_min, y_max)

    nodes = find_nodes_in_range(range_tree_x, (range_x, range_y))
    idxs, pnts = [], []
    for node_i in range(len(nodes)):
        idxs.append(nodes[node_i].index)
        pnts.append(nodes[node_i].pnt)

    max_dist_i = -1
    max_dist_sq = -1
    max_i_list = []
    i = 0
    while i < len(pnts):
        dist_sq = (pnts[i][0] - pnt_center[0]) ** 2 + (pnts[i][1] - pnt_center[1]) ** 2
        if dist_sq > radius ** 2:
            idxs.pop(i)
            pnts.pop(i)
            continue
        if max_dist_i == -1 or dist_sq >= max_dist_sq:
            max_dist_i = idxs[i]
            if dist_sq > max_dist_sq:
                max_dist_sq = dist_sq
                max_i_list = []
            max_i_list.append(max_dist_i)
        i += 1

    return idxs, pnts, max_i_list


def find_nodes_in_range(range_tree, ranges, xy_idx=0):
    range = ranges[xy_idx]
    nodes = []

    # find nodes in range of x
    cur = range_tree.root
    if cur is None:
        return []
    splitv = None
    while cur is not None:
        if cur.pnt[xy_idx] < range[0]:
            cur = cur.right
        elif cur.pnt[xy_idx] > range[1]:
            cur = cur.left
        else:
            splitv = cur
            break
    if splitv is None:
        return []
    nodes.append(splitv)
    t_l, t_r = splitv.left, splitv.right
    while t_l is not None:
        if t_l.pnt[xy_idx] < range[0]:
            t_l = t_l.right
        elif t_l.pnt[xy_idx] >= range[0]:
            nodes.append(t_l)
            nodes_subtree = get_nodes_in_subtree(t_l.right, [])
            nodes += nodes_subtree
            if t_l.pnt[xy_idx] == range[0]:
                break
            else:
                t_l = t_l.left
    while t_r is not None:
        if t_r.pnt[xy_idx] > range[1]:
            t_r = t_r.left
        elif t_r.pnt[xy_idx] <= range[1]:
            nodes.append(t_r)
            nodes_subtree = get_nodes_in_subtree(t_r.left, [])
            nodes += nodes_subtree
            if t_r.pnt[xy_idx] == range[1]:
                break
            else:
                t_r = t_r.right

    # Make range tree of y
    if xy_idx == 0:
        range_tree_y = make_range_tree_y(nodes)
        # range_tree_y.print_tree()
        return find_nodes_in_range(range_tree_y, ranges, 1)

    return nodes


def make_range_tree_y(nodes):
    range_tree_y = RedBlackTreePnt(1)
    for node in nodes:
        range_tree_y.insert(node.index, node.pnt)

    return range_tree_y


def get_nodes_in_subtree(cur, nodes):
    if cur is None:
        return []
    if cur.right is not None:
        get_nodes_in_subtree(cur.right, nodes)
    nodes.append(cur)
    if cur.left is not None:
        get_nodes_in_subtree(cur.left, nodes)
    return nodes


def main():
    range_tree_x = RedBlackTreePnt(0)

    fp_in = 'input.txt'
    pin = read_file(fp_in)

    fp_out = 'output.txt'
    pout = open(fp_out, 'w')

    n = len(pin)
    n_i = 1
    N_insert, N_delete, N_query = 0, 0, 0

    start = time.time()
    for query in pin:
        print('{} / {}'.format(n_i, n))
        n_i += 1
        q = query.split()

        if q[0] == '+':
            N_insert += 1
            index, pnt = int(q[1]), (int(q[2]), int(q[3]))
            POINT_DICT[index] = pnt
            range_tree_x.insert(index, POINT_DICT[index])
        elif q[0] == '-':
            N_delete += 1
            index = int(q[1])
            if index in POINT_DICT.keys():
                range_tree_x.delete(POINT_DICT[index])
                del POINT_DICT[index]
        elif q[0] == '?':
            N_query += 1
            pnt, r = (int(q[1]), int(q[2])), int(q[3])

            idxs, pnts, max_i_list = range_search(range_tree_x, pnt, r)
            pout.write(str(len(pnts)))
            if len(pnts) != 0:
                pout.write(' ' + str(min(max_i_list)))
            pout.write('\n')
        # range_tree_x.print_tree()
        # print('-----------------------------------------------------')

    range_tree_x.print_tree()

    end = time.time()
    pout.close()
    print('{} sec\n'.format(end - start))
    print('{} / {} insertion'.format(N_insert, n))
    print('{} / {} deletion'.format(N_delete, n))
    print('{} / {} query\n'.format(N_query, n))

    correct_fp = 'pout_2.txt'
    correct_f = open(correct_fp, 'r')
    correct_lines = correct_f.readlines()
    correct_f.close()
    my_fp = 'output.txt'
    my_f = open(my_fp, 'r')
    my_lines = my_f.readlines()
    my_f.close()

    N_out = 0
    N_acc = 0
    for i in range(len(my_lines)):
        if correct_lines[i] == my_lines[i]:
            N_acc += 1
        N_out += 1

    print('Correct : {} / {}'.format(N_acc, N_out))




if __name__ == '__main__':
    main()
