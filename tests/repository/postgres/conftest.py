import sqlalchemy
import pytest

from cms.repository.postgres_objects import Base, Member, Beneficiary, Case, CaseVotes, CaseDocs, CaseComments
from cms.domain.id_type import IDType


@pytest.fixture(scope="session")
def pg_session_empty(app_configuration):
    conn_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        app_configuration["POSTGRES_USER"],
        app_configuration["POSTGRES_PASSWORD"],
        app_configuration["POSTGRES_HOSTNAME"],
        app_configuration["POSTGRES_PORT"],
        app_configuration["APPLICATION_DB"],
    )
    engine = sqlalchemy.create_engine(conn_str)
    connection = engine.connect()

    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBSession()

    yield session

    session.close()
    connection.close


@pytest.fixture(scope="session")
def pg_test_data():
    return [
        {
            "member_id": "i.mem.1111",
            "fname": 'fname1',
            "lname": 'lname1',
            "govt_id": 'abcd1111',
            "id_type": IDType.AADHAAR,
            "phone" : "984561111",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.1111@gmail.com',
            "updated__by": "i.mem.1111",
         },
         {
            "member_id": "i.mem.2222",
            "fname": 'fname2',
            "lname": 'lname2',
            "govt_id": 'abcd2222',
            "id_type": IDType.AADHAAR,
            "phone" : "984562222",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.2222@gmail.com',
            "updated__by": "i.mem.1111",
         },
         {
            "member_id": "i.mem.3333",
            "fname": 'fname3',
            "lname": 'lname3',
            "govt_id": 'abcd3333',
            "id_type": IDType.AADHAAR,
            "phone" : "984563333",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.3333@gmail.com',
            "updated__by": "i.mem.1111",
         },
         {
            "member_id": "i.mem.4444",
            "fname": 'fname4',
            "lname": 'lname4',
            "govt_id": 'abcd4444',
            "id_type": IDType.AADHAAR,
            "phone" : "984564444",
            "mname" : None,
            "is_core": False,
            "email" : 'sample.4444@gmail.com',
            "updated__by": "i.mem.1111",
         },
    ]

@pytest.fixture(scope="session")
def pg_test_data_case():
    return [
        {
            "case_id": "i.case.1111",
            "beneficiary__id": "i.ben.1111",
            "updated__by": "i.mem.1111"
        },
        {
            "case_id": "i.case.2222",
            "beneficiary__id": "i.ben.2222",
            "updated__by": "i.mem.1111"
        }
    ]

@pytest.fixture(scope="session")
def pg_test_data_beneficiary():
    return [
        {
            "beneficiary_id": "i.ben.1111",
            "fname": 'fname1',
            "lname": 'lname1',
            "phone" : "984561111",
            "mname" : None,
            "email" : 'sample.1111@gmail.com',
            "updated__by": "i.mem.1111",
         },
         {
            "beneficiary_id": "i.ben.2222",
            "fname": 'fname2',
            "lname": 'lname2',
            "phone" : "984562222",
            "mname" : None,
            "email" : 'sample.2222@gmail.com',
            "updated__by": "i.mem.1111",
         },
         {
            "beneficiary_id": "i.ben.3333",
            "fname": 'fname3',
            "lname": 'lname3',
            "phone" : "984563333",
            "mname" : None,
            "email" : 'sample.3333@gmail.com',
            "updated__by": "i.mem.1111",
         },
         {
            "beneficiary_id": "i.ben.4444",
            "fname": 'fname4',
            "lname": 'lname4',
            "phone" : "984564444",
            "mname" : None,
            "email" : 'sample.4444@gmail.com',
            "updated__by": "i.mem.1111",
         },
    ]


@pytest.fixture(scope="function")
def pg_session(pg_session_empty,
    pg_test_data,
    pg_test_data_beneficiary,
    pg_test_data_case):

    for r in pg_test_data:
        new_member = Member(
            member_id=r["member_id"],
            is_core=r["is_core"],
            phone=r["phone"],
            email=r["email"],
            govt_id=r["govt_id"],
            id_type=r["id_type"],
            fname=r["fname"],
            lname=r["lname"],
            updated__by=r["updated__by"]
        )
        pg_session_empty.add(new_member)
        pg_session_empty.commit()

    for r in pg_test_data_beneficiary:
        new_beneficiary = Beneficiary(
            beneficiary_id=r["beneficiary_id"],
            phone=r["phone"],
            email=r["email"],
            fname=r["fname"],
            lname=r["lname"],
            updated__by=r["updated__by"]
        )
        pg_session_empty.add(new_beneficiary)
        pg_session_empty.commit()

    for r in pg_test_data_case:
        new_case = Case(
            case_id=r["case_id"],
            beneficiary__id=r["beneficiary__id"],
            updated__by=r["updated__by"]
        )
        pg_session_empty.add(new_case)
        pg_session_empty.commit()

    yield pg_session_empty

    pg_session_empty.query(CaseComments).delete()
    pg_session_empty.query(CaseVotes).delete()
    pg_session_empty.query(CaseDocs).delete()
    pg_session_empty.query(Case).delete()
    pg_session_empty.query(Beneficiary).delete()
    pg_session_empty.query(Member).delete()

