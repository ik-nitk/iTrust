from cms.domain.case_type import CaseType
from nanoid import generate
import pytest
from unittest import mock

from cms.domain.case import Case
from cms.domain.case_state import CaseState
from cms.domain.doc_type import DocType
from cms.domain.case_type import CaseType
from cms.use_cases.case import create_new_case, add_initial_documents_use_case
from common.responses import ResponseTypes



@pytest.fixture
def domain_case():
    case_1 =  Case(
        case_id=generate(size=10),
        case_state=CaseState.DRAFT,
        is_flagged=True,
        is_urgent=True,
        beneficiary__id='i.ben.1234'
    )

    case_2 =  Case(
        case_id=generate(size=10),
        case_state=CaseState.DRAFT,
        is_flagged=True,
        is_urgent=False,
        beneficiary__id='i.ben.1235'
    )

    return [case_1, case_2]

def test_create_case():
    repo = mock.Mock()
    repo.create_case.return_value = "i.case.xxxx"

    response = create_new_case(repo, beneficiary_id="i.ben.1235", purpose="", title="", description="",amount_needed=0, created_by='i.mem.111')

    assert bool(response) is True
    repo.create_case.assert_called_with(beneficiary_id="i.ben.1235", purpose="", title="", description="",amount_needed=0, created_by='i.mem.111')
    assert response.value == "i.case.xxxx"

def test_add_documents():
    repo = mock.Mock()
    repo.find_case.return_value = Case(
        case_id=generate(size=10),
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234'
    )
    response = add_initial_documents_use_case(repo, case_id='case_id', created_by='i.mem.1111' ,doc_list=[
        {"doc_url":"url1", "doc_name": "doc_name1"},
        {"doc_url":"url2", "doc_name": "doc_name2"}
    ])
    assert bool(response) is True