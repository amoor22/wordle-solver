from enum import Enum
from typing import List, Optional


class Hint(Enum):
    # wrong char
    GREY = 1
    # correct char but misplaced
    YELLOW = 2
    # correct char in place
    GREEN = 3


class Attempt:
    """
    Represents an attempt at guessing the Wordle word
    """

    def __init__(self, val: str, hints: Optional[List[Hint]] = []) -> None:
        self.val = val
        self.hints = hints

    def __iter__(self):
        # returns three iterators: index, char at index, hint for that char
        return iter(zip(range(len(self.val)), self.val, self.hints))
