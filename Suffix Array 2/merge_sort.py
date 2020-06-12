

def merge_sort(arr, start, end):
    if start < end:
        mid = int((start + end) / 2)
        merge_sort(arr, start, mid)
        merge_sort(arr, mid + 1, end)
        merge(arr, start, mid, end)


def merge(arr, start, mid, end):
    arr1, arr2 = arr[start:mid + 1], arr[mid + 1:end + 1]
    arr_sorted = []
    i, j = 0, 0


    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            arr_sorted.append(arr1[i])
            i += 1
        else:
            arr_sorted.append(arr2[j])
            j += 1

    if i == len(arr1) and j < len(arr2):
        while j < len(arr2):
            arr_sorted.append(arr2[j])
            j += 1

    elif i < len(arr1) and j == len(arr2):
        while i < len(arr1):
            arr_sorted.append(arr1[i])
            i += 1

    for k in range(start, end + 1):
        arr[k] = arr_sorted.pop(0)


if __name__ == '__main__':
    a = [512, 8, 15234, 7, 2, 5123, 613, 2153, 7, 5, 61, 1261, 65, 12, 2151]

    merge_sort(a, 0, len(a) - 1)
    print(a)


