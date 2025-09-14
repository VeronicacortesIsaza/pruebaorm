from sqlalchemy import UUID, Column, DateTime, String, Integer, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid
from datetime import datetime
class Habitacion(Base):
    __tablename__ = 'habitacion'

    id_habitacion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero = Column(Integer, nullable=False, unique=True, autoincrement=True)
    id_tipo = Column(UUID(as_uuid=True), ForeignKey('tipo_habitacion.id_tipo'), nullable=False)
    tipo = Column(String(20), nullable=False) 
    precio = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True, nullable=False)

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False, default=uuid.uuid4)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    tipo_habitacion = relationship("Tipo_Habitacion", back_populates="habitaciones")
    reservas = relationship("Reserva", back_populates="habitacion")
    
class HabitacionBase(BaseModel):
    numero: int
    id_tipo: uuid.UUID
    precio: float = Field(..., ge=0)
    disponible: bool = Field(default=True)

    @validator('numero')
    def numero_valido(cls, v):
        if v is not None and v < 1:
            raise ValueError('El número de habitación no puede ser menor que 1')
        return v

    @validator('precio')
    def precio_valido(cls, v):
        if v is not None and v < 0:
            raise ValueError('El precio no puede ser negativo')
        if v is not None and v > 999999:
            raise ValueError('El precio es demasiado alto')
        return v
    

class HabitacionCreate(HabitacionBase):
    pass

class HabitacionUpdate(BaseModel):
    numero: Optional[int] = None
    id_tipo: Optional[uuid.UUID] = None
    precio: Optional[float] = None
    disponible: Optional[bool] = None
    id_usuario_edita: Optional[uuid.UUID] = None
    fecha_edicion: Optional[datetime] = None

    @validator('numero')
    def numero_no_vacio(cls, v):
        if v is not None and v < 1:
            raise ValueError('El número no puede ser menor que 1')
        return v
    
    @validator('precio')
    def precio_valido(cls, v):
        if v is not None and v < 0:
            raise ValueError('El precio no puede ser negativo')
        if v is not None and v > 999999:
            raise ValueError('El precio es demasiado alto')
        return v
    

class HabitacionResponse(HabitacionBase):
    id_habitacion: uuid.UUID
    numero: int
    id_tipo: uuid.UUID
    precio: float
    disponible: bool
    id_usuario_crea: uuid.UUID
    id_usuario_edita: Optional[uuid.UUID] = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None,
            uuid.UUID: str  # convierte UUID a string
        }
    }
        
class HabitacionListResponse(BaseModel):
    """Esquema para lista de habitaciones"""
    habitaciones: List[HabitacionResponse]

    class Config:
        orm_mode = True
        from_attributes = True