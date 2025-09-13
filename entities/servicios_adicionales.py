from sqlalchemy import UUID, Column, ForeignKey, String, Float, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid
from datetime import datetime

class Servicios_Adicionales(Base):
    __tablename__ = 'servicios_adicionales'

    id_servicio = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_servicio = Column(String)
    precio = Column(Float)
    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(datetime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(datetime(timezone=True), onupdate=func.now(), nullable=True)

    reservas = relationship("Reserva_Servicios", back_populates="servicio")
    
class Servicios_AdicionalesBase(BaseModel):
    id_servicio: UUID = Field(..., gt=0)
    nombre_servicio: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., ge=0)
    id_usuario_crea: UUID = Field(..., description="ID del usuario que crea el servicio adicional")
    id_usuario_edita: Optional[UUID] = Field(None, description="ID del usuario que edita el servicio adicional")
    fecha_creacion: Optional[datetime] = Field(None, description="Fecha de creación del servicio adicional")
    fecha_edicion: Optional[datetime] = Field(None, description="Fecha de edición del servicio adicional")

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
    id_servicio: Optional[UUID] = None
    nombre_servicio: Optional[str]
    precio: Optional[float]
    id_usuario_edita: Optional[UUID] = None
    fecha_edicion: Optional[datetime] = None

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
    id_servicio: UUID
    nombre_servicio: str
    precio: float
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class Servicios_AdicionalesListResponse(BaseModel):
    """Esquema para lista de servicios adicionales"""
    servicios: List[Servicios_AdicionalesResponse]

    class Config:
        from_attributes = True