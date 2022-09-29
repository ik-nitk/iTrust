import dataclasses

@dataclasses.dataclass
class CaseVote:
    vote_id:str
    case_id: str
    voted_by: str
    amount_suggested:int
    comment: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
