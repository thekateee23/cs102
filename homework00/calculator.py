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
        b = ""
        while num_1 > 0:
            b = str(num_1 % num_2) + b
            num_1 = num_1 // num_2
        return b
    else:
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
    else:
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
            b = ""
            while num_1 > 0:
                b = str(num_1 % num_2) + b
                num_1 = num_1 // num_2
            return b
        case _:
            return f"неизвестный оператор: {command!r}."
    return f"неизвестный оператор: {command!r}."


def match_case_calc2(num_1: float, command: str) -> tp.Union[float, str]:
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
            else:
                return "логарифм должен быть строго больше нуля"
        case "lg":
            if num_1 > 0:
                return math.log10(num_1)
            else:
                return "десятичный логарифм должен быть строго больше нуля"
        case "ln":
            if num_1 > 0:
                return math.log(num_1)
            else:
                return "натуральный логарифм должен быть строго больше нуля"
        case _:
            return f"неизвестный оператор: {command!r}."
    return f"неизвестный оператор: {command!r}."


def count_result(opers: list[str]) -> str:
    operators_1 = ("+", "-", "/", "*")
    operators_2 = ("sin", "cos", "tg", "lg", "ln")
    if opers[0] == "-" and (opers[1].isdigit() or "." in opers[1]):
        opers[0:2] = ["-" + opers[1]]

    for i in range(2, len(opers)):
        if (
            not (opers[i].isdigit() or "." in opers[i])
            and opers[i - 1] == "-"
            and (opers[i].isdigit() or "." in opers[i])
        ):
            opers[i - 1 : i + 1] = ["-" + opers[i]]

    for i in operators_2:
        while i in opers:
            ind = opers.index(i)
            opers[ind : ind + 2] = [match_case_calc2(float(opers[ind + 1]), opers[ind])]
    while "**" in opers:
        ind = opers.index("**")
        opers[ind - 1 : ind + 2] = [float(opers[ind - 1]) ** float(opers[ind + 1])]
    while "/" in opers or "*" in opers:
        ind_1 = 10**9
        ind_2 = 10**9
        if "/" in opers:
            ind_1 = opers.index("/")
        if "*" in opers:
            ind_2 = opers.index("*")
        if ind_1 < ind_2:
            opers[ind_1 - 1 : ind_1 + 2] = [float(opers[ind_1 - 1]) / float(opers[ind_1 + 1])]
        else:
            opers[ind_2 - 1 : ind_2 + 2] = [float(opers[ind_2 - 1]) * float(opers[ind_2 + 1])]
    while "+" in opers or "-" in opers and len(opers) > 2:
        ind_1 = 10**9
        ind_2 = 10**9
        if "+" in opers:
            ind_1 = opers.index("+")
        if "-" in opers:
            ind_2 = opers.index("-")
        if ind_1 < ind_2:
            opers[ind_1 - 1 : ind_1 + 2] = [float(opers[ind_1 - 1]) + float(opers[ind_1 + 1])]
        else:
            opers[ind_2 - 1 : ind_2 + 2] = [float(opers[ind_2 - 1]) - float(opers[ind_2 + 1])]
    if opers[0] == "-":
        opers = [str(-1 * float(opers[1]))]
    return str(opers[0])


def calc(comm: str) -> tp.Optional[tp.Tuple[str, int]]:
    comm = comm.replace("^", "**")
    operators_1 = ("+", "-", "/", "*", "convert", "**")
    operators_2 = ("sin", "cos", "tg", "log", "lg", "ln")
    comm = "".join(comm.split())
    count = 0
    operations = []
    while count < len(comm):
        if not comm[count].isdigit():
            if comm[count] == "(":
                tmp = calc(comm[count + 1 :])
                if len(tmp) == 2:
                    tmp, count_tmp = calc(comm[count + 1 :])
                    count += count_tmp + 1
                    operations.append(tmp)
                else:
                    return None
            elif comm[count] == ")":
                count += 1
                return count_result(operations), count
            else:
                operation = comm[count]
                count += 1
                while (
                    count < len(comm)
                    and len(operation) < 3
                    and not (operation in operators_1 or operation in operators_2)
                ):
                    operation += comm[count]
                    count += 1
                if operation == "*" and comm[count] == "*":
                    count += 1
                    operation = "**"
                if count >= len(comm) or len(operation) > 3:
                    return None
                operations.append(operation)
        else:
            dig = comm[count]
            dop = ""
            count += 1
            while count < len(comm) and (comm[count].isdigit() or comm[count] == "."):
                dig += comm[count]
                count += 1
            operations.append(dig)
    return count_result(operations), count


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
        elif len(COMMAND) >= 3:
            result = calc(COMMAND)
            if len(result) == 2:
                print(calc(COMMAND)[0])
            else:
                print("Неправильный формат ввода")
        else:
            NUM_1 = 0
            NUM_2 = 0
            print(match_case_calc1(NUM_1, NUM_2, COMMAND))
