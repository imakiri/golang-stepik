import random as rand
import string

from testlib import *


class Main(DefaultTester):
    def __init__(self):
        super(Main, self).__init__()
        self._tests = self._generate()

    @staticmethod
    def randomString() -> str:
        alphabet = string.ascii_letters + string.digits + " "
        a = "".join(rand.choices(alphabet, k=rand.randrange(5, 10, 1)))
        b = "".join(rand.choices(alphabet + " ", k=rand.randrange(10, 100, 1)))
        return a + b

    def _generate(self) -> list[Test]:
        new = New("\n")

        Output_WaitingForMaxNum = Output(
            "Enter the maximum number of notes: ",
            "The program should ask user to enter the maximum number of notes")
        Output_WaitingForUserInput = Output(
            "Enter command and data: ",
            "The program should ask user for a command")
        Output_NoteCreated = Output(
            "[OK] The note was successfully created",
            "The program should inform the user about the successfully creation of the note")
        Output_ListFull = Output(
            "[Error] The list of notes is full",
            "")
        Output_ListCleared = Output(
            "[OK] All notes were successfully deleted",
            "")

        feedback_command = "The program should print back ONLY the given command and no more."
        feedback_bye = "The program should print the farewell message to the user upon its shutdown"
        message_deleted = "[OK] The note at index {} was successfully deleted"

        tests = [
            new.testFromList([
                Output_WaitingForMaxNum,
                Input("5"),
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
                Output("Index 3:", ""),
                Output("Index 4:", ""),
                Output_WaitingForUserInput,
                Input("create This is my third record!"),
                Output_NoteCreated,
                Output_WaitingForUserInput,
                Input("create This is my forth record!"),
                Output_NoteCreated,
                Output_WaitingForUserInput,
                Input("create This is my fifth record!"),
                Output_NoteCreated,
                Output_WaitingForUserInput,
                Input("create This is my sixth record!"),
                Output_ListFull,
                Output_WaitingForUserInput,
                Input("clear"),
                Output_ListCleared,
                Output_WaitingForUserInput,
                Input("create This is my sixth record!"),
                Output_NoteCreated,
                Output_WaitingForUserInput,
                Input("list"),
                Output("Index 0: This is my sixth record!\n", ""),
                Output("Index 1:", ""),
                Output("Index 2:", ""),
                Output("Index 3:", ""),
                Output("Index 4:", ""),
                Output_WaitingForUserInput,
                Input("exit"),
                Output("Bye!", feedback_bye)
            ])
        ]

        # for i in range(2):
        #     test = new.test()
        #     for j in range(rand.randrange(1 + 2 * i, 3 + 2 * i)):
        #         test.append(prompt_WaitingForUserInput)
        #         rs = self.randomString().partition(' ')
        #         test.append(Input(f"{rs[0]} {rs[2]}"))
        #         test.append(Output(f"{rs[0]}", feedback_command))
        #
        #     test.append(prompt_WaitingForUserInput)
        #     test.append(Input(f"exit {self.randomString()}"))
        #     test.append(Output("Bye!", feedback_bye))
        #     tests.append(test)

        return tests

    def tests(self) -> list[Test]:
        return self._tests


if __name__ == '__main__':
    main = Main()
    HSAdapter(main).run_tests()
