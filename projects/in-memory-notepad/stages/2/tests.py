import random as rand
import string

from hstest.stage_test import *
from hstest.test_case import TestCase


class Unit:
    def __init__(self, isExecutable: bool, separator: str, command: str, expectedResult: str, feedback: str):
        self.isExecutable = isExecutable
        self.separator = separator
        self.command = command
        self.expectedResult = expectedResult
        self.feedback = feedback

    def input(self) -> str:
        if self.isExecutable:
            return self.command + self.separator
        else:
            return ""

    def output(self) -> str:
        return self.expectedResult + self.separator


class Result:
    def __init__(self, isOk: bool, expected: str, got: str, feedback: str):
        self.isOk = isOk
        self.expected = expected
        self.got = got
        self.feedback = feedback

    def format(self) -> str:
        if self.isOk:
            return "You've passed!"
        else:
            return f"{self.feedback}\n" \
                   f"\n" \
                   f"Expected to find:\n" \
                   f'"{self.expected}"\n' \
                   f"in:\n" \
                   f'"{self.got}"\n'


class New:
    def __init__(self, separator: str):
        self.separator = separator

    def command(self, command: str, result: str, feedback: str) -> Unit:
        return Unit(True, self.separator, command, result, feedback)

    def prompt(self, result: str, feedback: str) -> Unit:
        return Unit(False, self.separator, "", result, feedback)


class Checker:
    def check(self, units: List[Unit], userOutput: str) -> Result:
        raise NotImplementedError


class MainChecker(Checker):
    def check(self, units: List[Unit], userOutput: str) -> Result:
        remainingUserOutput = userOutput
        index = 0

        while True:
            u = units[index]
            i = remainingUserOutput.find(u.expectedResult)

            if i == -1:
                return Result(False, u.expectedResult, remainingUserOutput, u.feedback)
            index += 1

            if index >= len(units):
                return Result(True, "", "", "")

            remainingUserOutput = remainingUserOutput[i:]


class Case:
    def __init__(self, checker: Checker, units: List[Unit]):
        self.units = units
        self.checker = checker

    def input(self) -> str:
        s = ""
        for u in self.units:
            s += u.input()
        return s

    def output(self) -> str:
        s = ""
        for u in self.units:
            s += u.output()
        return s

    def check(self, userOutput: str) -> Result:
        return self.checker.check(self.units, userOutput)


class HSTest(StageTest):
    def __init__(self, cases: List[Case]):
        super(HSTest, self).__init__()
        self.cases = cases

    def generate(self) -> List[TestCase]:
        cases = []
        for case in self.cases:
            cases.append((case.input(), case.output()))
        return TestCase.from_stepik(cases)

    def check(self, user_answer: str, correct_answer: Any) -> CheckResult:
        for case in self.cases:
            if correct_answer == case.output():
                result = case.check(user_answer)
                return CheckResult(result.isOk, result.format())


def randomString() -> str:
    alphabet = string.ascii_letters + string.digits + " "
    a = "".join(rand.choices(alphabet, k=rand.randrange(5, 10, 1)))
    b = "".join(rand.choices(alphabet + " ", k=rand.randrange(10, 100, 1)))
    return a + b


def main():
    new = New("\n")
    checker = MainChecker()

    prompt_WaitingForUserInput = new.prompt("Enter command and data: ", "The program should ask user for a command")

    cases = [
        Case(checker, [
            prompt_WaitingForUserInput,
            new.command("create This is my first record!", "The note was successfully created", ""),
            prompt_WaitingForUserInput,
            new.command("create This is my second record!", "The note was successfully created", ""),
            prompt_WaitingForUserInput,
            new.command("list",
                        "Index 0: This is my first record!\n"
                        "Index 1: This is my second record!\n",
                        ""),
            prompt_WaitingForUserInput,
            new.command("create This is my third record!", "The note was successfully created", ""),
            prompt_WaitingForUserInput,
            new.command("create This is my forth record!", "The note was successfully created", ""),
            prompt_WaitingForUserInput,
            new.command("create This is my fifth record!", "The note was successfully created", ""),
            prompt_WaitingForUserInput,
            new.command("create This is my sixth record!", "[Error] The list of notes is full", ""),
            prompt_WaitingForUserInput,
            new.command("clear", "[OK] All notes were successfully deleted", ""),
            prompt_WaitingForUserInput,
            new.command("create This is my sixth record!", "The note was successfully created", ""),
            prompt_WaitingForUserInput,
            new.command("list",
                        "Index 0: This is my sixth record!\n",
                        ""),
            prompt_WaitingForUserInput,
            new.command("exit", "Bye!", ""),
        ])
    ]
    #
    # for i in range(2):
    #     units = []
    #
    #     for j in range(rand.randrange(1 + 2 * i, 3 + 2 * i)):
    #         units.append(prompt_WaitingForUserInput)
    #         rs = randomString().partition(' ')
    #         units.append(new.command(f"{rs[0]} {rs[2]}", f"{rs[0]}", ""))
    #
    #     units.append(prompt_WaitingForUserInput)
    #     units.append(new.command(f"exit {randomString()}", "Bye!", ""))
    #     cases.append(Case(checker, units))

    test = HSTest(cases)
    test.run_tests()


if __name__ == '__main__':
    main()
