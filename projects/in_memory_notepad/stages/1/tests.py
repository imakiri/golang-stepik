from __future__ import annotations
import random as rand
import string

from hstest.stage_test import *
from hstest.test_case import TestCase
from projects.in_memory_notepad.extra.extra import *


def randomString() -> str:
    alphabet = string.ascii_letters + string.digits + " "
    a = "".join(rand.choices(alphabet, k=rand.randrange(5, 10, 1)))
    b = "".join(rand.choices(alphabet + " ", k=rand.randrange(10, 100, 1)))
    return a + b


class Test:
    def __init__(self):
        self.input: list[Input] = []
        self.output: list[Output] = []
        self.order: list[int] = []
        self.acceptedSymbols = "\n "
        self.threshold = 2

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
        remainingReply = reply
        index = 0

        while True:
            o = self.output[index]
            i = remainingReply.find(o.expectedResult)
            if i == -1:
                return Fail(self, index, remainingReply)

            j = 0
            th = 0
            while j < i:
                if remainingReply[j] not in self.acceptedSymbols:
                    th += 1
                    if th > self.threshold:
                        return FailFormatting(self, index, remainingReply)
                j += 1

            index += 1
            if index >= len(self.output):
                return Pass()

            remainingReply = remainingReply[i + len(o.expectedResult):]

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


class Tests(StageTest):
    def __init__(self):
        super(Tests, self).__init__()

    @staticmethod
    def toHS(tests: list[Test]) -> list[TestCase]:
        ts: list[TestCase] = []
        for test in tests:
            ts.append(TestCase(stdin=test.listInput(), attach=test))
        return ts

    def generate(self) -> list[TestCase]:
        tests: list[Test] = []

        tests.append(Test().appendList([
            Output_WaitingForUserInput,
            Input("create This is my first record!"),
            Output("create", feedback_command),

            Output_WaitingForUserInput,
            Input("create This is my second record!"),
            Output("create", feedback_command),

            Output_WaitingForUserInput,
            Input("list"),
            Output("list", feedback_command),

            Output_WaitingForUserInput,
            Input("exit 1098"),
            Output_Bye,
        ]))

        for i in range(2):
            test = Test()
            for j in range(rand.randrange(1 + 2 * i, 3 + 2 * i)):
                test.append(Output_WaitingForUserInput)
                rs = randomString().partition(' ')
                test.append(Input(f"{rs[0]} {rs[2]}"))
                test.append(Output(f"{rs[0]}", feedback_command))

            test.append(Output_WaitingForUserInput)
            test.append(Input(f"exit {randomString()}"))
            test.append(Output_Bye)

            tests.append(test)

        return self.toHS(tests)

    def check(self, reply: str, attach: any) -> CheckResult:
        test: Test = attach
        result = test.check(reply)
        return CheckResult(result.isOk(), result.toString())


if __name__ == '__main__':
    Tests().run_tests()
