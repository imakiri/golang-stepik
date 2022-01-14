from .testlib import *


class Pass(Result):
    def isOk(self) -> bool:
        return True

    def toString(self) -> str:
        return "You've passed!"


class Fail(Result):
    def __init__(self, expected: str, got: str, feedback: str, index: int, indexCase: int):
        self.expected = expected
        self.got = got
        self.feedback = feedback
        self.index = index
        self.indexCase = indexCase

    def isOk(self) -> bool:
        return False

    def toString(self) -> str:
        return f"{self.feedback}\n" \
               f"\n" \
               f"Expected to find:\n" \
               f'"{self.expected}"\n' \
               f"in:\n" \
               f'"{self.got}"\n' \
               f"Error index: {self.index}.{self.indexCase}\n"


class FailFormatting(Fail):
    def __init__(self, expected: str, got: str, feedback: str, index: int, indexCase: int):
        super(FailFormatting, self).__init__(expected, got, feedback, index, indexCase)

    def toString(self) -> str:
        return f"{self.feedback}\n" \
               f"\n" \
               f"Expected to find:\n" \
               f'"{self.expected}"\n' \
               f"in:\n" \
               f'"{self.got}"\n' \
               f"This error might be caused by an unacceptable string formatting.\n" \
               f"Please verify the string formatting and remove redundant symbols.\n" \
               f"Error index: {self.index}.{self.indexCase}\n"


class TestMain(Test):
    def __init__(self):
        super(TestMain, self).__init__("\n")
        self.acceptedSymbols = "\n "
        self.threshold = 2

    def check(self, index: int, userOutput: str) -> Result:
        remainingUserOutput = userOutput
        indexCase = 0

        while True:
            o = self.output[indexCase]
            i = remainingUserOutput.find(o.expectedResult)
            if i == -1:
                l = 2 * len(o.expectedResult) + 1
                l = l if l < len(remainingUserOutput) else len(remainingUserOutput) - 1
                return Fail(o.expectedResult, remainingUserOutput[:l], o.feedback, index, indexCase)

            j = 0
            th = 0
            while j < i:
                if remainingUserOutput[j] not in self.acceptedSymbols:
                    th += 1
                    if th > self.threshold:
                        l = 2 * len(o.expectedResult) + 1
                        l = l if l < len(remainingUserOutput) else len(remainingUserOutput) - 1
                        return FailFormatting(o.expectedResult, remainingUserOutput[:l], o.feedback, index, indexCase)
                j += 1

            indexCase += 1
            if indexCase >= len(self.output):
                return Pass()

            remainingUserOutput = remainingUserOutput[i + len(o.expectedResult):]
