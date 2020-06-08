import treap as tp
import binary_search_tree as bst
import heap as hp
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
    bst1 = bst.BST()
    hp1 = hp.MaxHeap()
    tp1 = tp.Treap()

    fn = 'data_10_6.txt'
    f = open(fn, 'r')
    lines = f.readlines()
    f.close()
    N = len(lines)

    bst_time = np.zeros((2, N))
    hp_time = np.zeros((2, N))
    tp_time = np.zeros((2, N))

    start = time.time()
    for i in range(N):
        bst1.insert(int(lines[i]))
        temp = time.time()
        bst_time[0, i] = i + 1
        bst_time[1, i] = temp - start
    end = time.time()
    bst_insert_time = end - start

    start = time.time()
    for i in range(N):
        bst1.insert(int(lines[i]))
        temp = time.time()
        hp_time[0, i] = i + 1
        hp_time[1, i] = temp - start
    end = time.time()
    hp_insert_time = end - start

    start = time.time()
    for i in range(N):
        bst1.insert(int(lines[i]))
        temp = time.time()
        tp_time[0, i] = i + 1
        tp_time[1, i] = temp - start
    end = time.time()
    tp_insert_time = end - start

    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3)
    ax1.scatter(bst_time[0], bst_time[1], c='red', s=200)
    ax2.scatter(hp_time[0], hp_time[1], c='green', s=200)
    ax3.scatter(tp_time[0], tp_time[1], c='blue', s=200)
    plt.show()
