from cms.domain.member import Member
from cms.domain.beneficiary import Beneficiary


class MemRepo:
    def __init__(self, data):
        self.data = data

    def member_list(self, filters=None):

        result = [Member.from_dict(i) for i in self.data]

        if filters is None:
            return result

        if "member_id__eq" in filters:
            result = [r for r in result if r.member_id == filters["member_id__eq"]]

        if "phone__eq" in filters:
            result = [
                r for r in result if r.phone == filters["phone__eq"]
            ]

        if "email__eq" in filters:
            result = [
                r for r in result if r.email == filters["email__eq"]
            ]

        if "govt_id__eq" in filters:
            result = [
                r for r in result if r.govt_id == filters["govt_id__eq"]
            ]

        return result

    def beneficiary_list(self, filters=None):

            result = [Beneficiary.from_dict(i) for i in self.data]

            if filters is None:
                return result

            if "beneficiary_id__eq" in filters:
                result = [r for r in result if r.beneficiary_id == filters["beneficiary_id__eq"]]

            if "phone__eq" in filters:
                result = [
                    r for r in result if r.phone == filters["phone__eq"]
                ]

            if "email__eq" in filters:
                result = [
                    r for r in result if r.email == filters["email__eq"]
                ]

            return result
