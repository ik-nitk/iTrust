import requests
from requests import Session
from unittest.mock import patch
import json
from cms.serializers.member import MemberJsonEncoder
import pytest

from cms.domain.member import Member
from cms.domain.id_type import IDType
from common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

from web.app import create_app


@pytest.fixture
def app():
    app = create_app("testing")
    return app

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

@patch.object(Session, 'get')
def test_get(mock_get, client):
    mock_get.return_value = requests.Response()
    json_data = json.dumps(members, cls=MemberJsonEncoder)
    mock_get.return_value.__setstate__({
            'status_code': 200, '_content': json_data.encode("utf-8")})

    http_response = client.get("/members")

    assert http_response.status_code == 200
    assert http_response.mimetype == "text/html"
