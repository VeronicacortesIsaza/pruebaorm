from sqlalchemy.orm import Session
from entities.habitacion import Habitacion

class HabitacionCRUD:
    @staticmethod
    def crear_habitacion(db: Session, habitacion: Habitacion):
        db.add(habitacion)
        db.commit()
        db.refresh(habitacion)
        return habitacion

    @staticmethod
    def obtener_habitacion(db: Session, id_habitacion: int):
        return db.query(Habitacion).filter(Habitacion.id_habitacion == id_habitacion).first()

    @staticmethod
    def actualizar_habitacion(db: Session, habitacion: Habitacion):
        db.merge(habitacion)
        db.commit()
        return habitacion

    @staticmethod
    def eliminar_habitacion(db: Session, id_habitacion: int):
        habitacion = db.query(Habitacion).filter(Habitacion.id_habitacion == id_habitacion).first()
        if habitacion:
            db.delete(habitacion)
            db.commit()
        return habitacion
