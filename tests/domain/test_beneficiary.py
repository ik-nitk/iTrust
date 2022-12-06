from nanoid import generate
from cms.domain.beneficiary import Beneficiary


def test_beneficiary_model_init():
    id = generate(size=10)
    beneficiary = Beneficiary(
        beneficiary_id=id,
        fname='fname',
        lname='lname',
        phone='9983100200',
        mname=None,
        email='bsample.1234@gmail.com',
        updated__by='i.mem.1111',
    )

    assert beneficiary.beneficiary_id == id
    assert beneficiary.fname == 'fname'
    assert beneficiary.lname == 'lname'
    assert beneficiary.phone == '9983100200'
    assert beneficiary.email == 'bsample.1234@gmail.com'


def test_beneficiary_model_from_dict():
    id = generate(size=10)
    init_dict = {
        "beneficiary_id": id,
        "fname": 'fname',
        "lname": 'lname',
        "phone" : "9983100200",
        "mname" : None,
        "email" : 'bsample.1234@gmail.com',
        "updated__by": 'i.mem.1111',
    }

    beneficiary = Beneficiary.from_dict(init_dict)

    assert beneficiary.beneficiary_id == id
    assert beneficiary.fname == 'fname'
    assert beneficiary.lname == 'lname'
    assert beneficiary.phone == '9983100200'
    assert beneficiary.email == 'bsample.1234@gmail.com'


def test_room_beneficiary_to_dict():
    id = generate(size=10)
    init_dict = {
        "beneficiary_id": id,
        "fname": 'fname',
        "lname": 'lname',
        "phone" : "9983100200",
        "mname" : None,
        "email" : 'bsample.1234@gmail.com',
        "updated__by": 'i.mem.1111',
    }

    beneficiary = Beneficiary.from_dict(init_dict)
    assert beneficiary.to_dict() == init_dict


def test_room_model_comparison():
    id = generate(size=10)
    init_dict = {
        "beneficiary_id": id,
        "fname": 'fname',
        "lname": 'lname',
        "phone" : "9983100200",
        "mname" : None,
        "email" : 'bsample.1234@gmail.com',
        "updated__by": 'i.mem.1111',
    }

    beneficiary1 = Beneficiary.from_dict(init_dict)
    beneficiary2 = Beneficiary.from_dict(init_dict)

    assert beneficiary1 == beneficiary2
