from Cryptodome.Util.number import getPrime, long_to_bytes, bytes_to_long
from os import urandom

name = [b'Sergey', b'Sergey\x00', b'Sergey\x00\x00', b'Sergey\x00\x00\x00', b'Sergey\x00\x00\x00\x00',]
salt = urandom(150) + b'rdg{Y3s_h0w_mUch_Can_y0U_m3sS_w1tH_RSA}'

def GenKey(L):
    e = 5
    while True:
        p, q = getPrime((L >> 1) + 1), getPrime((L >> 1) + 1)
        if (p - 1) % e != 0 and (q - 1) % e != 0:
            break
    n = p*q
    fi = (p - 1) * (q - 1)
    d = pow(e, -1, fi)
    return e, d, n

def encrypt(m, e, n):
    return pow(bytes_to_long(salt + m), e, n)

def decrypt(c, d, n):
    return long_to_bytes(pow(c, d, n))[len(salt): ]

def main():
    L = 2048
    E, D, N = [0] * len(name), [0] * len(name), [0] * len(name)
    for i in range(len(name)):
        E[i], D[i], N[i] = GenKey(L)
    C = [encrypt(name[i], E[i], N[i]) for i in range(len(name))]
    print(f'N = {N}')
    print(f'C = {C}')

if __name__ == "__main__":
    main()
