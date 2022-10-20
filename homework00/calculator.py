import math
import typing as tp


def calc1(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:
    if command == "+":
        return num_1 + num_2
    if command == "-":
        return num_1 - num_2
    if command == "/":
        if num_2 != 0:
            return num_1 / num_2
        return "на ноль делить нельзя"
    if command == "*":
        return num_1 * num_2
    if command == "** n":
        return num_1**num_2
    if command == "** 2":
        return num_1**2
    if command == "convert":
        num_1 = int(num_1)
        num_2 = int(num_2)
        if num_1 < 0:
            return "число должно быть неотрицательным"
        if not 2 <= num_2 <= 9:
            return "неподходящая система счисления"
        temporary_variable = ""
        while num_1 > 0:
            temporary_variable = str(num_1 % num_2) + temporary_variable
            num_1 = num_1 // num_2
        return temporary_variable
    return f"неизвестный оператор: {command!r}."


def calc2(num_1: float, command: str) -> tp.Union[float, str]:
    if command == "sin":
        return math.sin(num_1)
    if command == "cos":
        return math.cos(num_1)
    if command == "tg":
        return math.tan(num_1)
    if command == "log":
        if num_1 > 0:
            return math.log(num_1)
        return "логарифм должен быть строго больше нуля"
    if command == "lg":
        if num_1 > 0:
            return math.log10(num_1)
        return "десятичный логарифм должен быть строго больше нуля"
    return f"неизвестный оператор: {command!r}."


def match_case_calc1(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:
    match command:
        case "+":
            return num_1 + num_2
        case "-":
            return num_1 - num_2
        case "/":
            if num_2 != 0:
                return num_1 / num_2
            return "на ноль делить нельзя"
        case "*":
            return num_1 * num_2
        case "**":
            return num_1**num_2
        case "convert":
            num_1 = int(num_1)
            num_2 = int(num_2)
            if num_1 < 0:
                return "число должно быть неотрицательным"
            if not 2 <= num_2 <= 9:
                return "неподходящая система счисления"
            temporary_variable = ""
            while num_1 > 0:
                temporary_variable = str(num_1 % num_2) + temporary_variable
                num_1 = num_1 // num_2
            return temporary_variable
        case _:
            return f"неизвестный оператор: {command!r}."


def match_case_calc2(num_1: float, command: str) -> tp.Union[float, str]:  # type: ignore
    match command:
        case "**2":
            return num_1**2
        case "sin":
            return math.sin(num_1)
        case "cos":
            return math.cos(num_1)
        case "tg":
            return math.tan(num_1)
        case "log":
            if num_1 > 0:
                return math.log(num_1)
            return "логарифм должен быть строго больше нуля"
        case "lg":
            if num_1 > 0:
                return math.log10(num_1)
            return "десятичный логарифм должен быть строго больше нуля"
        case _:
            return f"неизвестный оператор: {command!r}."



if __name__ == "__main__":
    operators_1 = ("+", "-", "/", "*", "convert", "**")
    operators_2 = ("**2", "sin", "cos", "tg", "log", "lg")
    while True:
        COMMAND = input("Введите команду > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        if COMMAND in operators_1:
            NUM_1 = float(input("Введите число > "))
            NUM_2 = float(input("Введите число > "))
            print(match_case_calc1(NUM_1, NUM_2, COMMAND))
        elif COMMAND in operators_2:
            NUM_1 = float(input("Введите число > "))
            print(match_case_calc2(NUM_1, COMMAND))
