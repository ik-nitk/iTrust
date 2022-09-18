from contextlib import nullcontext
from cms.domain.case_state import CaseState
from cms.domain.case_type import CaseType
from nanoid import generate
from cms.domain.case import Case


def test_case_model_init():
    id = generate(size=10)
    case = Case(
        case_id=id,
        case_state=CaseState.DRAFT,
        beneficiary__id="id.121",
        purpose=CaseType.HOSPITAL,
        title="title",
        description="description",
        is_flagged=True,
        is_urgent=False,
        family_details="",
        amount_approved=0,
        amount_needed=0,
        avg_monthly_income= "",
        contact_details= "",
        contact_address= "",
        referred__by= "",
        closed__by= "",
        updated_by= ""
    )

    assert case.case_id == id
    assert case.case_state == CaseState.DRAFT
    assert case.beneficiary__id == "id.121"
    assert case.purpose == CaseType.HOSPITAL
    assert case.title == "title"
    assert case.description == "description"


def test_case_model_from_dict():
    id = generate(size=10)
    init_dict = {
        "case_id" : id,
        "case_state" : CaseState.DRAFT,
        "beneficiary__id" : "beneficiary__id",
        "purpose": CaseType.HOSPITAL,
        "title": "title",
        "description" : "description",
        "is_flagged": "",
        "is_urgent": "",
        "amount_needed": 0,
        "amount_approved": 0,
        "family_details": "",
        "avg_monthly_income": "",
        "contact_details": "",
        "contact_address": "",
        "referred__by": "",
        "closed__by": "",
        "updated_by": ""
    }

    case = Case.from_dict(init_dict)

    assert case.case_id == id
    assert case.purpose == CaseType.HOSPITAL
    assert case.title == "title"
    assert case.description == "description"
    assert case.beneficiary__id == "beneficiary__id"
    assert case.case_state == CaseState.DRAFT


def test_case_to_dict():
    id = generate(size=10)
    init_dict = {
        "case_id" : id,
        "case_state" : CaseState.DRAFT,
        "beneficiary__id" : "beneficiary__id",
        "purpose": CaseType.HOSPITAL,
        "title": "title",
        "description" : "description",
        "is_flagged": "",
        "is_urgent": "",
        "amount_needed": 0,
        "amount_approved": 0,
        "family_details": "",
        "avg_monthly_income": "",
        "contact_details": "",
        "contact_address": "",
        "referred__by": "",
        "closed__by": "",
        "updated_by": ""
    }

    case = Case.from_dict(init_dict)
    assert case.to_dict() == init_dict


def test_case_model_comparison():
    id = generate(size=10)
    init_dict = {
        "case_id" : id,
        "case_state" : CaseState.DRAFT,
        "beneficiary__id" : "beneficiary__id",
        "purpose": CaseType.HOSPITAL,
        "title": "title",
        "description" : "description",
        "is_flagged": "",
        "is_urgent": "",
        "amount_needed": 0,
        "amount_approved": 0,
        "family_details": "",
        "avg_monthly_income": "",
        "contact_details": "",
        "contact_address": "",
        "referred__by": "",
        "closed__by": "",
        "updated_by": ""
    }

    case1 = Case.from_dict(init_dict)
    case2 = Case.from_dict(init_dict)

    assert case1 == case2
