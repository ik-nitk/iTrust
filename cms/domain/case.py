import dataclasses
from cms.domain.case_state import CaseState
from cms.domain.case_type import CaseType

@dataclasses.dataclass
class Case:
    case_id: str
    beneficiary__id: str
    purpose: CaseType
    title: str
    description: str = ""
    family_details: str = ""
    amount_needed: int = 0
    amount_approved: int = 0
    avg_monthly_income: int = 0
    contact_details: str = ""
    contact_address: str = ""
    referred__by: str = ""
    closed__by: str = ""
    updated_by: str = ""
    case_state: CaseState = CaseState.DRAFT
    is_flagged: bool = False
    is_urgent: bool = False


    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
