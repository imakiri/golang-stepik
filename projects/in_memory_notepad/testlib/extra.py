from .testlib import *


class Pass(Result):
    def isOk(self) -> bool:
        return True

    def toString(self) -> str:
        return "You've passed!"


class Fail(Result):
    def __init__(self, test: Test, index: int, got: str):
        self.test = test
        self.index = index
        self.output = self.test.output[index]
        self.got = got
        self.traceInput = test.tracebackInput(index)
        self.l = 2 * len(self.output.expectedResult) + 1
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
               # f"Error index: {self.index}\n"


class FailFormatting(Fail):
    def __init__(self, test: Test, index: int, got: str):
        super(FailFormatting, self).__init__(test, index, got)

    def toString(self) -> str:
        return super(FailFormatting, self).toString() + \
               f"This error might be caused by an unacceptable string formatting.\n" \
               f"Please verify the string formatting and remove redundant symbols.\n" \


class TestMain(Test):
    def __init__(self):
        super(TestMain, self).__init__("\n")
        self.acceptedSymbols = "\n "
        self.threshold = 2

    def check(self, reply: str) -> Result:
        remainingReply = reply
        index = 0

        while True:
            o = self.output[index]
            i = remainingReply.find(o.expectedResult)
            if i == -1:
                return Fail(self, index, remainingReply)

            j = 0
            th = 0
            while j < i:
                if remainingReply[j] not in self.acceptedSymbols:
                    th += 1
                    if th > self.threshold:
                        return FailFormatting(self, index, remainingReply)
                j += 1

            index += 1
            if index >= len(self.output):
                return Pass()

            remainingReply = remainingReply[i + len(o.expectedResult):]
