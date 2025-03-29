from dataclasses import dataclass
from time import time
import uuid

@dataclass(frozen=True)
class Token:
    username: str
    uid : uuid
    time: int

    def isValid(self):
        elapsed = self.time - time()
        return elapsed < 86400 # 86400 -> amount of seconds 24 hours
                               # we only want a token to be valid for 24 hours
