from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class Servicios_Adicionales(Base):
    __tablename__ = 'servicios_adicionales'

    id_servicio = Column(Integer, primary_key=True)
    nombre_servicio = Column(String)
    precio = Column(Float)
    id_usuario_crea = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_usuario_edita = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    reservas = relationship("Reserva_Servicios", back_populates="servicio")
    
class Servicios_AdicionalesBase(BaseModel):
    id_servicio: int = Field(..., gt=0)
    nombre_servicio: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., ge=0)
    
    @validator('id_servicio')
    def id_servicio_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de servicio debe ser un número positivo')
        return v
    @validator('nombre_servicio')
    def nombre_servicio_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre del servicio no puede estar vacío')
        return v.strip()
    
    @validator('precio')
    def precio_no_negativo(cls, v):
        if v is not None and v < 0:
            raise ValueError('El precio no puede ser negativo')
        return v
    
class Servicios_AdicionalesCreate(Servicios_AdicionalesBase):
    pass

class Servicios_AdicionalesUpdate(Servicios_AdicionalesBase):
    id_servicio: Optional[int]
    nombre_servicio: Optional[str]
    precio: Optional[float]

    @validator('id_servicio')
    def id_servicio_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de servicio debe ser un número positivo')
        return v
    @validator('nombre_servicio')
    def nombre_servicio_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre del servicio no puede estar vacío')
        return v.strip()
    
    @validator('precio')
    def precio_no_negativo(cls, v):
        if v is not None and v < 0:
            raise ValueError('El precio no puede ser negativo')
        return v

class Servicios_AdicionalesResponse(Servicios_AdicionalesBase):
    id_servicio: int
    nombre_servicio: str
    precio: float

    class Config:
        orm_mode = True
        
class Servicios_AdicionalesListResponse(BaseModel):
    """Esquema para lista de servicios adicionales"""
    servicios: List[Servicios_AdicionalesResponse]

    class Config:
        from_attributes = True