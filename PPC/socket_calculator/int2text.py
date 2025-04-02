import sys


_nums = (
    '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
    'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen',
    'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen')

_tens = ('','',
    'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty',
    'Ninety')

_scales = ("Hundred", "Thousand", "Million", "Billion", "Trillion")


def int2text(number):
    """Converts an integer to the English language name of that integer.
    
    E.g. converts 1 to "One". Supports numbers 0 to 999999.
    This can be used in LilyPond identifiers (that do not support digits).
    
    """
    result = []
    if number >= 10**9:
        billions, number = divmod(number, 10**9)
        if number:
            result.append(int2text(billions) + " " + "Billion" + " ")
        else:
            result.append(int2text(billions) + " " + "Billion")
    
    if number >= 10**6:
        millions, number = divmod(number, 10**6)
        if number:
            result.append(int2text(millions) + " " + "Million" + " ")
        else:
            result.append(int2text(millions) + " " + "Million")
    
    if number >= 10**3:
        hundreds, number = divmod(number, 10**3)
        if number:
            result.append(int2text(hundreds) + " " + "Thousand" + " ")
        else:
            result.append(int2text(hundreds) + " " + "Thousand")
    
    if number >= 100:
        tens, number = divmod(number, 100)
        if number:
            result.append(_nums[tens] + " " + "Hundred" + " ")
        else:
            result.append(_nums[tens] + " " + "Hundred")
    if number < 20:
        result.append(_nums[number])
    else:
        tens, number = divmod(number, 10)
        if _nums[number]:
            result.append(_tens[tens] + " " + _nums[number])
        else:
            result.append(_tens[tens])
    text = "".join(result)
    return text or 'Zero'


def text2int(textnum, numwords={}):
    if not numwords:
        # units = [
        #     "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
        #     "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
        #     "Sixteen", "Seventeen", "Eighteen", "Nineteen",
        # ]

        # tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

        # scales = ["Hundred", "Thousand", "Million", "Billion", "Trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(_nums):    numwords[word] = (1, idx)
        for idx, word in enumerate(_tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(_scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise ValueError("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


if __name__ == "__main__":
    number = int(sys.argv[1])
    strnumber = int2text(number)
    print(strnumber)
