import copy
import math


def build_suffix_array(T, recur_f=False, recur_level=0, print_f=True):
    if not recur_f:
        reduced_T = reduced_str_dna(T, print_f)
    else:
        reduced_T = T

    s0, s1, s2 = s_012(reduced_T, recur_level, print_f)
    s12, s12_reduced_str, dup_f = merge_s12(s1, s2, recur_level, print_f)

    if dup_f:
        s12_reduced_str = build_suffix_array(s12_reduced_str, True, recur_level + 1, print_f)

    s1_rank, s2_rank = s12_reduced_str[:len(s1)], s12_reduced_str[len(s1):]

    if print_f:
        print('    ' * recur_level, end='')
        print('[4] Sort S0')

    for i in range(len(s1)):
        if i < len(s2):
            s1[i].append(s2_rank[i])

    for i in range(len(s0)):
        if i < len(s1):
            s0[i].append(s1_rank[i])
            if i < len(s2):
                s0[i].append(s2_rank[i])

    s_full = []
    s0_i, s1_i, s2_i = 0, 0, 0
    for i in range(len(reduced_T)):
        if i % 3 == 0:
            s_full.append(s0[s0_i])
            s0_i += 1
        elif i % 3 == 1:
            s_full.append(s1[s1_i])
            s1_i += 1
        else:
            s_full.append(s2[s2_i])
            s2_i += 1

    s_idx = []
    for i in range(len(reduced_T)):
        s_idx.append(i)

    if print_f:
        print('    ' * recur_level, end='')
        print('[5] Merge S0 & S12')

    merge_sort(s_full, s_idx, 0, len(s_full) - 1)
    for s in s_full:
        while len(s) > 3:
            s.pop(-1)

    s_rank = []
    for i in range(len(s_idx)):
        s_rank.append(0)

    rank_i = 0
    for i in s_idx:
        s_rank[i] = rank_i
        rank_i += 1

    s_rank_str = []
    for rank in s_rank:
        s_rank_str.append(rank)

    if print_f:
        print('    ' * recur_level, end='')
        print('    S reduced string : ', end='')
        print(s_rank)

    if recur_f:
        return s_rank_str

    if print_f:
        print('[6] Make suffix array')

    suffix_array = []
    sa_i = 0
    while sa_i < len(s_rank):
        for i in range(len(s_rank)):
            if sa_i == s_rank[i]:
                suffix_array.append(T[i:])
                sa_i += 1

    return suffix_array


def reduced_str_dna(str_data, print_f=True):
    if print_f:
        print('[1] Make integer sequence')
    reduced = []
    for c in str_data:
        if c == '$':
            reduced.append(0)
        elif c == 'a':
            reduced.append(1)
        elif c == 'c':
            reduced.append(2)
        elif c == 'g':
            reduced.append(3)
        elif c == 't':
            reduced.append(4)

    if print_f:
        print('    ', end='')
        print(reduced)
    return reduced


def s_012(str_data, recur_level, print_f=True):
    if print_f:
        print('    ' * recur_level, end='')
        print('[2] Make triplet sequence S0, S1, S2')

    s0, s1, s2 = [], [], []
    s0_done, s1_done, s2_done = False, False, False

    for i in range(math.ceil(len(str_data) / 3)):
        if not s0_done:
            str_temp = []
            for j in range(3):
                if 3 * i + j < len(str_data):
                    str_temp.append(str_data[3 * i + j])
            # str_temp = str_data[3 * i:3 * i + 3]
            if 3 * i + 3 == len(str_data):
                s0_done = True
            if len(str_temp) < 3:
                while len(str_temp) < 3:
                    str_temp.append(0)
                s0_done = True
            s0.append(str_temp)

        if not s1_done:
            str_temp = []
            for j in range(3):
                if 3 * i + 1 + j < len(str_data):
                    str_temp.append(str_data[3 * i + 1 + j])
            # str_temp = str_data[3 * i + 1:3 * i + 4]
            if 3 * i + 4 == len(str_data):
                s1_done = True
            if len(str_temp) < 3:
                while len(str_temp) < 3:
                    str_temp.append(0)
                s1_done = True
            s1.append(str_temp)

        if not s2_done:
            str_temp = []
            for j in range(3):
                if 3 * i + 2 + j < len(str_data):
                    str_temp.append(str_data[3 * i + 2 + j])
            # str_temp = str_data[3 * i + 2:3 * i + 5]
            if 3 * i + 5 == len(str_data):
                s2_done = True
            if len(str_temp) < 3:
                while len(str_temp) < 3:
                    str_temp.append(0)
                s2_done = True
            s2.append(str_temp)

    if print_f:
        print('    ' * recur_level, end='')
        print('    S0 : ', end='')
        print(s0)
        print('    ' * recur_level, end='')
        print('    S1 : ', end='')
        print(s1)
        print('    ' * recur_level, end='')
        print('    S2 : ', end='')
        print(s2)
    return s0, s1, s2


