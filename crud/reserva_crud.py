from sqlalchemy.orm import Session
from entities.reserva import Reserva

class ReservaCRUD:
    @staticmethod
    def crear_reserva(db: Session, reserva: Reserva):
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
        return reserva

    @staticmethod
    def obtener_reserva(db: Session, id_reserva: int):
        return db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

    @staticmethod
    def actualizar_reserva(db: Session, reserva: Reserva):
        db.merge(reserva)
        db.commit()
        return reserva

    @staticmethod
    def eliminar_reserva(db: Session, id_reserva: int):
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if reserva:
            db.delete(reserva)
            db.commit()
        return reserva
