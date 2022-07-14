from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nanoid import generate

from cms.domain import beneficiary
from cms.domain import member
from cms.domain import case
from cms.repository.postgres_objects import Base, Beneficiary, Member, Case


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

    def case_list(self, filters=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(Case)
        return self._create_case_objects(query.all())

    def _create_case_objects(self, results):
        return [
            case.Case(
                case_id=q.case_id,
                case_state= q.fname,
                is_flagged= q.lname,
                is_urgent= q.mname,
                beneficiary__id= q.phone,
                purpose= q.email,
                title= q.title,
                description= q.description,
                family_details= q.family_details,
                avg_monthly_income= q.avg_monthly_income,
                contact_details= q.contact_details,
                contact_address= q.contact_address,
                referred__by= q.referred__by,
                assigned__for_verification= q.assigned__for_verification,
                assigned__for_accounting= q.assigned__for_accounting,
                closed__by= q.closed__by,
                updated_by= q.updated_by
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

    def case_list(self, filters=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(Case)

        if filters is None:
            return self._create_case_objects(query.all())

        if "beneficiary__id__eq" in filters:
            query = query.filter(Beneficiary.beneficiary_id == filters["beneficiary__id__eq"])

        if "title__eq" in filters:
            query = query.filter(Beneficiary.phone == filters["title__eq"])

        if "purpose__eq" in filters:
            query = query.filter(Beneficiary.email == filters["purpose__eq"])


        return self._create_case_objects(query.all())

    def create_member(self, govt_id, id_type, fname,lname,mname, is_core, phone, email):
        member_id = f"i.mem.{generate()}"
        new_member = Member(member_id = member_id,govt_id = govt_id,id_type = id_type,fname = fname,lname=lname,mname = mname,is_core = is_core,phone = phone,email=email)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_member)
        session.commit()
        return new_member.member_id

    def create_beneficiary(self, fname,lname,mname, phone, email):
        beneficiary_id = f"i.ben.{generate()}"
        new_beneficiary = Beneficiary(beneficiary_id = beneficiary_id,fname = fname,lname=lname,mname = mname,phone = phone,email=email)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_beneficiary)
        session.commit()
        return new_beneficiary.beneficiary_id

    def create_case(self, title,purpose,description, contact_details, contact_address):
        case_id = f"i.case.{generate()}"
        new_case = Case(case_id = case_id,title = title,purpose=purpose,description = description,contact_details = contact_details,contact_address=contact_address)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_case)
        session.commit()
        return new_case.case_id

    def search_member(self, search_input):

        DBSession = sessionmaker(bind=self.engine)

        session = DBSession()

        query = session.query(Member)\
            .with_entities(Member)\
                .filter(Member.fname.like("%"+search_input+"%") | Member.mname.like("%"+search_input+"%") | Member.lname.like("%"+search_input+"%") | Member.govt_id.like("%"+search_input+"%")).all()
        
        return query
        
    def search_beneficiary(self, search_input):

        DBSession = sessionmaker(bind=self.engine)
        
        session = DBSession()

        query = session.query(Beneficiary)\
            .with_entities(Beneficiary)\
                .filter(Beneficiary.fname.like("%"+search_input+"%") | Beneficiary.mname.like("%"+search_input+"%") | Beneficiary.lname.like("%"+search_input+"%") ).all()
        
        return query

    def view_member(self, member_id):

        DBSession = sessionmaker(bind=self.engine)
        
        session = DBSession()

        query = session.query(Member)\
            .with_entities(Member)\
                .filter_by(member_id = member_id ).all()
        
        return query

    def update_member(self, member_id,govt_id,id_type,fname,mname,lname,is_core,phone,email):
        DBSession = sessionmaker(bind=self.engine)
        
        session = DBSession()

        member = session.query(Member)\
            .with_entities(Member)\
                .filter_by(member_id = member_id ).first()
        
        
        member.govt_id = govt_id
        member.id_type = id_type
        member.fname = fname
        member.mname = mname
        member.lname = lname
        member.is_core = is_core
        member.phone = phone
        member.email = email

        session.commit()

        return member

def view_beneficiary(self, beneficiary_id):

        DBSession = sessionmaker(bind=self.engine)
        
        session = DBSession()

        query = session.query(Beneficiary)\
            .with_entities(Beneficiary)\
                .filter_by(beneficiary_id = beneficiary_id ).all()
        
        return query

def update_beneficiary(self, beneficiary_id,fname,lname,mname, phone, email):
        DBSession = sessionmaker(bind=self.engine)
        
        session = DBSession()

        beneficiary = session.query(Beneficiary)\
            .with_entities(Beneficiary)\
                .filter_by(beneficiary_id = beneficiary_id ).first()
        
        
        beneficiary.fname = fname
        beneficiary.mname = mname
        beneficiary.lname = lname
        beneficiary.phone = phone
        beneficiary.email = email

        session.commit()

        return beneficiary






        
        
        
