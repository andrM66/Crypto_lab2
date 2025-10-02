import math
from scipy.special import gammainc


class AdditiveGenerator:
    def __init__(self, x_0: int, x_1: int, n: int):
        self.x_0 = x_0
        self.x_1 = x_1
        self.n = n


    def gen_random_int(self) -> int:
        x = (self.x_1 + self.x_0) % self.n
        self.x_0 = self.x_1
        self.x_1 = x
        return x


def find_period(sequence):
    """
    Находит период последовательности, ища повторяющуюся подпоследовательность
    """
    n = len(sequence)

    # Проверяем возможные длины периода
    for period in range(1, n // 2 + 1):
        is_periodic = True

        # Проверяем, повторяется ли последовательность с данным периодом
        for i in range(period, n):
            if sequence[i] != sequence[i % period]:
                is_periodic = False
                break

        if is_periodic:
            return period

    return n


def int_array_to_bit_strings(arr, bits=8):
    tmp = [format(num, f'0{bits}b') for num in arr]
    tmp = "".join(tmp)
    tmp = list(tmp)
    tmp = list(map(int, tmp))
    return tmp


def monobite_test(sequence: list, alpha: float):
    ones = sequence.count(1)
    zeros = sequence.count(0)
    s = abs(ones - zeros)/math.sqrt(len(sequence))
    p_value = math.erfc(s/math.sqrt(2))
    if p_value < alpha:
        print("the sequence is non-random")
    else:
        print("the sequence is random")


def run_test(sequence: list, alpha: float):
    pi = sequence.count(1)/len(sequence)
    #if abs(pi - 1/2) >= 2/math.sqrt(len(sequence)):
    #    print("Sequence will not pass monobite test, no run test is needed")
    #    return None
    v = 0
    for i in range(len(sequence) - 1):
        if sequence[i] != sequence[i+1]:
            v += 1
    v += 1
    p_val = math.erfc(abs(v - 2 * len(sequence) * pi * (1 - pi))/ (2 * math.sqrt(2 * len(sequence))*pi * (1 - pi)))
    if p_val < alpha:
        print("the sequence is non-random")
    else:
        print("the sequence is random")


def longest_run_of_ones(sequence: list) -> int:
    max_count = 0
    count = 0
    for i in sequence:
        if i == 1:
            count += 1
        if i ==0:
            count = 0
        if count > max_count:
            max_count = count
    return max_count


def run_of_ones_in_a_block_test(sequence: list, alpha: float):
    n = len(sequence)
    m = 0
    k = 0
    N = 0
    pi_vals = []
    if 128 <= n < 6272:
        m = 8
        k = 3
        N = 16
        pi_vals = [0.21148, 0.3672, 0.2305, 0.1875]
    elif 6272 <= n < 750000:
        m = 128
        k = 5
        N = 49
        pi_vals = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    elif n >= 750000:
        m = 10000
        k = 6
        N = 75
        pi_vals = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    else:
        print("the sequence is too short")
        return None
    blocked_sequence = [sequence[i:i + m] for i in range(0, len(sequence), m)]
    v_vals = str().zfill(k+1)
    v_vals = list(v_vals)
    v_vals = list(map(int, v_vals))
    #print(blocked_sequence)
    for chunk in blocked_sequence:
        once_run = longest_run_of_ones(chunk)
        if m == 8:
            if once_run <= 1:
                v_vals[0] += 1
            elif once_run == 2:
                v_vals[1] += 1
            elif once_run == 3:
                v_vals[2] += 1
            elif once_run >= 4:
                v_vals[3] += 1
        elif m == 128:
            if once_run <= 4:
                v_vals[0] += 1
            elif once_run == 5:
                v_vals[1] += 1
            elif once_run == 6:
                v_vals[2] += 1
            elif once_run == 7:
                v_vals[3] += 1
            elif once_run == 8:
                v_vals[4] += 1
            elif once_run >= 9:
                v_vals[5] += 1
        elif m == 10000:
            if once_run <= 10:
                v_vals[0] += 1
            elif once_run == 11:
                v_vals[1] += 1
            elif once_run == 12:
                v_vals[2] += 1
            elif once_run == 13:
                v_vals[3] += 1
            elif once_run == 14:
                v_vals[4] += 1
            elif once_run == 15:
                v_vals[5] += 1
            elif once_run >= 16:
                v_vals[6] += 1
    chi_square = 0.0
    for i in range(k+1):
        chi_square += ((v_vals[i] - N * pi_vals[i]) ** 2) / (N * pi_vals[i])
    p_val = gammainc(k/2, chi_square/2)
    if p_val < alpha:
        print("the sequence is non-random")
    else:
        print("the sequence is random")



if __name__ == '__main__':
    rnd = AdditiveGenerator(11, 19, 30)
    a = []
    for i in range(125000):
        a.append(rnd.gen_random_int())
    a_bits = int_array_to_bit_strings(a)
    print(find_period(a))
    print(find_period(a_bits))
    monobite_test(a_bits, 0.01)
    run_test(a_bits, 0.01)
    run_of_ones_in_a_block_test(a_bits, 0.01)

    print("\n")
    f = open("data.pi", "r")
    bits_pi = f.read()
    f.close()
    bits_pi = bits_pi.replace(' ', '').replace('\n', '').replace(',', '')
    bits_pi = list(bits_pi)
    bits_pi = list(map(int, bits_pi))
    monobite_test(bits_pi, 0.01)
    run_test(bits_pi, 0.01)
    run_of_ones_in_a_block_test(bits_pi, 0.01)

    print("\n")
    f = open("data.e", "r")
    bits_e = f.read()
    f.close()
    bits_e = bits_e.replace(' ', '').replace('\n', '').replace(',', '')
    bits_e = list(bits_e)
    bits_e = list(map(int, bits_e))
    monobite_test(bits_e, 0.01)
    run_test(bits_e, 0.01)
    run_of_ones_in_a_block_test(bits_e, 0.01)



