from functools import partial
from int2text import text2int
from int2roman import roman2int


SIGNS = ["+","-","*","plus","minus"]


def smart_convert(s: str|int) -> int:
    if isinstance(s, int):
        return s
    for converter in (
        partial(int, s.replace(',','')),
        partial(text2int, s),
        partial(roman2int, s)
    ):
        try:
            return converter()
        except:
            continue
    raise NotImplementedError(f"Unknown number format: {s}")


def get_answer_new(term: list[str|int]) -> int:
    print(term)
    result = 0
    i: int = 0
    lhs: int = 0
    while i<len(term):
        el = term[i]
        match el:
            case "(":
                end = term.index(")", i+1)
                result += get_answer_new(term[i+1:end])
                i = end + 1
            case "*":
                result *= get_answer_new(term[i+1:])
                i += 2
            case "+":
                result += get_answer_new(term[i+1:])
                i += 2
            case "-":
                result -= get_answer_new(term[i+1:])
                i += 2
            case _:
                result += smart_convert(el)
                i += 1
    return result


def mysplit(term) -> list:
    global SIGNS
    result = []
    number = ""
    for word in term.split(" "):
        word = word.strip()
        if word in SIGNS or word in "()":
            if number != "":
                result.append(number.strip())
            result.append(word)
            number = ""
        else:
            if number:
                number += " "
            number += word
    if number != "":
        result.append(number.strip())
    return result


def get_answer(term: list[str|int]) -> int:
    #считаем выражение в скобках
    while "(" in term:
        start = term.index("(")
        end = term.index(")", start+1)
        # print(term)
        term[start] = get_answer(term[start+1:end])
        del term[start+1:end+1]
    #выполняем умножение
    while "*" in term:
        index = term.index("*")
        term[index-1] = smart_convert(term[index-1])*smart_convert(term[index+1])
        del term[index:index+2]
    #складываем и вычитаем простое выражение
    result = smart_convert(term[0])
    for i in range(1,len(term),2):
        if term[i] == "+" or term[i] == "plus":
            result += smart_convert(term[i+1])
        elif term[i] == "-" or term[i] == "minus":
            result -= smart_convert(term[i+1])
    return result

