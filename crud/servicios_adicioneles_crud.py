from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.servicios_adicionales import Servicios_Adicionales

class ServiciosAdicionalesCRUD:
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_servicio(db: Session, servicio: Servicios_Adicionales):
        if not servicio.nombre or not servicio.nombre.strip():
            raise ValueError("El nombre del servicio no puede estar vacío")
        if servicio.precio <= 0:
            raise ValueError("El precio del servicio debe ser mayor a 0")
        
        existente = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.nombre == servicio.nombre).first()
        if existente:
            raise ValueError("El servicio adicional ya existe")

        db.add(servicio)
        db.commit()
        db.refresh(servicio)
        return servicio

    @staticmethod
    def obtener_servicio(db: Session, id_servicio: UUID):
        servicio = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio == id_servicio).first()
        if not servicio:
            raise ValueError("Servicio no encontrado")
        return servicio

    @staticmethod
    def obtener_servicios(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Servicios_Adicionales).offset(skip).limit(limit).all()

    @staticmethod
    def eliminar_servicio(db: Session, id_servicio: UUID) -> bool:
        servicio = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio == id_servicio).first()
        if not servicio:
            raise ValueError("Servicio no encontrado")
        db.delete(servicio)
        db.commit()
        return True
