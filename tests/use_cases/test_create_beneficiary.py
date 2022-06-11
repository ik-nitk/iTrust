from nanoid import generate
import pytest
from unittest import mock

from cms.domain.beneficiary import Beneficiary
from cms.use_cases.create_beneficiary import create_new_beneficiary
from common.responses import ResponseTypes



@pytest.fixture
def domain_members():
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

    return [beneficiary_1, beneficiary_2]

def test_create_beneficiary():
    repo = mock.Mock()
    repo.create_beneficiary.return_value = "i.ben.xxxx"

    response = create_new_beneficiary(repo, "fname","mname","lname","968612","sample@gmail.com")

    assert bool(response) is True
    repo.create_beneficiary.assert_called_with("fname","mname","lname","968612","sample@gmail.com")
    assert response.value == "i.ben.xxxx"

def test_create_member_exception():
    repo = mock.Mock()
    repo.create_beneficiary.side_effect = Exception("error")

    response = create_new_beneficiary(repo, "fname","mname","lname","968612","sample@gmail.com")

    assert bool(response) is False
    repo.create_beneficiary.assert_called_with("fname","mname","lname","968612","sample@gmail.com")

