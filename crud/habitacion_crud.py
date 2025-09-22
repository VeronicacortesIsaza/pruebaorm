from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.habitacion import Habitacion
from datetime import date

class HabitacionCRUD:
    """
    Módulo CRUD para la entidad Habitación.

    Define las operaciones relacionadas con la gestión de habitaciones en el hotel.
    Incluye validaciones de número único y precio positivo.

    Funciones principales:
        - crear_habitacion(db: Session, habitacion: Habitacion) -> Habitacion
        - obtener_habitacion(db: Session, id_habitacion: UUID) -> Habitacion
        - obtener_habitaciones(db: Session) -> List[Habitacion]
        - actualizar_habitacion(db: Session, id_habitacion: UUID, **kwargs) -> Habitacion
        - eliminar_habitacion(db: Session, id_habitacion: UUID) -> bool
    """
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_habitacion(db: Session, habitacion: Habitacion):
        if habitacion.precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        existente = db.query(Habitacion).filter(Habitacion.numero == habitacion.numero).first()
        if existente:
            raise ValueError("El número de habitación ya está en uso")

        db.add(habitacion)
        db.commit()
        db.refresh(habitacion)
        return habitacion

    @staticmethod
    def obtener_habitacion(db: Session, id_habitacion: UUID):
        habitacion = db.query(Habitacion).filter(Habitacion.id_habitacion == id_habitacion).first()
        if not habitacion:
            raise ValueError("Habitación no encontrada")
        return habitacion

    @staticmethod
    def obtener_habitaciones(db: Session):
        return db.query(Habitacion).all()

    @staticmethod
    def actualizar_habitacion(db: Session, id_habitacion: UUID, **kwargs):
        habitacion = db.query(Habitacion).filter(Habitacion.id_habitacion == id_habitacion).first()
        if not habitacion:
            raise ValueError("Habitación no encontrada")

        for key, value in kwargs.items():
            if hasattr(habitacion, key):
                setattr(habitacion, key, value)

        db.commit()
        db.refresh(habitacion)
        return habitacion

    @staticmethod
    def eliminar_habitacion(db: Session, id_habitacion: UUID) -> bool:
        habitacion = db.query(Habitacion).filter(Habitacion.id_habitacion == id_habitacion).first()
        if not habitacion:
            raise ValueError("Habitación no encontrada")
        db.delete(habitacion)
        db.commit()
        return True
