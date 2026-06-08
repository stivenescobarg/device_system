from app.database.connection import SessionLocal


def get_db():
    """
    Dependencia que entrega una sesión de base de datos.
    Cierra la sesión automáticamente al terminar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()