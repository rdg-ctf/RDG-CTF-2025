from random import choice, randint
from hashlib import sha256

n = 10
Field_opponent = [[0 for i in range(n)] for j in range(n)]
Dict_ships = {4: 1, 3: 2, 2: 3, 1: 4}
Dict_ships_opponent = {4: 1, 3: 2, 2: 3, 1: 4}
condition = 0
r_hit, c_hit = 0, 0
points_hit = [(0, 0)]
direction = True

class Ship():
    def __init__(self, x, y, length, tp = 0):
        self.x = x
        self.y = y
        self.length = length
        self.tp = tp
        self.coords_list = self.get_coords_list()
        self.cells = {coord: 0 for coord in self.coords_list}

    def set_start_coords(self, x, y):
        self.x = x
        self.y = y

    def get_start_coords(self):
        return (self.x, self.y)

    def get_coords_list(self):
        if self.tp == 0:
            return [(self.x + i, self.y) for i in range(self.length)]
        else:
            return [(self.x, self.y + i) for i in range(self.length)]

    def get_oreol_list(self):
        if self.tp == 0:
            res = []
            for j in range(3):
                res += [(self.x - 1 + i, self.y - 1 + j) for i in range(self.length + 2) if is_filed(self.x - 1 + i, self.y - 1 + j)]
        else:
            res = []
            for j in range(3):
                res += [(self.x - 1 + j, self.y - 1 + i) for i in range(self.length + 2) if is_filed(self.x - 1 + j, self.y - 1 + i)]
        return res

    def is_collide(self, other_ship):
        self_oreol = self.get_oreol_list()
        other_coords_list = other_ship.coords_list
        for other_coords in other_coords_list:
            if other_coords in self_oreol:
                return True
        return False

    def is_out_pole(self):
        if not(0 <= self.x < n and 0 <= self.y < n):
            return True
        if not(0 <= self.x + (self.length - 1) * (1 - self.tp) < n and 0 <= self.y + (self.length - 1) * self.tp < n):
            return True
        return False

    def is_hit(self, x, y):
        return (x, y) in self.coords_list

    def hit(self, x, y):
        self.cells[(x, y)] = 1

    def is_kill(self):
        return all([self.cells[k] == 1 for k in self.cells.keys()])

class GamePole():
    def __init__(self):
        filed = [(x, y) for x in range(n) for y in range(n)]
        self.ships_list = []
        for length in Dict_ships.keys():
            for _ in range(Dict_ships[length]):
                while True:
                    tp = randint(0, 1)
                    if tp == 0:
                        x, y = choice([coords for coords in filed if coords[0] <= n - length])
                    else:
                        x, y = choice([coords for coords in filed if coords[1] <= n - length])
                    ship = Ship(x, y, length, tp)
                    collide = False
                    for s in self.ships_list:
                        if ship.is_collide(s):
                            collide = True
                            break
                    if not collide:
                        oreol = ship.get_oreol_list()
                        filed = [coords for coords in filed if not(coords in oreol)]
                        self.ships_list.append(ship)
                        break
        self.filed = [[1 for i in range(n)] for j in range(n)]
        for ship in self.ships_list:
            for (x, y) in ship.coords_list:
                self.filed[x][y] = -1
        self.filed_player = [[0 for i in range(n)] for j in range(n)]

    def get_ships(self):
        return self.ships_list

    def get_filed(self):
        return self.filed

    def get_filed_player(self):
        return self.filed_player

    def shot(self, x, y):
        if self.filed[x][y] == 1:
            self.filed_player[x][y] = 1
            return 0
        for ship in self.ships_list:
            if ship.is_hit(x, y):
                self.filed_player[x][y] = -1
                ship.hit(x, y)
                if ship.is_kill():
                    for coord in [c for c in ship.get_oreol_list() if not(c in ship.coords_list)]:
                        self.filed_player[coord[0]][coord[1]] = 1
                    self.ships_list.remove(ship)
                    return 2
                return 1

    def is_game_over(self):
        return len(self.ships_list) == 0

def is_filed(x, y):
    return 0 <= x < n and 0 <= y < n
    
def weight_calculation():
    Field_weight = [[0 for i in range(n)] for j in range(n)]
    for L_ships in Dict_ships_opponent.keys():
        if L_ships != 1 and Dict_ships_opponent[L_ships] != 0:
            for row in range(n):
                for column in range(n - L_ships + 1):
                    if Field_opponent[row][column: column + L_ships] == [0]*L_ships:
                        for c in range(column, column + L_ships):
                            Field_weight[row][c] += Dict_ships_opponent[L_ships]
            for column in range(n):
                for row in range(n - L_ships + 1):
                    if all([Field_opponent[r][column] == 0 for r in range(row, row + L_ships)]):
                        for r in range(row, row + L_ships):
                            Field_weight[r][column] += Dict_ships_opponent[L_ships]
    for r in range(n):
        for c in range(n):
            if Field_opponent[r][c] != 0:
                Field_weight[r][c] = -1
    return Field_weight

