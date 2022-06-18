from sqlalchemy import Column, Integer, String, Float, Enum, TIMESTAMP, BOOLEAN
from sqlalchemy.sql import func
from cms.domain.id_type import IDType
from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    def __tablename__(self):
        return self.__name__.lower()
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())


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

class Beneficiary(Base):
    __tablename__ = "beneficiary"

    beneficiary_id = Column(String(40), primary_key=True)
    fname = Column(String, nullable=False)
    lname = Column(String)
    mname = Column(String)
    phone = Column(String(20))
    email = Column(String)


class Case(Base):
    __tablename__ = "case"

    case_id = Column(String(40), primary_key=True)
    case_state = Column(String)
    is_flagged = Column(BOOLEAN)
    is_urgent = Column(BOOLEAN)
    beneficiary__id = Column(String(40))
    purpose = Column(String)
    title = Column(String)
    description = Column(String)
    family_details = Column(String)
    avg_monthly_income: Column(Integer)
    contact_details = Column(String)
    contact_address = Column(String)
    referred__by = Column(String(40))
    assigned__for_verification = Column(String(40))
    assigned__for_accounting = Column(String(40))
    closed__by = Column(String(40))
    updated_by = Column(String(40))
