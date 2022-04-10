import dataclasses

@dataclasses.dataclass
class Beneficiary:
    beneficiary_id: str #TODO- Currently nanoid, move to some ID class
    fname: str
    lname: str
    mname: str
    phone: str
    email: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
