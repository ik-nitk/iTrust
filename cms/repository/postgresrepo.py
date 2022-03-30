from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cms.domain import beneficiary
from cms.domain import member
from cms.repository.postgres_objects import Base, Beneficiary, Member


class PostgresRepo:
    def __init__(self, configuration):
        connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            configuration["POSTGRES_USER"],
            configuration["POSTGRES_PASSWORD"],
            configuration["POSTGRES_HOSTNAME"],
            configuration["POSTGRES_PORT"],
            configuration["APPLICATION_DB"],
        )

        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

    def _create_member_objects(self, results):
        return [
            member.Member(
                member_id=q.member_id,
                is_core=q.is_core,
                fname=q.fname,
                lname=q.lname,
                mname=q.mname,
                govt_id=q.govt_id,
                id_type=q.id_type,
                phone=q.phone,
                email=q.email
            )
            for q in results
        ]


    def _create_beneficiary_objects(self, results):
        return [
            beneficiary.Beneficiary(
                beneficiary_id=q.beneficiary_id,
                fname=q.fname,
                lname=q.lname,
                mname=q.mname,
                phone=q.phone,
                email=q.email
            )
            for q in results
        ]

    def member_list(self, filters=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(Member)

        if filters is None:
            return self._create_member_objects(query.all())

        if "member_id__eq" in filters:
            query = query.filter(Member.member_id == filters["member_id__eq"])

        if "phone__eq" in filters:
            query = query.filter(Member.phone == filters["phone__eq"])

        if "email__eq" in filters:
            query = query.filter(Member.email == filters["email__eq"])

        if "govt_id__eq" in filters:
            query = query.filter(Member.govt_id == filters["govt_id__eq"])

        return self._create_member_objects(query.all())

    
    def beneficiary_list(self, filters=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(Beneficiary)

        if filters is None:
            return self._create_beneficiary_objects(query.all())

        if "beneficiary_id__eq" in filters:
            query = query.filter(Beneficiary.beneficiary_id == filters["beneficiary_id__eq"])

        if "phone__eq" in filters:
            query = query.filter(Beneficiary.phone == filters["phone__eq"])

        if "email__eq" in filters:
            query = query.filter(Beneficiary.email == filters["email__eq"])


        return self._create_beneficiary_objects(query.all())
