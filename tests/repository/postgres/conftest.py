import sqlalchemy
import pytest

from cms.repository.postgres_objects import Base, Member
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
            "email" : 'sample.1111@gmail.com'
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
            "email" : 'sample.2222@gmail.com'
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
            "email" : 'sample.3333@gmail.com'
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
            "email" : 'sample.4444@gmail.com'
         },
    ]


@pytest.fixture(scope="function")
def pg_session(pg_session_empty, pg_test_data):
    for r in pg_test_data:
        new_member = Member(
            member_id=r["member_id"],
            is_core=r["is_core"],
            phone=r["phone"],
            email=r["email"],
            govt_id=r["govt_id"],
            id_type=r["id_type"],
            fname=r["fname"],
            lname=r["lname"]
        )
        pg_session_empty.add(new_member)
        pg_session_empty.commit()

    yield pg_session_empty

    pg_session_empty.query(Member).delete()
