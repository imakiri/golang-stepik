import os

from projects.in_memory_notepad.extra.extra import *
import projects.in_memory_notepad.stages.s1.tests_source as s1
import projects.in_memory_notepad.stages.s2.tests_source as s2
import projects.in_memory_notepad.stages.s3.tests_source as s3
import projects.in_memory_notepad.stages.s4.tests_source as s4


class Stage:
    def __init__(self, source, i: int):
        self.source = source
        self.i = i

    def _path(self, i: int) -> str:
        return f"projects\in_memory_notepad\stages\s{i}\\tests.py"

    def dump(self, compiled: str):
        path = self._path(self.i)
        if os.path.exists(path):
            os.remove(path)

        with open(path, "w+") as f:
            f.write(compiled)


stages = [Stage(s1, 1), Stage(s2, 2), Stage(s3, 3), Stage(s4, 4)]


def fImports() -> str:
    return "from hstest import StageTest, TestedProgram, CheckResult, dynamic_test\n\n"


def fClass() -> str:
    return "class Test(StageTest):\n"


def fTestHeader(i: int) -> str:
    return "\t@dynamic_test\n" \
           f"\tdef test{i}(self) -> CheckResult:\n" \
           f"\t\tprogram = TestedProgram()\n\n" \
           f'\t\treply = program.start().strip().lower().split("\\n")\n'


def fTestCase(case: any, i: list[int]) -> str:
    if isinstance(case, Input):
        i[0] = 0
        return f'\n\t\treply = program.execute("{case.command}").strip().lower().split("\\n")\n'
    elif isinstance(case, Output):
        re = f'\t\tif "{case.expectedResult.strip().lower()}" not in reply[{i[0]}]:\n' \
             f"\t\t\treturn CheckResult.wrong({repr(case.feedback)})\n"
        i[0] += 1
        return re


def fTestFooter() -> str:
    return "\n\t\treturn CheckResult.correct()\n\n"


def fMain() -> str:
    return "\nif __name__ == '__main__':\n" \
           "\tTest().run_tests()\n"


def main():
    for stage in stages:
        tests = stage.source.Tests()._generate()
        compiled = ""
        compiled += fImports()
        compiled += fClass()
        for i, test in enumerate(tests):
            compiled += fTestHeader(i)

            j = [0]
            for case in test.list():
                compiled += fTestCase(case, j)

            compiled += fTestFooter()

        compiled += fMain()
        stage.dump(compiled)


if __name__ == '__main__':
    main()
