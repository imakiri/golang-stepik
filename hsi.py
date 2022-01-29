from typing import Any, Dict, List, Optional, Tuple, Type


class StageTest:
    def __init__(self):
        pass

class TestedProgram:
    def __init__(self):
        pass

    @property
    def run_args(self):
        raise NotImplementedError

    @property
    def executor(self):
        raise NotImplementedError

    def start(self, *args: str) -> str:
        raise NotImplementedError

    def execute(self, stdin: Optional[str]) -> str:
        raise NotImplementedError

class CheckResults:
    def __init__(self):
        pass

    @property
    def is_correct(self) -> bool:
        raise NotImplementedError

    @property
    def feedback(self) -> str:
        raise NotImplementedError

    @staticmethod
    def correct() -> 'CheckResult':
        raise NotImplementedError

    @staticmethod
    def wrong(feedback: str) -> 'CheckResult':
        raise NotImplementedError
