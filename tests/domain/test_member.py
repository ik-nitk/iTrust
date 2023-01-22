from contextlib import nullcontext
from cms.domain.id_type import IDType
from nanoid import generate
from cms.domain.member import Member


def test_member_model_init():
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
        updated__by=id
    )

    assert member.member_id == id
    assert member.is_core == False
    assert member.fname == 'fname'
    assert member.lname == 'lname'
    assert member.phone == '9983100200'
    assert member.email == 'sample.1234@gmail.com'


def test_member_model_from_dict():
    id = generate(size=10)
    init_dict = {
        "member_id": id,
        "fname": 'fname',
        "lname": 'lname',
        "govt_id": 'abcd1234',
        "id_type": IDType.AADHAAR,
        "phone" : "9983100200",
        "mname" : None,
        "is_core": False,
        "email" : 'sample.1234@gmail.com',
        "updated__by": id
    }

    member = Member.from_dict(init_dict)

    assert member.member_id == id
    assert member.is_core == False
    assert member.govt_id == 'abcd1234'
    assert member.id_type == IDType.AADHAAR
    assert member.fname == 'fname'
    assert member.lname == 'lname'
    assert member.phone == '9983100200'
    assert member.email == 'sample.1234@gmail.com'


def test_room_member_to_dict():
    id = generate(size=10)
    init_dict = {
        "member_id": id,
        "fname": 'fname',
        "lname": 'lname',
        "govt_id": 'abcd1234',
        "id_type": 1,
        "phone" : "9983100200",
        "mname" : None,
        "is_core": False,
        "email" : 'sample.1234@gmail.com',
        "updated__by": id
    }

    member = Member.from_dict(init_dict)
    assert member.to_dict() == init_dict


def test_room_model_comparison():
    id = generate(size=10)
    init_dict = {
        "member_id": id,
        "fname": 'fname',
        "lname": 'lname',
        "govt_id": 'abcd1234',
        "id_type": 1,
        "phone" : "9983100200",
        "mname" : None,
        "is_core": False,
        "email" : 'sample.1234@gmail.com',
        "updated__by": id
    }

    member1 = Member.from_dict(init_dict)
    member2 = Member.from_dict(init_dict)

    assert member1 == member2
