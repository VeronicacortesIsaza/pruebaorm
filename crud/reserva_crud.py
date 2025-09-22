from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.reserva import Reserva

class ReservaCRUD:
    """
    Módulo CRUD para la entidad Reserva.

    Gestiona las reservas realizadas por los clientes, validando fechas
    y asociando correctamente a cliente y habitación.

    Funciones principales:
        - crear_reserva(db: Session, reserva: Reserva) -> Reserva
        - obtener_reserva(db: Session, id_reserva: UUID) -> Reserva
        - obtener_reservas(db: Session) -> List[Reserva]
        - actualizar_reserva(db: Session, id_reserva: UUID, **kwargs) -> Reserva
        - eliminar_reserva(db: Session, id_reserva: UUID) -> bool
        - obtener_reservas_activas(db: Session) -> List[Reserva]
        - actualizar_costo_total(db: Session, id_reserva: UUID, monto_extra: float) -> Reserva

    Notas:
        - Se valida que la fecha de entrada sea menor a la de salida.
        - Al cancelar una reserva se recomienda actualizar el estado de la habitación.
    """
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
    def obtener_reservas(db: Session):
        return db.query(Reserva).all()

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
    @staticmethod
    def obtener_reservas_activas(db: Session):
        return db.query(Reserva).filter(Reserva.estado_reserva == "Activa").all()
    
    @staticmethod
    def actualizar_costo_total(db: Session, id_reserva, monto_extra: float):
        reserva = db.query(Reserva).filter_by(id_reserva=id_reserva).first()
        if not reserva:
            raise ValueError("Reserva no encontrada")

        reserva.costo_total += monto_extra
        db.add(reserva)
        return reserva
