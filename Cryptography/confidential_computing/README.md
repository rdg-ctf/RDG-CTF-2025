# Confidential Computing

|Название|Сложность|Автор|
|------|-----|-------|
|Confidential Computing|Medium|[@sergbyand](https://sergbyand) |

# Описание:

Я создал сервер для конфиденциальных вычислений. Для этого я использую протокол забывчивой передачи данных, прочитай про них. Давай посмотрим, сможешь ли ты узнать мой ключ.

# Решение

Перед нами сервер, в котором реализован алгоритм конфиденциального сложения. При этом мы точно не знаем какие числа будут сложены. Реализовано это с помощью протокола забывчивой передачи данных 1 к 2. Он описывается следующим образом:

В данной версии протокола, отправитель посылает два сообщения `m_0` и `m_1`, а получатель имеет би b, и хотел бы получить `m_b`, без того, что бы отправитель узнал `b`, в то же время отправитель хочет быть уверенным в том, что получатель получил только одно из двух сообщений. 

1. 	Отправитель имеет два сообщения, `m_0` и `m_1`, и хочет отправить одно единственное получателю, но не хочет знать какое из них именно он получит.

2. Отправитель генерирует пару ключей RSA, содержащие модули n, публичную экспоненту e и скрытую d.

3. 	Отправитель так же генерирует два случайных значения `x_0`,`x_1` и отсылает их получателю вместе с публичными модулями и экспонентой

4. Получатель выбирает `b = {1, 0}` и выбирает или первый или второй `x_b`.

5. Получатель генерирует случайное значение `k` и шифрует `x_b` рассчитывая `v=(x_b+k^e)  mod n`, которое возвращает отправителю.

6. Отправитель не знает какое из `x_0`  и `x_1` выбрал получатель, и пытается расшифровать оба случайных сообщения, получая два возможных значения: `k_0=(v-x_0 )^d  mod n и k_1=(v-x_1 )^d  mod n`. Одно из них будет соответствовать` k`, будучи корректно расшифрованным, тогда как другое будет случайным значение, не раскрывающем никакой информации о `k`.

7. Отправитель шифрует оба секретных сообщения с каждым возможным ключом `〖m_0〗^'=m_0+k_0, 〖m_1〗^'=m_1+k_1 `и посылает их оба получателю.

8. Получатель знает какое из двух сообщений может быть расшифровано с помощью `k`, и он получает возможность расшифровать только одно сообщение `m_b=〖m_b〗^'-k`

Тут нам ничего не остаётся, кроме того, как честно выполнить свои обязательства и получить сумму хешей отправленный нами сообщений. Проблема заключается в том, что мы не знаем какие сообщения складывались и надо как-то составить уравнение.

Это можно сделать следующим образом:

Пусть `bᵢ` – это значение неизвестного нам i-го бита, а `mᵢ₀` и `mᵢ₁` – это хеши соответствующих сообщений для бита 0 и бита 1. Тогда неизвестную сумму относительного этого бита можно записать следующим образом:

```
s = mᵢ₀(1 - bᵢ) + mᵢ₁bᵢ = (mᵢ₁ - mᵢ₀)bᵢ + mᵢ₀
```

Преобразуем уравнение:
```
(mᵢ₁ - mᵢ₀)bᵢ = s - mᵢ₀
```

Тогда проделав это для каждого неизвестного бита можно составить следующее уравнение:

```
∑(mᵢ₁ - mᵢ₀)bᵢ = s - ∑mᵢ₀
```

Где:
- `s` – это сумма полученных хешей
- `len_k` – длина ключа

Это линейное уравнение. Но проблема в том, что таких мы сможем получить только 2. А значит надо обходится этими двумя уравнениями. Для этого можно использовать LLL алгоритм, так как биты крайне малы по сравнению с числами. Но чтобы решить надо использовать оба уравнения одновременно. Решив систему получаем флаг.

Для решения можно составить следующий код на языке Python:

```
import telnetlib
from Cryptodome.Util.number import getPrime, long_to_bytes
from Cryptolib import LLL
from random import randint
from hashlib import md5
from time import time

HOST = "192.168.153.128"
PORT = 4442

tn = telnetlib.Telnet(HOST, PORT)

def long_to_bytes(m):
    if m.bit_length() % 8:
        return m.to_bytes(m.bit_length() // 8 + 1, byteorder = 'big')
    else:
        return m.to_bytes(m.bit_length() // 8, byteorder = 'big')

def genKey(L):
    p, q = getPrime((L >> 1) + 1), getPrime((L >> 1) + 1)
    n = p*q
    fi = (p - 1)*(q - 1)
    e = 0x10001
    d = pow(e, -1, fi)
    return n, e, d

def getCoef(M_new, has):
    Coef = [0] * len(M_new)
    for i in range(len(Coef)):
        m0, m1 = int(md5(long_to_bytes(M_new[i][0])).hexdigest(), 16), int(md5(long_to_bytes(M_new[i][1])).hexdigest(), 16)
        Coef[i] = m1 - m0
        has -= m0
    return Coef, has
    
def main():    
    n, e, d = genKey(2048)
    for _ in range(4):
        tn.read_until(b"\n")

    len_action = 2
    Coef = [0] * len_action
    has = [0] * len_action
    for num in range(len_action):
        M = []
        tn.read_until(b"\n")
        tn.write(f'{1}'.encode() + b'\n')
        tn.read_until(b"\n")
        tn.write(f'{e}'.encode() + b'\n')
        tn.read_until(b"\n")
        tn.write(f'{n}'.encode() + b'\n')
        stop = tn.read_until(b"\n")
        while stop == b'x0:\n':
            x = [randint(2, n - 2) for _ in range(2)]
            tn.write(f'{x[0]}'.encode() + b'\n')
            tn.read_until(b"\n")
            tn.write(f'{x[1]}'.encode() + b'\n')
            v = int(tn.read_until(b"\n")[3: ])
            M += [[randint(0, n) for _ in range(2)]]
            k = [pow((v - x[i]) % n, d, n) for i in range(2)]
            m = [(M[-1][i] + k[i]) % n for i in range(2)]
            tn.read_until(b"\n")
            tn.write(f'{m[0]}'.encode() + b'\n')
            tn.read_until(b"\n")
            tn.write(f'{m[1]}'.encode() + b'\n')
            stop = tn.read_until(b"\n")
        has[num] = int(stop[10:])
        Coef[num], has[num] = getCoef(M, has[num])
    len_key = len(Coef[0])
    N = 1 << 128
    Matrix = [[1 if i == j else 0 for j in range(len_key)] + [N*Coef[j][i] for j in range(len_action)] for i in range(len_key)] + \
             [[0 for i in range(len_key)] + [N*has[i] for i in range(len_action)]]
    Matrix = LLL(Matrix)
    for M in Matrix:
        if all([m == 1 or m == -1 or m == 0 for m in M[:-len_action]] + \
               [m == 0 for m in M[-len_action:]]):
            Key = M
    Key = sum([abs(Key[len_key - i - 1]) << i for i in range(len(Key))])
    tn.read_until(b"\n")
    tn.write(f'{2}'.encode() + b'\n')
    tn.read_until(b"\n")
    tn.write(f'{Key}'.encode() + b'\n')
    print(tn.read_until(b"\n"))
    
if __name__ == "__main__":
    main()
```

# Flag

rdg{C0nF1d3nTiAl_c0mpUt1Ng_1s_c00L}
