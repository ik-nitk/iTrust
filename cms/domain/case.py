import dataclasses

@dataclasses.dataclass
class Case:
    case_id: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
