from collections.abc import Mapping


class CaseListInvalidRequest:
    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self):
        return len(self.errors) > 0

    def __bool__(self):
        return False


class CaseListValidRequest:
    def __init__(self, filters=None, limit=100):
        self.filters = filters
        self.limit = limit

    def __bool__(self):
        return True


def build_case_list_request(filters=None, limit=100):
    accepted_filters = ["beneficiary_id__eq","member_id__eq","case_state__eq"]
    invalid_req = CaseListInvalidRequest()

    if filters is not None:
        if not isinstance(filters, Mapping):
            invalid_req.add_error("filters", "Is not iterable")
            return invalid_req

        for key, value in filters.items():
            if key not in accepted_filters:
                invalid_req.add_error(
                    "filters", "Key {} cannot be used".format(key)
                )

        if invalid_req.has_errors():
            return invalid_req

    return CaseListValidRequest(filters=filters, limit=limit)
