from suffix_array_2 import *


fp = './input1.txt'
datas = datafile(fp)

N, T, SA, LCP, M, Q = datas[0], datas[1], datas[2], datas[3], datas[4], datas[5]

reduced_T = reduced_str(T)
s0, s1, s2 = s_012(reduced_T)

s1_s2 = s1
for s in s2:
    s1_s2.append(s)

# reduced_s1_s2 = 0

s1_s2.sort()
