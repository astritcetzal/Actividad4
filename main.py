import strawberry
from typing import Optional, List
from datetime import datetime, timezone
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from database import get_db

from models import (
    Company as CompanyModel,
    User as UserModel,
    CompanyUser as CompanyUserModel
)

from security import (
    hash_password,
    verify_password,
    validate_email
)

@strawberry.type
class Company:
    id: strawberry.ID
    name: str
    legalName: Optional[str]
    taxId: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    emailVerified: bool
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

@strawberry.type
class CompanyUser:
    id: strawberry.ID
    companyId: strawberry.ID
    userId: strawberry.ID
    isAdmin: bool
    isActive: bool
    joinedAt: datetime
    company: Company
    user: User

@strawberry.input
class CreateCompanyInput:
    name: str
    legalName: Optional[str] = None
    taxId: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@strawberry.input
class UpdateCompanyInput:
    id: strawberry.ID
    name: Optional[str] = None
    legalName: Optional[str] = None
    taxId: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    isActive: Optional[bool] = None


@strawberry.input
class LoginInput:
    email: str
    password: str

@strawberry.input
class CreateCompanyAdminInput:
    companyId: strawberry.ID
    name: str
    email: str
    password: str

@strawberry.type
class AuthUser:
    id: strawberry.ID
    name: str
    email: str

@strawberry.type
class AuthPayload:
    token: str
    tokenType: str
    user: AuthUser

@strawberry.type
class Query:

    @strawberry.field
    def companies(
        self,
        info: Info,
        activeOnly: Optional[bool] = None
    ) -> List[Company]:

        db = info.context["db"]

        query = db.query(CompanyModel)

        if activeOnly:
            query = query.filter(
                CompanyModel.isActive == True
            )

        empresas_db = query.all()

        return [
            Company(
                id=emp.id,
                name=emp.name,
                legalName=emp.legalName,
                taxId=emp.taxId,
                email=emp.email,
                phone=emp.phone,
                isActive=emp.isActive,
                createdAt=emp.createdAt,
                updatedAt=emp.updatedAt
            )
            for emp in empresas_db
        ]

    @strawberry.field
    def company(
        self,
        info: Info,
        id: strawberry.ID
    ) -> Optional[Company]:

        db = info.context["db"]

        empresa_db = (
            db.query(CompanyModel)
            .filter(CompanyModel.id == id)
            .first()
        )

        if not empresa_db:
            return None

        return Company(
            id=empresa_db.id,
            name=empresa_db.name,
            legalName=empresa_db.legalName,
            taxId=empresa_db.taxId,
            email=empresa_db.email,
            phone=empresa_db.phone,
            isActive=empresa_db.isActive,
            createdAt=empresa_db.createdAt,
            updatedAt=empresa_db.updatedAt
        )

