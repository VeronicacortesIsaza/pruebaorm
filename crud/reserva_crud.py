from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.reserva import Reserva

class ReservaCRUD:
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_reserva(db: Session, reserva: Reserva):
        if not reserva.id_cliente or not reserva.id_habitacion:
            raise ValueError("La reserva debe estar asociada a un cliente y una habitación")

        if reserva.fecha_entrada >= reserva.fecha_salida:
            raise ValueError("La fecha de entrada debe ser anterior a la fecha de salida")

        db.add(reserva)
        db.commit()
        db.refresh(reserva)
        return reserva

    @staticmethod
    def obtener_reserva(db: Session, id_reserva: UUID):
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            raise ValueError("Reserva no encontrada")
        return reserva

    @staticmethod
    def obtener_reservas(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Reserva).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar_reserva(db: Session, id_reserva: UUID, **kwargs):
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            raise ValueError("Reserva no encontrada")

        for key, value in kwargs.items():
            if hasattr(reserva, key):
                setattr(reserva, key, value)

        if reserva.fecha_inicio and reserva.fecha_fin and reserva.fecha_inicio >= reserva.fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")

        db.commit()
        db.refresh(reserva)
        return reserva

    @staticmethod
    def eliminar_reserva(db: Session, id_reserva: UUID) -> bool:
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            raise ValueError("Reserva no encontrada")
        db.delete(reserva)
        db.commit()
        return True
    
    def obtener_reservas_activas(self):
        return self.db.query(Reserva).filter(Reserva.estado_reserva == "Activa").all()
