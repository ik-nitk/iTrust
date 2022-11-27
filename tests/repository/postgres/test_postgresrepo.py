from cms.domain import case_docs
from cms.domain import doc_type
from cms.domain.case_type import CaseType
from cms.domain.comment_type import CommentType
from cms.domain.case_state import CaseState
from cms.domain.vote_type import VoteType
import pytest
from cms.repository import postgresrepo
from cms.domain.doc_type import DocType

pytestmark = pytest.mark.integration


## CASE TESTING -------------------------------
def test_case_list_without_parameters(
    app_configuration, pg_session, pg_test_data_case
):
    repo = postgresrepo.PostgresRepo(app_configuration)
    repo_case = repo.case_list()

    assert set([r.case_id for r in repo_case]) == set(
        [r["case_id"] for r in pg_test_data_case]
    )

## CREATE CASE TESTING -------------------------------
def test_create_case(
    app_configuration, pg_session, pg_test_data_case
):
    repo = postgresrepo.PostgresRepo(app_configuration)
    case_id = repo.create_case(beneficiary_id='i.ben.1111', title='t.121', purpose=CaseType.EDUCATION, description='',amount_needed= 0)
    repo_case = repo.find_case(case_id)

    assert repo_case.title == 't.121'

## CREATE CASE TESTING NOT FOUND-------------------------------
def test_create_case_not_found(
    app_configuration, pg_session, pg_test_data_case
):
    repo = postgresrepo.PostgresRepo(app_configuration)
    repo_case = repo.find_case('i.ben.not_found')
    assert repo_case == None

## CREATE CASE WITH CHANGE STATE
def test_create_case_change_state(
    app_configuration, pg_session, pg_test_data_case
):
    repo = postgresrepo.PostgresRepo(app_configuration)
    case_id = repo.create_case(beneficiary_id='i.ben.1111', title='t.121', purpose=CaseType.EDUCATION, description='',amount_needed= 0)
    repo.update_case_state(case_id, CaseState.PUBLISHED)
    repo_case = repo.find_case(case_id)
    assert repo_case.case_state == CaseState.PUBLISHED

## CREATE CASE AND ADD DOCUMENT TEST-------------------------------
def test_create_case_add_doc(
    app_configuration, pg_session, pg_test_data_case
):
    repo = postgresrepo.PostgresRepo(app_configuration)
    case_id = repo.create_case(beneficiary_id='i.ben.1111', title='t.555', purpose=CaseType.EDUCATION, description='',amount_needed= 0)
    # Add 2 docuemnts to the case
    doc1 = repo.create_case_doc(case_id, doc_type=DocType.INITIAL_CASE_DOC, doc_name='', doc_url='some_url')
    doc2 = repo.create_case_doc(case_id, doc_type=DocType.INITIAL_CASE_DOC, doc_name='', doc_url='some_url')
    docs = [
        case_docs.CaseDocs(
            case_id=case_id,
            doc_id=str(i),
            doc_name=str(i),
            doc_url=str(i),
            doc_type=DocType.CASE_PAYMENT_RECEIPTS
        )
        for i in range(2)
    ]
    repo.add_case_docs(docs)
    repo_case_docs = repo.case_doc_list(case_id, DocType.INITIAL_CASE_DOC)

    repo.delete_case_doc(doc1)
    repo.delete_case_doc(doc2)
    repo.delete_case_doc('0')
    repo.delete_case_doc('1')

    assert len(repo_case_docs) == 2


## CREATE CASE AND ADD COMMENTS TEST-------------------------------
def test_create_case_add_comments(
    app_configuration, pg_session, pg_test_data_case
):
    repo = postgresrepo.PostgresRepo(app_configuration)
    case_id = repo.create_case(beneficiary_id='i.ben.1111', title='t.555', purpose=CaseType.EDUCATION, description='',amount_needed= 0)
    # Add 2 docuemnts to the case
    comment1 = repo.create_case_comment(case_id, comment_type=CommentType.APPROVAL_COMMENTS, comment='comment', comment_data={}, c_by='i.mem.2222')
    comment2 = repo.create_case_comment(case_id, comment_type=CommentType.VERIFICATION_COMMENTS, comment='comment', comment_data={'data': 'sample'}, c_by='i.mem.2222')

    approved_case_comments = repo.case_comment_list(case_id, CommentType.APPROVAL_COMMENTS)
    all_case_comments = repo.case_comment_list(case_id, None)
    repo.delete_case_comment(comment1)
    repo.delete_case_comment(comment2)

    assert len(approved_case_comments) == 1
    assert len(all_case_comments) == 2