def Best_choice():
    Field_weight = weight_calculation()
    maximum = 0
    List_maximum = []
    for row in range(n):
        for column in range(n):
            if Field_weight[row][column] > maximum:
                maximum = Field_weight[row][column]
                List_maximum = [(row, column)]
            elif Field_weight[row][column] == maximum:
                List_maximum += [(row, column)]
    return choice(List_maximum)

def weight_hit_one():
    weight = {(r_hit - 1, c_hit): 0, (r_hit + 1, c_hit): 0, (r_hit, c_hit - 1): 0, (r_hit, c_hit + 1): 0}
    for L_ships in Dict_ships_opponent.keys():
        if L_ships != 1 and L_ships != 2 and Dict_ships_opponent[L_ships] != 0:
            for row in range(r_hit - L_ships + 1, r_hit + 1):
                if 0 <= row < n and 0 <= row + L_ships < n:
                    if all([Field_opponent[r][c_hit] == 0 or r == r_hit for r in range(row, row + L_ships)]):
                        if row == r_hit - L_ships + 1:
                            weight[(r_hit - 1, c_hit)] += Dict_ships_opponent[L_ships]
                        elif row == r_hit:
                            weight[(r_hit + 1, c_hit)] += Dict_ships_opponent[L_ships]
                        else:
                            weight[(r_hit - 1, c_hit)] += Dict_ships_opponent[L_ships]
                            weight[(r_hit + 1, c_hit)] += Dict_ships_opponent[L_ships]
            for column in range(c_hit - L_ships + 1, c_hit + 1):
                if 0 <= column < n and 0 <= column + L_ships < n:
                    if all([Field_opponent[r_hit][c] == 0 or c == c_hit for c in range(column, column + L_ships)]):
                        if column == c_hit - L_ships + 1:
                            weight[(r_hit, c_hit - 1)] += Dict_ships_opponent[L_ships]
                        elif column == c_hit:
                            weight[(r_hit, c_hit + 1)] += Dict_ships_opponent[L_ships]
                        else:
                            weight[(r_hit, c_hit - 1)] += Dict_ships_opponent[L_ships]
                            weight[(r_hit, c_hit + 1)] += Dict_ships_opponent[L_ships]
    for r, c in weight.keys():
        if 0 <= r < n and 0 <= c < n:
            if Field_opponent[r][c] != 0:
                weight[(r, c)] = -1
        else:
            weight[(r, c)] = -1
    return weight

def Best_choice_hit_one():
    weight = weight_hit_one()
    maximum = 0
    List_maximum = []
    for row, column in weight.keys():
            if weight[(row, column)] > maximum:
                maximum = weight[(row, column)]
                List_maximum = [(row, column)]
            elif weight[(row, column)] == maximum:
                List_maximum += [(row, column)]
    return choice(List_maximum)

def weight_hit_two():
    if direction:
        column = points_hit[0][1]
        r_left = points_hit[0][0]
        r_right = points_hit[-1][0]
        weight = {(r_left - 1, column): 0, (r_right + 1, column): 0}
        for L_ships in Dict_ships_opponent.keys():
            if L_ships != 1 and L_ships != 2 and L_ships != 3 and Dict_ships_opponent[L_ships] != 0:
                for row in range(r_right - L_ships + 1, r_left + 1):
                    if 0 <= row < n and 0 <= row + L_ships < n:
                        if all([Field_opponent[r][column] == 0 or r_left <= r <= r_right for r in range(row, row + L_ships)]):
                            if row == r_right - L_ships + 1:
                                weight[(r_left - 1, column)] += Dict_ships_opponent[L_ships]
                            elif row == r_left:
                                weight[(r_right + 1, column)] += Dict_ships_opponent[L_ships]
                            else:
                                weight[(r_left - 1, column)] += Dict_ships_opponent[L_ships]
                                weight[(r_right + 1, column)] += Dict_ships_opponent[L_ships]
    else:
        row = points_hit[0][0]
        c_upper = points_hit[0][1]
        c_lower = points_hit[-1][1]
        weight = {(row, c_upper - 1): 0, (row, c_lower + 1): 0}
        for L_ships in Dict_ships_opponent.keys():
            if L_ships != 1 and L_ships != 2 and L_ships != 3 and Dict_ships_opponent[L_ships] != 0:
                for column in range(c_lower - L_ships + 1, c_upper + 1):
                    if 0 <= column < n and 0 <= column + L_ships < n:
                        if all([Field_opponent[row][c] == 0 or c_upper <= c <= c_lower for c in range(column, column + L_ships)]):
                            if column == c_lower - L_ships + 1:
                                weight[(row, c_upper - 1,)] += Dict_ships_opponent[L_ships]
                            elif column == c_upper:
                                weight[(row, c_lower + 1)] += Dict_ships_opponent[L_ships]
                            else:
                                weight[(row, c_upper - 1)] += Dict_ships_opponent[L_ships]
                                weight[(row, c_lower + 1)] += Dict_ships_opponent[L_ships]
    for r, c in weight.keys():
        if 0 <= r < n and 0 <= c < n:
            if Field_opponent[r][c] != 0:
                weight[(r, c)] = -1
        else:
            weight[(r, c)] = -1
    return weight

