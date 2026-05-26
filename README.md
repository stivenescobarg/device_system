# device_systems API REST

API REST para la gestión de usuarios del sistema device_systems, construida con FastAPI y Python.

---

## Tecnologías utilizadas

- Python 3.13
- FastAPI 0.115.0
- Uvicorn 0.31.0
- Pydantic v2

---

## Instalación

### 1. Clonar el repositorio
```bash
git clone 
cd device_systems
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv
source venv/Scripts/activate
```

![Entorno virtual activado](images/entorno_virtual.png)

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
pip install email-validator
```

![Instalación de dependencias](images/instalacion_dependencias.png)

![Dependencia email-validator](images/dep_email-validator.png)

### 4. Ejecutar el servidor
```bash
uvicorn app.main:app --reload
```

![Servidor corriendo en terminal](images/correr_servidor.png)

![Servidor en navegador](images/servidor_navegador.png)

---
```
## Estructura del proyecto
device_systems/
│── app/
│   │── main.py
│   │── schemas/
│   │   └── user_schema.py
│   └── routes/
│       └── user_routes.py
│── images/
│── requirements.txt
└── README.md
```
---

## Modelo de usuario con Pydantic

Los datos del usuario se validan con Pydantic v2. Los campos son:

| Campo | Tipo | Validación |
|---|---|---|
| id | int | Autoincremental |
| name | str | Mínimo 3 caracteres |
| email | EmailStr | Formato válido |
| role | enum | admin, support, user |
| is_active | bool | True o False |

![Modelo Pydantic](images/Modelo%20de%20usuario_Pydantic.png)

---

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | /users | Lista todos los usuarios |
| GET | /users?role=admin | Filtra usuarios por rol |
| GET | /users?is_active=true | Filtra por estado |
| GET | /users/{user_id} | Obtiene un usuario por ID |
| POST | /users | Crea un nuevo usuario |

---

## Swagger UI

![Swagger UI endpoints GET](images/endpoint_get.png)

![Swagger UI endpoint POST](images/endpoint_post.png)

---

## Pruebas GET /users

### Todos los usuarios
![GET todos los usuarios](images/GET_user_todos_usuarios.png)

### Filtrar por rol admin
![GET filtro rol admin](images/GET_user_admin.png)

### Filtrar por rol user
![GET filtro rol user](images/GET_rol_user.png)

---

## Pruebas GET /users/{user_id}

### Obtener usuario con id 1
![GET usuario id 1](images/GET_user_1.png)

### Error usuario no encontrado id 10
![GET usuario no encontrado](images/GET_user_10_fail.png)

---

## Pruebas POST /users

### Crear nuevo usuario
![POST nuevo usuario](images/POST_Newuser.png)

### Error email duplicado
![POST email repetido](images/POST_email_repetido.png)

---

## GET /users después de crear el nuevo usuario

Una vez creado el nuevo usuario con POST, al consultar GET /users se puede ver que aparece junto a los demás usuarios del sistema.

![GET todos los usuarios incluyendo el nuevo](images/GET_AllUser_Newuser.png)

---

## Cabeceras HTTP personalizadas

Cada respuesta incluye las siguientes cabeceras personalizadas:

- `X-App-Name: device_systems`
- `X-API-Version: 1.0`

---

## Reflexión

Trabajar con FastAPI fue una experiencia muy práctica para entender cómo funcionan las APIs REST. Lo más útil fue la integración automática con Pydantic, que permite validar los datos de entrada sin escribir código extra. La documentación automática con Swagger UI facilita mucho las pruebas y la revisión de los endpoints. Además, la forma en que FastAPI maneja los path parameters y query parameters hace que el código sea muy limpio y fácil de entender. Esta actividad me ayudó a comprender cómo se estructura un proyecto backend real con separación de rutas, esquemas y la aplicación principal.

## Video Explicación
[Youtube](https://youtu.be/vKPdV7m22IQ)