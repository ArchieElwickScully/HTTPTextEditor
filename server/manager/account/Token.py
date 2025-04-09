from dataclasses import dataclass
from time import time
import uuid

@dataclass(frozen=True)     # defining the class as a dataclass, frozen makes it immutable so no accidental
class Token:                # (or intentional and malicious) changing of variables in the class can cause issues
    username: str
    uid : uuid
    time: int

    SessionAESKey: bytes

    def isValid(self) -> bool:
        elapsed = self.time - time()
        return elapsed < 86400 # 86400 -> amount of seconds 24 hours
                               # we only want a token to be valid for 24 hours
