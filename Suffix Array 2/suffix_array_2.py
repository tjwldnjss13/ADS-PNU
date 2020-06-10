
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


def reduced_str(str_data):
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

    for i in range(int(len(str_data) / 3)):
        str_temp = str_data[3 * i:3 * i + 3]
        while len(str_temp) < 3:
            str_temp += '0'
        s0.append(str_temp)

        str_temp = str_data[3 * i + 1:3 * i + 4]
        while len(str_temp) < 3:
            str_temp += '0'
        s1.append(str_temp)

        str_temp = str_data[3 * i + 2:3 * i + 5]
        while len(str_temp) < 3:
            str_temp += '0'
        s2.append(str_temp)

    return s0, s1, s2

