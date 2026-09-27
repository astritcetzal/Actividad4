# Sistema General de Ingresos

Actividad 3 de desarrollo backend. API GraphQL para registrar empresas y los usuarios que pertenecen a cada una.

La empresa es la raíz del dominio. Un usuario no guarda la empresa dentro de su propio registro: la relación vive en `CompanyUser`, para que más adelante una persona pueda pertenecer a varias empresas.

## Equipo

| Persona | Responsable | Alcance |
|---|---|---|
| 1 | Astrit Cetzal | Empresas: modelo, esquema GraphQL y operaciones de alta, consulta, actualización y desactivación |
| 2 | Venus Semino | Identidad: `User`, `CompanyUser`, hash de contraseña, validación de correo, `createCompanyAdmin` y `login` |
| 3 | Reglas de negocio y control de calidad | `createCompanyUser`, `deactivateCompanyUser`, `companyUsers`, un solo administrador principal por empresa y pruebas de los casos de error |

## Tecnologías

- FastAPI y Strawberry GraphQL
- SQLAlchemy y Alembic
- MySQL 8
- Docker Compose
- Contraseñas con bcrypt y sesión con JWT

## Cómo ejecutarlo

Desde la carpeta del proyecto:

```powershell
docker compose up -d --build
docker compose exec api alembic upgrade head
```

El primer comando levanta el API y la base. El segundo crea las tablas.

GraphQL queda en [http://localhost:8000/graphql](http://localhost:8000/graphql).

Si el puerto 8000 ya está ocupado por otro programa, cambia el puerto publicado en `compose.yaml` (`"8001:8000"`) y abre `http://localhost:8001/graphql`.

Para detener los contenedores:

```powershell
docker compose down
```

## Operaciones

Consultas:

- `companies(activeOnly)`: lista las empresas. Con `activeOnly: true` devuelve solo las activas.
- `company(id)`: devuelve una empresa.
- `companyUsers(companyId)`: devuelve los usuarios ligados a esa empresa.

Mutaciones:

- `createCompany`: crea una empresa activa.
- `updateCompany`: actualiza los datos enviados.
- `deactivateCompany`: marca la empresa como inactiva. No la borra.
- `createCompanyAdmin`: crea el administrador principal de una empresa.
- `createCompanyUser`: crea un usuario normal de una empresa (`isAdmin: false`).
- `deactivateCompanyUser`: desactiva el vínculo de un usuario con la empresa. No borra al usuario.
- `login`: valida correo y contraseña, y devuelve un token JWT.

## Reglas de negocio

1. Cada empresa conserva sus propios datos: nombre, razón social, identificador fiscal, correo y teléfono.
2. El nombre de la empresa es obligatorio y no puede ir vacío.
3. Una empresa solo puede tener un administrador principal activo. Un segundo `createCompanyAdmin` se rechaza.
4. El correo debe tener un formato válido y no puede repetirse.
5. La contraseña se guarda con hash. El login no revela si falló el correo o la contraseña.
6. No se puede registrar un administrador ni un usuario en una empresa que no existe.
7. Un usuario inactivo no puede iniciar sesión.
8. Desactivar una empresa o un usuario cambia `isActive` a `false`. El registro se conserva.

## Casos de prueba

Estas son las pruebas de la persona 3. Las capturas de GraphQL sirven como evidencia.

| Caso | Operación | Resultado esperado |
|---|---|---|
| Administrador correcto | `createCompanyAdmin` | Crea el usuario con `isAdmin: true` |
| Usuario correcto | `createCompanyUser` | Crea el usuario con `isAdmin: false` |
| Correo duplicado | `createCompanyAdmin` o `createCompanyUser` | Error: el correo ya está registrado |
| Segundo administrador | `createCompanyAdmin` sobre la misma empresa | Error: la empresa ya tiene un administrador principal |
| Empresa inexistente | Alta con un `companyId` que no existe | Error: la empresa especificada no existe |
| Login correcto | `login` con la contraseña real | Devuelve `token` y `tokenType: Bearer` |
| Login incorrecto | `login` con la contraseña equivocada | Error: correo o contraseña incorrectos |
