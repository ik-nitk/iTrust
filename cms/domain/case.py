import dataclasses
from cms.domain.id_type import IDType

@dataclasses.dataclass
class Case:
    case_id: str
    case_state: str
    is_flagged: bool
    is_urgent: bool
    beneficiary__id: str
    purpose: str
    title: str
    description: str
    family_details: str
    avg_monthly_income: int
    contact_details: str
    contact_address: str
    referred__by: str
    assigned__for_verification: str
    assigned__for_accounting: str
    closed__by: str
    updated_by: str


    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
