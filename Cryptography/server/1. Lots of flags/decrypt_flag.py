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
    c = 9101218151416839946279127426029865246188554060460699516676914318600908693975135281144788650256360189413425308000051415156449553933308035531494074853592870613584785550266779016261740956797439652229348924884736791639453352035768986756792567271942255850225591495018545248684273307936438473440291368437435268882955596999684642346421524587510400889163132559446777044724304007121672138308722030793073467154635188875575347688749364128591409684822655328235404744124623690423291756749093931976286423315043852208100715158221741071883694204019992916790140772828022967205353478059422944640873496733685814737520476365227550414674 
    p = 140531706152571206505837384626519062309360938149408815804918132467519838162960283348889864135086397226434892067246496824316981864477516265903289754946955168092498089000756495332625426562330024004593045130859491515176850409579204060133504116145924012457365087767993637249185066379687770890884781794533745985739
    k1 = 55637513923242589482770417464693910314530027554654983921358464734056554504729658529024490357849521382268125242322042294667774434660529493266256592143424304196365499484149271404567267542574903991799643528461007578574105887380791471663451933088383774611280749049868388762371907949679952372890178522057344552259
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
