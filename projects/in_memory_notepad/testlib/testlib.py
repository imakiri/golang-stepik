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


class Result:
    def isOk(self) -> bool:
        raise NotImplementedError

    def toString(self) -> str:
        raise NotImplementedError


class Test:
    def __init__(self, commandSeparator: str):
        self.commandSeparator = commandSeparator
        self.input: list[Input] = []
        self.output: list[Output] = []
        self.order: list[int] = []

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

    def check(self, index: int, userOutput: str) -> Result:
        raise NotImplementedError

    def append(self, unit: any) -> Test:
        if isinstance(unit, Input):
            self.input.append(unit)
            self.order.append(0)
            return self
        elif isinstance(unit, Output):
            self.output.append(unit)
            self.order.append(1)
            return self
        else:
            raise Exception(f"given type {type(unit)} is not supported")

    def appendList(self, units: list[any]) -> Test:
        for u in units:
            self.append(u)
        return self


class HSAdapter(StageTest):
    def __init__(self, tests: list[Test]):
        super(HSAdapter, self).__init__()
        self.tests = tests

    def generate(self) -> list[TestCase]:
        ts = []
        for test in self.tests:
            ts.append((test.compileInput(), test.compileOutput()))
        return TestCase.from_stepik(ts)

    def check(self, user_answer: str, correct_answer: Any) -> CheckResult:
        for index, test in enumerate(self.tests):
            if correct_answer == test.compileOutput():
                result = test.check(index, user_answer)
                return CheckResult(result.isOk(), result.toString())
