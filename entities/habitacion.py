from sqlalchemy import UUID, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid

class Habitacion(Base):
    __tablename__ = 'habitacion'

    id_habitacion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    numero = Column(String, nullable=False, unique=True)
    id_tipo = Column(UUID(as_uuid=True), ForeignKey('tipo_habitacion.id_tipo'), nullable=False)
    precio = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True, nullable=False)

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    tipo_habitacion = relationship("Tipo_Habitacion", back_populates="habitaciones")
    reservas = relationship("Reserva", back_populates="habitacion")
    
class HabitacionBase(BaseModel):
    numero: str = Field(..., min_length=1, max_length=10)
    id_tipo: UUID = Field(..., gt=0)
    precio: float = Field(..., ge=0)
    disponible: bool = Field(default=False)

    @validator('numero')
    def numero_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El número no puede estar vacío')
        return v.strip()

class HabitacionCreate(HabitacionBase):
    pass

class HabitacionUpdate(BaseModel):
    numero: Optional[str] = None
    id_tipo: Optional[UUID] = None
    precio: Optional[float] = None
    disponible: Optional[bool] = None

    @validator('numero')
    def numero_no_vacio(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El número no puede estar vacío')
        return v.strip() if v else v

class HabitacionResponse(HabitacionBase):
    id_habitacion: UUID
    fecha_creacion: DateTime
    fecha_edicion: Optional[DateTime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            DateTime: lambda v: v.isoformat()
        }
        
class HabitacionListResponse(BaseModel):
    """Esquema para lista de habitaciones"""
    habitaciones: List[HabitacionResponse]

    class Config:
        from_attributes = True