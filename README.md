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

## PARTE 2 - Endpoints Completos (CRUD)

En esta segunda parte se completó el CRUD de la API implementando PUT, PATCH y DELETE,
se reestructuró el proyecto en capas, se mejoró el manejo de errores con HTTPException,
se aplicaron códigos de estado HTTP correctos y se implementó Dependency Injection con Depends().

---

## Estructura del proyecto v2.0
```
app/
├── main.py                        → Configuración de FastAPI
├── data/
│   └── users_db.py                → Base de datos simulada en memoria
├── schemas/
│   └── user_schema.py             → Modelos de entrada y salida (Pydantic)
├── routes/
│   └── user_routes.py             → Definición de endpoints
├── services/
│   └── user_service.py            → Lógica de negocio
└── dependencies/
└── user_dependencies.py       → Validaciones reutilizables con Depends()
```

Cada capa tiene una responsabilidad única. Las rutas no tienen lógica, los servicios
no validan datos de entrada, y las dependencias se reutilizan entre endpoints.

---

## Documentación Swagger/OpenAPI

FastAPI genera automáticamente la documentación interactiva con todos los endpoints.

![Swagger UI](images/Parte_2/API_swagger_endpoints.png)

---

## Endpoints de la API

| Método | Endpoint | Descripción | Códigos de estado |
|--------|----------|-------------|-------------------|
| GET | /users | Listar todos los usuarios | 200 OK |
| GET | /users/{id} | Obtener usuario por ID | 200 OK, 404 |
| POST | /users | Crear nuevo usuario | 201 Created, 400, 422 |
| PUT | /users/{id} | Actualizar usuario completamente | 200 OK, 400, 404, 422 |
| PATCH | /users/{id} | Actualizar usuario parcialmente | 200 OK, 400, 404 |
| DELETE | /users/{id} | Eliminar usuario | 200 OK, 404 |

---

## Pruebas GET /users y GET /users/{user_id}

### GET /users — Listar todos los usuarios
![GET usuarios Thunder](images/Parte_2/01_users_thunder.png)

---

## Pruebas POST /users — Crear usuario

### POST exitoso (201 Created)
![POST usuario Thunder](images/Parte_2/02_post_thunder.png)

### Error: Campo faltante (422 Unprocessable Entity)
![POST campo faltante](images/Parte_2/04_POST_thunder_campo_faltante.png)

---
### GET /users/{user_id} — Obtener usuario Nuevo
![GET usuario específico](images/Parte_2/03_GET_user.png)
---

## Pruebas PUT /users/{user_id} — Actualización completa

PUT reemplaza **todos** los campos del usuario. Es obligatorio enviar name, email, role e is_active.

### PUT exitoso (200 OK)
![PUT thunder exitoso](images/Parte_2/07_PUT_thunder.png)

### Error: Campo faltante (422 Unprocessable Entity)
![PUT campo faltante](images/Parte_2/06_PUT_thunder_campo_faltante.png)

### Error: Usuario no encontrado (404 Not Found)
![PUT sin ID](images/Parte_2/12_PUT_swagger_sin_id.png)

---

## Pruebas PATCH /users/{user_id} — Actualización parcial

PATCH modifica **solo los campos enviados**. Los demás campos no se tocan.
Internamente usa `model_dump(exclude_unset=True)` para detectar qué campos llegaron.

### PATCH exitoso — Actualizar solo el nombre (200 OK)
![PATCH nombre actualizado](images/Parte_2/05_PATCH_thunder_name_actualizado.png)

### Error: PATCH sin datos (400 Bad Request)
![PATCH sin campos](images/Parte_2/13_PATCH_thunder_sin_datos.png)

---

## Pruebas DELETE /users/{user_id} — Eliminar usuario

### DELETE exitoso (200 OK)
![DELETE thunder exitoso](images/Parte_2/08_DELETE_thunder.png)

### Error: Usuario inexistente (404 Not Found)
![DELETE usuario inexistente Thunder](images/Parte_2/09_DELETE_thunder_id_no_encontrado.png)

![DELETE usuario inexistente Swagger](images/Parte_2/11_DELETE_swagger_usuario_inexistente.png)

### Verificación: Confirmar que el usuario fue eliminado
![GET usuario eliminado](images/Parte_2/10_GET_ID_swagger_usuario_eliminado.png)

---

## Manejo de errores con HTTPException

Todos los errores se manejan con `HTTPException` y retornan respuestas estructuradas:

```json
{
  "detail": "Usuario con ID 999 no encontrado"
}
```

