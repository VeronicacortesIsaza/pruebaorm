from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from entities.usuario import Usuario, UsuarioCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class UsuarioCRUD:
    @staticmethod
    def crear_usuario(db: Session, usuario: UsuarioCreate):
        existente = db.query(Usuario).filter(Usuario.nombre_usuario == usuario.nombre_usuario).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso, elige otro"
            )
    
        nuevo_usuario = Usuario(**usuario.dict())
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def obtener_usuario(db: Session, id_usuario: int):
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    @staticmethod
    def actualizar_usuario(db: Session, usuario: Usuario):
        db.merge(usuario)
        db.commit()
        return usuario

    @staticmethod
    def eliminar_usuario(db: Session, id_usuario: int):
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            db.delete(usuario)
            db.commit()
        return usuario
    
    @staticmethod
    async def authenticate(session: AsyncSession, nombre_usuario: str, clave: str) -> Usuario | None:
        result = await session.execute(
            select(Usuario).where(Usuario.nombre_usuario == nombre_usuario)
        )
        usuario = result.scalars().first()
        if usuario and usuario.clave == clave:
            return usuario
        return None