def Best_choice_hit_two():
    weight = weight_hit_two()
    maximum = 0
    List_maximum = []
    for row, column in weight.keys():
            if weight[(row, column)] > maximum:
                maximum = weight[(row, column)]
                List_maximum = [(row, column)]
            elif weight[(row, column)] == maximum:
                List_maximum += [(row, column)]
    return choice(List_maximum)  

def choosing_an_action():
    if condition == 0:
        return Best_choice()
    elif condition == 1:
        return Best_choice_hit_one()
    else:
        return Best_choice_hit_two()

def complement_points_hit(r, c):
    global condition
    global r_hit
    global c_hit
    global points_hit
    global direction
    if condition == 0:
        r_hit, c_hit = r, c
        points_hit = [(r, c)]
        condition = 1
    elif condition == 1:
        if (r, c) == (r_hit, c_hit + 1):
            direction = False
            points_hit += [(r_hit, c_hit + 1)]
        elif (r, c) == (r_hit, c_hit - 1):
            direction = False
            points_hit = [(r_hit, c_hit - 1)] + points_hit
        elif (r, c) == (r_hit + 1, c_hit):
            direction = True
            points_hit += [(r_hit + 1, c_hit)]
        else:
            direction = True
            points_hit = [(r_hit - 1, c_hit)] + points_hit
        condition = 2
    else:
        if direction:
            if r == points_hit[0][0] - 1:
                points_hit = [(r, points_hit[0][1])] + points_hit
            else:
                points_hit += [(r, points_hit[0][1])]
        else:
            if c == points_hit[0][1] - 1:
                points_hit = [(points_hit[0][0], c)] + points_hit
            else:
                points_hit += [(points_hit[0][0], c)]

def killed_ship():
    if len(points_hit) == 1:
        row, column = points_hit[0]
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if (r, c) != (row, column) and 0 <= r < n and 0 <= c < n:
                    Field_opponent[r][c] = 1
        Dict_ships_opponent[1] -= 1
    elif direction:
        column = points_hit[0][1]
        r_left = points_hit[0][0]
        r_right = points_hit[-1][0]
        for r in range(r_left - 1, r_right + 2):
            for c in range(column - 1, column + 2):
                if not((r, c) in points_hit) and 0 <= r < n and 0 <= c < n:
                    Field_opponent[r][c] = 1
        Dict_ships_opponent[len(points_hit)] -= 1
    else:
        row = points_hit[0][0]
        c_upper = points_hit[0][1]
        c_lower = points_hit[-1][1]
        for c in range(c_upper - 1, c_lower + 2):
            for r in range(row - 1, row + 2):
                if not((r, c) in points_hit) and 0 <= r < n and 0 <= c < n:
                    Field_opponent[r][c] = 1
        Dict_ships_opponent[len(points_hit)] -= 1

def step_game(answer, r, c):
    global condition
    if answer == 0:
        Field_opponent[r][c] = 1
    elif answer == 1:
        Field_opponent[r][c] = -1
        complement_points_hit(r, c)
    else:
        Field_opponent[r][c] = -1
        complement_points_hit(r, c)
        killed_ship()
        condition = 0
    return choosing_an_action()

def str_f(f):
    if f == 0:
        return '.'
    elif f == 1:
        return 'o'
    else:
        return 'x'

def str_num(num):
    return '10 ' if num == 9 else f'{num + 1}  '

def str_coordinate(row, column):
    List_letter = 'ABCDEFGHIJ'
    return List_letter[column] + f'{row + 1}'

def int_coordinate(str_coord):
    List_letter = 'ABCDEFGHIJ'
    if len(str_coord) == 2:
        return (int(str_coord[1]) - 1, List_letter.index(str_coord[0]))
    else:
        return (9, List_letter.index(str_coord[0]))
    