| Error | Código | Causa |
|---|---|---|
| Usuario no encontrado | 404 | ID inexistente en la base de datos |
| Email duplicado | 400 | El email ya está registrado por otro usuario |
| Rol no permitido | 400 | El rol no es admin, support ni user |
| PATCH sin datos | 400 | No se envió ningún campo para actualizar |
| Validación de campos | 422 | Pydantic detectó datos inválidos o faltantes |

---

## Dependency Injection con Depends()

Se implementaron 6 dependencias reutilizables en `user_dependencies.py`:

| Dependencia | Qué hace |
|---|---|
| `get_user_or_404` | Busca usuario por ID, lanza 404 si no existe |
| `validate_unique_email` | Verifica que el email no esté registrado (para POST) |
| `validate_unique_email_for_update` | Igual pero excluye al propio usuario (para PUT/PATCH) |
| `validate_role` | Verifica que el rol sea admin, support o user |
| `get_api_config` | Retorna configuración general de la API |
| `get_current_user` | Simula autenticación básica con token |

Uso en las rutas con `Depends()`:

```python
@router.get("/users/{user_id}")
def get_user(user = Depends(get_user_or_404)):
    return user
```

`Depends()` ejecuta la dependencia antes del endpoint. Si falla, FastAPI detiene
la petición y retorna el error automáticamente, sin llegar al cuerpo del endpoint.

**Ventajas:**
- Validaciones centralizadas y reutilizables entre endpoints
- Código más limpio — las rutas solo coordinan, no validan
- Manejo de errores consistente en toda la API
- Mayor facilidad para hacer pruebas unitarias

---

## Reflexión final — Evolución del proyecto

La versión 1.0 era un prototipo funcional pero limitado, solo GET y POST, y sin manejo de errores estructurado.

La versión 2.0 representa un salto hacia una arquitectura profesional. Separar el proyecto
en rutas, schemas, servicios y dependencias hace que cada parte sea independiente y fácil
de modificar sin afectar el resto. Implementar PUT, PATCH y DELETE completó el CRUD, pero
lo más valioso fue entender la diferencia entre ambos: PUT obliga a enviar todo,
PATCH solo toca lo que llega gracias a `exclude_unset=True`.

El uso de `Depends()` fue el cambio más significativo en términos de arquitectura —
elimina la repetición de validaciones y centraliza el manejo de errores de forma elegante.
Finalmente, Swagger UI sigue siendo una herramienta invaluable: la documentación se genera
sola desde el código, lo que garantiza que siempre esté actualizada.

## === VIDEO EXPLICATIVO ====

