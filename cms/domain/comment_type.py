from enum import Enum

class CommentType(str, Enum):
    VERIFICATION_COMMENTS = 'VERIFICATION_COMMENTS'
    PAYMENT_COMMENTS = 'PAYMENT_COMMENTS'
    APPROVAL_COMMENTS = 'APPROVAL_COMMENTS'
    OTHER_COMMENTS = 'OTHER_COMMENTS'
