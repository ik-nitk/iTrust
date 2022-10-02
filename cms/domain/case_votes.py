import dataclasses

from cms.domain.vote_type import VoteType

@dataclasses.dataclass
class CaseVote:
    vote_id:str
    case_id: str
    voted_by: str
    amount_suggested:int
    vote: VoteType

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
