import pytest

from cms.domain.member import Member
from cms.domain.id_type import IDType
from cms.repository.memrepo import MemRepo


@pytest.fixture
def member_dicts():
    return [
        {
            "member_id": "i.mem.1111",
            "fname": 'fname1',
            "lname": 'lname1',
            "govt_id": 'abcd1111',
            "id_type": IDType.AADHAAR,
            "phone" : "984561111",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.1111@gmail.com'
         },
         {
            "member_id": "i.mem.2222",
            "fname": 'fname2',
            "lname": 'lname2',
            "govt_id": 'abcd2222',
            "id_type": IDType.AADHAAR,
            "phone" : "984562222",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.2222@gmail.com'
         },
         {
            "member_id": "i.mem.3333",
            "fname": 'fname3',
            "lname": 'lname3',
            "govt_id": 'abcd3333',
            "id_type": IDType.AADHAAR,
            "phone" : "984563333",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.3333@gmail.com'
         },
         {
            "member_id": "i.mem.4444",
            "fname": 'fname4',
            "lname": 'lname4',
            "govt_id": 'abcd4444',
            "id_type": IDType.AADHAAR,
            "phone" : "984564444",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.4444@gmail.com'
         },
    ]


def test_repository_list_without_parameters(member_dicts):
    repo = MemRepo(member_dicts)

    members = [Member.from_dict(i) for i in member_dicts]

    assert repo.member_list() == members


def test_repository_list_with_phone_equal_filter(member_dicts):
    repo = MemRepo(member_dicts)

    members = repo.member_list(
        filters={"phone__eq": "984564444"}
    )

    assert len(members) == 1
    assert members[0].phone == "984564444"


def test_repository_list_with_email_equal_filter(member_dicts):
    repo = MemRepo(member_dicts)

    members = repo.member_list(filters={"email__eq": 'sample.2222@gmail.com'})

    assert len(members) == 1
    assert members[0].member_id == "i.mem.2222"


def test_repository_list_with_govt_id_filter(member_dicts):
    repo = MemRepo(member_dicts)

    members = repo.member_list(filters={"govt_id__eq": 'abcd3333'})

    assert len(members) == 1
    assert members[0].member_id == "i.mem.3333"


def test_repository_list_with_member_id_filter(member_dicts):
    repo = MemRepo(member_dicts)

    members = repo.member_list(filters={"member_id__eq": 'i.mem.1111'})

    assert len(members) == 1
    assert members[0].member_id == "i.mem.1111"
