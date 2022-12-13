import json
from nanoid import generate

from cms.serializers.beneficiary import BeneficiaryJsonEncoder
from cms.domain.beneficiary import Beneficiary
from cms.domain.id_type import IDType


def test_serialize_domain_beneficiary():
    id = generate(size=10)

    beneficiary = Beneficiary(
        beneficiary_id=id,
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
            "beneficiary_id": "{id}",
            "fname": "fname",
            "lname": "lname",
            "govt_id": "abcd1234",
            "id_type": "AADHAAR",
            "phone" : "9983100200",
            "mname" : null,
            "email" : "sample.1234@gmail.com",
            "updated__by" : "i.mem.111"
        }}
    """

    beneficiary_x = json.dumps(beneficiary, cls=BeneficiaryJsonEncoder)

    assert json.loads(beneficiary_x) == json.loads(expected_json)
