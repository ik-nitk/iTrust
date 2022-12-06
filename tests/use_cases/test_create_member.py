from nanoid import generate
import pytest
from unittest import mock
from cms.domain.id_type import IDType

from cms.domain.member import Member
from cms.use_cases.member import create_new_member
from common.responses import ResponseTypes



@pytest.fixture
def domain_members():
    member_1 =  Member(
        member_id=generate(size=10),
        is_core= False,
        fname='fname1',
        lname='lname1',
        mname='maname1',
        govt_id='gid-111',
        id_type=IDType.AADHAAR,
        phone='968611',
        email='sample@gmail.com',
        updated__by='i.mem.1111'
    )

    member_2 =  Member(
        member_id=generate(size=10),
        is_core= False,
        fname='fname2',
        lname='lname2',
        mname='maname2',
        govt_id='gid-222',
        id_type=IDType.AADHAAR,
        phone='968612',
        email='sample2@gmail.com',
        updated__by='i.mem.1111'
    )

    return [member_1, member_2]

def test_create_member():
    repo = mock.Mock()
    repo.create_member.return_value = "i.mem.xxxx"

    response = create_new_member(repo, "gid-111", IDType.AADHAAR,"fname","mname","lname",False,"968612","sample@gmail.com", "i.mem.xxxx")

    assert bool(response) is True
    repo.create_member.assert_called_with("gid-111", IDType.AADHAAR,"fname","mname","lname",False,"968612","sample@gmail.com", "i.mem.xxxx")
    assert response.value == "i.mem.xxxx"

def test_create_member_exception():
    repo = mock.Mock()
    repo.create_member.side_effect = Exception("error")

    response = create_new_member(repo, "gid-111", IDType.AADHAAR,"fname","mname","lname",False,"968612","sample@gmail.com", "i.mem.xxxx")

    assert bool(response) is False
    repo.create_member.assert_called_with("gid-111", IDType.AADHAAR,"fname","mname","lname",False,"968612","sample@gmail.com", "i.mem.xxxx")

