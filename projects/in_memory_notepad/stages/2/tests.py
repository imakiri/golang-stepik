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

    @dynamic_test(order=0)
    def t0(self) -> CheckResult:
        program = TestedProgram()

        reply = [program.start()]
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input("create This is my first record!").executeBy(program)]
        with Output_NoteCreated as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_List.executeBy(program)]
        with Output_Note(0, "This is my first record!") as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput.append(feedback_printingEmptyNotes) as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Clear.executeBy(program)]
        with Output_ListCleared as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_List.executeBy(program)]
        with Output("", "") as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput.append(feedback_printingEmptyNotes) as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Exit.executeBy(program)]
        with Output_Bye as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        return CheckResult.correct()

    @dynamic_test(order=1)
    def t1(self) -> CheckResult:
        program = TestedProgram()

        reply = [program.start()]
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Create("This is my first record!").executeBy(program)]
        with Output_NoteCreated as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Create("This is my second record!").executeBy(program)]
        with Output_NoteCreated as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Create("This is my third record!").executeBy(program)]
        with Output_NoteCreated as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Create("This is my forth record!").executeBy(program)]
        with Output_NoteCreated as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Create("This is my fifth record!").executeBy(program)]
        with Output_NoteCreated as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Create("This is my sixth record!").executeBy(program)]
        with Output_ListFull as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_List.executeBy(program)]
        with Output_Note(0, "This is my first record!") as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_Note(1, "This is my second record!") as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_Note(2, "This is my third record!") as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_Note(3, "This is my forth record!") as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_Note(4, "This is my fifth record!") as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Clear.executeBy(program)]
        with Output_ListCleared as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Create("This is my sixth record!").executeBy(program)]
        with Output_NoteCreated as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput.append(feedback_printingEmptyNotes) as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_List.executeBy(program)]
        with Output_Note(0, "This is my sixth record!") as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input_Exit.executeBy(program)]
        with Output_Bye as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        return CheckResult.correct()


if __name__ == '__main__':
    Tests().run_tests()
