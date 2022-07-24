import dataclasses
from cms.domain.doc_type import DocType

@dataclasses.dataclass
class CaseDocs:
    case_id: str
    doc_type: DocType
    doc_id: str
    doc_name: str
    doc_url: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
