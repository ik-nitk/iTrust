import json


class CaseJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "case_id": o.case_id,
                "case_state": o.fname,
                "is_flagged": o.lname,
                "is_urgent": o.mname,
                "beneficiary__id": o.phone,
                "purpose": o.email,
                "title": o.title,
                "description": o.description,
                "family_details": o.family_details,
                "avg_monthly_income": o.avg_monthly_income,
                "contact_details": o.contact_details,
                "contact_address": o.contact_address,
                "referred__by": o.referred__by,
                "assigned__for_verification": o.assigned__for_verification,
                "assigned__for_accounting": o.assigned__for_accounting,
                "closed__by": o.closed__by,
                "updated_by": o.updated_by
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)