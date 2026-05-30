# 🖥️ device_systems API

API REST para gestión de usuarios construida con **FastAPI** y **Pydantic v2**.

## ⚙️ Instalación

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
uvicorn app.main:app --reload
```

Swagger UI disponible en: http://127.0.0.1:8000/docs

## 📌 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /users | Listar todos los usuarios |
| GET | /users?role=admin | Filtrar por rol |
| GET | /users?is_active=true | Filtrar por estado |
| GET | /users/{id} | Obtener usuario por ID |
| POST | /users | Crear nuevo usuario |

## 🔧 Cabeceras personalizadas

Todos los endpoints retornan:
- `X-App-Name: device_systems`
- `X-API-Version: 1.0`

## 📸 Capturas Swagger UI
![Captura](./Captura/1.png) 

## 💡 Reflexión
FastAPI permite construir APIs REST de forma rápida y segura gracias a la
integración automática con Pydantic para validaciones y la generación
automática de documentación con Swagger UI.