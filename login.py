from database.config import SessionLocal
from entities.usuario import Usuario

def login():
    session = SessionLocal()
    try:
        user = input("Usuario: ").strip()
        password = input("Contraseña: ").strip()

        usuario = session.query(Usuario).filter_by(nombre_usuario=user, clave=password).first()
        if usuario:
            print(f"Bienvenido {usuario.nombre_usuario}")
            return True
        else:
            print("Usuario o contraseña incorrectos.")
            return False
    finally:
        session.close()
