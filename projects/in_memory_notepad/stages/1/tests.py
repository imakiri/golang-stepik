from __future__ import annotations
import random as rand
import string

from hstest.stage_test import *
from hstest import StageTest, dynamic_test, TestedProgram, CheckResult
from projects.in_memory_notepad.extra.extra import *


def randomString() -> str:
    alphabet = string.ascii_letters + string.digits + " "
    a = "".join(rand.choices(alphabet, k=rand.randrange(5, 10, 1)))
    b = "".join(rand.choices(alphabet + " ", k=rand.randrange(10, 100, 1)))
    return a + b


class Tests(StageTest):
    def __init__(self):
        super(Tests, self).__init__()
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

        self.tests = tests

    def t(self, test: Test) -> CheckResult:
        program = TestedProgram()
        index = 0
        indexOutput = 0
        output = [program.start()]
        parsedOutput: list[str] = []
        for unit in test.list():
            if isinstance(unit, Input):
                output.append(program.execute(unit.command))
                index += 1
            elif isinstance(unit, Output):
                remainingReply = output[len(output)-1]
                while test.nextInputAfter(index) > 0:
                    o = test.output[indexOutput]
                    i = remainingReply.find(o.expectedResult)
                    if i == -1:
                        return CheckResult(False, feedback(test, parsedOutput, indexOutput, remainingReply))

                    j = 0
                    th = 0
                    while j < i:
                        if remainingReply[j] not in test.acceptedSymbols:
                            th += 1
                            if th > test.threshold:
                                fb = feedback(test, parsedOutput, indexOutput, remainingReply)
                                fb += f"\n" \
                                      f"This error might be caused by an unacceptable string formatting.\n" \
                                      f"Please verify the string formatting and remove redundant symbols.\n"
                                return CheckResult(False, fb)
                        j += 1
                    indexOutput += 1
                    index += 1
                    parsedOutput.append(remainingReply[:i + len(o.expectedResult)])
                    remainingReply = remainingReply[i + len(o.expectedResult):]
            else:
                raise Exception(f"given type {type(unit)} is not supported")

        return CheckResult.correct()

    @dynamic_test(order=0)
    def t0(self) -> CheckResult:
        test = self.tests[0]
        return self.t(test)

    @dynamic_test(order=1)
    def t1(self) -> CheckResult:
        test = self.tests[1]
        return self.t(test)

    @dynamic_test(order=2)
    def t2(self) -> CheckResult:
        test = self.tests[2]
        return self.t(test)


if __name__ == '__main__':
    Tests().run_tests()
