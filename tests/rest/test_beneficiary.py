import json
from unittest import mock
from cms.domain.id_type import IDType

import pytest

from cms.domain.beneficiary import Beneficiary
from common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

beneficiary_dict = {
    "beneficiary_id": "i.ben.1111",
    "fname": 'fname1',
    "govt_id": 'abcd1234',
    "id_type": IDType.AADHAAR,
    "lname": 'lname1',
    "phone" : "984561111",
    "mname" : None,
    "email" : 'bsample.1111@gmail.com',
    "updated__by": "i.mem.1111"
}

beneficiaries = [Beneficiary.from_dict(beneficiary_dict)]

@mock.patch("application.rest.beneficiary.beneficiary_list_use_case")
def test_get(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(beneficiaries)

    http_response = client.get("/api/v1/beneficiaries")

    assert json.loads(http_response.data.decode("UTF-8")) == [beneficiary_dict]

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {}

    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


@mock.patch("application.rest.beneficiary.beneficiary_list_use_case")
def test_get_with_filters(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(beneficiaries)

    http_response = client.get(
        "/api/v1/beneficiaries?filter_phone__eq=984561111"
    )

    assert json.loads(http_response.data.decode("UTF-8")) == [beneficiary_dict]

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {"phone__eq": "984561111"}

    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


@pytest.mark.parametrize(
    "response_type, expected_status_code",
    [
        (ResponseTypes.PARAMETERS_ERROR, 400),
        (ResponseTypes.RESOURCE_ERROR, 404),
        (ResponseTypes.SYSTEM_ERROR, 500),
    ],
)
@mock.patch("application.rest.beneficiary.beneficiary_list_use_case")
def test_get_response_failures(
    mock_use_case,
    client,
    response_type,
    expected_status_code,
):
    mock_use_case.return_value = ResponseFailure(
        response_type,
        message="Just an error message",
    )

    http_response = client.get("/api/v1/beneficiaries?dummy_request_string")

    mock_use_case.assert_called()

    assert http_response.status_code == expected_status_code


@mock.patch("application.rest.beneficiary.create_new_beneficiary")
def test_post(mock_use_case, client):

    mock_use_case.return_value = ResponseSuccess(beneficiaries)
    data = {"govtId": "abcd1234", "idType": "AADHAAR", "firstName": "fname", "lastName":"lname", "middleName":"mname", "phone":"23456","email":"abc@gmail.com", "created_by": "i.mem.1111" }

    res = client.post("/api/v1/beneficiaries",json=data)

    assert res.status_code == 200
    assert res.mimetype == "application/json"

