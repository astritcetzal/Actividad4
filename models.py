from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    legalName = Column(String(255), nullable=True)
    taxId = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    isActive = Column(Boolean, default=True, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    passwordHash = Column(String(255), nullable=False)

    emailVerified = Column(
        Boolean,
        default=False,
        nullable=False
    )

    isActive = Column(
        Boolean,
        default=True,
        nullable=False
    )

    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)


class CompanyUser(Base):
    __tablename__ = "company_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    companyId = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    userId = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    isAdmin = Column(
        Boolean,
        default=False,
        nullable=False
    )

    isActive = Column(
        Boolean,
        default=True,
        nullable=False
    )

    joinedAt = Column(DateTime, nullable=False)

    company = relationship("Company")
    user = relationship("User")