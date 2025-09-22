from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.administrador import Administrador

class AdministradorCRUD:
    """
    Módulo CRUD para la entidad Administrador.

    Este archivo gestiona la persistencia de los administradores del sistema,
    los cuales deben estar asociados a un usuario previamente creado.

    Funciones principales:
        - crear_administrador(db: Session, administrador: Administrador) -> Administrador
        - obtener_administrador(db: Session, id_admin: UUID) -> Administrador
        - obtener_administradores(db: Session, skip: int = 0, limit: int = 100) -> List[Administrador]
        - eliminar_administrador(db: Session, id_admin: UUID) -> bool

    Notas:
        - Se valida que cada administrador esté asociado a un usuario existente.
    """
    def __init__(self, db):
        self.db = db
        
    @staticmethod
    def crear_administrador(db: Session, administrador: Administrador):
        if not administrador.id_admin:
            raise ValueError("El administrador debe estar asociado a un usuario")
        
        db.add(administrador)
        db.commit()
        db.refresh(administrador)
        return administrador

    @staticmethod
    def obtener_administrador(db: Session, id_admin: UUID):
        admin = db.query(Administrador).filter(Administrador.id_admin == id_admin).first()
        if not admin:
            raise ValueError("Administrador no encontrado")
        return admin

    @staticmethod
    def obtener_administradores(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Administrador).offset(skip).limit(limit).all()

    @staticmethod
    def eliminar_administrador(db: Session, id_admin: UUID) -> bool:
        admin = db.query(Administrador).filter(Administrador.id_admin == id_admin).first()
        if not admin:
            raise ValueError("Administrador no encontrado")
        db.delete(admin)
        db.commit()
        return True
