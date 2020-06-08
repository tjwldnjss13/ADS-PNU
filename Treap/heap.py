from math import *


class MinHeap:
    def __init__(self):
        self.queue = [None]

    @staticmethod
    def parent(idx):
        return floor(idx / 2)

    def swap(self, idx1, idx2):
        temp = self.queue[idx1]
        self.queue[idx1] = self.queue[idx2]
        self.queue[idx2] = temp

    def insert(self, data):
        self.queue.append(data)
        idx = len(self.queue) - 1
        while idx > 1:
            parent = self.parent(idx)
            if self.queue[idx] < self.queue[parent]:
                self.swap(idx, parent)
                idx = parent
            else:
                break

    def delete(self):
        self.swap(1, -1)
        self.queue.pop(-1)
        idx = 1
        while idx <= len(self.queue) - 1 and idx * 2 + 1 <= len(self.queue) - 1 and idx * 2 + 1 <= len(self.queue) - 1:
            if self.queue[idx] > self.queue[idx * 2 + 1]:
                self.swap(idx, idx * 2 + 1)
                idx = idx * 2 + 1
            elif self.queue[idx] > self.queue[idx * 2]:
                self.swap(idx, idx * 2)
                idx = idx * 2
            else:
                break

    def print_heap_util(self, idx=1):
        if idx * 2 + 1 <= len(self.queue) - 1:
            self.print_heap_util(idx * 2 + 1)
        print('      ' * floor(log2(idx)), end='')
        print(self.queue[idx])
        if idx * 2 <= len(self.queue) - 1:
            self.print_heap_util(idx * 2)

    def print_heap(self):
        self.print_heap_util(1)


class MaxHeap:
    def __init__(self):
        self.queue = [None]

    @staticmethod
    def parent(idx):
        return floor(idx / 2)

    def swap(self, idx1, idx2):
        temp = self.queue[idx1];
        self.queue[idx1] = self.queue[idx2]
        self.queue[idx2] = temp

    def insert(self, data):
        self.queue.append(data)
        idx = len(self.queue) - 1
        while idx > 1:
            parent = self.parent(idx)
            if self.queue[idx] > self.queue[parent]:
                self.swap(idx, parent)
                idx = parent
            else:
                break

    def delete(self):
        self.swap(1, -1)
        self.queue.pop(-1)
        idx = 1
        while idx <= len(self.queue) - 1:
            if idx * 2 <= len(self.queue) - 1 and self.queue[idx] < self.queue[idx * 2]:
                self.swap(idx, idx * 2)
                idx = idx * 2
            elif idx * 2 + 1 <= len(self.queue) - 1 and self.queue[idx] < self.queue[idx * 2 + 1]:
                self.swqp(idx, idx * 2 + 1)
                idx = idx * 2 + 1
            else:
                break

    def print_heap_util(self, idx=1):
        if idx * 2 + 1 <= len(self.queue) - 1:
            self.print_heap_util(idx * 2 + 1)
        print('      ' * floor(log2(idx)), end='')
        print(self.queue[idx])
        if idx * 2 <= len(self.queue) - 1:
            self.print_heap_util(idx * 2)

    def print_heap(self):
        self.print_heap_util(1)


def main():
    h = MaxHeap()

    h.insert(61)
    h.insert(623)
    h.insert(239)
    h.insert(1560)
    h.insert(12)
    h.insert(734)
    h.insert(30)

    h.print_heap()
    print('----------------')

    h.delete()

    h.print_heap()


if __name__ == '__main__':
    main()
