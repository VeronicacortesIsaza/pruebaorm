from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, Float, func
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
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    reservas_servicios = relationship("Reserva_Servicios", back_populates="servicio")
    
class Servicios_AdicionalesBase(BaseModel):
    nombre_servicio: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., ge=0)
   
    @validator('nombre_servicio')
    def nombre_servicio_no_vacio(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre del servicio no puede estar vacío')
        return v.strip() if v else v

    @validator('precio')
    def precio_no_negativo(cls, v):
        if v is not None and v < 0:
            raise ValueError('El precio no puede ser negativo')
        if v is not None and v > 999999:
            raise ValueError('El precio es demasiado alto')
        return v
    
class Servicios_AdicionalesCreate(Servicios_AdicionalesBase):
    pass

class Servicios_AdicionalesUpdate(Servicios_AdicionalesBase):
    nombre_servicio: Optional[str] = None
    precio: Optional[float] = None
    id_usuario_edita: Optional[uuid.UUID] = None
    fecha_edicion: Optional[datetime] = None

   
    @validator('nombre_servicio')
    def nombre_servicio_no_vacio(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre del servicio no puede estar vacío')
        return v.strip() if v else v

    @validator('precio')
    def precio_no_negativo(cls, v):
        if v is not None and v < 0:
            raise ValueError('El precio no puede ser negativo')
        if v is not None and v > 999999:
            raise ValueError('El precio es demasiado alto')
        return v
class Servicios_AdicionalesResponse(Servicios_AdicionalesBase):
    id_servicio: uuid.UUID
    nombre_servicio: str
    precio: float
    id_usuario_crea: Optional[uuid.UUID] = None
    id_usuario_edita: Optional[uuid.UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None,
            uuid.UUID: str 
        }
    }
        
class Servicios_AdicionalesListResponse(BaseModel):
    """Esquema para lista de servicios adicionales"""
    servicios: List[Servicios_AdicionalesResponse]

    class Config:
        orm_mode = True
        from_attributes = True