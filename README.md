<<<<<<< HEAD
# device_systems — v4.0 (Security Branch)

API REST segura para gestión de **usuarios**, **dispositivos** y **préstamos**, construida con FastAPI + SQLAlchemy + SQLite.

Esta versión agrega sobre la v3.0 una capa completa de seguridad: autenticación JWT, hash de contraseñas, protección de rutas por roles, middleware personalizado, CORS, rate limiting y validaciones avanzadas con Pydantic v2.
=======
# device_systems API — v4.0 (Alembic + Relaciones + Joins)

API REST construida con **FastAPI**, **SQLAlchemy** y **Alembic** que gestiona
usuarios, dispositivos tecnológicos y préstamos entre ambos.
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf

---

## Estructura del proyecto

```
device_systems/
│── app/
│   │── main.py
<<<<<<< HEAD
│   │── auth/
│   │   │── auth_routes.py       # POST /auth/register, /login, GET /auth/me
│   │   │── auth_service.py      # Lógica de registro y autenticación
│   │   │── security.py          # Hash bcrypt, creación y validación JWT
│   │── database/
│   │   │── connection.py        # SQLAlchemy engine + SessionLocal + Base
│   │── models/
│   │   │── user_model.py        # Tabla users (incluye hashed_password, role)
│   │   │── device_model.py      # Tabla devices
│   │   │── loan_model.py        # Tabla loans (FK users + devices)
│   │── schemas/
│   │   │── auth_schema.py       # UserRegister, UserLogin, Token, TokenData
│   │   │── user_schema.py       # UserCreate, UserUpdate, UserPatch, UserResponse
│   │   │── device_schema.py     # DeviceCreate/Update/Patch/Response
│   │   │── loan_schema.py       # LoanCreate, LoanResponse, LoanDetail
│   │── routes/
│   │   │── user_routes.py       # CRUD /users (protegido)
│   │   │── device_routes.py     # CRUD /devices (protegido por rol)
│   │   │── loan_routes.py       # CRUD /loans (protegido)
│   │── services/
│   │   │── user_service.py
│   │   │── device_service.py
│   │   │── loan_service.py
│   │── dependencies/
│   │   │── database_dependency.py   # get_db()
│   │   │── auth_dependency.py       # get_current_user, require_admin, etc.
│   │── middlewares/
│   │   │── request_middleware.py    # X-Process-Time, X-App-Name, X-Request-ID
│── alembic/
│   │── versions/                    # Migración generada automáticamente
│── .env
│── .env.example
=======
│   │
│   │── database/
│   │   └── connection.py
│   │
│   │── models/
│   │   │── __init__.py            # importa User, Device, Loan
│   │   │── user_model.py
│   │   │── device_model.py
│   │   └── loan_model.py
│   │
│   │── schemas/
│   │   │── user_schema.py
│   │   │── device_schema.py
│   │   └── loan_schema.py
│   │
│   │── routes/
│   │   │── user_routes.py
│   │   │── device_routes.py
│   │   └── loan_routes.py
│   │
│   │── services/
│   │   │── user_service.py
│   │   │── device_service.py
│   │   └── loan_service.py
│   │
│   └── dependencies/
│       └── database_dependency.py
│
│── alembic/
│   │── versions/
│   │   └── d169f21aeac6_create_users_devices_and_loans_tables.py
│   └── env.py
│
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
│── alembic.ini
│── requirements.txt
│── README.md
```

---

## Instalación y ejecución

```bash
# Clonar el repo y entrar al directorio
git clone https://github.com/KelinMontoya/device_systems
cd device_systems
git checkout device_systems_security

# Crear entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt

<<<<<<< HEAD
# Copiar variables de entorno
copy .env.example .env         # Windows
# cp .env.example .env         # Linux/Mac
# (Editar SECRET_KEY en .env)

# Aplicar migraciones Alembic
python -m alembic upgrade head

# Iniciar servidor
python -m uvicorn app.main:app --reload
```

Documentación Swagger disponible en: `http://localhost:8000/docs`
=======
# Aplicar migraciones (crea las tablas)
alembic upgrade head

