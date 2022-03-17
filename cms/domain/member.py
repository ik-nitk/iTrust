import dataclasses
from cms.domain.id_type import IDType

@dataclasses.dataclass
class Member:
    member_id: str #TODO- Currently nanoid, move to some ID class
    is_core: bool
    fname: str
    lname: str
    mname: str
    govt_id: str
    id_type: IDType
    phone: str
    email: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
