import asyncio
from database.connection import get_session
from crud.usuario_crud import UsuarioCRUD

async def login(nombre_usuario: str, clave: str):
    async for session in get_session():
        usuario = await UsuarioCRUD.authenticate(session, nombre_usuario, clave)
        if usuario:
            print(f"Inicio de sesión exitoso para: {usuario.nombre_usuario}")
            return usuario
        else:
            print("Nombre de usuario o clave incorrectos")
            return None

async def main():
    # Prueba de login
    await login("juanp", "clave123")  

if __name__ == "__main__":
    asyncio.run(main())