import json
from nanoid import generate
from cms.domain.id_type import IDType

from cms.serializers.member import MemberJsonEncoder
from cms.domain.member import Member


def test_serialize_domain_member():
    id = generate(size=10)

    member = Member(
        member_id=id,
        is_core=False,
        fname='fname',
        lname='lname',
        govt_id='abcd1234',
        id_type=IDType.AADHAAR,
        phone='9983100200',
        mname=None,
        email='sample.1234@gmail.com',
        updated__by='i.mem.111'
    )

    expected_json = f"""
        {{
            "member_id": "{id}",
            "fname": "fname",
            "lname": "lname",
            "govt_id": "abcd1234",
            "id_type": "AADHAAR",
            "phone" : "9983100200",
            "mname" : null,
            "is_core": false,
            "email" : "sample.1234@gmail.com",
            "updated__by" : "i.mem.111"
        }}
    """

    member_room = json.dumps(member, cls=MemberJsonEncoder)

    assert json.loads(member_room) == json.loads(expected_json)
