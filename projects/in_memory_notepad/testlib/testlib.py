from __future__ import annotations
import string
from copy import copy

from hstest.stage_test import *
from hstest.test_case import TestCase


class Input:
    def __init__(self, string: str):
        self.command = string


class Output:
    def __init__(self, expectedResult: str, feedback: str):
        self.expectedResult = expectedResult
        self.feedback = feedback

    def __copy__(self):
        return type(self)(self.expectedResult, self.feedback)

    def append(self, additionalFeedback: str) -> Output:
        co = copy(self)
        co.feedback += "\n"
        co.feedback += additionalFeedback
        return co


class Test:
    def __init__(self, commandSeparator: str):
        self.commandSeparator = commandSeparator
        self.input: list[Input] = []
        self.output: list[Output] = []
        self.order: list[int] = []

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
    def tests(self) -> list[Test]:
        raise NotImplementedError

    def check(self, test: Test, userOutput: str) -> Result:
        raise NotImplementedError


class New:
    def __init__(self, separator: str):
        self._separator = separator

    def test(self) -> Test:
        return Test(self._separator)

    def testFromList(self, units: list[any]) -> Test:
        t = self.test()
        for u in units:
            t.append(u)
        return t


class DefaultTester(Tester):
    def __init__(self):
        self.acceptedSymbols = "\n "
        self.threshold = 2

    def check(self, testIndex: int, test: Test, userOutput: str) -> Result:
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
                if remainingUserOutput[j] not in self.acceptedSymbols:
                    th += 1
                    if th > self.threshold:
                        return Fail(o.expectedResult, remainingUserOutput, o.feedback + \
                                    "\nThis error might be caused by an unacceptable string formatting."
                                    "\nPlease verify the string formatting and remove redundant symbols."
                                    f"\nError index: {testIndex}.{index}")
                j += 1

            index += 1
            if index >= len(test.output):
                return Pass()

            remainingUserOutput = remainingUserOutput[i + len(o.expectedResult):]


class HSAdapter(StageTest):
    def __init__(self, tester: Tester):
        super(HSAdapter, self).__init__()
        self.tester = tester

    def generate(self) -> list[TestCase]:
        ts = []
        for test in self.tester.tests():
            ts.append((test.compileInput(), test.compileOutput()))
        return TestCase.from_stepik(ts)

    def check(self, user_answer: str, correct_answer: Any) -> CheckResult:
        for index, test in enumerate(self.tester.tests()):
            if correct_answer == test.compileOutput():
                result = self.tester.check(index, test, user_answer)
                return CheckResult(result.isOk(), result.toString())
