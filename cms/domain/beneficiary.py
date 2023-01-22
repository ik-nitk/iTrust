import dataclasses
from cms.domain.id_type import IDType

@dataclasses.dataclass
class Beneficiary:
    beneficiary_id: str #TODO- Currently nanoid, move to some ID class
    fname: str
    lname: str
    mname: str
    phone: str
    govt_id: str
    id_type: IDType
    email: str
    updated__by: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
