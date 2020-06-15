from suffix_array_2 import *
import time

fn = 'input.txt'
T = datafile(fn)

start = time.time()
suffix_array = build_suffix_array(T, print_f=False)
end = time.time()

print('Time : {}'.format(end - start))

print('\n>Final result (Suffix array)')
for sa in suffix_array:
    print(sa)
