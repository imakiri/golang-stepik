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
        Output_Bye,
    ]))

    for i in range(2):
        test = TestMain()
        for j in range(rand.randrange(1 + 2 * i, 3 + 2 * i)):
            test.append(Output_WaitingForUserInput)
            rs = randomString().partition(' ')
            test.append(Input(f"{rs[0]} {rs[2]}"))
            test.append(Output(f"{rs[0]}", feedback_command))

        test.append(Output_WaitingForUserInput)
        test.append(Input(f"exit {randomString()}"))
        test.append(Output_Bye)

        tests.append(test)

    return tests


if __name__ == '__main__':
    tests = generate()
    HSAdapter(tests).run_tests()
