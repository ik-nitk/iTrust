import dataclasses
from cms.domain.comment_type import CommentType

@dataclasses.dataclass
class CaseComment:
    case_id: str
    comment_type: CommentType
    comment_id: str
    comment: str
    commented_by: str
    comment_data: dict

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
