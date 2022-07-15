import json


class CaseJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "case_id": o.case_id,
                "case_state": o.case_state,
                "is_flagged": o.is_flagged,
                "is_urgent": o.is_urgent,
                "beneficiary__id": o.beneficiary__id,
                "purpose": o.purpose,
                "title": o.title,
                "description": o.description,
                "family_details": o.family_details,
                "avg_monthly_income": o.avg_monthly_income,
                "contact_details": o.contact_details,
                "contact_address": o.contact_address,
                "referred__by": o.referred__by,
                "closed__by": o.closed__by,
                "updated_by": o.updated_by
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)