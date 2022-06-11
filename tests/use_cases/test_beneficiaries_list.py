import pytest
from nanoid import generate
from unittest import mock

from cms.domain.beneficiary import Beneficiary
from cms.use_cases.beneficiary_list import beneficiary_list_use_case
from cms.requests.beneficiary_list import build_beneficiary_list_request
from common.responses import ResponseTypes


@pytest.fixture
def domain_beneficiaries():
    beneficiary_1 =  Beneficiary(
        beneficiary_id=generate(size=10),
        fname='fname1',
        lname='lname1',
        mname='maname1',
        phone='968611',
        email='bsample@gmail.com'
    )

    beneficiary_2 =  Beneficiary(
        beneficiary_id=generate(size=10),
        fname='fname2',
        lname='lname2',
        mname='maname2',
        phone='968612',
        email='bsample2@gmail.com'
    )

    beneficiary_3 =  Beneficiary(
        beneficiary_id=generate(size=10),
        fname='fname3',
        lname='lname3',
        mname='maname3',
        phone='968613',
        email='bsample3@gmail.com'
    )

    beneficiary_4 =  Beneficiary(
        beneficiary_id=generate(size=10),
        fname='fname4',
        lname='lname4',
        mname='maname4',
        phone='968614',
        email='bsample4@gmail.com'
    )

    return [beneficiary_1, beneficiary_2,beneficiary_3,beneficiary_4]


def test_member_list_without_parameters(domain_beneficiaries):
    repo = mock.Mock()
    repo.beneficiary_list.return_value = domain_beneficiaries

    request = build_beneficiary_list_request()

    response = beneficiary_list_use_case(repo, request)

    assert bool(response) is True
    repo.beneficiary_list.assert_called_with(filters=None)
    assert response.value == domain_beneficiaries


def test_beneficiary_list_with_filters(domain_beneficiaries):
    repo = mock.Mock()
    repo.beneficiary_list.return_value = domain_beneficiaries

    qry_filters = {"phone__eq": '333300200'}
    request = build_beneficiary_list_request(filters=qry_filters)

    response = beneficiary_list_use_case(repo, request)

    assert bool(response) is True
    repo.beneficiary_list.assert_called_with(filters=qry_filters)
    assert response.value == domain_beneficiaries


def test_beneficiary_list_handles_generic_error():
    repo = mock.Mock()
    repo.beneficiary_list.side_effect = Exception("Just an error message")

    request = build_beneficiary_list_request(filters={})

    response = beneficiary_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.SYSTEM_ERROR,
        "message": "Exception: Just an error message",
    }


def test_beneficiary_list_handles_bad_request():
    repo = mock.Mock()

    request = build_beneficiary_list_request(filters=5)

    response = beneficiary_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.PARAMETERS_ERROR,
        "message": "filters: Is not iterable",
    }
