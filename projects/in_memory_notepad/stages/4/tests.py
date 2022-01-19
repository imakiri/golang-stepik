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
            Output_WaitingForMaxNum,
            Input("3"),

            Output_WaitingForUserInput,
            Input_List,
            Output_ListEmpty,

            Output_WaitingForUserInput,
            Input_Create("This is my first record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my first record!"),

            Output_WaitingForUserInput,
            Input_Update(0, "  "),
            Output_MissingNote,

            Output_WaitingForUserInput,
            Input("update one Updated first note!"),
            Output_InvalidIndex("one"),

            Output_WaitingForUserInput,
            Input("update   "),
            Output_MissingIndex,

            Output_WaitingForUserInput,
            Input("update"),
            Output_MissingIndex,

            Output_WaitingForUserInput,
            Input_Update(0, "Updated first note!"),
            Output_Updated(0),

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "Updated first note!"),

            Output_WaitingForUserInput,
            Input("delete one"),
            Output_InvalidIndex("one"),

            Output_WaitingForUserInput,
            Input("delete   "),
            Output_MissingIndex,

            Output_WaitingForUserInput,
            Input("delete"),
            Output_MissingIndex,

            Output_WaitingForUserInput,
            Input_Delete(0),
            Output_Deleted(0),

            Output_WaitingForUserInput,
            Input_List,
            Output_ListEmpty,

            Output_WaitingForUserInput,
            Input_Exit,
            Output_Bye
        ]))

        tests.append(Test().appendList([
            Output_WaitingForMaxNum,
            Input("3"),

            Output_WaitingForUserInput,
            Input("create          "),
            Output_MissingNote,

            Output_WaitingForUserInput,
            Input("create"),
            Output_MissingNote,

            Output_WaitingForUserInput,
            Input("get 2"),
            Output_UnknownCommand,

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
            Output_ListFull,

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my first record!"),
            Output_Note(1, "This is my second record!"),
            Output_Note(2, "This is my third record!"),

            Output_WaitingForUserInput,
            Input_Clear,
            Output_ListCleared,

            Output_WaitingForUserInput,
            Input_Create("This is my forth record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my forth record!"),

            Output_WaitingForUserInput,
            Input_Exit,
            Output_Bye
        ]))

        tests.append(Test().appendList([
            Output_WaitingForMaxNum,
            Input("3"),

            Output_WaitingForUserInput,
            Input_Create("This is my first record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_Create("This is my second record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my first record!"),
            Output_Note(1, "This is my second record!"),

            Output_WaitingForUserInput,
            Input_Delete(0),
            Output_Deleted(0),

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my second record!"),

            Output_WaitingForUserInput,
            Input_Create("This is my third record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_Create("This is my forth record!"),
            Output_NoteCreated,

            Output_WaitingForUserInput,
            Input_Update(1, "Updated third record!"),
            Output_Updated(1),

            Output_WaitingForUserInput,
            Input_List,
            Output_Note(0, "This is my second record!"),
            Output_Note(1, "Updated third record!"),
            Output_Note(2, "This is my forth record!"),

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
