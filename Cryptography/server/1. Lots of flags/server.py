from Cryptodome.Util.number import long_to_bytes, bytes_to_long

FLAG = b'rdg{Th1S_1S_a_R3aL_fLaG}'
FLAG_ = b'rdg{negated_encryption_is_cool} If this flag was not accepted, then contact the organizers'

seed = 255
key = 0b10000000000000100111
L = 19
mod = 2**L - 1

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

def KTO(A, P):
    M = 1
    for p in P:
        M *= p
    res = 0
    for i in range(len(A)):
        Mi = M // P[i]
        res = (res + A[i] * Mi * pow(Mi, -1, P[i])) % M
    return res

def main():
    p_, k1_, k2_ = genKey()
    c_ = encrypt(bytes_to_long(FLAG_), k1_, k2_, p_)
    p, k1, k2 = genKey()
    c = encrypt(bytes_to_long(FLAG), k1, k2, p)
    C = KTO([c_, c], [p_, p])
    print(p_, k1_)
    print(C)
    
if __name__ == "__main__":
    main()
