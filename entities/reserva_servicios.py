from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel
from typing import List

class Reserva_Servicios(Base):
    __tablename__ = 'reserva_servicios'

    id_reserva = Column(UUID(as_uuid=True), ForeignKey('reserva.id_reserva'), primary_key=True)
    id_servicio = Column(UUID(as_uuid=True), ForeignKey('servicios_adicionales.id_servicio'), primary_key=True)

    reserva = relationship("Reserva", back_populates="servicios")
    servicio = relationship("Servicios_Adicionales", back_populates="reserva")

    def __repr__(self):
        return f"<Reserva_Servicios(id_reserva={self.id_reserva}, id_servicio={self.id_servicio})>"

class ReservaServicioBase(BaseModel):
    id_reserva: UUID
class ReservaServicioCreate(ReservaServicioBase):
    pass

class ReservaServicioResponse(ReservaServicioBase):
    class Config:
        from_attributes = True

class ReservaServicioListResponse(BaseModel):
    """Esquema para lista de reservas con servicios"""
    reservas_servicios: List[ReservaServicioResponse]

    class Config:
        from_attributes = True