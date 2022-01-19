from __future__ import annotations
import string
from copy import copy


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


class Pass(Result):
    def isOk(self) -> bool:
        return True

    def toString(self) -> str:
        return "You've passed!"


class Fail(Result):
    def __init__(self, test: Test, index: int, got: str):
        self.test = test
        self.index = index
        self.output = self.test.output[index]
        self.got = got
        self.traceInput = test.tracebackInput(index)
        self.l = 2 * len(self.output.expectedResult) + 1
        self.l = self.l if self.l < len(got) else len(got) - 1

    def isOk(self) -> bool:
        return False

    def toString(self) -> str:
        return f'When executing "{self.traceInput[0].command}"\n' \
               f"Expected to find:\n" \
               f'"{self.output.expectedResult}"\n' \
               f"in:\n" \
               f'"{self.got[:self.l]}..."\n' \
               f"{self.output.feedback}\n" \
            # f"Error index: {self.index}\n"


class FailFormatting(Fail):
    def __init__(self, test: Test, index: int, got: str):
        super(FailFormatting, self).__init__(test, index, got)

    def toString(self) -> str:
        return super(FailFormatting, self).toString() + \
               f"This error might be caused by an unacceptable string formatting.\n" \
               f"Please verify the string formatting and remove redundant symbols.\n"


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
