# battleship

# Описание 
|Название|Сложность|Автор|
|------|-----|-------|
|Battleship|Medium|[@sergbyand](https://sergbyand) |

# Описание: 

Я люблю играть в морской бой. Попробуй победить меня 100 раз подряд. Естественно, чтобы было всё честно перед игрой будем отправлять друг другу хеш поля.

# Решение

Это действительно обычный морской бой. Причём у игрока действительно не лучшая стратегия расстановки кораблей. Из-за чего его можно победить даже в честном бою. Причём вероятность победы будет более 50% (естественно, если вы выбрали лучшую стратегию). Но чтобы выиграть 100 раз подряд всё равно недостаточно. 

В начале обсудим нашу стратегию честной игры. Для этого достаточно покрывать поле так, чтобы в начале найти 4 палубный корабль, потом 3 палубный и 2 палубный. А одиночные корабли ищутся только наугад. Также важно, что если мы попали в корабль, то надо его добить. В целом поражение можно задать по следующей картинке, причём так как компьютер каждый раз запускает игру по новой, то и нашу стратегию можно не менять.

Для поиска 4 палубного:

<img width="195" alt="изображение" src="https://github.com/user-attachments/assets/917490d3-6655-4c63-90c0-c58d7bda2670" />

Для поиска 3 и 2 палубного:

<img width="219" alt="изображение" src="https://github.com/user-attachments/assets/64d40bf5-df1e-4b75-90a0-f436a4870535" />

И по стратегии расстановки кораблей поступаем так, чтобы ореол от взрыва покрывал как можно меньшую площадь. Вот несколько примеров (однопалубные можно расположить любым способом):

<img width="435" alt="изображение" src="https://github.com/user-attachments/assets/7c5cfd84-bca7-4f78-ab1c-8319fdc4ef2b" />

Но что же надо сделать чтобы победить 100 раз подряд? 

Для этого рассмотрим систему безопасности. Это просто sha256 от поля. 

Вообще расположений полей очень много, поэтому перебрать значения под хеш не выйдет. Но можно сделать это под конец игры. Когда у вас остаётся 25 не исследованных квадрата, то вы можете перебрать все возможные варианты. В таком случае концовку игры вы завершите точными выстрелами по целям. При этом как раз концовка морского боя и является самой вероятной для проигрыша. 

Таким образом у нас честное начало игры и жульнический конец за счёт того, что у хеша отсутствует соль.

Можно реализовать следующий код на языке Python:
```
import telnetlib
from hashlib import sha256
from itertools import combinations

HOST = "192.168.153.128"
PORT = 4443

tn = telnetlib.Telnet(HOST, PORT)

n = 10

class Ship():
    def __init__(self, x, y, length, tp = 0):
        self.x = x
        self.y = y
        self.length = length
        self.tp = tp
        self.coords_list = self.get_coords_list()
        self.cells = {coord: 0 for coord in self.coords_list}

    def get_coords_list(self):
        if self.tp == 0:
            return [(self.x + i, self.y) for i in range(self.length)]
        else:
            return [(self.x, self.y + i) for i in range(self.length)]

    def is_hit(self, x, y):
        return (x, y) in self.coords_list

    def hit(self, x, y):
        self.cells[(x, y)] = 1

    def is_kill(self):
        return all([self.cells[k] == 1 for k in self.cells.keys()])

class GamePole():
    def __init__(self, ships_list):
        self.ships_list = [Ship(s[0], s[1], s[2], s[3]) for s in ships_list]
        self.filed = [[0 for i in range(n)] for j in range(n)]
        for ship in self.ships_list:
            for (x, y) in ship.coords_list:
                self.filed[x][y] = 1

    def shot(self, x, y):
        if self.filed[x][y] == 0:
            return 0
        for ship in self.ships_list:
            if ship.is_hit(x, y):
                ship.hit(x, y)
                if ship.is_kill():
                    self.ships_list.remove(ship)
                    return 2
                return 1

ships_list = [(0, 0, 4, 0),
              (0, 9, 3, 0),
              (7, 9, 3, 0),
              (5, 0, 2, 0),
              (8, 0, 2, 0),
              (4, 9, 2, 0),
              (0, 2, 1, 0),
              (9, 2, 1, 0),
              (0, 7, 1, 0),
              (7, 7, 1, 0)]

my_pole = GamePole(ships_list)

my_pole_bin = ''
for row in my_pole.filed:
    for bit in row:
        my_pole_bin += str(bit)

hashsum_my_pole = sha256(int(my_pole_bin, 2).to_bytes(13, byteorder = 'big')).hexdigest()

shot_list = ['A4', 'B3', 'C2', 'D1', 'A8', 'B7', 'C6', 'D5', 'E4', 'F3',
             'G2', 'H1', 'C10', 'D9', 'E8', 'F7', 'G6', 'H5', 'I4', 'J3',
             'G10', 'H9', 'I8', 'J7', 'A2', 'B1', 'A6', 'B5', 'C4', 'D3',
             'E2', 'F1', 'A10', 'B9', 'C8', 'D7', 'E6', 'F5', 'G4', 'H3',
             'I2', 'J1', 'E10', 'F9', 'G8', 'H7', 'I6', 'J5', 'I10', 'J9',
             'A1', 'C1', 'E1', 'G1', 'I1', 'B2', 'D2', 'F2', 'H2', 'J2',
             'A3', 'C3', 'E3', 'G3', 'I3', 'B4', 'D4', 'F4', 'H4', 'J4',
             'A5', 'C5', 'E5', 'G5', 'I5', 'B6', 'D6', 'F6', 'H6', 'J6',
             'A7', 'C7', 'E7', 'G7', 'I7', 'B8', 'D8', 'F8', 'H8', 'J8',
             'A9', 'C9', 'E9', 'G9', 'I9', 'B10', 'D10', 'F10', 'H10', 'J10',]

def str_coordinate(row, column):
    List_letter = 'ABCDEFGHIJ'
    return List_letter[column] + f'{row + 1}'

def int_coordinate(str_coord):
    List_letter = 'ABCDEFGHIJ'
    if len(str_coord) == 2:
        return (int(str_coord[1]) - 1, List_letter.index(str_coord[0]))
    else:
        return (9, List_letter.index(str_coord[0]))

def Game():
    my_pole = GamePole(ships_list)
    tn.read_until(b"\n")
    hashsum_oponent = str(tn.read_until(b"\n")[: -1])[2: -1]
    tn.read_until(b"\n")
    tn.write(f'{hashsum_my_pole}'.encode() + b'\n')
    my_motion = False
    oponent_pole = [[-1 for y in range(n)] for x in range(n)]
    condition = 0
    num_shot = 0
    hit_point = []
    while True:
        for _ in range(26):
            tn.read_until(b"\n")

        stop = tn.read_until(b"\n")
        if not(b'motion' in stop):
            break
        if my_motion:
            
            if condition != 3 and sum([op.count(-1) for op in oponent_pole]) <= 25:
                len_bit = sum([op.count(-1) for op in oponent_pole])
                len_unit = 20 - sum([op.count(1) for op in oponent_pole])
                for units_list in list(combinations([i for i in range(len_bit)], len_unit)):
                    num_bit = 0
                    oponent_pole_new = [[0 for y in range(n)] for x in range(n)]
                    h = 0
                    for x in range(n):
                        for y in range(n):
                            h <<= 1
                            if oponent_pole[x][y] == 1:
                                h ^= 1
                                oponent_pole_new[x][y] = 1
                            if oponent_pole[x][y] == -1:
                                bit = 1 if num_bit in units_list else 0
                                h ^= bit
                                oponent_pole_new[x][y] = bit
                                num_bit += 1
                    if sha256(h.to_bytes(13, byteorder = 'big')).hexdigest() == hashsum_oponent:
                        condition = 3
                        break 
 
            if condition != 3:
                if condition == 0:
                    shot_x, shot_y = int_coordinate(shot_list[num_shot])
                    while oponent_pole[shot_x][shot_y] != -1:
                        num_shot += 1
                        shot_x, shot_y = int_coordinate(shot_list[num_shot])
                    tn.write(f'{shot_list[num_shot]}'.encode() + b'\n')
                    num_shot += 1
                elif condition == 1:
                    for xy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        shot_x, shot_y = hit_point[0][0] + xy[0], hit_point[0][1] + xy[1]
                        if 0 <= shot_x < n and 0 <= shot_y < n and oponent_pole[shot_x][shot_y] == -1:
                            tn.write(f'{str_coordinate(shot_x, shot_y)}'.encode() + b'\n')
                            break
                elif condition == 2:
                    if tp == 0:
                        for x in [hit_point[0][0] - 1, hit_point[-1][0] + 1]:
                            shot_x, shot_y = x, hit_point[0][1]
                            if 0 <= shot_x < n and 0 <= shot_y < n and oponent_pole[shot_x][shot_y] == -1:
                                tn.write(f'{str_coordinate(shot_x, shot_y)}'.encode() + b'\n')
                                break
                    else:
                        for y in [hit_point[0][1] - 1, hit_point[-1][1] + 1]:
                            shot_x, shot_y = hit_point[0][0], y
                            if 0 <= shot_x < n and 0 <= shot_y < n and oponent_pole[shot_x][shot_y] == -1:
                                tn.write(f'{str_coordinate(shot_x, shot_y)}'.encode() + b'\n')
                                break
                    

                is_shot = str(tn.read_until(b"\n")[: -1])[2: -1]
                if is_shot == 'away':
                    my_motion = False
                    oponent_pole[shot_x][shot_y] = 0
                elif is_shot == 'hit':
                    oponent_pole[shot_x][shot_y] = 1
                    if condition == 0:
                        hit_point = [(shot_x, shot_y)]
                        condition = 1
                    elif condition == 1:
                        if hit_point[0][1] == shot_y:
                            tp = 0
                            if shot_x == hit_point[0][0] - 1:
                                hit_point = [(shot_x, shot_y)] + hit_point
                            else:   
                                hit_point += [(shot_x, shot_y)]
                        else:
                            tp = 1
                            if shot_y == hit_point[0][1] - 1:
                                hit_point = [(shot_x, shot_y)] + hit_point
                            else:   
                                hit_point += [(shot_x, shot_y)]
                        condition = 2
                    elif condition == 2:
                        if tp == 0:
                            if shot_x == hit_point[0][0] - 1:
                                hit_point = [(shot_x, shot_y)] + hit_point
                            else:   
                                hit_point += [(shot_x, shot_y)]
                        else:
                            if shot_y == hit_point[0][1] - 1:
                                hit_point = [(shot_x, shot_y)] + hit_point
                            else:   
                                hit_point += [(shot_x, shot_y)]
                elif is_shot == 'kill':
                    oponent_pole[shot_x][shot_y] = 1
                    if len(hit_point) == 0:
                        hit_point = [(shot_x, shot_y)]
                    elif len(hit_point) == 1:
                        if hit_point[0][1] == shot_y:
                            if shot_x == hit_point[0][0] - 1:
                                hit_point = [(shot_x, shot_y)] + hit_point
                            else:   
                                hit_point += [(shot_x, shot_y)]
                        else:
                            if shot_y == hit_point[0][1] - 1:
                                hit_point = [(shot_x, shot_y)] + hit_point
                            else:   
                                hit_point += [(shot_x, shot_y)]
                    else:
                        if tp == 0:
                            if shot_x == hit_point[0][0] - 1:
                                hit_point = [(shot_x, shot_y)] + hit_point
                            else:   
                                hit_point += [(shot_x, shot_y)]
                        else:
                            if shot_y == hit_point[0][1] - 1:
                                hit_point = [(shot_x, shot_y)] + hit_point
                            else:   
                                hit_point += [(shot_x, shot_y)]
                    for y in range(hit_point[0][1] - 1, hit_point[-1][1] + 2):
                        for x in range(hit_point[0][0] - 1, hit_point[-1][0] + 2):
                            if 0 <= x < n and 0 <= y < n and not((x, y) in hit_point):
                                oponent_pole[x][y] = 0
                    hit_point = []
                    condition = 0

            else:
                f = False
                for shot_x in range(n):
                    for shot_y in range(n):
                        if oponent_pole[shot_x][shot_y] == -1 and oponent_pole_new[shot_x][shot_y] == 1:
                            tn.write(f'{str_coordinate(shot_x, shot_y)}'.encode() + b'\n')
                            oponent_pole[shot_x][shot_y] = 1
                            f = True
                            break
                    if f:
                        break
                    
                tn.read_until(b"\n")
                        
                
        else:
            shot_x, shot_y = int_coordinate(str(stop[11: -1])[2: -1])
            tn.read_until(b"\n")
            is_shot = my_pole.shot(shot_x, shot_y) 
            tn.write(f'{is_shot}'.encode() + b'\n')
            my_motion = (is_shot == 0)
            
    if stop == b"The game is over. You've won\n":
        win = 1
    else:
        win = 0
    tn.read_until(b"\n")
    oponent_bin = str(tn.read_until(b"\n")[: -1])[2: -1]
    tn.read_until(b"\n")
    tn.write(f'{my_pole_bin}'.encode() + b'\n')
    return win

def main():
    win_size = 0
    for _ in range(100):
        win = Game()
        if win == 1:
            win_size += 1
            print(f'{win_size} wins')
        else:
            print(f'Game over')
            break
    print(tn.read_until(b"\n"))
    
if __name__ == "__main__":
    main()	
```

# Flag:

rdg{Us3_m0r3_saLt_1n_th3_hAsH}