# Levantar el servidor
python -m uvicorn app.main:app --reload
```

Documentación:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## Migraciones con Alembic

### Inicialización
```bash
alembic init alembic
```
Esto generó la carpeta `alembic/`, el archivo `alembic.ini` y `alembic/env.py`.

### Configuración
En `alembic.ini` se definió la URL de conexión:
```ini
sqlalchemy.url = sqlite:///./device_systems.db
```

En `alembic/env.py` se importó la `Base` y todos los modelos para que Alembic
detecte los cambios automáticamente:
```python
from app.database.connection import Base
from app.models import User, Device, Loan
target_metadata = Base.metadata
```

### Generar migración
```bash
alembic revision --autogenerate -m "create devices and loans tables"
```
Alembic detectó automáticamente las tablas `users`, `devices` y `loans`, sus
índices y las claves foráneas de `loans` hacia `users` y `devices`.

### Aplicar migración
```bash
alembic upgrade head
```

### Ver historial
```bash
alembic history
```
Salida:
```
<base> -> d169f21aeac6 (head), create users devices and loans tables
```

---

## Modelos y relaciones

### User (1) ── (N) Loan
Un usuario puede tener muchos préstamos.
```python
# user_model.py
loans = relationship("Loan", back_populates="user")
```

### Device (1) ── (N) Loan
Un dispositivo puede aparecer en muchos préstamos históricos.
```python
# device_model.py
loans = relationship("Loan", back_populates="device")
```

### Loan (N) ── (1) User / (N) ── (1) Device
Cada préstamo pertenece a un usuario y a un dispositivo.
```python
# loan_model.py
user_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

user   = relationship("User", back_populates="loans")
device = relationship("Device", back_populates="loans")
```
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf

---

## Variables de entorno (.env)

<<<<<<< HEAD
```env
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./device_systems.db
```

---

## Migración Alembic aplicada

```
INFO  [alembic.autogenerate] Detected added table 'devices'
INFO  [alembic.autogenerate] Detected added table 'loans'
INFO  [alembic.autogenerate] Detected added column 'users.hashed_password'
Running upgrade -> 496a79d7c403, add_authentication_fields_devices_loans
```

---

## Endpoints y protección por roles

| Método | Ruta | Protección |
|--------|------|-----------|
| POST | /auth/register | Pública (rate limit: 3/min) |
| POST | /auth/login | Pública (rate limit: 5/min) |
| GET | /auth/me | Token válido |
| GET | /users/ | Usuario autenticado (rate limit: 30/min) |
| GET | /users/{id} | Usuario autenticado |
| POST | /users/ | Solo admin |
| PUT | /users/{id} | Solo admin |
| DELETE | /users/{id} | Solo admin |
| GET | /devices/ | Admin o support |
| POST | /devices/ | Admin o support |
| PUT/PATCH | /devices/{id} | Admin o support |
| DELETE | /devices/{id} | Solo admin |
| GET | /loans/ | Usuario autenticado |
| POST | /loans/ | Usuario autenticado (rate limit: 10/min) |
| GET | /loans/details | Admin o support |
| PATCH | /loans/{id}/return | Admin o support |

---

## Pruebas funcionales

### 1. Registro exitoso
```
POST /auth/register
{"name":"Admin SENA","email":"admin@sena.edu.co","password":"Admin1234","role":"admin"}
→ 201 {"id":1,"name":"Admin SENA","email":"admin@sena.edu.co","role":"admin","is_active":true}
```

### 2. Contraseña débil (Pydantic v2 field_validator)
```
POST /auth/register  {"password":"1234", ...}
→ 422 {"detail":[{"msg":"Value error, La contraseña debe tener al menos 8 caracteres"}]}
```

### 3. Email duplicado
```
POST /auth/register  (mismo email)
→ 400 {"detail":"El correo 'admin@sena.edu.co' ya está registrado"}
```

### 4. Login correcto — token JWT generado
```
POST /auth/login  username=admin@sena.edu.co  password=Admin1234
→ 200 {"access_token":"eyJhbGci...","token_type":"bearer"}
```

### 5. Login con contraseña incorrecta
```
POST /auth/login  password=wrong
→ 401 {"detail":"Credenciales incorrectas"}
```

### 6. GET /auth/me
```
GET /auth/me  Authorization: Bearer <token>
→ 200 {"id":1,"name":"Admin SENA","email":"admin@sena.edu.co","role":"admin",...}
  (hashed_password NO aparece en la respuesta)
```

### 7. Acceso a ruta protegida sin token
```
GET /users/
→ 401 {"detail":"Not authenticated"}
```

### 8. Token inválido
```
GET /users/  Authorization: Bearer token_falso
→ 401 {"detail":"Token inválido o expirado"}
```

### 9. Usuario sin permisos (support intenta DELETE)
```
DELETE /devices/1  Authorization: Bearer <token_support>
→ 403 {"detail":"Se requiere rol admin"}
```

### 10. Creación de dispositivo con rol permitido
```
POST /devices/  Authorization: Bearer <token_admin>
{"name":"MacBook","serial":"SN002","brand":"Apple","device_type":"laptop"}
→ 201 {"id":2,"name":"MacBook","serial":"SN002",...}
```

### 11. Cabeceras del middleware
```
GET /
→ Headers:
  X-App-Name: device_systems
  X-Process-Time: 0.004263
  X-Request-ID: b255159d
