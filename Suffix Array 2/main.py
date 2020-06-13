from suffix_array_2 import *

# fp = './input1.txt'
# datas = datafile(fp)
#
# N, T, SA, LCP, M, Q = datas[0], datas[1], datas[2], datas[3], datas[4], datas[5]

# T = 'baabaabbaa$'
T = 'agacgtctacgacgtacagcatgcatcgtagct$'

suffix_array = build_suffix_array(T)
print('>Final result (Suffix array)')
for sa in suffix_array:
    print(sa)
