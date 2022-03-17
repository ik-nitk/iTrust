import json
from unittest import mock

import pytest

from cms.domain.member import Member
from cms.domain.id_type import IDType
from cms.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

member_dict = {
    "member_id": "i.mem.1111",
    "fname": 'fname1',
    "lname": 'lname1',
    "govt_id": 'abcd1111',
    "id_type": IDType.AADHAAR,
    "phone" : "984561111",
    "mname" : None,
    "is_core": False,
    "email" : 'sample.1111@gmail.com'
}

members = [Member.from_dict(member_dict)]

@mock.patch("application.rest.member.member_list_use_case")
def test_get(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(members)

    http_response = client.get("/members")

    assert json.loads(http_response.data.decode("UTF-8")) == [member_dict]

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {}

    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


@mock.patch("application.rest.member.member_list_use_case")
def test_get_with_filters(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(members)

    http_response = client.get(
        "/members?filter_phone__eq=984561111&filter_govt_id__eq=abcd1111"
    )

    assert json.loads(http_response.data.decode("UTF-8")) == [member_dict]

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {"phone__eq": "984561111", "govt_id__eq": "abcd1111"}

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
@mock.patch("application.rest.member.member_list_use_case")
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

    http_response = client.get("/members?dummy_request_string")

    mock_use_case.assert_called()

    assert http_response.status_code == expected_status_code
