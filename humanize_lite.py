"""Pure python module for displaying words to humans"""


USUAL_NUMBERS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
}

DECADES = {
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
}

GROUP_SUFFIXES = (
    "",
    "thousand",
    "million",
    "billion",
    "trillion",
    "quadrillion",
    "quintillion",
    "sextillion",
    "septillion",
    "octillion",
    "nonillion",
    "decillion",
    "are you so bored?",
)


def spell_usual_number(number):
    if number >= 20:
        raise ValueError("Expected a number under 20")

    return USUAL_NUMBERS[number]


def spell_two_digits_number(number):
    if number > 99:
        raise ValueError("Expected a number under 100")

    if number < 20:
        return spell_usual_number(number)

    decades = ((number % 100) // 10) * 10
    ones = number % 10

    words = list()
    if decades:
        words.append(f"{DECADES[decades]}")
    if ones:
        words.append(spell_usual_number(ones))

    return "-".join(words)


def spell_number_group(number):
    if number > 999:
        raise ValueError("Group number cannot be larger than 999")

    hundreds = number // 100
    two_digits = number % 100

    words = list()
    if hundreds:
        words.append(f"{spell_usual_number(hundreds)} hundred")
        if two_digits:
            words.append("and")
    if two_digits:
        words.append(spell_two_digits_number(two_digits))

    return " ".join(words)


def pluralize(noun, quantity):
    assert noun

    if quantity > 1:
        last_letter = noun[-1]
        if last_letter == "y":
            return noun[:-1] + "ies"
        elif last_letter == "s":
            return noun + "es"
        else:
            return noun + "s"
    return noun


def spell_number(number):
    words = list()
    group_index = 0
    subgroup = 0

    while number is not None:
        subgroup = number % 1000

        if group_index:
            limit = min(group_index, len(GROUP_SUFFIXES) - 1)
            words.append(GROUP_SUFFIXES[limit])

        words.append(spell_number_group(subgroup))

        number = number // 1000
        group_index += 1
        if number == 0:
            number = None

    return " ".join(reversed(words)) or "zero"


if __name__ == "__main__":
    for x in range(35):
        print(x, "->", spell_number(x))

    for x in [21, 1013, 29, 1_999, 1_002_001, 1_392_471, 5_629_296]:
        print(f"{x:,}", "->", spell_number(x))

    words = ["society", "bear", "city", "bus"]
    for word in words:
        print(word, "->", spell_number(2), pluralize(word, 2))
