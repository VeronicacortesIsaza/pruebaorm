from sqlalchemy import UUID, Column, Integer, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid
from datetime import datetime

class Habitacion(Base):
    __tablename__ = 'habitacion'

    id_habitacion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero = Column(Integer, nullable=False, unique=True)
    id_tipo = Column(UUID(as_uuid=True), ForeignKey('tipo_habitacion.id_tipo'), nullable=False)
    precio = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True, nullable=False)

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True)

    fecha_creacion = Column(datetime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(datetime(timezone=True), onupdate=func.now(), nullable=True)

    tipo_habitacion = relationship("Tipo_Habitacion", back_populates="habitaciones")
    reservas = relationship("Reserva", back_populates="habitacion")
    
class HabitacionBase(BaseModel):
    numero: int = Field(..., ge=1, le=10)
    id_tipo: UUID = Field(..., description="ID del tipo de habitación")
    precio: float = Field(..., ge=0)
    disponible: bool = Field(default=False)

    @validator('numero')
    def numero_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El número no puede estar vacío')
        return v.strip()
    def validar_numero(cls, v):
        if v is not None and (v > 0):
            raise ValueError('El número debe estar entre 1 y 10')
        return v

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
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
class HabitacionListResponse(BaseModel):
    """Esquema para lista de habitaciones"""
    habitaciones: List[HabitacionResponse]

    class Config:
        from_attributes = True