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
        remainingReply = reply
        index = 0
        output: list[str] = []

        while True:
            o = test.output[index]
            i = remainingReply.find(o.expectedResult)
            if i == -1:
                return CheckResult(False, feedback(test, output, index, remainingReply))

            j = 0
            th = 0
            while j < i:
                if remainingReply[j] not in test.acceptedSymbols:
                    th += 1
                    if th > test.threshold:
                        fb = feedback(test, output, index, remainingReply)
                        fb += f"\n" \
                              f"This error might be caused by an unacceptable string formatting.\n" \
                              f"Please verify the string formatting and remove redundant symbols.\n"
                        return CheckResult(False, fb)
                j += 1

            index += 1
            output.append(remainingReply[:i+len(o.expectedResult)])
            if index >= len(test.output):
                return CheckResult(True, "")

            remainingReply = remainingReply[i + len(o.expectedResult):]


if __name__ == '__main__':
    Tests().run_tests()
