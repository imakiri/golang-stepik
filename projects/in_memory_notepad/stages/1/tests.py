import random as rand
import string

from projects.in_memory_notepad.testlib.testlib import *
from projects.in_memory_notepad.data.data import *


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

        tests = [
            new.testFromList([
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
                Output_Bye
            ])
        ]

        for i in range(2):
            test = new.test()
            for j in range(rand.randrange(1 + 2 * i, 3 + 2 * i)):
                test.append(Output_WaitingForUserInput)
                rs = self.randomString().partition(' ')
                test.append(Input(f"{rs[0]} {rs[2]}"))
                test.append(Output(f"{rs[0]}", feedback_command))

            test.append(Output_WaitingForUserInput)
            test.append(Input(f"exit {self.randomString()}"))
            test.append(Output_Bye)
            tests.append(test)

        return tests

    def tests(self) -> list[Test]:
        return self._tests


if __name__ == '__main__':
    main = Main()
    HSAdapter(main).run_tests()
