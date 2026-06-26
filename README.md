# device_systems — v4.0 (Security Branch)

API REST segura para gestión de **usuarios**, **dispositivos** y **préstamos**, construida con FastAPI + SQLAlchemy + SQLite.

Esta versión agrega sobre la v3.0 una capa completa de seguridad: autenticación JWT, hash de contraseñas, protección de rutas por roles, middleware personalizado, CORS, rate limiting y validaciones avanzadas con Pydantic v2.

---

## Estructura del proyecto

```
device_systems/
│── app/
│   │── main.py
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

---

## Variables de entorno (.env)

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
