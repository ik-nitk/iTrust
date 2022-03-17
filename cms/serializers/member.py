import json


class MemberJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "member_id": o.member_id,
                "is_core": o.is_core,
                "fname": o.fname,
                "lname": o.lname,
                "mname": o.mname,
                "govt_id": o.govt_id,
                "id_type": o.id_type,
                "phone": o.phone,
                "email": o.email
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)
