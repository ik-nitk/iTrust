from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP, BOOLEAN, JSON
from sqlalchemy.sql import func, expression
from cms.domain.id_type import IDType
from cms.domain.case_type import CaseType
from cms.domain.doc_type import DocType
from cms.domain.comment_type import CommentType
from cms.domain.case_state import CaseState
from cms.domain.vote_type import VoteType
from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    def __tablename__(self):
        return self.__name__.lower()
    created = Column(TIMESTAMP, name='created', nullable=False, server_default=func.now())
    modified = Column(TIMESTAMP, name='modified', nullable=False, server_default=func.now(), onupdate=func.current_timestamp())


Base = declarative_base(cls=Base)


class Member(Base):
    __tablename__ = "member"

    member_id = Column(String(40), primary_key=True)
    govt_id = Column(String, nullable=False)
    id_type = Column(Enum(IDType))
    fname = Column(String, nullable=False)
    lname = Column(String)
    mname = Column(String)
    is_core = Column(BOOLEAN)
    phone = Column(String(20))
    email = Column(String)
    updated__by = Column(String(40), ForeignKey("member.member_id"), nullable=False)

class Beneficiary(Base):
    __tablename__ = "beneficiary"

    beneficiary_id = Column(String(40), primary_key=True)
    govt_id = Column(String, nullable=False)
    id_type = Column(Enum(IDType))
    fname = Column(String, nullable=False)
    lname = Column(String)
    mname = Column(String)
    phone = Column(String(20))
    email = Column(String)
    updated__by = Column(String(40), ForeignKey("member.member_id"), nullable=False)

class CaseDocs(Base):
    __tablename__ = "t_case_docs"
    doc_id = Column(String(40), primary_key=True)
    doc_type = Column(Enum(DocType))
    doc_url = Column(String)
    case_id = Column(String(40), ForeignKey("t_case.case_id"))
    doc_name = Column(String)
    updated__by = Column(String(40), ForeignKey("member.member_id"), nullable=False)


class CaseComments(Base):
    __tablename__ = "t_case_comments"
    comment_id = Column(String(40), primary_key=True)
    comment_type = Column(Enum(CommentType))
    case_id = Column(String(40), ForeignKey("t_case.case_id"), nullable=False)
    comment = Column(String)
    commented__by = Column(String(40), ForeignKey("member.member_id"), nullable=False)
    comment_data = Column(JSON)

class CaseVotes(Base):
    __tablename__ = "t_case_votes"
    vote_id = Column(String(40), primary_key=True)
    case_id = Column(String(40), ForeignKey("t_case.case_id"), nullable=False)
    voted__by = Column(String(40), ForeignKey("member.member_id"), nullable=False)
    is_core = Column(BOOLEAN)
    amount_suggested = Column(Integer)
    vote = Column(Enum(VoteType))
    comment = Column(String)


class Case(Base):
    __tablename__ = "t_case"

    case_id = Column(String(40), primary_key=True)
    case_state = Column(Enum(CaseState))
    is_flagged = Column(BOOLEAN, server_default=expression.false())
    is_urgent = Column(BOOLEAN, server_default=expression.false())
    beneficiary__id = Column(String(40), ForeignKey("beneficiary.beneficiary_id"), nullable=False)
    purpose = Column(Enum(CaseType))
    title = Column(String)
    description = Column(String)
    amount_needed = Column(Integer)
    amount_approved = Column(Integer)
    family_details = Column(String)
    avg_monthly_income= Column(Integer)
    contact_details = Column(String)
    contact_address = Column(String)
    referred__by = Column(String(40), ForeignKey("member.member_id"))
    closed__by = Column(String(40), ForeignKey("member.member_id"))
    updated__by = Column(String(40), ForeignKey("member.member_id"), nullable=False)
