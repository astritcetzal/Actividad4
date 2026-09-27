import strawberry

@strawberry.type
class Company :
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
        legalName: Optional[str]
        taxId: Optional[str]
        email: Optional[str]
        phone: Optional[str]

@strawberry.input
class UpdateCompanyInput:
    id: strawberry.ID
    name: Optional[str]
    legalName: Optional[str]
    taxId: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    isActive: Optional[bool]
    
@strawberry.type
class Query:
    @strawberry.field
    def companies(self, activeOnly: Optional[bool] = None) -> List[Company]:
        # Aquí irá la lógica para consultar SQLAlchemy
        return []

    @strawberry.field
    def company(self, id: strawberry.ID) -> Optional[Company]:
        # Aquí irá la lógica de consulta por ID
        return None

@strawberry.type
class Mutation:
    @strawberry.field
    def createCompany(self, input: CreateCompanyInput) -> Company:
        # Aquí irá la lógica de inserción
        pass

    @strawberry.field
    def updateCompany(self, input: UpdateCompanyInput) -> Company:
        # Aquí irá la lógica de actualización
        pass

    @strawberry.field
    def deactivateCompany(self, id: strawberry.ID) -> Company:
        # Aquí irá la baja lógica (isActive = False)
        pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="Sistema General de Ingresos")
app.include_router(graphql_app, prefix="/graphql")