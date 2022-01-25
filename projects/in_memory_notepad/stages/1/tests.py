from __future__ import annotations
import random as rand
import string

from hstest.stage_test import *
from hstest import StageTest, dynamic_test, TestedProgram, CheckResult
from projects.in_memory_notepad.extra.extra import *


def randomString() -> str:
    alphabet = string.ascii_letters + string.digits + " "
    a = "".join(rand.choices(alphabet, k=rand.randrange(5, 10, 1)))
    b = "".join(rand.choices(alphabet + " ", k=rand.randrange(10, 100, 1)))
    return a + b


class Tests(StageTest):
    """
    Парсер в С17 коммите проверяет пропущенный интервал на наличие посторонних символов.
    Так же, в С17 коммите не наблюдается описанной ошибки, когда, будучи в начале вывода,
    можно найти "правильный ответ" где то в конце вывода.

    Хочу так же отметить, что в тестах нету надобности в проверке "аргументов" вывода, а так же в ветвлении\условном вводе.

    Сравнивая код тестов, написанных в динамическом стиле и код тестов C17, не могу не отметить что
    динамический стиль сложнее для восприятия и анализа так как содержит множество элементов,
    мешающих пониманию тестов, но необходимых для их корректной работы.
    """
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
        with Output("create", feedback_command) as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input("create This is my second record!").executeBy(program)]
        with Output("create", feedback_command) as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input("list").executeBy(program)]
        with Output("list", feedback_command) as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        reply = [Input("exit 1098").executeBy(program)]
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

        for j in range(rand.randrange(1, 3)):
            rs = randomString().partition(' ')

            reply = [Input(f"{rs[0]} {rs[2]}").executeBy(program)]
            with Output(f"{rs[0]}", feedback_command) as o:
                if not o.check(reply):
                    return CheckResult.wrong(o.feedback)
            with Output_WaitingForUserInput as o:
                if not o.check(reply):
                    return CheckResult.wrong(o.feedback)

        reply = [Input(f"exit {randomString()}").executeBy(program)]
        with Output_Bye as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        return CheckResult.correct()

    @dynamic_test(order=2)
    def t2(self) -> CheckResult:
        program = TestedProgram()

        reply = [program.start()]
        with Output_WaitingForUserInput as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        for j in range(rand.randrange(3, 5)):
            rs = randomString().partition(' ')

            reply = [Input(f"{rs[0]} {rs[2]}").executeBy(program)]
            with Output(f"{rs[0]}", feedback_command) as o:
                if not o.check(reply):
                    return CheckResult.wrong(o.feedback)
            with Output_WaitingForUserInput as o:
                if not o.check(reply):
                    return CheckResult.wrong(o.feedback)

        reply = [Input(f"exit {randomString()}").executeBy(program)]
        with Output_Bye as o:
            if not o.check(reply):
                return CheckResult.wrong(o.feedback)

        return CheckResult.correct()


if __name__ == '__main__':
    Tests().run_tests()
