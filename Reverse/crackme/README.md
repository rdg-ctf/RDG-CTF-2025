# CrackMe

## Описание 
| Название | Сложность | TLDR | Автор |
|------|-----|-------|--------|
| CrackMe | Medium | python decompilation with RSA  |[@maxhays](https://t.me/maxhays) |

# Решение

Разбираем Pyinstaller, достаём главный исполняемый модуль. При помощи pycdc, uncompyle6 или decompyle3

![изображение](https://github.com/user-attachments/assets/d9205fbf-4089-4741-8f3a-aa9965c043df)

Видим, что у нас идёт проверка пароля. При помощи функции decrypt, которая на самом деле является xor шифрованием и вводит нас в заблуждение своим названием.

Расшифрованный пароль «RDGCTFPASSpaaaaaasssssssspaaaasssssssssssss» позволяет нам попасть во вторую стадию. Восстанавливаем исходники второй стадии.

![изображение](https://github.com/user-attachments/assets/bde9d4fc-dd16-45da-a436-a50d5eb156bf)

Во второй стадии код также зашифрован xor’ом. Правильный ключ позволяет получить правильный исполняемый код. Пробуем его перебрать, проверяя хэш кода. Ключ P@SS.

Переходим к третьей стадии.

Восстановленная финальная стадия является реализацией алгоритма RSA с уязвимостью. 

Уязвимость в том, что `n = p*q = p*2^(L // 2) + a`, где `L` - это длина в битах числа `n`, `a` - какое-то размера `L // 2` бит

И получается, что старшие биты - это и есть простое число p. Таким образом создан бэкдор, что зная n можно найти p. 

Отдаём это все криптографу, прогоняем через RSACTFTool и получаем флаг. Скрипт факторизации:

```
log = gmpy.log
is_divisible = lambda n, p: n % p == 0
next_prime = gmpy.next_prime

n =  #from pub.key file
def factor_XYXZ(n, base=3):
    """
    Factor a x^y*x^z form integer with x prime.
    """
    power = 1
    max_power = (int(log(n) / log(base)) + 1) >> 1
    while power <= max_power:
        p = next_prime(base ** power)
        if is_divisible(n, p):
            return p, n // p
        power += 1


for base in [2, 3, 5, 7, 11, 13, 17]:
    p,q = factor_XYXZ(n, base)
    if p != None:
        print(p,q)
```

## Flag
rdg{pyth0n_m@tr3shk@}
