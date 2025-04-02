# Lots of flags

|Название|Сложность|Автор|
|------|-----|-------|
|Lots of flags|Hard|[@sergbyand](https://sergbyand) |


# Описание: 

Нам удалось перехватить зашифрованный алгоритм шифрования. Но кажется его и не очень-то сильно охраняли. В любом случае извлеки из этого флаг.

# Решение:

Для старта информации мало. Значит надо анализировать текст. Он достаточно большой, а значит его можно закинуть в CrypTool и посмотреть статистику.

![изображение](https://github.com/user-attachments/assets/7b0dbc91-7c35-40d8-b332-8ab977f3ace6)

Он явно проваливает статистику на XOR и причём длина ключа всего 3. Так что нам не составляет труда подобать ключ и расшифровать файл Python.

![изображение](https://github.com/user-attachments/assets/4d2cd949-75d3-42b5-b5a8-a89fd0164ede)

В итоге получаем Python документ и осталось разобраться что он делает. В нем указан алгоритм шифрования и даже есть декриптор. Однако тут замазан сам флаг и функция случайной генерации бит. Так же тут есть часть ключа и шифртекст. Осталось получить одну из частей ключа и можно будет получить флаг.
Так как числа большие, а единственная зацепка — это скрытый псевдослучайный генератор, то нам остаётся только провести анализ того, что мы имеем.
Запустим все бинарные графические тесты для большого простого числа, чтобы понять, что делать.

Проверка серий:

![изображение](https://github.com/user-attachments/assets/9be672b3-83f8-4883-9d43-3f184d9a5b6d)

![изображение](https://github.com/user-attachments/assets/a4b05465-c83c-4982-b7b5-0afb88fc4c4f)

![изображение](https://github.com/user-attachments/assets/c5b06334-cd72-4b99-9a3e-a840470567f0)

![изображение](https://github.com/user-attachments/assets/d9b09de7-0069-44ae-93cf-bde68ea23068)

Проверка серий не дала никаких результатов, вроде все серии равномерны. Большие длины серий анализировать смысла нет, так как битов не так много.

Теперь запустим тест бинарной автокорреляции, для нахождения зависимости между битами.

![изображение](https://github.com/user-attachments/assets/0cd250d0-d8a5-4235-9e26-a115ea6d469e)

Этот тест тоже ничего нам не сказал, по крайней мере можно исключит малый период и нельзя установить прямую зависимость между битами.
Теперь спектральный анализ

![изображение](https://github.com/user-attachments/assets/1488ff65-de21-4a3e-8fa9-fee2b04a7040)

Собственно спектральный тест подтвердил, что здесь не наблюдается периодичности.
Остался профиль линейной сложности.

![изображение](https://github.com/user-attachments/assets/38187099-022c-475d-92ce-10f72143d5fb)

И тут удача. Профиль линейной сложности полностью завален и значит это LFSR генератор, причём его линейная сложность ровна 19. Значит осталось с помощью алгоритма Берлекэмпа-Мэсси получить образующий многочлен и тогда мы сможем продолжить генерацию битов и получить оставшийся ключ.

В итоге работы алгоритма линейная сложность равна 19. А образующий многочлен имеет вид `C(x) = 1 + x + x^2  + x^5  + x^19.` 

В качестве состояния генератора берём последние 19 бит от k1. И получаем ключ k2, продолжив генерацию. 

Теперь расшифровываем текст и получаем следующий флаг с сообщением: «rdg{negated_encryption_is_cool} If this flag was not accepted, then contact the organizers». 

Если проверить флаг, то его не примут. Но флаг называется отрицаемое шифрование. Если не знаете, что это такое, то можно про него прочитать и его суть в том, что одно и тоже сообщение расшифровывается по-разному для разных ключей. И это можно было понять и самому, если сразу посмотреть на размерность шифротекста, в нём лишняя информация, потому он и такой большой.

Для получения настоящего ключа просто продолжим генерацию ключей. Получим следующий ключ, и он уже должен быть правильным. И с помощью него уже получим флаг.

Для решения можно составить следующий код на языке Python:

```
from Cryptodome.Util.number import long_to_bytes, bytes_to_long
import numpy as np

seed = 0
key = 0
L = 0
mod = 0

def Berlekamp_Messi(A_bin):
    n = len(A_bin)
    C = np.zeros(n, int)
    C[0] = 1
    B = np.zeros(n, int)
    B[0] = 1
    L, m = 0, -1
    for N in range(n):
        d = np.sum( A_bin[N-L: N+1][::-1] & C[: L+1] )  & 1
        if d == 1:
            T = np.copy(C)
            C = C ^ np.roll(B, N-m)
            if L <= (N >> 1):
                L, m, B = N + 1 - L, N, np.copy(T)
    return L, list(C[: L+1])

def polinom_to_str(Coef):
    return "1 + " + " + ".join([f'x^{i}' for i in range(1, len(Coef)) if Coef[i] == 1])

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def getrandbits(n):
    res = 0
    global seed
    for _ in range(n):
        d = seed & (key >> 1)
        new_b = sum([(d >> i) & 1 for i in range(L)]) & 1
        seed = ((seed << 1) ^ new_b) & mod
        res = (res << 1) ^ new_b
    return res

def isPrime(p):
    for _ in range(100):
        a = getrandbits(p.bit_length())
        if pow(a, p - 1, p) != 1:
            return False
    return True

def getPrime(n):
    p = getrandbits(n)
    while not isPrime(p):
        p = getrandbits(n)
    return p
    
def genKey():
    p = getPrime(1024)
    k1 = getrandbits(1023)
    k2 = getrandbits(1023)
    while gcd(p - 1, k2) != 1:
        k2 = getrandbits(1023)
    return p, k1, k2

def encrypt(m, k1, k2, p):
    return (pow(m, k2, p) * k1) % p

def decrypt(c, k1, k2, p):
    return pow((c * pow(k1, -1, p)) % p, pow(k2, -1, p - 1), p)

def main():
    global seed
    global L
    global key
    global mod
    c = 910121…4674 
    p = 140531…5739
    k1 = 556375…2259
    k_bin_list = np.array([int(b) for b in bin(k1)[2:]])
    L, Coef = Berlekamp_Messi(k_bin_list)
    print(f'L = {L}')
    print(f'C(x) = {polinom_to_str(Coef)}')
    mod = 2**L - 1
    seed = k1 & mod
    key = sum([int(Coef[-i]) << (L + 1 - i) for i in range(1, len(Coef) + 1)])
    k2 = getrandbits(1023)
    while gcd(p - 1, k2) != 1:
        k2 = getrandbits(1023)
    flag = long_to_bytes(decrypt(c, k1, k2, p))
    print(flag)
    p_, k1_, k2_ = genKey()
    FLAG = long_to_bytes(decrypt(c, k1_, k2_, p_))
    print(FLAG)

if __name__ == "__main__":
    main()
```

# Флаг
rdg{Th1S_1S_a_R3aL_fLaG} 
