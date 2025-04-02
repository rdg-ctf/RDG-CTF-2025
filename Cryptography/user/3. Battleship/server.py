from hashlib import sha256

flag = 'rdg{????????????????????????}'
n = 10
Dict_ships = {4: 1, 3: 2, 2: 3, 1: 4}

def field_to_bin(field):
    h = ''
    for row in range(n):
        for column in range(n):
            if field[row][column] == 0:
                h += '0'
            if field[row][column] == 1:
                h += '1'
    return h

def hashsum(h):
    h = int(h, 2).to_bytes(13, byteorder = 'big')
    return sha256(h).hexdigest()

def Game():
    ???????????????

def main():
    f = True
    for _ in range(100):
        res = Game()
        if res != 0 and res != 1:
            print(res)
            f = False
            break
        elif res == 0:
            f = False
            break
    if f:
        print(flag)
    else:
        print('You could not win me')

if __name__ == "__main__":
    main()
