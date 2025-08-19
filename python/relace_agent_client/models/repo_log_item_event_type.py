from enum import Enum


class RepoLogItemEventType(str, Enum):
    AGENT = "agent"
    BUILD = "build"
    COMMITTED = "committed"
    DEPLOYED = "deployed"
    DONE = "done"
    PROMPT_ERROR = "prompt_error"
    STARTED = "started"
    TEST = "test"
    TOOL = "tool"
    USER_PROMPT = "user_prompt"

    def __str__(self) -> str:
        return str(self.value)
