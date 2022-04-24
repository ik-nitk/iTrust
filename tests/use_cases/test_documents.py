import pytest
from unittest import mock

from fms.domain.documents import Document
from fms.use_cases.documents import create_new_document, find_document
from common.responses import ResponseTypes


@pytest.fixture
def domain_documents():
    document_1 =  Document(
        _id="document_1",
        uploaded_by='fname1',
        filename='lname1',
        created_at=123456,
    )

    document_2 =  Document(
        _id="document_2",
        uploaded_by='fname2',
        filename='lname2',
        created_at=123456,
    )

    return [document_1, document_2]

def test_document_create():
    repo = mock.Mock()
    repo.insert_document.return_value = "i.doc.xxxx"

    response = create_new_document(repo, "sample", "user")

    assert bool(response) is True
    repo.insert_document.assert_called_with("sample", "user")
    assert response.value == "i.doc.xxxx"

def test_document_create_exception():
    repo = mock.Mock()
    repo.insert_document.side_effect = Exception("error")

    response = create_new_document(repo, "sample", "user")

    assert bool(response) is False
    repo.insert_document.assert_called_with("sample", "user")

def test_document_find(domain_documents):
    repo = mock.Mock()
    repo.find_document.return_value = domain_documents[0]

    response = find_document(repo, "document_1")

    assert bool(response) is True
    repo.find_document.assert_called_with("document_1")
    assert response.value._id == "document_1"

def test_document_find_exception():
    repo = mock.Mock()
    repo.find_document.side_effect = Exception("Error")

    response = find_document(repo, "document_1")

    assert bool(response) is False
    repo.find_document.assert_called_with("document_1")