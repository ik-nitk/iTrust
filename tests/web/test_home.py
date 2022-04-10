from requests import Session
from unittest.mock import patch
from unittest import mock
import json

import pytest

from cms.domain.member import Member
from cms.domain.id_type import IDType
from cms.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

from web.app import create_app


@pytest.fixture
def app():
    app = create_app("testing")
    return app

def test_home_page(client):
    http_response = client.get("/")

    assert http_response.status_code == 200
    assert http_response.mimetype == "text/html"