```

### 12. Rate limiting activado
```
POST /auth/login  (6 veces seguidas, límite: 5/min)
Petición 1: 200 OK
Petición 2: 200 OK
Petición 3: 429 Too Many Requests ← RATE LIMIT ACTIVO
Petición 4: 429 Too Many Requests
...
```

---

## CORS — Explicación

La API tiene CORS configurado para dos orígenes locales de desarrollo:

```python
allow_origins=[
    "http://localhost:5173",   # Vite / React
    "http://localhost:3000",   # Create React App / Next.js
],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
```

### ¿Por qué NO se recomienda usar `"*"` en producción con credenciales?

Cuando `allow_credentials=True`, el navegador exige que `allow_origins` contenga URLs específicas, no `"*"`. Si se usa `allow_origins=["*"]` con credenciales, el navegador rechaza la respuesta por política de seguridad CORS y los tokens/cookies no se transmiten.

Además, permitir cualquier origen (`"*"`) en producción expone la API a solicitudes cruzadas desde sitios maliciosos (ataques CSRF), permitiéndoles hacer peticiones autenticadas en nombre del usuario. En producción siempre se deben listar únicamente los dominios del frontend oficial.

---

## Hash de contraseñas con passlib + bcrypt

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

- Las contraseñas **nunca se almacenan en texto plano**.
- bcrypt aplica salt automático y es resistente a ataques de fuerza bruta.
- El campo `hashed_password` **nunca aparece en los schemas de respuesta**.

---

## Autenticación OAuth2 + JWT

1. El usuario hace `POST /auth/login` con email y password.
2. La API verifica la contraseña contra el hash en BD con `passlib`.
3. Si es válida, genera un token JWT firmado con `python-jose` usando `SECRET_KEY`.
4. El cliente envía el token en cada petición: `Authorization: Bearer <token>`.
5. La dependencia `get_current_user` decodifica el token y carga el usuario de BD.

---

## Reflexión — Importancia de la seguridad en APIs REST

Una API sin seguridad expone datos sensibles, permite manipulación de registros por cualquier cliente y puede ser víctima de ataques automatizados. En esta actividad se aplicaron capas de protección complementarias:

- **JWT** evita que sesiones sean robadas o falsificadas sin la clave secreta.
- **bcrypt** protege las contraseñas incluso si la base de datos es comprometida.
- **Autorización por roles** garantiza que cada usuario solo pueda hacer lo que corresponde a su perfil.
- **Rate limiting** previene ataques de fuerza bruta sobre el login.
- **Middleware de trazabilidad** permite auditar cada petición recibida.
- **CORS restrictivo** evita que sitios externos consuman la API sin autorización.

La seguridad no es opcional en una API REST profesional: es parte del diseño desde el primer día.
=======
### Users
| Método | Ruta                  | Descripción                          |
|--------|-----------------------|---------------------------------------|
| GET    | /users                | Listar usuarios                       |
| GET    | /users/{id}           | Buscar por ID                         |
| POST   | /users                | Crear usuario                         |
| PUT    | /users/{id}           | Actualizar completo                   |
| PATCH  | /users/{id}           | Actualizar parcial                    |
| DELETE | /users/{id}           | Eliminar                              |
| GET    | /users/{id}/loans     | Préstamos del usuario (JOIN)          |

### Devices
| Método | Ruta                    | Descripción                         |
|--------|-------------------------|---------------------------------------|
| GET    | /devices                | Listar (filtros: device_type, is_available, brand, search) |
| GET    | /devices/{id}           | Buscar por ID                       |
| POST   | /devices                | Crear dispositivo                   |
| PUT    | /devices/{id}           | Actualizar completo                 |
| PATCH  | /devices/{id}           | Actualizar parcial                  |
| DELETE | /devices/{id}           | Eliminar                            |
| GET    | /devices/{id}/loans     | Historial de préstamos (JOIN)       |

### Loans
| Método | Ruta                     | Descripción                                  |
|--------|--------------------------|-----------------------------------------------|
| GET    | /loans                   | Listar (filtros: status, user_id, device_id, user_email, device_type) |
| GET    | /loans/details           | Listar con datos de usuario y dispositivo (JOIN) |
| GET    | /loans/{id}              | Detalle de un préstamo (JOIN)                |
| POST   | /loans                   | Crear préstamo (valida usuario, dispositivo y disponibilidad) |
| PATCH  | /loans/{id}/return       | Devolver dispositivo                         |

---

## Consultas con joins y filtros

`loan_service.get_all_loans()` combina las tres tablas:

```python
query = (
    db.query(Loan)
    .join(User, Loan.user_id == User.id)
    .join(Device, Loan.device_id == Device.id)
    .options(joinedload(Loan.user), joinedload(Loan.device))
)
```

Filtros aplicados con `and_()` y `ilike()`:
```python
filters = []
if status:      filters.append(Loan.status == status)
if user_email:  filters.append(User.email.ilike(f"%{user_email}%"))
if device_type: filters.append(Device.device_type == device_type)
query = query.filter(and_(*filters))
```

Ejemplo de respuesta de `GET /loans/details`:
```json
{
  "loan_id": 1,
  "status": "active",
  "user": {
    "id": 1,
    "name": "Ana Pérez",
    "email": "ana@sena.edu.co"
  },
  "device": {
    "id": 3,
    "name": "Laptop Lenovo ThinkPad",
    "serial_number": "LEN-2024-001",
    "device_type": "laptop"
  }
}
```

---

## Reglas de negocio en préstamos

**POST /loans**
1. Verifica que el usuario exista → si no, `404`
2. Verifica que el dispositivo exista → si no, `404`
3. Verifica que el dispositivo esté disponible → si no, `409`
4. Crea el préstamo con `status="active"`
5. Marca `device.is_available = False`

**PATCH /loans/{id}/return**
1. Verifica que el préstamo exista → si no, `404`
2. Verifica que no esté ya devuelto → si lo está, `409`
3. Cambia `status="returned"` y asigna `return_date`
4. Marca `device.is_available = True`

---

## Manejo de errores

| Caso                              | Código |
|-----------------------------------|--------|
| Registro creado                   | 201    |
| Consulta exitosa                  | 200    |
| Devolución exitosa                | 200    |
| Eliminación exitosa               | 204    |
| Recurso no encontrado             | 404    |
| Dato duplicado (email/serial)     | 400    |
| Regla de negocio incumplida       | 409    |
| Error de validación (Pydantic)    | 422    |

---
## CAPTURAS

## Estructura de tablas generadas
![Tablas de la base de datos](Captura/tablas.png)

## Migraciones con Alembic

### alembic revision --autogenerate
![Alembic revision](Captura/alembic%20revision.png)

### alembic upgrade head
![Alembic upgrade head](Captura/alembic%20upgrade%20head.png)

### alembic history
![Alembic history](Captura/alembic%20history.png)

## Swagger UI

### Documentación general
![Docs Swagger](Captura/docs.png)

### Endpoints de Devices
![Devices](Captura/Devices.png)

### Endpoints de Loans
![Loans](Captura/loans.png)

![Loans detalle](Captura/loans2.png)

## Pruebas funcionales

### Prueba 1
![Prueba 1](Captura/1.png)

### Prueba 2
![Prueba 2](Captura/2.png)

### Prueba 3
![Prueba 3](Captura/3.png)

### Prueba 4
![Prueba 4](Captura/4.png)

### Prueba 5
![Prueba 5](Captura/5.png)

### Prueba 6
![Prueba 6](Captura/6.png)

### Prueba 7
![Prueba 7](Captura/7.png)

### Prueba 8
![Prueba 8](Captura/8.png)

### Prueba 9
![Prueba 9](Captura/9.png)

### Prueba 10
![Prueba 10](Captura/10.png)

### Prueba 11
![Prueba 11](Captura/11.png)

## Modelo SQLAlchemy vs Schema Pydantic

| Aspecto | Modelo SQLAlchemy | Schema Pydantic |
|---|---|---|
| ¿Para qué sirve? | Representa la tabla en la BD | Valida datos de la API |
| ¿Dónde actúa? | En la base de datos | En el request y response |
| ¿Qué valida? | Constraints de BD (unique, nullable, FK) | Reglas de negocio (min_length, email, enums) |
| ¿Quién lo usa? | SQLAlchemy (ORM) | FastAPI (endpoints) |

---

## Reflexión final

**Sobre migraciones:** Antes de Alembic, cualquier cambio en los modelos exigía
borrar la base de datos y recrearla desde cero, perdiendo todos los datos. Con
Alembic, cada cambio estructural queda versionado en un archivo de migración
que se puede aplicar (`upgrade`) o revertir (`downgrade`) de forma controlada,
igual que se versiona el código fuente con Git.

**Sobre las relaciones:** Modelar `User`, `Device` y `Loan` como tablas
relacionadas en lugar de mezclar todo en una sola tabla permite mantener la
integridad de los datos: un préstamo nunca puede existir sin un usuario y un
dispositivo válidos gracias a las claves foráneas (`ForeignKey`).

**Sobre los joins:** Las consultas con `join()` y `joinedload()` permiten
traer información relacionada de varias tablas en una sola consulta eficiente,
evitando hacer múltiples llamadas separadas a la base de datos y entregando al
cliente de la API respuestas ya enriquecidas con el contexto que necesita.

---

*Rama de desarrollo: `device_systems_alembic_relaciones` — incorpora Alembic, modelos relacionados (Device, Loan) y consultas con joins.*
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
