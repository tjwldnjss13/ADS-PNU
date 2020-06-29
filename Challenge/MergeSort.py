def merge_sort_ptn(ptns, xy_idx, start, end):
    if start < end:
        mid = int((start + end) / 2)
        merge_sort_ptn(ptns, xy_idx, start, mid)
        merge_sort_ptn(ptns, xy_idx, mid + 1, end)
        merge_ptn(ptns, xy_idx, start, mid, end)


def merge_ptn(ptns, xy_idx, start, mid, end):
    ptns1, ptns2 = ptns[start:mid + 1], ptns[mid + 1:end + 1]
    ptns_sorted = []
    i1, i2 = 0, 0

    while i1 < len(ptns1) and i2 < len(ptns2):
        if ptns1[i1][xy_idx] < ptns2[i2][xy_idx]:
            ptns_sorted.append(ptns1[i1])
            i1 += 1
        else:
            ptns_sorted.append(ptns2[i2])
            i2 += 1

    if i1 == len(ptns1) and i2 < len(ptns2):
        ptns_sorted += ptns2[i2:]
    elif i1 < len(ptns1) and i2 == len(ptns2):
        ptns_sorted += ptns1[i1:]

    ptns[start:end + 1] = ptns_sorted
