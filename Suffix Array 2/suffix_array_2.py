import copy
import math

def build_suffix_array(T):
    reduced_T = reduced_str_dna(T)
    dup_f = True

    while dup_f:
        s0, s1, s2 = s_012(reduced_T)

        # Concatenate S1, S2
        s12 = copy.deepcopy(s1)
        for s in s2:
            s12.append(s)
        s12_sorted = copy.deepcopy(s12)
        s12_sorted = list(set(s12_sorted))
        s12_sorted.sort()
        s12_reduced_str = ''
        for i in range(len(s12)):
            for j in range(len(s12_sorted)):
                if s12[i] == s12_sorted[j]:
                    s12_reduced_str += str(j)
                    break

        # Check duplicated ranks
        dup_f = False
        for i in range(len(s12_reduced_str) - 1):
            if s12_reduced_str[i] in s12_reduced_str[i + 1:]:
                dup_f = True
                break
        print(s12_reduced_str)
        if dup_f:
            reduced_T = s12_reduced_str
            continue
        break

    # Sort S0 & S12


    print(s0)
    print(s12)





def datafile(fp):
    f = open(fp, 'r')
    lines = f.readlines()
    f.close()
    N = int(lines[0])
    T = lines[1]
    SA_str = lines[2].strip().split(' ')
    SA = []
    for sa in SA_str:
        SA.append(int(sa))
    LCP = lines[3]
    N_q = int(lines[4])
    Q = []
    for i in range(5, N_q + 5):
        q_temp = lines[i].split('\n')[0]
        q_temp += '$'
        Q.append(q_temp)

    return [N, T, SA, LCP, N_q, Q]


def reduced_str_dna(str_data):
    reduced = ''
    for c in str_data:
        if c == '$':
            reduced += '0'
        elif c == 'a':
            reduced += '1'
        elif c == 'c':
            reduced += '2'
        elif c == 'g':
            reduced += '3'
        elif c == 't':
            reduced += '4'
    return reduced


def s_012(str_data):
    s0, s1, s2 = [], [], []
    s0_done, s1_done, s2_done = False, False, False

    for i in range(math.ceil(len(str_data) / 3)):
        if not s0_done:
            str_temp = str_data[3 * i:3 * i + 3]
            if 3 * i + 3 == len(str_data):
                s0_done = True
            if len(str_temp) < 3:
                while len(str_temp) < 3:
                    str_temp += '0'
                s0_done = True
            s0.append(str_temp)

        if not s1_done:
            str_temp = str_data[3 * i + 1:3 * i + 4]
            if 3 * i + 4 == len(str_data):
                s1_done = True
            if len(str_temp) < 3:
                while len(str_temp) < 3:
                    str_temp += '0'
                s1_done = True
            s1.append(str_temp)

        if not s2_done:
            str_temp = str_data[3 * i + 2:3 * i + 5]
            if 3 * i + 5 == len(str_data):
                s2_done = True
            if len(str_temp) < 3:
                while len(str_temp) < 3:
                    str_temp += '0'
                s2_done = True
            s2.append(str_temp)

    return s0, s1, s2

