from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from nanoid import generate

from cms.domain import beneficiary
from cms.domain import member
from cms.domain import case
from cms.domain import case_docs
from cms.domain import case_comments
from cms.domain import case_votes
from cms.domain.case_state import CaseState
from cms.repository.postgres_objects import Base, Beneficiary, Member, Case, CaseDocs, CaseComments,CaseVotes


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
                email=q.email,
                updated__by=q.updated__by
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
                doc_url=q.doc_url,
                updated__by=q.updated__by
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
                govt_id=q.govt_id,
                id_type=q.id_type,
                mname=q.mname,
                phone=q.phone,
                email=q.email,
                updated__by=q.updated__by
            )
            for q in results
        ]

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
                amount_approved=q.amount_approved,
                amount_needed=q.amount_needed,
                avg_monthly_income= q.avg_monthly_income,
                contact_details= q.contact_details,
                contact_address= q.contact_address,
                referred__by= q.referred__by,
                closed__by= q.closed__by,
                updated__by= q.updated__by
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

    def case_list(self, filters=None, limit=100):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(Case)

        if filters is None:
            return self._create_case_objects(query.order_by(Base.modified.desc()).limit(limit).all())

        if "beneficiary_id__eq" in filters:
            query = query.filter(Case.beneficiary__id == filters["beneficiary_id__eq"])

        if "member_id__eq" in filters:
            query = query.filter(Case.referred__by == filters["member_id__eq"])

        if "case_state__eq" in filters:
            query = query.filter(Case.case_state == filters["case_state__eq"])
        return self._create_case_objects(query.order_by(Base.modified.desc()).limit(limit).all())

    def create_member(self, govt_id, id_type, fname,lname,mname, is_core, phone, email, created_by):
        member_id = f"i.mem.{generate()}"
        new_member = Member(member_id = member_id,govt_id = govt_id,id_type = id_type,fname = fname,lname=lname,mname = mname,is_core = is_core,phone = phone,email=email, updated__by=created_by)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_member)
        session.commit()
        return new_member.member_id

    def _create_case_comment_objects(self, results):
        return [
            case_comments.CaseComment(
                case_id=q.case_id,
                comment_type=q.comment_type,
                comment_id=q.comment_id,
                comment=q.comment,
                commented_by=q.commented__by,
                comment_data=q.comment_data
            )
            for q in results
        ]

    def case_comment_list(self, case_id, comment_type):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(CaseComments)
        if comment_type == None:
            return self._create_case_comment_objects(query.filter(
                CaseComments.case_id == case_id
            ))
        else:
            return self._create_case_comment_objects(query.filter(
                and_(
                    CaseComments.case_id == case_id,
                    CaseComments.comment_type == comment_type
            )))

    def create_case_comment(self, case_id, comment_type, comment, comment_data, c_by):
        comment_id = f"i.comment.{generate()}"
        new_comment = CaseComments(comment_id=comment_id, comment_type=comment_type, case_id=case_id, comment=comment, comment_data=comment_data, commented__by=c_by)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_comment)
        session.commit()
        return new_comment.comment_id

    def delete_case_comment(self, comment_id):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        comment = session.query(CaseComments).get(comment_id)
        session.delete(comment)
        session.commit()

    def _create_case_votes_objects(self, results):
        return [
            case_votes.CaseVote(
                case_id=q.case_id,
                vote_id = q.vote_id,
                voted__by=q.voted__by,
                is_core=q.is_core,
                amount_suggested=q.amount_suggested,
                vote=q.vote,
                comment= q.comment
            )
            for q in results
        ]

    def find_case_vote(self, case_id, voted_by):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(CaseVotes)\
            .with_entities(CaseVotes)\
                .filter_by(case_id = case_id, voted__by = voted_by ).first()
        print(query, type(query))
        return query

    def upsert_case_vote(self, case_id, vote,comment, amount_suggested, created_by):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        member = self.view_member(created_by)[0]
        caseVote = session.query(CaseVotes).filter(CaseVotes.case_id == case_id, CaseVotes.voted__by == created_by).first()
        if caseVote is None:
            vote_id = f"i.vote.{generate()}"
            new_vote = CaseVotes(vote_id = vote_id, case_id=case_id, vote=vote,comment = comment,amount_suggested = amount_suggested, voted__by=created_by, is_core=member.is_core)
            session.add(new_vote)
            session.commit()
            return new_vote.vote_id
        else:
            caseVote.vote = vote
            caseVote.comment = comment
            caseVote.amout_suggested = amount_suggested
            session.commit()
            return caseVote.vote_id

    def case_vote_list(self, case_id):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(CaseVotes)
        return self._create_case_votes_objects(query.filter(
                CaseVotes.case_id == case_id
            ))

    def delete_case_vote(self, vote_id):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        vote = session.query(CaseVotes).get(vote_id)
        session.delete(vote)
        session.commit()

    def create_case_doc(self, case_id, doc_type, doc_name, doc_url, updated_by):
        doc_id = f"i.doc.{generate()}"
        new_doc = CaseDocs(doc_id=doc_id, doc_type=doc_type, case_id=case_id, doc_url=doc_url, doc_name=doc_name, updated__by=updated_by)
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
                doc_url=q.doc_url,
                updated__by=q.updated__by
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

    def create_beneficiary(self, govt_id, id_type, fname,lname, mname, phone, email, created_by):
        beneficiary_id = f"i.ben.{generate()}"
        new_beneficiary = Beneficiary(beneficiary_id = beneficiary_id,govt_id=govt_id, id_type=id_type, fname=fname,lname=lname,mname = mname,phone = phone,email=email, updated__by=created_by)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_beneficiary)
        session.commit()
        return new_beneficiary.beneficiary_id

    def create_case(self, beneficiary_id, purpose, title, created_by, description='',amount_needed = 0, contact_details='', contact_address=''):
        case_id = f"i.case.{generate()}"
        new_case = Case(case_id = case_id, beneficiary__id=beneficiary_id, case_state=CaseState.DRAFT, title=title, purpose=purpose, description=description,amount_needed =  amount_needed,contact_details=contact_details,contact_address=contact_address, updated__by=created_by)
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.add(new_case)
        session.commit()
        return new_case.case_id

    def update_approved_amount(self, case_id, amount_paid, updated_by):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.query(
            Case
        ).filter(
            Case.case_id == case_id
        ).update({
            Case.amount_approved: amount_paid,
            Case.updated__by: updated_by
        })
        session.commit()

    def update_case_state(self, case_id, new_state, updated_by):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        session.query(
            Case
        ).filter(
            Case.case_id == case_id
        ).update({
            Case.case_state: new_state,
            Case.updated__by: updated_by
        })
        session.commit()

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

    def view_member_by_email(self, email_id):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(Member)\
            .with_entities(Member)\
                .filter_by(email = email_id ).all()
        return query

    def find_member(self, member_id):
        return self.view_member(member_id)[0]

    def view_member(self, member_id):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(Member)\
            .with_entities(Member)\
                .filter_by(member_id = member_id ).all()
        return query

    def update_member(self, member_id, govt_id, id_type, fname, mname, lname, is_core, phone, email, updated_by):
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
        member.updated__by = updated_by
        session.commit()
        return member

    def view_beneficiary(self, beneficiary_id):
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            query = session.query(Beneficiary)\
                .with_entities(Beneficiary)\
                    .filter_by(beneficiary_id = beneficiary_id ).all()
            return query

    def update_beneficiary(self, beneficiary_id,govt_id, id_type, fname,lname,mname, phone, email, updated_by):
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            beneficiary = session.query(Beneficiary)\
                .with_entities(Beneficiary)\
                    .filter_by(beneficiary_id = beneficiary_id ).first()
            beneficiary.fname = fname
            beneficiary.govt_id = govt_id
            beneficiary.id_type = id_type
            beneficiary.mname = mname
            beneficiary.lname = lname
            beneficiary.phone = phone
            beneficiary.email = email
            beneficiary.updated__by = updated_by
            session.commit()
            return beneficiary

    def find_case(self, case_id):
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            return self._create_case_object(session.query(Case).get(case_id))
