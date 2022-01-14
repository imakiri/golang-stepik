import random as rand
import string

from projects.in_memory_notepad.testlib.testlib import *
from projects.in_memory_notepad.testlib.extra import TestMain
from projects.in_memory_notepad.data.data import *


def randomString() -> str:
    alphabet = string.ascii_letters + string.digits + " "
    a = "".join(rand.choices(alphabet, k=rand.randrange(5, 10, 1)))
    b = "".join(rand.choices(alphabet + " ", k=rand.randrange(10, 100, 1)))
    return a + b


def generate() -> list[Test]:
    tests: list[Test] = []

    tests.append(TestMain().appendList([
        Output_WaitingForMaxNum,
        Input("3"),

        Output_WaitingForUserInput,
        Input("create This is my first record!"),
        Output_NoteCreated,

        Output_WaitingForUserInput,
        Input("create This is my second record!"),
        Output_NoteCreated,

        Output_WaitingForUserInput,
        Input("list"),
        Output("Index 0: This is my first record!", ""),
        Output("Index 1: This is my second record!", ""),
        Output("Index 2:", ""),

        Output_WaitingForUserInput,
        Input("delete 0"),
        Output(message_noteDeleted(0), feedback_noteDeleted),

        Output_WaitingForUserInput,
        Input("list"),
        Output("Index 0: This is my second record!", ""),
        Output("Index 1:", ""),
        Output("Index 2:", ""),

        Output_WaitingForUserInput,
        Input("create This is my third record!"),
        Output_NoteCreated,

        Output_WaitingForUserInput,
        Input("create This is my forth record!"),
        Output_NoteCreated,

        Output_WaitingForUserInput,
        Input("update 1 Updated third record!"),
        Output(message_noteUpdated(1), feedback_noteUpdated),

        Output_WaitingForUserInput,
        Input("list"),
        Output("Index 0: This is my second record!", ""),
        Output("Index 1: Updated third record!", ""),
        Output("Index 2: This is my forth record!", ""),

        Output_WaitingForUserInput,
        Input("exit"),
        Output_Bye
    ]))

    return tests


if __name__ == '__main__':
    tests = generate()
    HSAdapter(tests).run_tests()
