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
