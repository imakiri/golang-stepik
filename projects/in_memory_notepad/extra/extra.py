from __future__ import annotations
import string
from copy import copy

from hstest import StageTest, dynamic_test, TestedProgram, CheckResult


class Input:
    def __init__(self, string: str):
        self.command = string

    def executeBy(self, program: TestedProgram) -> str:
        return program.execute(self.command)


class Output:
    def __init__(self, expectedResult: str, feedback: str):
        self.expectedResult = expectedResult
        self.feedback = feedback
        self.acceptedSymbols = "\n "
        self.threshold = 2

    def __copy__(self):
        return type(self)(self.expectedResult, self.feedback)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def append(self, additionalFeedback: str) -> Output:
        co = copy(self)
        co.feedback += "\n"
        co.feedback += additionalFeedback
        return co

    def check(self, reply: list[str]) -> bool:
        i = reply[0].find(self.expectedResult)
        if i == -1:
            return False

        j = 0
        th = 0
        while j < i:
            if reply[0][j] not in self.acceptedSymbols:
                th += 1
                if th > self.threshold:
                    return False
            j += 1

        reply[0] = reply[0][i + len(self.expectedResult):]
        return True


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

    def nextInputAfter(self, indexInput: int) -> int:
        a = 0
        for t in self.order[indexInput:]:
            if t == 1:
                a += 1
            elif t == 0:
                break
            else:
                raise Exception(f"Test.list error")
        return a

    def list(self) -> list[any]:
        re = []
        i = 0
        o = 0
        for t in self.order:
            if t == 0:
                re.append(self.input[i])
                i += 1
            elif t == 1:
                re.append(self.output[o])
                o += 1
            else:
                raise Exception(f"Test.list error")

        return re

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


def traceback(test: Test, userOutput: list[str], indexOutput: int, depth: int) -> str:
    tb = ""
    n = 0
    i = 0
    o = 0
    while o < indexOutput:
        if test.order[n] == 0:
            tb += "> "
            tb += test.input[i].command
            tb += "\n"
            i += 1
        if test.order[n] == 1:
            tb += userOutput[o]
            o += 1
        n += 1

    return tb


def feedback(test: Test, userOutput: list[str], indexOutput: int, got: str) -> str:
    output = test.output[indexOutput]
    l = 2 * len(output.expectedResult) + 1
    l = l if l < len(got) else len(got) - 1
    re = ""

    tb = traceback(test, userOutput, indexOutput, -1)
    if len(tb) == 0:
        re += "This error happened at the very beginning of the program execution\n\n"
    else:
        re += "The error happened after:\n"
        re += tb
        re += "\n\n"

    re += f"Expected to find:\n" \
          f'"{output.expectedResult}"\n' \
          f"in:\n" \
          f'"{got[:l]}..."\n\n' \
          f"{output.feedback}\n"

    return re


Output_WaitingForMaxNum = Output(
    "Enter the maximum number of notes: ",
    "The program should ask user to enter the maximum number of notes"
)
Output_WaitingForUserInput = Output(
    "Enter command and data: ",
    "The program should ask user for a command"
)
Output_NoteCreated = Output(
    "[OK] The note was successfully created",
    "The program should inform the user about the successful creation of the note"
)
Output_MissingIndex = Output(
    "[Error] Missing position argument",
    "The program should inform the user when it can't find the position argument"
)
Output_MissingNote = Output(
    "[Error] Missing note argument",
    "The program should inform the user when it can't find the note argument"
)
Output_NothingToUpdate = Output(
    "[Error] There is nothing to update",
    "The program should inform the user when there is no note to update"
)
Output_NothingToDelete = Output(
    "[Error] There is nothing to delete",
    "The program should inform the user when there is no note to delete"
)
Output_ListFull = Output(
    "[Error] Notepad is full",
    "The program should inform the user when the internal storage is full"
)
Output_ListEmpty = Output(
    "[Info] Notepad is empty",
    "The program should inform the user when there is no notes"
)
Output_ListCleared = Output(
    "[OK] All notes were successfully deleted",
    "The program should inform the user about the successful deletion of notes"
)
Output_UnknownCommand = Output(
    "[Error] Unknown command",
    "The program should inform the user when it can't recognize the given command"
)
Output_Bye = Output(
    "[Info] Bye!",
    "The program should print the farewell message to the user upon its shutdown"
)


def Output_InvalidIndex(index: str) -> Output:
    return Output(f"[Error] Invalid position: {index}",
                  "The program should inform the user when it cannot interpret the given position as an integer")


def Output_IndexOutOfBoundaries(index: int, upper: int) -> Output:
    return Output(f"[Error] Position {index + 1} is out of the boundaries [1, {upper}]",
                  "The program should inform the user when the given position is out of the boundaries")


def Output_Updated(index: int) -> Output:
    return Output(f"[OK] The note at position {index + 1} was successfully updated", feedback_noteUpdated)


def Output_Deleted(index: int) -> Output:
    return Output(f"[OK] The note at position {index + 1} was successfully deleted", feedback_noteDeleted)


def Output_Note(index: int, value: str) -> Output:
    return Output(f"[Info] {index + 1}: {value}", "")


feedback_command = "The program should print back only the given command and no more"
feedback_printingEmptyNotes = "The program shouldn't print empty notes"
feedback_noteUpdated = "The program should inform the user about the successful update of the note"
feedback_noteDeleted = "The program should inform the user about the successful deletion of the note"

Input_List = Input("list")
Input_Clear = Input("clear")
Input_Exit = Input("exit")


def Input_Create(value: str) -> Input:
    return Input(f"create {value}")


def Input_Update(index: int, value: str) -> Input:
    return Input(f"update {index + 1} {value}")


def Input_Delete(index: int) -> Input:
    return Input(f"delete {index + 1}")
