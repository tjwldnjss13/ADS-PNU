import time


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


def brute_force(T, Q):
    start = time.time()
    equal_cnt_list = []

    for q in Q:
        equal_cnt = 0
        for T_i in range(len(T) - len(q) + 1):
            equal_F = True
            for q_i in range(len(q) - 1):
                if q[q_i] != T[T_i + q_i]:
                    equal_F = False
                    break
            if equal_F:
                equal_cnt += 1
        equal_cnt_list.append(equal_cnt)
    end = time.time()

    return equal_cnt_list, end - start


def binary_search_with_suffix_array(N, T, SA, Q):
    start = time.time()

    equal_cnt = []
    for q in Q:
        l_min, r_min = 0, N
        l_max, r_max = 0, N
        q_min = q.split('$')[0] + '#'
        q_max = q.split('$')[0] + '~'
        while r_min - l_min != 1:
            m_min = int((l_min + r_min) / 2)
            SA_m_min = T[SA[m_min]:]

            f = str_compare(q_min, SA_m_min)
            if f == 1:
                l_min = m_min
            elif f == 2:
                r_min = m_min

        while r_max - l_max != 1:
            m_max = int((l_max + r_max) / 2)
            SA_m_max = T[SA[m_max]:]

            f = str_compare(q_max, SA_m_max)
            if f == 1:
                l_max = m_max
            elif f == 2:
                r_max = m_max

        m_min, m_max = (l_min + r_min) / 2, (l_max + r_max) / 2
        equal_cnt.append(int(m_max - m_min))

    end = time.time()

    return equal_cnt, end - start


def better_tech(N, T, SA, Q):
    start = time.time()
    equal_cnt = []
    for q in Q:
        l_min, r_min = 0, N - 1
        l_max, r_max = 0, N - 1
        q_min = q.split('$')[0] + '#'
        q_max = q.split('$')[0] + '~'

        lcp_l, lcp_r = lcp(q_min, T[SA[l_min]:]), lcp(q_min, T[SA[r_min]:])
        while r_min - l_min != 1:
            m_min = int((l_min + r_min) / 2)
            SA_m_min = T[SA[m_min]:]

            skip = min(lcp_l, lcp_r)
            f = str_compare(q_min[skip:], SA_m_min[skip:])
            if f == 1:
                l_min = m_min
                lcp_l = lcp(T[SA[l_min]:], q_min)
            elif f == 2:
                r_min = m_min
                lcp_r = lcp(T[SA[r_min]:], q_min)

        lcp_l, lcp_r = lcp(q_min, T[SA[l_max]:]), lcp(q_min, T[SA[r_max]:])
        while r_max - l_max != 1:
            m_max = int((l_max + r_max) / 2)
            SA_m_max = T[SA[m_max]:]

            skip = min(lcp_l, lcp_r)
            f = str_compare(q_max[skip:], SA_m_max[skip:])
            if f == 1:
                l_max = m_max
                lcp_l = lcp(T[SA[l_max]:], q_max)
            elif f == 2:
                r_max = m_max
                lcp_r = lcp(T[SA[r_max]:], q_max)

        m_min, m_max = (l_min + r_min) / 2, (l_max + r_max) / 2
        equal_cnt.append(int(m_max - m_min))
    end = time.time()

    return equal_cnt, end - start


def str_compare(str1, str2):
    len1, len2 = len(str1), len(str2)
    length = 0

    if len1 < len2:
        length = len1
    else:
        length = len2

    for i in range(length):
        if str1[i] < str2[i]:
            return 2
        elif str1[i] > str2[i]:
            return 1
        else:
            continue

    return 0


def lcp(str1, str2):
    len1, len2 = len(str1), len(str2)
    lcp_val = 0

    length = 0
    if len1 < len2:
        length = len1
    else:
        length = len2
    for i in range(length):
        if str1[i] == '$' or str1[i] == '~' or str1[i] == '#' or str2[i] == '$' or str2[i] == '~' or str2[i] == '#' or str1[i] != str2[i]:
            break
        lcp_val += 1

    return lcp_val


def main():
    fp = './dna.txt'
    datas = datafile(fp)

    N, T, SA, LCP, M, Q = datas[0], datas[1], datas[2], datas[3], datas[4], datas[5]

    result1, time1 = brute_force(T, Q)
    result2, time2 = binary_search_with_suffix_array(N, T, SA, Q)
    result3, time3 = better_tech(N, T, SA, Q)
    print(time1)
    print(time2)
    print(time3)
    print(result1)
    print(result2)
    print(result3)


if __name__ == '__main__':
    main()
