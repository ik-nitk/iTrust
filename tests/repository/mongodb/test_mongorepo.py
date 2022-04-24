from pydoc import doc
import pytest
from fms.repository import mongorepo
from fms.domain.documents import Document

pytestmark = pytest.mark.integration

def test_repository_insert_document(
    app_configuration, mg_database, mg_test_data
):
    repo = mongorepo.MongoRepo(app_configuration)
    id = repo.insert_document("sample", "user")
    assert "i.doc." in id

def test_repository_insert_and_find_document(
    app_configuration, mg_database, mg_test_data
):
    repo = mongorepo.MongoRepo(app_configuration)
    id = repo.insert_document("sample_test", "test_user")
    assert "i.doc." in id
    document = repo.find_document(id)
    assert document.uploaded_by == "test_user"
    assert document.filename == "sample_test"
