import matplotlib.pyplot as plt
from collections import Counter
import itertools
import numpy as np

def checking_the_series(text_bin, m):
    series_list = [text_bin[i: i+m] for i in range(0, len(text_bin) - (m-1))]
    B = dict(Counter(series_list))
    plt.bar(B.keys(), B.values(), 0.5)
    plt.xlabel('Серия')
    plt.ylabel('Количество')
    plt.title(f'Проверка серий длины {m}')
    plt.show()

def autocorrelation_test_bin(B):
    n = len(B)
    C = [np.sum(B*np.roll(B, j)) / n for j in range(1, n)]
    plt.plot(list(range(1, n)), C, 1, linewidth = 0.5)
    plt.xlabel('номер коэффициента корреляции')
    plt.ylabel('значение коэффициента корреляции')
    plt.title('Бинарная автокорреляция')
    plt.show()

def linear_complexity_profile(A_bin):
    n = len(A_bin)
    C = np.zeros(n, int)
    C[0] = 1
    B = np.zeros(n, int)
    B[0] = 1
    L, m = 0, -1
    L_list = [0] * n
    for N in range(n):
        d = np.sum( A_bin[N-L: N+1][::-1] & C[: L+1] )  & 1
        if d == 1:
            T = np.copy(C)
            C = C ^ np.roll(B, N-m)
            if L <= (N >> 1):
                L, m, B = N + 1 - L, N, np.copy(T)
        L_list[N] = L
    plt.plot(list(range(n)), L_list, 1, linewidth = 1)
    plt.xlabel('размер подпоследовательности')
    plt.ylabel('линейная сложность')
    plt.title('Профиль линейной сложности')
    plt.show()

def spectral_test(B):
    n = len(B)
    S = np.fft.fft(B * np.exp(2j * np.pi * np.arange(n) / n))
    M = np.abs(S)
    plt.plot(list(range(n // 2)), M[:n // 2], 1, linewidth = 1)
    plt.xlabel('номер гармоники')
    plt.ylabel('модуль гармоники')
    plt.title('Спектральный тест')
    plt.show()

def main():
    p = 140531706152571206505837384626519062309360938149408815804918132467519838162960283348889864135086397226434892067246496824316981864477516265903289754946955168092498089000756495332625426562330024004593045130859491515176850409579204060133504116145924012457365087767993637249185066379687770890884781794533745985739
    p_bin = bin(p)[2:]
    p_bin_list = np.array([int(b) for b in p_bin])
    for i in range(1, 9):
        checking_the_series(p_bin, i)
    autocorrelation_test_bin(p_bin_list)
    linear_complexity_profile(p_bin_list)
    spectral_test(p_bin_list)

if __name__ == "__main__":
    main()
