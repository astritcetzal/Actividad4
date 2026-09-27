import strawberry
from typing import Optional, List
from datetime import datetime, timezone
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from database import get_db
from models import Company as CompanyModel

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

#Lectura
@strawberry.type
class Query:
    @strawberry.field
    def companies(self, info: Info, activeOnly: Optional[bool] = None) -> List[Company]:
        db = info.context["db"]
        query = db.query(CompanyModel)
        
        # Filtro dinámico según el parámetro opcional
        if activeOnly:
            query = query.filter(CompanyModel.isActive == True)
            
        empresas_db = query.all()
        
        # Mapeo manual para proteger el estado interno del ORM
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
            ) for emp in empresas_db
        ]

    @strawberry.field
    def company(self, info: Info, id: strawberry.ID) -> Optional[Company]:
        db = info.context["db"]
        empresa_db = db.query(CompanyModel).filter(CompanyModel.id == id).first()
        
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

#Escritura
@strawberry.type
class Mutation:
    @strawberry.field
    def createCompany(self, info: Info, input: CreateCompanyInput) -> Company:
        db = info.context["db"]
        
        # Regla de negocio: El nombre es obligatorio
        if not input.name.strip():
            raise Exception("El nombre de la empresa es obligatorio.")
            
        nueva_empresa = CompanyModel(
            name=input.name,
            legalName=input.legalName,
            taxId=input.taxId,
            email=input.email,
            phone=input.phone,
            isActive=True, # Regla de negocio: Alta lógica por defecto
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
    def updateCompany(self, info: Info, input: UpdateCompanyInput) -> Company:
        db = info.context["db"]
        empresa_db = db.query(CompanyModel).filter(CompanyModel.id == input.id).first()
        
        # Regla de negocio: Validar existencia
        if not empresa_db:
            raise Exception("La empresa solicitada no existe.")
            
        # Asignación condicionada para actualizar solo lo que se envía
        if input.name is not None:
            if not input.name.strip():
                raise Exception("El nombre de la empresa no puede estar vacío.")
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

        empresa_db.updatedAt = datetime.now(timezone.utc)
        
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
    def deactivateCompany(self, info: Info, id: strawberry.ID) -> Company:
        db = info.context["db"]
        empresa_db = db.query(CompanyModel).filter(CompanyModel.id == id).first()
        
        if not empresa_db:
            raise Exception("La empresa no existe.")
            
        # Regla de negocio: Baja lógica en lugar de borrado físico
        empresa_db.isActive = False
        empresa_db.updatedAt = datetime.now(timezone.utc)
        
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


schema = strawberry.Schema(query=Query, mutation=Mutation)

async def get_context(db=Depends(get_db)):
    return {"db": db}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="Sistema General de Ingresos")
app.include_router(graphql_app, prefix="/graphql")