from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class Habitacion(Base):
    __tablename__ = 'habitacion'

    id_habitacion = Column(Integer, primary_key=True)
    numero = Column(String)
    id_tipo = Column(Integer, ForeignKey('tipo_habitacion.id_tipo'))
    precio = Column(Float)
    disponible = Column(Boolean)
    id_usuario_crea = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    tipo_habitacion = relationship("Tipo_Habitacion", back_populates="habitacion")
    reservas = relationship("Reserva", back_populates="habitacion")
    
class HabitacionBase(BaseModel):
    numero: str = Field(..., min_length=1, max_length=10)
    id_tipo: int = Field(..., gt=0)
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
    id_tipo: Optional[int] = None
    precio: Optional[float] = None
    disponible: Optional[bool] = None

    @validator('numero')
    def numero_no_vacio(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El número no puede estar vacío')
        return v.strip() if v else v

class HabitacionResponse(HabitacionBase):
    id_habitacion: int
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
class HabitacionListResponse(BaseModel):
    """Esquema para lista de habitaciones"""
    habitaciones: List[HabitacionResponse]

    class Config:
        from_attributes = True