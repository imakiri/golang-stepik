import random as rand
import string

from hstest.stage_test import *
from hstest.test_case import TestCase


class Input:
    def __init__(self, string: str):
        self.command = string


class Output:
    def __init__(self, expectedResult: str, feedback: str):
        self.expectedResult = expectedResult
        self.feedback = feedback


class Test:
    def __init__(self, commandSeparator: str):
        self.commandSeparator = commandSeparator
        self.input: List[Input] = []
        self.output: List[Output] = []
        self.order: List[int] = []

    def append(self, unit: any):
        if isinstance(unit, Input):
            self.input.append(unit)
            self.order.append(0)
        elif isinstance(unit, Output):
            self.output.append(unit)
            self.order.append(1)
        else:
            raise Exception(f"given type {type(unit)} is not supported")

    def compileInput(self) -> str:
        re = ""
        for v in self.input:
            re += v.command + self.commandSeparator
        return re

    def compileOutput(self) -> str:
        re = ""
        for v in self.output:
            re += v.expectedResult
        return re


class Result:
    def isOk(self) -> bool:
        raise NotImplementedError

    def toString(self) -> str:
        raise NotImplementedError


class Pass(Result):
    def isOk(self) -> bool:
        return True

    def toString(self) -> str:
        return "You've passed!"


class Fail(Result):
    def __init__(self, expected: str, got: str, feedback: str):
        self.expected = expected
        self.got = got
        self.feedback = feedback

    def isOk(self) -> bool:
        return False

    def toString(self) -> str:
        return f"{self.feedback}\n" \
               f"\n" \
               f"Expected to find:\n" \
               f'"{self.expected}"\n' \
               f"in:\n" \
               f'"{self.got}"\n'


class Tester:
    def tests(self) -> List[Test]:
        raise NotImplementedError

    def check(self, test: Test, userOutput: str) -> Result:
        raise NotImplementedError


class New:
    def __init__(self, separator: str):
        self._separator = separator

    def test(self) -> Test:
        return Test(self._separator)

    def testFromList(self, units: List[any]) -> Test:
        t = self.test()
        for u in units:
            t.append(u)
        return t


class Main(Tester):
    def __init__(self):
        self._as = "\n "
        self._threshold = 2
        self._tests = self._generate()

    @staticmethod
    def randomString() -> str:
        alphabet = string.ascii_letters + string.digits + " "
        a = "".join(rand.choices(alphabet, k=rand.randrange(5, 10, 1)))
        b = "".join(rand.choices(alphabet + " ", k=rand.randrange(10, 100, 1)))
        return a + b

    def _generate(self) -> List[Test]:
        new = New("\n")

        prompt_WaitingForUserInput = Output("Enter command and data: ", "Please verify the correctness of the program."
                                                                        "\nTip: The program should ask user for a command")
        feedback_command = "Please verify the correctness of the program. " \
                           "\nTip: The program should print back ONLY the given command and no more."
        feedback_bye = "Please verify the correctness of the program." \
                       "\nTip: The program should print the farewell message to the user upon its shutdown"

        tests = [
            new.testFromList([
                prompt_WaitingForUserInput,
                Input("create This is my first record!"), Output("create", feedback_command),
                prompt_WaitingForUserInput,
                Input("create This is my second record!"), Output("create", feedback_command),
                prompt_WaitingForUserInput,
                Input("list"), Output("list", feedback_command),
                prompt_WaitingForUserInput,
                Input("exit 1098"), Output("Bye!", feedback_bye)
            ])
        ]

        for i in range(2):
            test = new.test()
            for j in range(rand.randrange(1 + 2 * i, 3 + 2 * i)):
                test.append(prompt_WaitingForUserInput)
                rs = self.randomString().partition(' ')
                test.append(Input(f"{rs[0]} {rs[2]}"))
                test.append(Output(f"{rs[0]}", feedback_command))

            test.append(prompt_WaitingForUserInput)
            test.append(Input(f"exit {self.randomString()}"))
            test.append(Output("Bye!", feedback_bye))
            tests.append(test)

        return tests

    def tests(self) -> List[Test]:
        return self._tests

    def check(self, test: Test, userOutput: str) -> Result:
        remainingUserOutput = userOutput
        index = 0

        while True:
            o = test.output[index]
            i = remainingUserOutput.find(o.expectedResult)
            if i == -1:
                return Fail(o.expectedResult, remainingUserOutput, o.feedback)

            j = 0
            th = 0
            while j < i:
                if remainingUserOutput[j] not in self._as:
                    th += 1
                    if th > self._threshold:
                        return Fail(o.expectedResult, remainingUserOutput, o.feedback + \
                                    "\nThis error might be caused by unacceptable string formatting."
                                    "\nPlease verify the string formatting and remove redundant symbols")
                j += 1

            index += 1
            if index >= len(test.output):
                return Pass()

            remainingUserOutput = remainingUserOutput[i + len(o.expectedResult):]


class HSAdapter(StageTest):
    def __init__(self, tester: Tester):
        super(HSAdapter, self).__init__()
        self.tester = tester

    def generate(self) -> List[TestCase]:
        ts = []
        for test in self.tester.tests():
            ts.append((test.compileInput(), test.compileOutput()))
        return TestCase.from_stepik(ts)

    def check(self, user_answer: str, correct_answer: Any) -> CheckResult:
        for test in self.tester.tests():
            if correct_answer == test.compileOutput():
                result = self.tester.check(test, user_answer)
                return CheckResult(result.isOk(), result.toString())


if __name__ == '__main__':
    main = Main()
    HSAdapter(main).run_tests()