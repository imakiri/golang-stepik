from .testlib import *


class Pass(Result):
    def isOk(self) -> bool:
        return True

    def toString(self) -> str:
        return "You've passed!"


class Fail(Result):
    def __init__(self, output: Output, got: str, indexTest: int, indexCase: int, traceInput: list[Input]):
        self.output = output
        self.got = got
        self.traceInput = traceInput
        self.indexTest = indexTest
        self.indexCase = indexCase
        self.l = 2 * len(output.expectedResult) + 1
        self.l = self.l if self.l < len(got) else len(got) - 1

    def isOk(self) -> bool:
        return False

    def toString(self) -> str:
        return f'When executing "{self.traceInput[0].command}"\n' \
               f"Expected to find:\n" \
               f'"{self.output.expectedResult}"\n' \
               f"in:\n" \
               f'"{self.got[:self.l]}..."\n' \
               f"{self.output.feedback}\n" \
               f"Error index: {self.indexTest}.{self.indexCase}\n"


class FailFormatting(Result):
    def __init__(self, output: Output, got: str, indexTest: int, indexCase: int, traceInput: list[Input]):
        super(FailFormatting, self).__init__(output, got, indexTest, indexCase, traceInput)

    def toString(self) -> str:
        return f'When executing "{self.traceInput[0].command}"\n' \
               f"Expected to find:\n" \
               f'"{self.output.expectedResult}"\n' \
               f"in:\n" \
               f'"{self.got[:self.l]}..."\n' \
               f"{self.output.feedback}\n" \
               f"This error might be caused by an unacceptable string formatting.\n" \
               f"Please verify the string formatting and remove redundant symbols.\n" \
               f"Error index: {self.indexTest}.{self.indexCase}\n"


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
                return Fail(o, remainingUserOutput, index, indexCase, self.tracebackInput(indexCase))

            j = 0
            th = 0
            while j < i:
                if remainingUserOutput[j] not in self.acceptedSymbols:
                    th += 1
                    if th > self.threshold:
                        return FailFormatting(o, remainingUserOutput, index, indexCase, self.tracebackInput(indexCase))
                j += 1

            indexCase += 1
            if indexCase >= len(self.output):
                return Pass()

            remainingUserOutput = remainingUserOutput[i + len(o.expectedResult):]
