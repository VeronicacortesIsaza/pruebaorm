from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid
from datetime import datetime

class Tipo_Habitacion(Base):
    __tablename__ = 'tipo_habitacion'

    id_tipo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_tipo = Column(String)
    descripcion = Column(Text)
    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    habitaciones = relationship("Habitacion", back_populates="tipo_habitacion")
    
class Tipo_HabitacionBase(BaseModel):
    nombre_tipo: str = Field(..., min_length=1, max_length=100)
    descripcion: str = Field(..., min_length=1)

    @validator('nombre_tipo')
    def nombre_tipo_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre del tipo no puede estar vacío')
        return v.strip()

    @validator('descripcion')
    def descripcion_no_vacia(cls, v):
        if not v.strip():
            raise ValueError('La descripción no puede estar vacía')
        return v.strip()

class Tipo_HabitacionCreate(Tipo_HabitacionBase):
    pass

class Tipo_HabitacionUpdate(Tipo_HabitacionBase):
    nombre_tipo: Optional[str] = None
    descripcion: Optional[str] = None
    id_usuario_edita: Optional[uuid.UUID] = None
    fecha_edicion: Optional[datetime] = None

    @validator('nombre_tipo')
    def nombre_tipo_no_vacio(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre del tipo no puede estar vacío')
        return v.strip() if v else v

    @validator('descripcion')
    def descripcion_no_vacia(cls, v):
        if v is not None and not v.strip():
            raise ValueError('La descripción no puede estar vacía')
        return v.strip() if v else v

class Tipo_HabitacionResponse(Tipo_HabitacionBase):
    id_tipo: uuid.UUID
    nombre_tipo: str
    descripcion: str
    id_usuario_crea: uuid.UUID
    id_usuario_edita: Optional[uuid.UUID] = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None,
            uuid.UUID: str 
        }
    }
        
class Tipo_HabitacionListResponse(BaseModel):
    """Esquema para lista de tipos de habitación"""
    tipos_habitacion: List[Tipo_HabitacionResponse]
    
    class Config:
        orm_mode = True
        from_attributes = True