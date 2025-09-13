from sqlalchemy.orm import Session
from entities.tipo_habitacion import Tipo_Habitacion
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class TipoHabitacionCRUD:
    @staticmethod
    def crear_tipo_habitacion(db: Session, tipo_habitacion: Tipo_Habitacion):
        db.add(tipo_habitacion)
        db.commit()
        db.refresh(tipo_habitacion)
        return tipo_habitacion

    @staticmethod
    def obtener_tipo_habitacion(db: Session, id_tipo_habitacion: int):
        return db.query(Tipo_Habitacion).filter(Tipo_Habitacion.id_tipo_habitacion == id_tipo_habitacion).first()

    @staticmethod
    def actualizar_tipo_habitacion(db: Session, tipo_habitacion: Tipo_Habitacion):
        db.merge(tipo_habitacion)
        db.commit()
        return tipo_habitacion

    @staticmethod
    def eliminar_tipo_habitacion(db: Session, id_tipo_habitacion: int):
        tipo_habitacion = db.query(Tipo_Habitacion).filter(Tipo_Habitacion.id_tipo_habitacion == id_tipo_habitacion).first()
        if tipo_habitacion:
            db.delete(tipo_habitacion)
            db.commit()
        return tipo_habitacion
