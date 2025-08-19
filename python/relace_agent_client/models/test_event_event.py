from enum import Enum


class TestEventEvent(str, Enum):
    FAIL = "fail"
    PASS = "pass"
    START = "start"

    def __str__(self) -> str:
        return str(self.value)
