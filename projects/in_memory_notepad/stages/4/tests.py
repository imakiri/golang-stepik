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
        Input("update zero Updated first note!"),
        Output_InvalidIndex("zero"),

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
        Input("delete zero"),
        Output_InvalidIndex("zero"),

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

    tests.append(TestMain().appendList([
        Output_WaitingForMaxNum,
        Input("3"),

        Output_WaitingForUserInput,
        Input("create          "),
        Output_MissingNote,

        Output_WaitingForUserInput,
        Input("create"),
        Output_MissingNote,

        Output_WaitingForUserInput,
        Input("get 1"),
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

    tests.append(TestMain().appendList([
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

    return tests


if __name__ == '__main__':
    tests = generate()
    HSAdapter(tests).run_tests()
