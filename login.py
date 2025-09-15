from database.config import SessionLocal
from entities.usuario import Usuario

def login():
    with SessionLocal() as session:
        user = input("Usuario: ").strip()
        password = input("Contraseña: ").strip()

        usuario = session.query(Usuario).filter_by(
            nombre_usuario=user, clave=password
        ).first()

        if usuario:
            print(f"Bienvenido {usuario.nombre_usuario}")
            return usuario
        else:
            print("Usuario o contraseña incorrectos.")
            return None
