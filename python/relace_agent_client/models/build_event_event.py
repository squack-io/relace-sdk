from enum import Enum


class BuildEventEvent(str, Enum):
    FAIL = "fail"
    PASS = "pass"
    START = "start"

    def __str__(self) -> str:
        return str(self.value)
