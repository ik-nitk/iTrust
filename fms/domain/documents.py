import dataclasses

@dataclasses.dataclass
class Document(dict):
    _id: str
    uploaded_by: str
    filename: str
    created_at: int

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
