import sys


_roman_numerals = {"M": 1000,"CM": 900,"D": 500,"CD": 400,"C": 100,"XC": 90,"L": 50,"XL": 40,"X": 10,"IX": 9,"V": 5,"IV": 4,"I": 1}


def int2roman(n: int) -> str:
    """Convert an integer value to a roman number.
    E.g. 1 -> "I", 12 -> "XII", 2015 -> "MMXV"
    n has to be > 1.
    """
    global _roman_numerals
    if n < 1:
        raise ValueError('Roman numerals must be positive integers, got %s' % n)
    roman = []
    for ltr, num in _roman_numerals.items():
        k, n = divmod(n, num)
        roman.append(ltr * k)
    return "".join(roman)


def roman2int(number):
    global _roman_numerals
    index = 0
    intResult = 0
    for romanNumeral, integer in _roman_numerals.items():
        romanNumeral_len = len(romanNumeral)
        while number[index : index + romanNumeral_len] == romanNumeral:
            intResult += integer
            index += romanNumeral_len
    if intResult < 1:
        raise ValueError(f"Unknown roman number: {number}")
    return intResult


if __name__ == "__main__":
    number = int(sys.argv[1])
    romannumber = int2roman(number)
    print(romannumber)
    number = roman2int(romannumber)
    print(number)
