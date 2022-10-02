from enum import Enum

class VoteType(str, Enum):
    APPROVE = 'APPROVE'
    REJECT = 'REJECT'