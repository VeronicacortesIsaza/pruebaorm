from sqlalchemy.orm import Session
from entities.reserva_servicios import Reserva_Servicios 

class ReservaServiciosCRUD:
    @staticmethod
    def crear_reserva_servicio(db: Session, reserva_servicio: Reserva_Servicios):
        db.add(reserva_servicio)
        db.commit()
        db.refresh(reserva_servicio)
        return reserva_servicio

    @staticmethod
    def obtener_reserva_servicio(db: Session, id_reserva_servicio: int):
        return db.query(Reserva_Servicios).filter(Reserva_Servicios.id_reserva_servicio == id_reserva_servicio).first()

    @staticmethod
    def actualizar_reserva_servicio(db: Session, reserva_servicio: Reserva_Servicios):
        db.merge(reserva_servicio)
        db.commit()
        return reserva_servicio

    @staticmethod
    def eliminar_reserva_servicio(db: Session, id_reserva_servicio: int):
        reserva_servicio = db.query(Reserva_Servicios).filter(Reserva_Servicios.id_reserva_servicio == id_reserva_servicio).first()
        if reserva_servicio:
            db.delete(reserva_servicio)
            db.commit()
        return reserva_servicio
