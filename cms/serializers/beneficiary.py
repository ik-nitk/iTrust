import json


class BeneficiaryJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "beneficiary_id": o.beneficiary_id,
                "fname": o.fname,
                "lname": o.lname,
                "mname": o.mname,
                "phone": o.phone,
                "email": o.email
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)
