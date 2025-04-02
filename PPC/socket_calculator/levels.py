import math, random
from int2text import int2text
from int2roman import int2roman


def _generate_brackets(_round: int) -> list[str]:
    indexes = list(range(_round+3))
    brackets = []
    if _round > 0:
        while 1:
            begin = random.choice(indexes[:-2])
            try:
                end = random.choice(indexes[begin+2:])
            except:
                end = indexes[-1]
            brackets.append((begin,end))
            indexes = indexes[end:]
            if len(indexes) < 3:
                break
    return brackets


def level_1(_round: int) -> str:
    # numbers, +-
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round, int(2*math.pow(3,_round)+10)))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-"))

    term = ""
    for i in range(_round+1):
        term += str(numbers[i]) + " "
        term += signs[i] + " "

    term += str(numbers[-1])

    return term


def level_2(_round: int) -> str:
    # numbers, +-, ()
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round, int(2*math.pow(3,_round)+10)))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-"))

    brackets = _generate_brackets(_round)
    if brackets:
        while brackets[0][0] == 0 and brackets[0][1] == _round + 2:
            brackets = _generate_brackets(_round)

    term = ""
    for i in range(_round+1):
        for bracket in brackets:
            if bracket[0] == i:
                term += "( "
                break
        term += str(numbers[i]) + " "
        for bracket in brackets:
            if bracket[1] == i+1:
                term += ") "
                break
        term += signs[i] + " "
    term += str(numbers[-1])
    if brackets and (brackets[-1][1] == _round+2):
        term += " )"

    return term


def level_3(_round: int) -> str:
    # numbers, +-, *, ()
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round, int(math.pow(3,_round)+10)))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-*"))

    brackets = _generate_brackets(_round)
    if brackets:
        while brackets[0][0] == 0 and brackets[0][1] == _round + 2:
            brackets = _generate_brackets(_round)

    term = ""
    for i in range(_round+1):
        for bracket in brackets:
            if bracket[0] == i:
                term += "( "
                break
        term += str(numbers[i]) + " "
        for bracket in brackets:
            if bracket[1] == i+1:
                term += ") "
                break
        term += signs[i] + " "

    term += str(numbers[-1])
    if brackets and (brackets[-1][1] == _round+2):
        term += " )"

    return term


def level_4(_round: int) -> str:
    # text numbers, +-
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round, int(2*math.pow(3,_round)+10)))

    str_numbers = []
    for number in numbers:
        str_numbers.append(int2text(number))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-"))

    term = ""
    for i in range(_round+1):
        term += str_numbers[i] + " "
        term += signs[i] + " "
    
    term += str_numbers[-1]

    return term


def level_5(_round: int) -> str:
    # text numbers, +-, *, ()
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round,int(2*math.pow(3,_round)+10)))

    str_numbers = []
    for number in numbers:
        str_numbers.append(int2text(number))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-*"))

    brackets = _generate_brackets(_round)
    if brackets:
        while brackets[0][0] == 0 and brackets[0][1] == _round + 2:
            brackets = _generate_brackets(_round)

    term = ""
    for i in range(_round+1):
        for bracket in brackets:
            if bracket[0] == i:
                term += "( "
                break
        term += str_numbers[i] + " "
        for bracket in brackets:
            if bracket[1] == i+1:
                term += ") "
                break
        term += signs[i] + " "

    term += str_numbers[-1]
    if brackets and (brackets[-1][1] == _round+2):
        term += " )"

    return term


def level_6(_round: int) -> str:
    # roman numbers, +-
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round, int(5*math.pow(2,_round))))

    str_numbers = []
    for number in numbers:
        str_numbers.append(int2roman(number))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-"))

    term = ""
    for i in range(_round+1):
        term += str_numbers[i] + " "
        term += signs[i] + " "

    term += str_numbers[-1]

    return term


def level_7(_round: int) -> str:
    # roman numbers, +-, *, ()
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round,1+int(4*math.pow(2,_round))))

    str_numbers = []
    for number in numbers:
        str_numbers.append(int2roman(number))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-*"))

    brackets = _generate_brackets(_round)
    if brackets:
        while brackets[0][0] == 0 and brackets[0][1] == _round + 2:
            brackets = _generate_brackets(_round)

    term = ""
    for i in range(_round+1):
        for bracket in brackets:
            if bracket[0] == i:
                term += "( "
                break
        term += str_numbers[i] + " "
        for bracket in brackets:
            if bracket[1] == i+1:
                term += ") "
                break
        term += signs[i] + " "

    term += str_numbers[-1]
    if brackets and (brackets[-1][1] == _round+2):
        term += " )"

    return term


def level_8(_round: int) -> str:
    # numbers and text numbers, +-, *, ()
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round, 1+int(4*math.pow(3,_round))))

    str_numbers = []
    for number in numbers:
        converter = random.choice([int2text, int2roman])
        str_numbers.append(converter(number))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-*"))

    brackets = _generate_brackets(_round)
    if brackets:
        while brackets[0][0] == 0 and brackets[0][1] == _round + 2:
            brackets = _generate_brackets(_round)

    term = ""
    for i in range(_round+1):
        for bracket in brackets:
            if bracket[0] == i:
                term += "( "
                break
        term += str_numbers[i] + " "
        for bracket in brackets:
            if bracket[1] == i+1:
                term += ") "
                break
        term += signs[i] + " "

    term += str_numbers[-1]
    if brackets and (brackets[-1][1] == _round+2):
        term += " )"

    return term


def level_9(_round: int) -> str:
    # numbers and roman numbers, +-, *, ()
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round, int(7*math.pow(2,_round))))

    str_numbers = []
    for number in numbers:
        converter = random.choice([int2text, int2roman])
        str_numbers.append(converter(number))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice("+-*"))

    brackets = _generate_brackets(_round)
    if brackets:
        while brackets[0][0] == 0 and brackets[0][1] == _round + 2:
            brackets = _generate_brackets(_round)

    term = ""
    for i in range(_round+1):
        for bracket in brackets:
            if bracket[0] == i:
                term += "( "
                break
        term += str_numbers[i] + " "
        for bracket in brackets:
            if bracket[1] == i+1:
                term += ") "
                break
        term += signs[i] + " "

    term += str_numbers[-1]
    if brackets and (brackets[-1][1] == _round+2):
        term += " )"

    return term


def level_10(_round: int) -> str:
    # numbers, roman and text numbers, +-, *, ()
    numbers = []
    for i in range(_round+2):
        numbers.append(random.randrange(1+_round, 1+int(4*math.pow(2,_round))))

    str_numbers = []
    for number in numbers:
        converter = random.choice([str, int2text, int2roman])
        str_numbers.append(converter(number))

    signs = []
    for i in range(_round+1):
        signs.append(random.choice(["+","-","*","plus","minus"]))

    brackets = _generate_brackets(_round)
    if brackets:
        while brackets[0][0] == 0 and brackets[0][1] == _round + 2:
            brackets = _generate_brackets(_round)

    term = ""
    for i in range(_round+1):
        for bracket in brackets:
            if bracket[0] == i:
                term += "( "
                break
        term += str_numbers[i] + " "
        for bracket in brackets:
            if bracket[1] == i+1:
                term += ") "
                break
        term += signs[i] + " "

    term += str_numbers[-1]
    if brackets and (brackets[-1][1] == _round+2):
        term += " )"

    return term

