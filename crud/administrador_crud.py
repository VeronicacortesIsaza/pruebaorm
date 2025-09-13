from sqlalchemy.orm import Session
from entities.administrador import Administrador
from sqlalchemy.ext.asyncio import AsyncSession

class AdministradorCRUD:
    @staticmethod
    def crear_administrador(db: Session, administrador: Administrador):
        db.add(administrador)
        db.commit()
        db.refresh(administrador)
        return administrador

    @staticmethod
    def obtener_administrador(db: Session, id_administrador: int):
        return db.query(Administrador).filter(Administrador.id_administrador == id_administrador).first()

    @staticmethod
    def actualizar_administrador(db: Session, administrador: Administrador):
        db.merge(administrador)
        db.commit()
        return administrador

    @staticmethod
    def eliminar_administrador(db: Session, id_administrador: int):
        administrador = db.query(Administrador).filter(Administrador.id_administrador == id_administrador).first()
        if administrador:
            db.delete(administrador)
            db.commit()
        return administrador
    

