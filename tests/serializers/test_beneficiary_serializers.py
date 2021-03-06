import json
from nanoid import generate

from cms.serializers.beneficiary import BeneficiaryJsonEncoder
from cms.domain.beneficiary import Beneficiary


def test_serialize_domain_beneficiary():
    id = generate(size=10)

    beneficiary = Beneficiary(
        beneficiary_id=id,
        fname='fname',
        lname='lname',
        phone='9983100200',
        mname=None,
        email='sample.1234@gmail.com'
    )

    expected_json = f"""
        {{
            "beneficiary_id": "{id}",
            "fname": "fname",
            "lname": "lname",
            "phone" : "9983100200",
            "mname" : null,
            "email" : "sample.1234@gmail.com"
        }}
    """

    beneficiary_x = json.dumps(beneficiary, cls=BeneficiaryJsonEncoder)

    assert json.loads(beneficiary_x) == json.loads(expected_json)
