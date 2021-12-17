import random as rand
import string

from hstest.stage_test import *
from hstest.test_case import TestCase


def randomString() -> str:
    alphabet = string.ascii_letters + string.digits + " "
    a = "".join(rand.choices(alphabet, k=rand.randrange(5, 10, 1)))
    b = "".join(rand.choices(alphabet + " ", k=rand.randrange(10, 100, 1)))
    return a + b


class Unit:
    def __init__(self, separator: str, command: str, result: str, feedback: str):
        self.isUnit = True
        self.separator = separator
        self.command = command
        self.result = result
        self.feedback = feedback

    def input(self) -> str:
        return self.command + self.separator

    def output(self) -> str:
        return self.result + self.separator


class Prompt(Unit):
    def __init__(self, separator: str, result: str, feedback: str):
        super().__init__(separator, "", result, feedback)
        self.isUnit = False

    def input(self) -> str:
        raise AttributeError


class Result:
    def __init__(self, isOk: bool, expected: str, got: str, feedback: str):
        self.isOk = isOk
        self.expected = expected
        self.got = got
        self.feedback = feedback

    def format(self) -> str:
        return f"expected to find:\n" \
               f"{self.expected}\n" \
               f"in:\n" \
               f"{self.got}\n" \
               f"{self.feedback}\n"

    def formatToHS(self) -> CheckResult:
        return CheckResult(self.isOk, self.format())


class Case:
    def __init__(self, units: List[Unit]):
        self.units = units

    def input(self) -> str:
        s = ""
        for u in self.units:
            if u.isUnit:
                s += u.input()
        return s

    def output(self) -> str:
        s = ""
        for u in self.units:
            s += u.output()

        return s

    def check(self, user_output: str) -> Result:
        remaining_user_output = user_output
        index = 0

        while True:
            u = self.units[index]
            i = remaining_user_output.find(u.result)

            if i == -1:
                return Result(False, u.result, remaining_user_output, u.feedback)
            index += 1

            if index >= len(self.units):
                return Result(True, "", "", "")

            remaining_user_output = remaining_user_output[i:]


class New:
    def __init__(self, separator: str):
        self.separator = separator

    def unit(self, command: str, result: str, feedback: str) -> Unit:
        return Unit(self.separator, command, result, feedback)

    def prompt(self, result: str, feedback: str) -> Prompt:
        return Prompt(self.separator, result, feedback)


def newCases() -> List[Case]:
    new = New("\n")

    cases = [
        Case([
            new.prompt("Enter command and data: ", "The program should ask user for a command"),
            new.unit("create This is my first record!", "create", ""),
            new.prompt("Enter command and data: ", "The program should ask user for a command"),
            new.unit("create This is my second record!", "create", ""),
            new.prompt("Enter command and data: ", "The program should ask user for a command"),
            new.unit("list", "list", ""),
            new.prompt("Enter command and data: ", "The program should ask user for a command"),
            new.unit("exit 1098", "Bye!", ""),
        ])
    ]

    for i in range(2):
        units = []

        for j in range(rand.randrange(1 + 2 * i, 3 + 2 * i)):
            units.append(new.prompt("Enter command and data: ", "The program should ask user for a command"))
            rs = randomString().partition(' ')
            units.append(new.unit(f"{rs[0]} {rs[2]}", f"{rs[0]}", ""))

        units.append(new.prompt("Enter command and data: ", "The program should ask user for a command"))
        units.append(new.unit(f"exit {randomString()}", "Bye!", ""))
        cases.append(Case(units))

    return cases


class Test(StageTest):
    def __init__(self):
        super().__init__()
        self.cases = newCases()

    def generate(self) -> List[TestCase]:
        cases = []
        for case in self.cases:
            cases.append((case.input(), case.output()))

        return TestCase.from_stepik(cases)

    def check(self, user_answer: str, correct_answer: Any) -> CheckResult:
        for case in self.cases:
            if correct_answer == case.output():
                return case.check(user_answer).formatToHS()


if __name__ == '__main__':
    Test().run_tests()
