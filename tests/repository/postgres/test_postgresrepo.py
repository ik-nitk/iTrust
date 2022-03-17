import pytest
from cms.repository import postgresrepo

pytestmark = pytest.mark.integration


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


