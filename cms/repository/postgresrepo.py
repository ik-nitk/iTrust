from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from nanoid import generate

from cms.domain import beneficiary
from cms.domain import member
from cms.domain import case
from cms.domain import case_docs
from cms.domain.case_state import CaseState
from cms.repository.postgres_objects import Base, Beneficiary, Member, Case, CaseDocs


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

    def _create_case_docs_objects(self, results):
        return [
            case_docs.CaseDocs(
                case_id=q.case_id,
                doc_type=q.doc_type,
                doc_id=q.doc_id,
                doc_name=q.doc_name,
                doc_url=q.doc_url
            )
            for q in results
        ]

    def case_doc_list(self, case_id, doc_type):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(CaseDocs)
        return self._create_case_docs_objects(query.filter(
            and_(
                CaseDocs.case_id == case_id,
                CaseDocs.doc_type == doc_type
        )))

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

    def _create_case_object(self, q):
        if q is None:
            return None
        return case.Case(
                case_id=q.case_id,
                case_state= q.case_state,
                is_flagged= q.is_flagged,
                is_urgent= q.is_urgent,
                beneficiary__id= q.beneficiary__id,
                purpose= q.purpose,
                title= q.title,
                description= q.description,
                family_details= q.family_details,
                avg_monthly_income= q.avg_monthly_income,
                contact_details= q.contact_details,
                contact_address= q.contact_address,
                referred__by= q.referred__by,
                closed__by= q.closed__by,
                updated_by= q.updated_by
            )

    def _create_case_objects(self, results):
        return [
            self._create_case_object(q) for q in results
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

    def create_case_doc(self, case_id, doc_type, doc_name, doc_url):
        doc_id = f"i.doc.{generate()}"
        new_doc = CaseDocs(doc_id=doc_id, doc_type=doc_type, case_id=case_id, doc_url=doc_url, doc_name=doc_name)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_doc)
        session.commit()
        return new_doc.doc_id

    def add_case_docs(self, doc_list: list[case_docs.CaseDocs]):
        db_doc_objs = [
            CaseDocs(
                case_id=q.case_id,
                doc_type=q.doc_type,
                doc_id=q.doc_id if q.doc_id else f"i.doc.{generate()}",
                doc_name=q.doc_name,
                doc_url=q.doc_url
            )
            for q in doc_list
        ]
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add_all(db_doc_objs)
        session.commit()
        return

    def delete_case_doc(self, doc_id):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        doc = session.query(CaseDocs).get(doc_id)
        session.delete(doc)
        session.commit()

    def create_beneficiary(self, fname,lname, mname, phone, email):
        beneficiary_id = f"i.ben.{generate()}"
        new_beneficiary = Beneficiary(beneficiary_id = beneficiary_id,fname = fname,lname=lname,mname = mname,phone = phone,email=email)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_beneficiary)
        session.commit()
        return new_beneficiary.beneficiary_id

    def create_case(self, beneficiary_id, purpose, title, description='', contact_details='', contact_address=''):
        case_id = f"i.case.{generate()}"
        new_case = Case(case_id = case_id, beneficiary__id=beneficiary_id, case_state=CaseState.DRAFT, title=title, purpose=purpose, description=description, contact_details=contact_details,contact_address=contact_address)
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
                .filter(Member.fname.ilike("%"+search_input+"%") | Member.mname.ilike("%"+search_input+"%") | Member.lname.ilike("%"+search_input+"%") | Member.govt_id.ilike("%"+search_input+"%")).all()
        return query

    def search_beneficiary(self, search_input):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(Beneficiary)\
            .with_entities(Beneficiary)\
                .filter(Beneficiary.fname.ilike("%"+search_input+"%") | Beneficiary.mname.ilike("%"+search_input+"%") | Beneficiary.lname.ilike("%"+search_input+"%") ).all()
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

    def find_case(self, case_id):
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            return self._create_case_object(session.query(Case).get(case_id))
