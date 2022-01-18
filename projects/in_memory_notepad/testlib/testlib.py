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

    def listInput(self) -> list[str]:
        re: list[str] = []
        for v in self.input:
            re.append(v.command)
        return re

    def tracebackInput(self, outputIndex: int) -> list[Input]:
        l: list[Input] = []
        i = 0
        o = 0
        n = 0
        while o < outputIndex:
            if self.order[n] == 0:
                i += 1
            if self.order[n] == 1:
                o += 1
            n += 1

        for j in range(i, -1, -1):
            l.append(self.input[j])

        return l


    def check(self, reply: str) -> Result:
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
    def __init__(self):
        super(HSAdapter, self).__init__()

    @staticmethod
    def toHS(tests: list[Test]) -> list[TestCase]:
        ts: list[TestCase] = []
        for test in tests:
            ts.append(TestCase(stdin=test.listInput(), attach=test))
        return ts

    def check(self, reply: str, attach: any) -> CheckResult:
        test: Test = attach
        result = test.check(reply)
        return CheckResult(result.isOk(), result.toString())
