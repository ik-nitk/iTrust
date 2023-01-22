from cms.domain.case_type import CaseType
from nanoid import generate
import pytest
from unittest import mock

from cms.domain.member import Member
from cms.domain.case import Case
from cms.domain.id_type import IDType
from cms.domain.case_votes import CaseVote
from cms.domain.case_state import CaseState
from cms.domain.case_type import CaseType
from cms.domain.case_comments import CommentType
from cms.domain.vote_type import VoteType
from cms.use_cases.case import create_new_case, add_initial_documents_use_case, add_vote, close_case_with_details, add_payment_details_use_case
from common.responses import ResponseTypes


@pytest.fixture
def core_member():
    member_1 =  Member(
        member_id=generate(size=10),
        is_core=True,
        fname='fname1',
        lname='lname1',
        govt_id='1111',
        id_type=IDType.AADHAAR,
        phone='111100200',
        mname=None,
        email='sample.1111@gmail.com',
        updated__by='i.mem.111'
    )

    return member_1

@pytest.fixture
def non_core_member():
    member_1 =  Member(
        member_id=generate(size=10),
        is_core=False,
        fname='fname1',
        lname='lname1',
        govt_id='1111',
        id_type=IDType.AADHAAR,
        phone='111100200',
        mname=None,
        email='sample.1111@gmail.com',
        updated__by='i.mem.111'
    )

    return member_1

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

def test_case_closed_non_core(non_core_member):
    repo = mock.Mock()
    case_id="i.case.xxxx"
    repo.find_case.return_value = Case(
        case_id=case_id,
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.VOTING
    )
    repo.find_member.return_value = non_core_member
    response = close_case_with_details(repo, case_id, "comment", closed_by='i.mem.111')
    assert bool(response) is False
    repo.create_case_comment.assert_not_called()

def test_case_closed_core(core_member):
    repo = mock.Mock()
    case_id="i.case.xxxx"
    repo.find_case.return_value = Case(
        case_id=case_id,
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.VOTING
    )
    repo.find_member.return_value = core_member
    response = close_case_with_details(repo, case_id, "comment", closed_by='i.mem.111')
    assert bool(response) is True
    repo.create_case_comment.assert_called_with(case_id, comment_type=CommentType.CLOSING_COMMENTS, comment="comment", comment_data={}, c_by='i.mem.111')
    repo.update_case_state.assert_called_with(case_id, CaseState.CLOSE, 'i.mem.111')

def test_case_approved_without_votes():
    repo = mock.Mock()
    case_id="i.case.xxxx"
    repo.find_case.return_value = Case(
        case_id=case_id,
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.VOTING
    )
    repo.upsert_case_vote.return_value = "i.vote.123"
    repo.case_vote_list.return_value = []

    response = add_vote(repo, case_id, VoteType.APPROVE, "comment", 1000, created_by='i.mem.111')
    assert bool(response) is True
    repo.upsert_case_vote.assert_called_with(case_id, VoteType.APPROVE, "comment", 1000, 'i.mem.111')
    repo.update_case_state.assert_not_called()

def test_case_approved_with_one_vote():
    repo = mock.Mock()
    case_id="i.case.xxxx"
    repo.find_case.return_value = Case(
        case_id=case_id,
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.VOTING
    )
    repo.upsert_case_vote.return_value = "i.vote.123"
    repo.case_vote_list.return_value = [
        CaseVote(is_core=True, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=False, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment='')
    ]

    response = add_vote(repo, case_id, VoteType.APPROVE, "comment", 1000, created_by='i.mem.111')
    assert bool(response) is True
    repo.upsert_case_vote.assert_called_with(case_id, VoteType.APPROVE, "comment", 1000, 'i.mem.111')
    repo.update_case_state.assert_not_called()


def test_case_approved_with_two_vote():
    repo = mock.Mock()
    case_id="i.case.xxxx"
    repo.find_case.return_value = Case(
        case_id=case_id,
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.VOTING
    )
    repo.upsert_case_vote.return_value = "i.vote.123"
    repo.case_vote_list.return_value = [
        CaseVote(is_core=True, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment='')
    ]

    response = add_vote(repo, case_id, VoteType.APPROVE, "comment", 1000, created_by='i.mem.111')
    assert bool(response) is True
    repo.upsert_case_vote.assert_called_with(case_id, VoteType.APPROVE, "comment", 1000, 'i.mem.111')
    repo.update_case_state.assert_called_with(case_id, CaseState.APPROVED, 'i.mem.111')