def merge_s12(s1, s2, recur_level, print_f=True):
    if print_f:
        print('    ' * recur_level, end='')
        print('[3] Merge S1, S2 & Sort S12')

    # Concatenate S1, S2gte
    s12 = copy.deepcopy(s1)
    for s in s2:
        s12.append(s)
    s12_sorted = copy.deepcopy(s12)
    # s12_sorted = list(set(s12_sorted))

    s12_i = 0
    while s12_i < len(s12_sorted) - 1:
        if s12_sorted[s12_i] in s12_sorted[s12_i + 1:]:
            s12_sorted.pop(s12_i)
        s12_i += 1

    # for s12_i in range(len(s12_sorted) - 1):
    #     if s12_sorted[s12_i] in s12_sorted[s12_i + 1:]:
    #         s12_sorted.pop(s12_i)

    s12_sorted.sort()
    s12_reduced_str = []
    for i in range(len(s12)):
        for j in range(len(s12_sorted)):
            if s12[i] == s12_sorted[j]:
                s12_reduced_str.append(j)
                break

    # Check duplicated ranks
    dup_f = False
    for i in range(len(s12_reduced_str) - 1):
        if s12_reduced_str[i] in s12_reduced_str[i + 1:]:
            dup_f = True
            break

    if print_f:
        print('    ' * recur_level, end='')
        print('    S12 : ', end='')
        print(s12)
        print('    ' * recur_level, end='')
        print('    S12 reduced string : ', end='')
        print(s12_reduced_str)
    return s12, s12_reduced_str, dup_f


def merge_sort(arr, idx_arr, start, end):
    if start < end:
        mid = int((start + end) / 2)
        merge_sort(arr, idx_arr, start, mid)
        merge_sort(arr, idx_arr, mid + 1, end)
        merge(arr, idx_arr, start, mid, end)


def merge(arr, idx_arr, start, mid, end):
    arr1, arr2 = arr[start:mid + 1], arr[mid + 1:end + 1]
    idx_arr1, idx_arr2 = idx_arr[start:mid + 1], idx_arr[mid + 1: end + 1]
    arr_sorted, idx_arr_sorted = [], []
    i, j = 0, 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            arr_sorted.append(arr1[i])
            idx_arr_sorted.append(idx_arr1[i])
            i += 1
        else:
            arr_sorted.append(arr2[j])
            idx_arr_sorted.append(idx_arr2[j])
            j += 1

    if i == len(arr1) and j < len(arr2):
        while j < len(arr2):
            arr_sorted.append(arr2[j])
            idx_arr_sorted.append(idx_arr2[j])
            j += 1

    elif i < len(arr1) and j == len(arr2):
        while i < len(arr1):
            arr_sorted.append(arr1[i])
            idx_arr_sorted.append(idx_arr1[i])
            i += 1

    for k in range(start, end + 1):
        arr[k] = arr_sorted.pop(0)
        idx_arr[k] = idx_arr_sorted.pop(0)


def datafile(fn):
    f = open(fn, 'r')
    str = f.readline()
    f.close()

    return str


if __name__ == '__main__':
    fn = 'input.txt'
    T = datafile(fn)

    suffix_array = build_suffix_array(T, print_f=False)

    print('\n>Final result (Suffix array)')
    for sa in suffix_array:
        print(sa)