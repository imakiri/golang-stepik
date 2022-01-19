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
            Input_Create("This is my first record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my first record!"),

            Output_WaitingForUserInput.append(feedback_printingEmptyNotes),
            Input_Clear,
            Output_ListCleared,

            Output_WaitingForUserInput,
            Input_List,
            Output("", ""),

            Output_WaitingForUserInput.append(feedback_printingEmptyNotes),
            Input_Exit,
            Output_Bye
        ]))

        tests.append(Test().appendList([
            Output_WaitingForUserInput,
            Input_Create("This is my first record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_Create("This is my second record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_Create("This is my third record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_Create("This is my forth record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_Create("This is my fifth record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_Create("This is my sixth record!"),
            Output_ListFull,

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my first record!"),
            Output_Note(1, "This is my second record!"),
            Output_Note(2, "This is my third record!"),
            Output_Note(3, "This is my forth record!"),
            Output_Note(4, "This is my fifth record!"),

            Output_WaitingForUserInput,
            Input_Clear,
            Output_ListCleared,

            Output_WaitingForUserInput,
            Input_Create("This is my sixth record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my sixth record!"),

            Output_WaitingForUserInput,
            Input_Exit,
            Output_Bye
        ]))

        return self.toHS(tests)

    def check(self, reply: str, attach: any) -> CheckResult:
        test: Test = attach
        remainingReply = reply
        index = 0

        while True:
            o = test.output[index]
            i = remainingReply.find(o.expectedResult)
            if i == -1:
                result = Fail(test, index, remainingReply)
                return CheckResult(result.isOk(), result.toString())

            j = 0
            th = 0
            while j < i:
                if remainingReply[j] not in test.acceptedSymbols:
                    th += 1
                    if th > test.threshold:
                        result = FailFormatting(test, index, remainingReply)
                        return CheckResult(result.isOk(), result.toString())
                j += 1

            index += 1
            if index >= len(test.output):
                result = Pass()
                return CheckResult(result.isOk(), result.toString())

            remainingReply = remainingReply[i + len(o.expectedResult):]


if __name__ == '__main__':
    Tests().run_tests()

