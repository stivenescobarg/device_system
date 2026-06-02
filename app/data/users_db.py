# Base de datos simulada en memoria
users_db = [
    {"id": 1, "name": "Stiven Escobar", "email": "stiven@email.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Lina Escobar", "email": "lina@email.com", "role": "support", "is_active": True},
    {"id": 3, "name": "Nayelly Chaverra", "email": "nayelly@email.com", "role": "user", "is_active": False},
]

def get_next_id() -> int:
    """Obtiene el siguiente ID disponible"""
    if not users_db:
        return 1
    return max(user["id"] for user in users_db) + 1