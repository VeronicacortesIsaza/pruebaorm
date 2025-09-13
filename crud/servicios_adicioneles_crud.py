from sqlalchemy.orm import Session
from entities.servicios_adicionales import Servicios_Adicionales

class ServiciosAdicionalesCRUD:
    @staticmethod
    def crear_servicio_adicional(db: Session, servicio_adicional: Servicios_Adicionales):
        db.add(servicio_adicional)
        db.commit()
        db.refresh(servicio_adicional)
        return servicio_adicional

    @staticmethod
    def obtener_servicio_adicional(db: Session, id_servicio_adicional: int):
        return db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio_adicional == id_servicio_adicional).first()

    @staticmethod
    def actualizar_servicio_adicional(db: Session, servicio_adicional: Servicios_Adicionales):
        db.merge(servicio_adicional)
        db.commit()
        return servicio_adicional

    @staticmethod
    def eliminar_servicio_adicional(db: Session, id_servicio_adicional: int):
        servicio_adicional = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio_adicional == id_servicio_adicional).first()
        if servicio_adicional:
            db.delete(servicio_adicional)
            db.commit()
        return servicio_adicional
