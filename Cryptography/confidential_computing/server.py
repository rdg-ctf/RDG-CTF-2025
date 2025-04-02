from hashlib import md5
from random import randint, getrandbits

flag = 'rdg{C0nF1d3nTiAl_c0mpUt1Ng_1s_c00L}'
len_key = 56
Key = getrandbits(len_key)

def long_to_bytes(m):
    if m.bit_length() % 8:
        return m.to_bytes(m.bit_length() // 8 + 1, byteorder = 'big')
    else:
        return m.to_bytes(m.bit_length() // 8, byteorder = 'big')

def Confidential_computing():
    print('e:')
    e = int(input())
    print('n:')
    n = int(input())
    if n.bit_length() < 2048:
        return 0
    hashsum = 0
    for bit in [(Key >> (len_key - 1 - i)) & 1 for i in range(len_key)]:
        x = [0, 0]
        print('x0:')
        x[0] = int(input())
        print('x1:')
        x[1] = int(input())
        k = randint(2, n - 2)
        v = (x[bit] + pow(k, e, n)) % n
        print(f'v: {v}')
        m_ = [0, 0]
        print('m0:')
        m_[0] = int(input())
        print('m1:')
        m_[1] = int(input())
        m = (m_[bit] - k) % n
        hashsum += int(md5(long_to_bytes(m)).hexdigest(), 16)
    print(f'hashsum = {hashsum}')
                
def main():
    s_computing = 2
    print('list of actions:')
    print('0) Exit')
    print('1) Calculate')
    print('2) Get flag')

    while True:
        print('Select an action:')
        action = input()
        if action == '0':
            break
        elif action == '1':
            if s_computing != 0:
                Confidential_computing()
                s_computing -= 1
            else:
                print('The calculations are over')
        elif action == '2':
            print('Enter the key:')
            k = int(input())
            if k == Key:
                print(flag)
            else:
                print('The key is incorrect')

if __name__ == "__main__":
    main()
