from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.reserva_servicios import Reserva_Servicios

class ReservaServiciosCRUD:
    """
    Módulo CRUD para la entidad Reserva_Servicios.

    Administra la relación entre las reservas y los servicios adicionales contratados.

    Funciones principales:
        - crear_reserva_servicio(db: Session, reserva_servicio: Reserva_Servicios) -> Reserva_Servicios
        - obtener_reserva_servicio(db: Session, id_reserva_servicio: UUID) -> Reserva_Servicios
        - obtener_reservas_servicios(db: Session, skip: int = 0, limit: int = 100) -> List[Reserva_Servicios]
        - eliminar_reserva_servicio(db: Session, id_reserva_servicio: UUID) -> bool
    """
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_reserva_servicio(db: Session, reserva_servicio: Reserva_Servicios):
        if not reserva_servicio.id_reserva or not reserva_servicio.id_servicio:
            raise ValueError("El registro debe estar asociado a una reserva y un servicio")
        
        db.add(reserva_servicio)
        db.commit()
        db.refresh(reserva_servicio)
        return reserva_servicio

    @staticmethod
    def obtener_reserva_servicio(db: Session, id_reserva_servicio: UUID):
        rs = db.query(Reserva_Servicios).filter(Reserva_Servicios.id_reserva_servicio == id_reserva_servicio).first()
        if not rs:
            raise ValueError("Reserva-Servicio no encontrado")
        return rs

    @staticmethod
    def obtener_reservas_servicios(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Reserva_Servicios).offset(skip).limit(limit).all()

    @staticmethod
    def eliminar_reserva_servicio(db: Session, id_reserva_servicio: UUID) -> bool:
        rs = db.query(Reserva_Servicios).filter(Reserva_Servicios.id_reserva_servicio == id_reserva_servicio).first()
        if not rs:
            raise ValueError("Reserva-Servicio no encontrado")
        db.delete(rs)
        db.commit()
        return True