## CREATE CASE AND ADD VOTES TEST-------------------------------
def test_create_case_add_votes(
    app_configuration, pg_session, pg_test_data_case
):
    repo = postgresrepo.PostgresRepo(app_configuration)
    case_id = repo.create_case(beneficiary_id='i.ben.1111', title='t.555', purpose=CaseType.EDUCATION, description='',amount_needed= 1000)
    # Add 2 votes to the case
    vote1 = repo.create_case_vote(case_id, vote=VoteType.APPROVE,comment='comment', amount_suggested=1000)
    vote2 = repo.create_case_vote(case_id, vote=VoteType.APPROVE,comment='comment', amount_suggested=1000)

    case_votes = repo.case_vote_list(case_id)
    repo.delete_case_vote(vote1)
    repo.delete_case_vote(vote2)

    assert len(case_votes) == 2

## MEMBERS TESTING -------------------------------
def test_repository_list_without_parameters(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_members = repo.member_list()

    assert set([r.member_id for r in repo_members]) == set(
        [r["member_id"] for r in pg_test_data]
    )


def test_repository_list_with_phone_equal_filter(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_members = repo.member_list(
        filters={"phone__eq": "984561111"}
    )

    assert len(repo_members) == 1
    assert repo_members[0].member_id == "i.mem.1111"


def test_repository_get_member_by_email(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_members = repo.view_member_by_email(
        email_id='sample.1111@gmail.com'
    )

    assert len(repo_members) == 1
    assert repo_members[0].member_id == "i.mem.1111"

def test_repository_list_with_member_id_equal_filter(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_members = repo.member_list(filters={"member_id__eq": "i.mem.3333"})

    assert len(repo_members) == 1
    assert repo_members[0].member_id == "i.mem.3333"


def test_repository_list_with_govt_id_equal_filter(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_members = repo.member_list(filters={"govt_id__eq": "abcd3333"})

    assert len(repo_members) == 1
    assert repo_members[0].member_id == "i.mem.3333"

def test_repository_list_with_email_equal_filter(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_members = repo.member_list(filters={"email__eq": "sample.2222@gmail.com"})

    assert len(repo_members) == 1
    assert repo_members[0].member_id == "i.mem.2222"

#--------------------------------------------------
#each table seperate test file?
def test_repository_beneficiary_list_without_parameters(
    app_configuration, pg_session, pg_test_data_beneficiary
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_beneficiarys = repo.beneficiary_list()

    assert set([r.beneficiary_id for r in repo_beneficiarys]) == set(
        [r["beneficiary_id"] for r in pg_test_data_beneficiary]
    )


def test_repository_beneficiary_list_with_phone_equal_filter(
    app_configuration, pg_session, pg_test_data_beneficiary
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_beneficiarys = repo.beneficiary_list(
        filters={"phone__eq": "984561111"}
    )

    assert len(repo_beneficiarys) == 1
    assert repo_beneficiarys[0].beneficiary_id == "i.ben.1111"


def test_repository_beneficiary_list_with_beneficiary_id_equal_filter(
    app_configuration, pg_session, pg_test_data_beneficiary
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_beneficiarys = repo.beneficiary_list(filters={"beneficiary_id__eq": "i.ben.3333"})

    assert len(repo_beneficiarys) == 1
    assert repo_beneficiarys[0].beneficiary_id == "i.ben.3333"


def test_repository_beneficiary_list_with_email_equal_filter(
    app_configuration, pg_session, pg_test_data_beneficiary
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_beneficiarys = repo.beneficiary_list(filters={"email__eq": "sample.2222@gmail.com"})

    assert len(repo_beneficiarys) == 1
    assert repo_beneficiarys[0].beneficiary_id == "i.ben.2222"