def str_field(Field):
    str_res = '   A B C D E F G H I J\n'
    str_res += '\n'.join([str_num(row) + ' '.join([str_f(Field[row][column]) for column in range(n)]) for row in range(n)])
    return str_res

def Gameover():
    global Field_opponent
    global Dict_ships
    global Dict_ships_opponent
    global condition
    global r_hit
    global c_hit
    global points_hit
    global direction
    Field_opponent = [[0 for i in range(n)] for j in range(n)]
    Dict_ships = {4: 1, 3: 2, 2: 3, 1: 4}
    Dict_ships_opponent = {4: 1, 3: 2, 2: 3, 1: 4}
    condition = 0
    r_hit, c_hit = 0, 0
    points_hit = [(0, 0)]
    direction = True

def field_to_bin(field):
    h = ''
    for x in range(n):
        for y in range(n):
            if field[x][y] == 1:
                h += '0'
            if field[x][y] == -1:
                h += '1'
    return h

def hashsum(h):
    h = int(h, 2).to_bytes(13, byteorder = 'big')
    return sha256(h).hexdigest()

def Game():
    Field_self = GamePole()
    Field_self_bin = field_to_bin(Field_self.get_filed())
    print('hash of my field: ')
    print(hashsum(Field_self_bin))
    print('send your hash: ')
    hash_oponent = input()
    motion = True
    r, c = Best_choice()
    while True:
        print(f'your field:\n{str_field(Field_opponent)}\n')
        print(f'my field:\n{str_field(Field_self.get_filed_player())}\n')
        if all([Dict_ships_opponent[k] == 0 for k in Dict_ships_opponent.keys()]):
            print("The game is over. You've lost")
            win = 0
            field_p = Field_opponent.copy()
            Gameover()
            break
        if Field_self.is_game_over():
            print("The game is over. You've won")
            win = 1
            field_p = Field_opponent.copy()
            Gameover()
            break
        if motion:
            print(f'my motion: {str_coordinate(r, c)}')
            print('is hit? (away - 0, hit - 1, kill - 2):')
            p = int(input())
            r, c = step_game(p, r, c)
            if p == 0:
                motion = False
        else:
            while True:
                print('yor motion: ')
                x, y = int_coordinate(input())
                if Field_self.get_filed_player()[x][y] != 0:
                    print('Have you shot this cage before')
                else:
                    break
            p = Field_self.shot(x, y)
            if p == 0:
                motion = True
                print('away')
            elif p == 1:
                print('hit')
            else:
                print('kill')
    print('my field is in binary form:')
    print(Field_self_bin)
    print('you field is in binary form:')
    field_oponent_bin = input()
    field_oponent = [[0 for y in range(n)] for x in range(n)]
    for x in range(n):
        for y in range(n):
            if field_oponent_bin[n*x + y] == '1':
                field_oponent[x][y] = 1
    if not(pruff_filed(field_oponent)):
        return 'Your field is constructed incorrectly'
    for x in range(n):
        for y in range(n):
            if field_oponent[x][y] == 0 and field_p[x][y] == -1:
                return 'The playing fields do not match'
            elif field_oponent[x][y] == 1 and field_p[x][y] == 1:
                return 'The playing fields do not match'
    if hashsum(field_oponent_bin) != hash_oponent:
        return 'hash does not match'
    return win

def pruff_filed(filed):
    ships_dickt = {4: 1, 3: 2, 2: 3, 1: 4}
    ships_list = []
    filed_new = [(x, y) for x in range(n) for y in range(n)]
    for x in range(n):
        for y in range(n):
            if filed[x][y] == 1:
                stat = (x, y)
                tp = 0
                length = 1
                if (x, y) in filed_new:
                    filed_new.remove((x, y))
                else:
                    continue
                if x + 1 < n and filed[x+1][y] == 1:
                    tp = 0
                    length += 1
                    while x + length < n and filed[x + length][y] == 1:
                        length += 1
                if y + 1 < n and filed[x][y+1] == 1:
                    tp = 1
                    length += 1
                    while y + length < n and filed[x][y + length] == 1:
                        length += 1
                if length > 4:
                    return False
                ships_list += [Ship(x, y, length, tp)]
                ships_dickt[length] -= 1
                if ships_dickt[length] == -1:
                    return False
                filed_new = [(c[0], c[1]) for c in filed_new if not((c[0], c[1]) in ships_list[-1].coords_list)]
    for k in ships_dickt.keys():
        if ships_dickt[k] != 0:
            return False
    for i_ship in range(1, len(ships_list)):
        for j_ship in range(i_ship):
            if ships_list[i_ship].is_collide(ships_list[j_ship]):
                return False
    return True

flag = 'rdg{Us3_m0r3_saLt_1n_th3_hAsH}'

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
