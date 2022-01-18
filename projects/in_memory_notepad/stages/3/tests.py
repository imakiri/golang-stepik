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


class HSTests(HSAdapter):
    def __init__(self):
        super(HSTests, self).__init__()

    def generate(self) -> list[TestCase]:
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
            Input_Clear,
            Output_ListCleared,

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

        return self.toHS(tests)


if __name__ == '__main__':
    HSTests().run_tests()