def test_case_approved_with_two_vote_approved_one_reject():
    repo = mock.Mock()
    case_id="i.case.xxxx"
    repo.find_case.return_value = Case(
        case_id=case_id,
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.VOTING
    )
    repo.upsert_case_vote.return_value = "i.vote.123"
    repo.case_vote_list.return_value = [
        CaseVote(is_core=True, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.REJECT, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
    ]

    response = add_vote(repo, case_id, VoteType.APPROVE, "comment", 1000, created_by='i.mem.111')
    assert bool(response) is True
    repo.upsert_case_vote.assert_called_with(case_id, VoteType.APPROVE, "comment", 1000, 'i.mem.111')
    repo.update_case_state.assert_called_with(case_id, CaseState.APPROVED, 'i.mem.111')


def test_case_approved_with_two_vote_rejected_one_approved():
    repo = mock.Mock()
    case_id="i.case.xxxx"
    repo.find_case.return_value = Case(
        case_id=case_id,
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.VOTING
    )
    repo.upsert_case_vote.return_value = "i.vote.123"
    repo.case_vote_list.return_value = [
        CaseVote(is_core=True, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.REJECT, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.REJECT, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.REJECT, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment='')
    ]

    response = add_vote(repo, case_id, VoteType.APPROVE, "comment", 1000, created_by='i.mem.111')
    assert bool(response) is True
    repo.upsert_case_vote.assert_called_with(case_id, VoteType.APPROVE, "comment", 1000, 'i.mem.111')
    repo.update_case_state.assert_called_with(case_id, CaseState.REJECTED, 'i.mem.111')


def test_case_approved_with_two_vote_rejected_two_approved():
    repo = mock.Mock()
    case_id="i.case.xxxx"
    repo.find_case.return_value = Case(
        case_id=case_id,
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.VOTING
    )
    repo.upsert_case_vote.return_value = "i.vote.123"
    repo.case_vote_list.return_value = [
        CaseVote(is_core=True, vote=VoteType.APPROVE, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.REJECT, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment=''),
        CaseVote(is_core=True, vote=VoteType.REJECT, vote_id='123', case_id='123', voted__by='i.mem.111', amount_suggested=1000, comment='')
    ]

    response = add_vote(repo, case_id, VoteType.APPROVE, "comment", 1000, created_by='i.mem.111')
    assert bool(response) is True
    repo.upsert_case_vote.assert_called_with(case_id, VoteType.APPROVE, "comment", 1000, 'i.mem.111')
    repo.update_case_state.assert_called_with(case_id, CaseState.REJECTED, 'i.mem.111')


def test_add_payment_details_use_case_reject(core_member):
    repo = mock.Mock()
    repo.find_case.return_value = Case(
        case_id=generate(size=10),
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.REJECTED
    )
    repo.add_case_docs.return_value = None
    repo.find_member.return_value = core_member
    response = add_payment_details_use_case(repo, case_id='case_id', comment="comment", amount_paid=10000, created_by='i.mem.1111' ,doc_list=[
        {"doc_url":"url1", "doc_name": "doc_name1"},
        {"doc_url":"url2", "doc_name": "doc_name2"}
    ])
    assert bool(response) is False
    repo.update_case_state.assert_not_called()

def test_add_payment_details_use_case_approved(core_member):
    repo = mock.Mock()
    case_id='case_id'
    repo.find_case.return_value = Case(
        case_id=generate(size=10),
        title="title",
        purpose=CaseType.EDUCATION,
        beneficiary__id='i.ben.1234',
        case_state=CaseState.APPROVED
    )
    repo.find_member.return_value = core_member
    response = add_payment_details_use_case(repo, case_id='case_id', comment="comment", amount_paid=10000, created_by='i.mem.1111' ,doc_list=[
        {"doc_url":"url1", "doc_name": "doc_name1"},
        {"doc_url":"url2", "doc_name": "doc_name2"}
    ])
    assert bool(response) is True
    repo.update_approved_amount.assert_called_with(case_id, 10000, 'i.mem.1111')
    repo.update_case_state.assert_called_with(case_id, CaseState.PAYMENT_DONE, 'i.mem.1111')

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