[Youtube](https://www.youtube.com/watch?v=A1J01vLPdaA)

## PARTE 3 - Persistencia de Datos con SQLAlchemy

En esta tercera parte se evolucionó la API para dejar de trabajar con datos en memoria
y utilizar una base de datos real mediante SQLAlchemy y SQLite.

---
```
## Estructura del proyecto v3.0
device_systems/
├── app/
│   ├── main.py                        → Configuración de FastAPI y arranque
│   ├── database/
│   │   └── connection.py              → Engine, SessionLocal, Base, create_tables()
│   ├── models/
│   │   └── user_model.py              → Modelo SQLAlchemy (tabla users)
│   ├── schemas/
│   │   └── user_schema.py             → Schemas Pydantic: Create, Update, Patch, Response
│   ├── routes/
│   │   └── user_routes.py             → Endpoints REST con Depends(get_db)
│   ├── services/
│   │   └── user_service.py            → Lógica CRUD contra base de datos
│   └── dependencies/
│       └── database_dependency.py     → Dependencia get_db() con yield
├── images/
├── requirements.txt
└── README.md
```
---

## Base de datos generada

Al iniciar el servidor, SQLAlchemy crea automáticamente el archivo `device_systems.db`
con la tabla `users` y sus columnas.

![Base de datos generada](images/Parte_3/Base_de_datos_device_system.png)

---

## Documentación Swagger UI

![Swagger UI endpoints](images/Parte_3/GET_redoc.png)

---
---

## Documentación ReDoc

ReDoc es la vista alternativa de documentación que genera FastAPI automáticamente
en `/redoc`. Muestra los mismos endpoints con un diseño diferente.

### GET /users
![GET ReDoc](images/Parte_3/GET_redoc.png)

### GET /users/{id}
![GET por ID ReDoc](images/Parte_3/GET_id_redoc.png)

### POST /users
![POST ReDoc](images/Parte_3/POST_redoc.png)

### PATCH /users/{id}
![PATCH ReDoc](images/Parte_3/PATCH_redoc.png)

### PUT /users/{id}
![PUT ReDoc](images/Parte_3/PUT_redoc.png)

### DELETE /users/{id}
![DELETE ReDoc](images/Parte_3/DELETE_redoc.png)

---

## Pruebas GET /users — Listar usuarios

### Listar todos los usuarios
![GET listar usuarios](images/Parte_3/GET_listar_usuario.png)

### Filtrar por rol
![GET filtrar por rol](images/Parte_3/GET_filtrar_por_rol.png)

### Filtrar activos
![GET filtrar activos](images/Parte_3/GET_filtrar_activos.png)

### Filtrar inactivos
![GET filtrar inactivos](images/Parte_3/GET_filtrar_inactivos.png)

---

## Pruebas GET /users/{id}

### Consultar usuario por ID
![GET por ID](images/Parte_3/GET_por_ID.png)

### Usuario inexistente (404)
![GET usuario inexistente](images/Parte_3/GET_usuario_inexistente.png)

---

## Pruebas POST /users — Crear usuario

### POST exitoso (201 Created)
![POST usuario válido](images/Parte_3/POST_usuario_válido.png)

### Error: Email duplicado (400)
![POST email repetido](images/Parte_3/POST_email_repetido.png)

### Persistencia: usuarios siguen guardados al reiniciar el servidor
![Usuarios persistidos](images/Parte_3/GET_usuarios_guardados_luego_servidor_nuevo.png)

---

## Pruebas PUT /users/{id} — Actualización completa

### PUT exitoso (200 OK)
![PUT completo](images/Parte_3/PUT_completo.png)

### Error: Campos incompletos (422)
![PUT campos incompletos](images/Parte_3/PUT_campos_incompletos.png)

---

## Pruebas PATCH /users/{id} — Actualización parcial

### PATCH exitoso (200 OK)
![PATCH parcial](images/Parte_3/PATCH_parcial.png)

### Error: Email ya existente (400)
![PATCH email existente](images/Parte_3/PATCH_email_existente.png)

---

## Pruebas DELETE /users/{id} — Eliminar usuario

### DELETE exitoso (200 OK)
![DELETE](images/Parte_3/DELETE.png)

### Error: Usuario inexistente (404)
![DELETE inexistente](images/Parte_3/DELETE_inexistente.png)

### Verificación: usuario eliminado ya no existe
![GET eliminado inexistente](images/Parte_3/GET_eliminado_inexistente.png)

---

## Manejo de errores

| Error | Código | Causa |
|---|---|---|
| Usuario no encontrado | 404 | ID inexistente en la base de datos |
| Email duplicado | 400 | El email ya está registrado |
| PATCH sin datos | 400 | No se envió ningún campo |
| Datos inválidos | 422 | Pydantic detectó campos incorrectos |
| ID con string | 422 | El ID debe ser un número entero |

![Error ID con string](images/Parte_3/ERROR_ID_con_string.png)

---

## Modelo SQLAlchemy vs Schema Pydantic

| | Modelo SQLAlchemy | Schema Pydantic |
|---|---|---|
| Archivo | `models/user_model.py` | `schemas/user_schema.py` |
| Propósito | Define la tabla en la BD | Valida datos de entrada/salida |
| Representa | Columnas SQL con constraints | Campos JSON del request/response |
| Se usa en | Servicio / ORM | Rutas / endpoints |

---

## Reflexión final — Evolución del proyecto

La diferencia más importante entre la versión 2.0 y la 3.0 no está solo en la parte técnica, sino también en la forma de pensar el proyecto. Pasar de manejar una lista en memoria a trabajar con una base de datos real hace que sea necesario organizar mejor las responsabilidades de cada componente.

En este caso, los modelos de SQLAlchemy se encargan de definir cómo se estructura la base de datos, mientras que los schemas de Pydantic establecen cómo se envían y reciben los datos a través de la API. Por otro lado, el servicio actúa como intermediario entre ambos, evitando que todo quede mezclado.

Además, el uso de get_db() junto con yield permite que cada petición tenga su propia conexión o sesión con la base de datos y asegura que esta se cierre correctamente al finalizar, incluso cuando ocurre algún error durante la ejecución.

## === VIDEO EXPLICATIVO ===

[Youtube](https://youtu.be/qSGZEgONhTs)

## PARTE 4 - Migraciones con Alembic, Asociaciones de Modelos y Joins

En esta cuarta parte se amplió device_systems para gestionar dispositivos y préstamos,
incorporando migraciones de base de datos controladas con Alembic, relaciones entre
modelos con SQLAlchemy y consultas avanzadas con joins y filtros.

Rama de trabajo: `device_systems_alembic_relaciones`

---

## Estructura del proyecto v4.0
```
device_systems/
├── app/
│   ├── main.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── user_model.py          → Se agregó relationship con Loan
│   │   ├── device_model.py        → Nuevo
│   │   └── loan_model.py          → Nuevo
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── device_schema.py       → Nuevo
│   │   └── loan_schema.py         → Nuevo
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── device_routes.py       → Nuevo
│   │   └── loan_routes.py         → Nuevo
│   ├── services/
│   │   ├── user_service.py
│   │   ├── device_service.py      → Nuevo
│   │   └── loan_service.py        → Nuevo
│   └── dependencies/
│       └── database_dependency.py
├── alembic/
│   └── versions/
├── alembic.ini
├── requirements.txt
└── README.md
```
---

## Instalación y configuración de Alembic

### Instalación
```bash
pip install alembic
```

![Instalación de Alembic](images/Parte_4/Instalacion_Alembic.png)

### Inicialización
```bash
alembic init alembic
```

Esto generó la carpeta `alembic/` con `env.py`, `script.py.mako` y la carpeta `versions/`.

### Configuración

En `alembic.ini` se configuró la URL de conexión:
```ini
sqlalchemy.url = sqlite:///./device_systems.db
```

En `alembic/env.py` se importó la metadata de los modelos para que Alembic pudiera
detectarlos automáticamente:
```python
from app.database.connection import Base
from app.models import User, Device, Loan

target_metadata = Base.metadata
```

---

## Generación y aplicación de migraciones

### Migración automática
```bash
alembic revision --autogenerate -m "create devices and loans tables"
```

![Migración automática generada](images/Parte_4/migracion_automatica.png)

### Aplicación de la migración
```bash
alembic upgrade head
```

![Migración aplicada contra device_systems.db](images/Parte_4/migracion_contra_device_systems.db.png)

### Historial de migraciones
```bash
alembic history
```

![Historial de Alembic](images/Parte_4/alembic_history.png)

### Tablas generadas

Verificación de las tablas creadas en `device_systems.db` mediante SQLite Viewer:
`users`, `devices`, `loans` y la tabla interna `alembic_version`.

![Tablas creadas](images/Parte_4/tablas_creadas.png)

---

## Modelos y asociaciones

### Modelo Device

```python
class Device(Base):
    __tablename__ = "devices"
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False, index=True)
    device_type   = Column(String, nullable=False)
    brand         = Column(String, nullable=True)
    is_available  = Column(Boolean, default=True)
    created_at    = Column(DateTime, default=datetime.utcnow)

    loans = relationship("Loan", back_populates="device")
```

### Modelo Loan

```python
class Loan(Base):
    __tablename__ = "loans"
    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id   = Column(Integer, ForeignKey("devices.id"), nullable=False)
    loan_date   = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    status      = Column(String, nullable=False, default="active")

    user   = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")
```

### Relaciones implementadas

| Relación | Tipo | Descripción |
|---|---|---|
| User → Loan | One-to-Many | Un usuario puede tener muchos préstamos |
| Device → Loan | One-to-Many | Un dispositivo puede tener muchos préstamos históricos |
| Loan → User | Many-to-One | Cada préstamo pertenece a un usuario |
| Loan → Device | Many-to-One | Cada préstamo pertenece a un dispositivo |

La integridad referencial se garantiza con `ForeignKey("users.id")` y `ForeignKey("devices.id")`,
impidiendo crear un préstamo con un usuario o dispositivo inexistente.

---

## Documentación Swagger / ReDoc

![Endpoints en Swagger](images/Parte_4/DOCS_endpoints.png)

### ReDoc por recurso

![ReDoc Users](images/Parte_4/REDOC_users.png)
![ReDoc Devices](images/Parte_4/REDOC_devices.png)
![ReDoc Loans](images/Parte_4/REDOC_loans.png)

---

## Pruebas — Dispositivos

### Crear dispositivo
![POST dispositivo nuevo](images/Parte_4/Devices/POST_dispositivo_nuevo.png)
![POST dispositivo nuevo 2](images/Parte_4/Devices/POST_dispotivo_nuevo_2.png)
![POST dispositivo nuevo 3](images/Parte_4/Devices/POST_dispositivo_nuevo_3.png)

### Error: número de serie duplicado (400)
![POST número de serie duplicado](images/Parte_4/Devices/POST_numero_serie_duplicado.png)

### Listar dispositivos
![GET dispositivos](images/Parte_4/Devices/GET_dispositivos.png)

### Consultar dispositivo prestado
![GET dispositivo ID2 prestado](images/Parte_4/Devices/GET_dispositivo_ID2_prestado.png)

### Error: eliminar dispositivo con préstamo activo (409)
![DELETE dispositivo prestado](images/Parte_4/Devices/DELETE_dispositivo_prestado.png)

---

## Pruebas — Préstamos

### Crear préstamo válido
![POST préstamo](images/Parte_4/Loans/POST_prestamo.png)

### Error: dispositivo inexistente (404)
![POST dispositivo inexistente](images/Parte_4/Loans/POST_dispositivo_inexistente.png)

### Error: dispositivo no disponible (409)
![POST dispositivo no disponible](images/Parte_4/Loans/POST_dispositivo_no_disponible.png)

### Devolver dispositivo
![PATCH devuelta préstamo](images/Parte_4/Loans/PATCH_devuelta_prestamo.png)

### Error: préstamo inexistente (404)
![PATCH préstamo inexistente](images/Parte_4/Loans/PATCH_prestamo_inexistente.png)

### Error: préstamo ya devuelto (409)
![PATCH préstamo ya devuelto](images/Parte_4/Loans/PATCH_prestamo_ya_devuelto.png)

### Consultar préstamos de un usuario
![GET préstamo usuarios](images/Parte_4/Loans/GET_prestamo_usuarios.png)

### Consultar historial de préstamos de un dispositivo
![GET historial dispositivos prestados](images/Parte_4/Loans/GET_historial_dispositivos_prestados.png)

---

## Pruebas con Postman — Joins y filtros

### Listar préstamos con información de usuario y dispositivo (join)
![GET lista préstamos](images/Parte_4/Postman/GET_lista_prestamos.png)

### Filtrar préstamos por estado activo
![GET préstamo activo](images/Parte_4/Postman/GET_prestamo_active.png)

### Filtrar préstamos devueltos
![GET préstamos devueltos](images/Parte_4/Postman/GET_prestamos_returned.png)

### Filtrar por tipo de dispositivo
![GET dispositivo tipo laptop](images/Parte_4/Postman/GET_dispositivo_type=laptop.png)

### Verificar que el dispositivo devuelto vuelve a estar disponible
![GET dispositivo devuelto disponible](images/Parte_4/Postman/GET_dispositivo_devuelto_vuelve_a_estar_disponible.png)

---

## Manejo de errores

| Error | Código | Causa |
|---|---|---|
| Usuario inexistente | 404 | El `user_id` enviado no existe en la base de datos |
| Dispositivo inexistente | 404 | El `device_id` enviado no existe |
| Dispositivo no disponible | 409 | El dispositivo ya tiene un préstamo activo |
| Préstamo inexistente | 404 | El `loan_id` no existe al consultar o devolver |
| Préstamo ya devuelto | 409 | Se intenta devolver un préstamo con estado `returned` |
| Número de serie duplicado | 400 | El `serial_number` ya está registrado por otro dispositivo |
| Eliminar dispositivo prestado | 409 | El dispositivo tiene un préstamo activo asociado |

### Error al aplicar migraciones

Aunque en este proyecto las migraciones se aplicaron sin conflictos, este tipo de error
ocurre cuando una migración intenta ejecutar una operación inválida contra la base de
datos real, por ejemplo referenciar una tabla o columna que no existe, o violar una
restricción de clave foránea con datos ya existentes. Alembic detiene la ejecución y
lanza una excepción (`OperationalError` o similar) mostrando la causa exacta en la
terminal. La forma de resolverlo es corregir el archivo de migración en
`alembic/versions/` y volver a ejecutar `alembic upgrade head`, o revertir con
`alembic downgrade -1` si la migración ya se aplicó parcialmente.

---

## Reflexión final

Esta etapa representó el salto de un CRUD simple hacia un sistema con relaciones reales
entre tablas. Alembic resolvió un problema que antes no existía: versionar los cambios
de la base de datos de forma controlada, en lugar de borrar y recrear el archivo `.db`
cada vez que cambia un modelo.

Las asociaciones con `relationship()` y `back_populates()` permiten navegar entre
objetos relacionados directamente en Python (`loan.user`, `loan.device`) sin escribir
consultas SQL manuales, mientras que `ForeignKey()` garantiza la integridad referencial
a nivel de base de datos, impidiendo crear préstamos huérfanos.

Las consultas con `join()` y `joinedload()` permitieron construir respuestas que combinan
información de varias tablas en una sola petición, evitando que el cliente tenga que
hacer múltiples llamadas para obtener los datos relacionados de un préstamo.

## === VIDEO EXPLICATIVO ===

[Youtube]()