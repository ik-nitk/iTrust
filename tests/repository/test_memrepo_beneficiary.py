import pytest

from cms.domain.beneficiary import Beneficiary
from cms.domain.id_type import IDType
from cms.repository.memrepo import MemRepo


@pytest.fixture
def beneficiary_dicts():
    return [
        {
            "beneficiary_id": "i.ben.1111",
            "fname": 'fname1',
            "lname": 'lname1',
            "phone" : "984561111",
            "mname" : None,
            "email" : 'sample.1111@gmail.com',
            "updated__by": "i.mem.1111"
         },
         {
            "beneficiary_id": "i.ben.2222",
            "fname": 'fname2',
            "lname": 'lname2',
            "phone" : "984562222",
            "mname" : None,
            "email" : 'sample.2222@gmail.com',
            "updated__by": "i.mem.1111"
         },
         {
            "beneficiary_id": "i.ben.3333",
            "fname": 'fname3',
            "lname": 'lname3',
            "phone" : "984563333",
            "mname" : None,
            "email" : 'sample.3333@gmail.com',
            "updated__by": "i.mem.1111"
         },
    ]


def test_repository_list_without_parameters(beneficiary_dicts):
    repo = MemRepo(beneficiary_dicts)

    beneficiarys = [Beneficiary.from_dict(i) for i in beneficiary_dicts]

    assert repo.beneficiary_list() == beneficiarys


def test_repository_list_with_phone_equal_filter(beneficiary_dicts):
    repo = MemRepo(beneficiary_dicts)

    beneficiarys = repo.beneficiary_list(
        filters={"phone__eq": "984562222"}
    )

    assert len(beneficiarys) == 1
    assert beneficiarys[0].phone == "984562222"


def test_repository_list_with_email_equal_filter(beneficiary_dicts):
    repo = MemRepo(beneficiary_dicts)

    beneficiarys = repo.beneficiary_list(filters={"email__eq": 'sample.2222@gmail.com'})

    assert len(beneficiarys) == 1
    assert beneficiarys[0].beneficiary_id == "i.ben.2222"


def test_repository_list_with_member_id_filter(beneficiary_dicts):
    repo = MemRepo(beneficiary_dicts)

    beneficiarys = repo.beneficiary_list(filters={"beneficiary_id__eq": 'i.ben.1111'})

    assert len(beneficiarys) == 1
    assert beneficiarys[0].beneficiary_id == "i.ben.1111"