@strawberry.type
class Mutation:

    @strawberry.field
    def createCompany(
        self,
        info: Info,
        input: CreateCompanyInput
    ) -> Company:

        db = info.context["db"]

        if not input.name.strip():
            raise Exception(
                "El nombre de la empresa es obligatorio."
            )

        nueva_empresa = CompanyModel(
            name=input.name,
            legalName=input.legalName,
            taxId=input.taxId,
            email=input.email,
            phone=input.phone,
            isActive=True,
            createdAt=datetime.now(timezone.utc),
            updatedAt=datetime.now(timezone.utc)
        )

        db.add(nueva_empresa)
        db.commit()
        db.refresh(nueva_empresa)

        return Company(
            id=nueva_empresa.id,
            name=nueva_empresa.name,
            legalName=nueva_empresa.legalName,
            taxId=nueva_empresa.taxId,
            email=nueva_empresa.email,
            phone=nueva_empresa.phone,
            isActive=nueva_empresa.isActive,
            createdAt=nueva_empresa.createdAt,
            updatedAt=nueva_empresa.updatedAt
        )

    @strawberry.field
    def updateCompany(
        self,
        info: Info,
        input: UpdateCompanyInput
    ) -> Company:

        db = info.context["db"]

        empresa_db = (
            db.query(CompanyModel)
            .filter(CompanyModel.id == input.id)
            .first()
        )

        if not empresa_db:
            raise Exception(
                "La empresa solicitada no existe."
            )

        if input.name is not None:
            if not input.name.strip():
                raise Exception(
                    "El nombre de la empresa no puede estar vacío."
                )

            empresa_db.name = input.name

        if input.legalName is not None:
            empresa_db.legalName = input.legalName

        if input.taxId is not None:
            empresa_db.taxId = input.taxId

        if input.email is not None:
            empresa_db.email = input.email

        if input.phone is not None:
            empresa_db.phone = input.phone

        if input.isActive is not None:
            empresa_db.isActive = input.isActive

        empresa_db.updatedAt = datetime.now(
            timezone.utc
        )

        db.commit()
        db.refresh(empresa_db)

        return Company(
            id=empresa_db.id,
            name=empresa_db.name,
            legalName=empresa_db.legalName,
            taxId=empresa_db.taxId,
            email=empresa_db.email,
            phone=empresa_db.phone,
            isActive=empresa_db.isActive,
            createdAt=empresa_db.createdAt,
            updatedAt=empresa_db.updatedAt
        )

    @strawberry.field
    def deactivateCompany(
        self,
        info: Info,
        id: strawberry.ID
    ) -> Company:

        db = info.context["db"]
        empresa_db = (
            db.query(CompanyModel)
            .filter(CompanyModel.id == id)
            .first()
        )

        if not empresa_db:
            raise Exception(
                "La empresa no existe."
            )

        empresa_db.isActive = False
        empresa_db.updatedAt = datetime.now(
            timezone.utc
        )

        db.commit()
        db.refresh(empresa_db)

        return Company(
            id=empresa_db.id,
            name=empresa_db.name,
            legalName=empresa_db.legalName,
            taxId=empresa_db.taxId,
            email=empresa_db.email,
            phone=empresa_db.phone,
            isActive=empresa_db.isActive,
            createdAt=empresa_db.createdAt,
            updatedAt=empresa_db.updatedAt
        )

    @strawberry.field
    def createCompanyAdmin(
        self,
        info: Info,
        input: CreateCompanyAdminInput
    ) -> CompanyUser:

        db = info.context["db"]

        name = input.name.strip()
        email = input.email.strip().lower()

        if not name:
            raise Exception(
                "El nombre del usuario es obligatorio."
            )

        if not validate_email(email):
            raise Exception(
                "El correo electrónico no tiene un formato válido."
            )

        if not input.password:
            raise Exception(
                "La contraseña es obligatoria."
            )

        empresa_db = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.id == input.companyId
            )
            .first()
        )

        if not empresa_db:
            raise Exception(
                "La empresa especificada no existe."
            )

        usuario_existente = (
            db.query(UserModel)
            .filter(
                UserModel.email == email
            )
            .first()
        )

        if usuario_existente:
            raise Exception(
                "El correo electrónico ya está registrado."
            )

        password_hash = hash_password(
            input.password
        )

        ahora = datetime.now(timezone.utc)
        nuevo_usuario = UserModel(
            name=name,
            email=email,
            passwordHash=password_hash,
            emailVerified=False,
            isActive=True,
            createdAt=ahora,
            updatedAt=ahora
        )

        db.add(nuevo_usuario)
        db.flush()
        nueva_relacion = CompanyUserModel(
            companyId=empresa_db.id,
            userId=nuevo_usuario.id,
            isAdmin=True,
            isActive=True,
            joinedAt=ahora
        )

        db.add(nueva_relacion)
        db.commit()
        db.refresh(nuevo_usuario)
        db.refresh(nueva_relacion)

        return CompanyUser(
            id=nueva_relacion.id,
            companyId=nueva_relacion.companyId,
            userId=nueva_relacion.userId,
            isAdmin=nueva_relacion.isAdmin,
            isActive=nueva_relacion.isActive,
            joinedAt=nueva_relacion.joinedAt,

            company=Company(
                id=empresa_db.id,
                name=empresa_db.name,
                legalName=empresa_db.legalName,
                taxId=empresa_db.taxId,
                email=empresa_db.email,
                phone=empresa_db.phone,
                isActive=empresa_db.isActive,
                createdAt=empresa_db.createdAt,
                updatedAt=empresa_db.updatedAt
            ),

            user=User(
                id=nuevo_usuario.id,
                name=nuevo_usuario.name,
                email=nuevo_usuario.email,
                emailVerified=nuevo_usuario.emailVerified,
                isActive=nuevo_usuario.isActive,
                createdAt=nuevo_usuario.createdAt,
                updatedAt=nuevo_usuario.updatedAt
            )
        )

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

async def get_context(db=Depends(get_db)):
    return {
        "db": db
    }

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app = FastAPI(
    title="Sistema General de Ingresos"
)

app.include_router(
    graphql_app,
    prefix="/graphql"
)