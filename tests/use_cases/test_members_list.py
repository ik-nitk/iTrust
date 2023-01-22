import pytest
from nanoid import generate
from unittest import mock

from cms.domain.member import Member
from cms.domain.id_type import IDType
from cms.use_cases.member import member_list_use_case,create_new_member
from cms.requests.member_list import build_member_list_request
from common.responses import ResponseTypes


@pytest.fixture
def domain_members():
    member_1 =  Member(
        member_id=generate(size=10),
        is_core=False,
        fname='fname1',
        lname='lname1',
        govt_id='1111',
        id_type=IDType.AADHAAR,
        phone='111100200',
        mname=None,
        email='sample.1111@gmail.com',
        updated__by='i.mem.111'
    )

    member_2 =  Member(
        member_id=generate(size=10),
        is_core=False,
        fname='fname2',
        lname='lname2',
        govt_id='2222',
        id_type=IDType.AADHAAR,
        phone='222200200',
        mname=None,
        email='sample.2222@gmail.com',
        updated__by='i.mem.111'
    )

    member_3 =  Member(
        member_id=generate(size=10),
        is_core=False,
        fname='fname3',
        lname='lname3',
        govt_id='3333',
        id_type=IDType.AADHAAR,
        phone='333300200',
        mname=None,
        email='sample.3333@gmail.com',
        updated__by='i.mem.111'
    )

    member_4 =  Member(
        member_id=generate(size=10),
        is_core=False,
        fname='fname3',
        lname='lname3',
        govt_id='3333',
        id_type=IDType.AADHAAR,
        phone='333300200',
        mname=None,
        email='sample.3333@gmail.com',
        updated__by='i.mem.111'
    )

    return [member_1, member_2, member_3, member_4]

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


def test_member_list_without_parameters(domain_members):
    repo = mock.Mock()
    repo.member_list.return_value = domain_members

    request = build_member_list_request()

    response = member_list_use_case(repo, request)

    assert bool(response) is True
    repo.member_list.assert_called_with(filters=None)
    assert response.value == domain_members


def test_member_list_with_filters(domain_members):
    repo = mock.Mock()
    repo.member_list.return_value = domain_members

    qry_filters = {"phone__eq": '333300200'}
    request = build_member_list_request(filters=qry_filters)

    response = member_list_use_case(repo, request)

    assert bool(response) is True
    repo.member_list.assert_called_with(filters=qry_filters)
    assert response.value == domain_members


def test_member_list_handles_generic_error():
    repo = mock.Mock()
    repo.member_list.side_effect = Exception("Just an error message")

    request = build_member_list_request(filters={})

    response = member_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.SYSTEM_ERROR,
        "message": "Exception: Just an error message",
    }


def test_member_list_handles_bad_request():
    repo = mock.Mock()

    request = build_member_list_request(filters=5)

    response = member_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.PARAMETERS_ERROR,
        "message": "filters: Is not iterable",
    }
