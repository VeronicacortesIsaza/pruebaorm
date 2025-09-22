from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.servicios_adicionales import Servicios_Adicionales
from datetime import date

class ServiciosAdicionalesCRUD:
    """
    Módulo CRUD para la entidad Servicios_Adicionales.

    Gestiona los servicios extra que ofrece el hotel, como lavandería,
    transporte, restaurante, entre otros.

    Funciones principales:
        - crear_servicio(db: Session, servicio: Servicios_Adicionales) -> Servicios_Adicionales
        - obtener_servicio(db: Session, id_servicio: UUID) -> Servicios_Adicionales
        - obtener_servicios(db: Session) -> List[Servicios_Adicionales]
        - actualizar_servicio(db: Session, servicio: Servicios_Adicionales, id_usuario_edita: int, fecha_edita: date) -> Servicios_Adicionales
        - eliminar_servicio(db: Session, id_servicio: UUID) -> bool

    Notas:
        - Se valida nombre no vacío, precio mayor a 0 y unicidad del servicio.
    """
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_servicio(db: Session, servicio: Servicios_Adicionales):
        if not servicio.nombre_servicio or not servicio.nombre_servicio.strip():
            raise ValueError("El nombre del servicio no puede estar vacío")
        if servicio.precio <= 0:
            raise ValueError("El precio del servicio debe ser mayor a 0")
        
        existente = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.nombre_servicio == servicio.nombre_servicio).first()
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
    def obtener_servicios(db: Session):
        return db.query(Servicios_Adicionales).all()
    
    @staticmethod
    def actualizar_servicio(db, servicio: Servicios_Adicionales, id_usuario_edita: int, fecha_edita: date):
        servicio.id_usuario_edita = id_usuario_edita
        servicio.fecha_edita = fecha_edita
        db.commit()
        db.refresh(servicio)
        return servicio

    @staticmethod
    def eliminar_servicio(db: Session, id_servicio: UUID) -> bool:
        servicio = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio == id_servicio).first()
        if not servicio:
            raise ValueError("Servicio no encontrado")
        db.delete(servicio)
        db.commit()
        return True
