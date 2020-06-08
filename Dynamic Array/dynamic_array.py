import math
import random

cost_F = 0
insert_cost = 0
search_cost = 0

class DynamicArray:
    def __init__(self):
        self.heads = []
        self.N_key = 0
        self.size = 0

    def set_size(self):
        pre_size = self.size
        self.size = math.floor(math.log2(self.N_key)) + 1

        if self.size == pre_size + 1:
            self.heads.append([])

    def search(self, key):
        global search_cost

        for i in range(self.size):
            if len(self.heads[i]) is 0:
                continue
            if key >= self.heads[i][0]:
                sub_arr = self.heads[i]
                for j in range(len(sub_arr)):
                    if cost_F is True:
                        search_cost += 1
                    if key is sub_arr[j]:
                        return not None
        return None

    def insert(self, key):
        global insert_cost

        # Check duplicated
        if self.search(key) is not None:
            print('{} duplicated :('.format(key))
            return

        # Case of first insertion
        if len(self.heads) == 0:
            self.heads.append([key])
            self.N_key += 1
            self.set_size()

            insert_cost += 1
        # Case when the first sub-array is empty
        elif len(self.heads[0]) == 0:
            self.heads[0].append(key)
            self.N_key += 1
            self.set_size()

            insert_cost += 1
        # Case when the first sub-array is full
        else:
            head_idx = 0
            while head_idx < self.size:
                if head_idx == 0:
                    arr = [key]
                    self.N_key += 1
                    self.set_size()
                else:
                    arr = self.heads[head_idx - 1]
                    self.heads[head_idx - 1] = []

                if len(self.heads[head_idx]) == 0:
                    self.heads[head_idx] = arr

                    insert_cost += len(arr)
                    return
                else:
                    for m in range(len(arr)):
                        for n in range(len(self.heads[head_idx])):
                            if 0 <= n < len(self.heads[head_idx]) - 1:
                                if n == 0:
                                    if arr[m] < self.heads[head_idx][n]:
                                        self.heads[head_idx].insert(0, arr[m])

                                        insert_cost += 1
                                        break
                                else:
                                    if self.heads[head_idx][n] < arr[m] < self.heads[head_idx][n + 1]:
                                        self.heads[head_idx].insert(n + 1, arr[m])

                                        insert_cost += 1
                                        break
                            else:
                                if self.heads[head_idx][n] < arr[m]:
                                    self.heads[head_idx].append(arr[m])

                                    insert_cost += 1
                                    break
                if len(self.heads[head_idx]) is pow(2, head_idx):
                    return
                head_idx += 1

    @staticmethod
    def print_da(da):
        for i in range(da.size):
            print(da.heads[i])


if __name__ == '__main__':
    da = DynamicArray()

    insert_cost = 0

    fn = 'data_insert.txt'
    f = open(fn, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        da.insert(int(line))

    print('Insert cost : {}'.format(insert_cost))
    print('Search cost : {}'.format(search_cost))

    # cost_F = True
    #
    # fn = 'data_search.txt'
    # f = open(fn, 'r')
    # lines = f.readlines()
    # f.close()
    # for line in lines:
    #     da.search(int(line))
    #
    # print('Search cost : {}'.format(search_cost))
