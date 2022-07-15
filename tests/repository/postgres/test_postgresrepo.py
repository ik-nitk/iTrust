from cms.domain.case_type import CaseType
import pytest
from cms.repository import postgresrepo

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
    case_id = repo.create_case(beneficiary_id='i.ben.1111', title='t.121', purpose=CaseType.EDUCATION, description='')
    repo_case = repo.find_case(case_id)

    assert repo_case.title == 't.121'

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


