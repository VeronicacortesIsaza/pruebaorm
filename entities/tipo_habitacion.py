from sqlalchemy import UUID, Column, ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid

class Tipo_Habitacion(Base):
    __tablename__ = 'tipo_habitacion'

    id_tipo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    nombre_tipo = Column(String)
    descripcion = Column(Text)
    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    habitaciones = relationship("Habitacion", back_populates="tipo_habitacion")
    
class Tipo_HabitacionBase(BaseModel):
    id_tipo: UUID = Field(..., gt=0)
    nombre_tipo: str = Field(..., min_length=1, max_length=100)
    descripcion: str = Field(..., min_length=1)
    id_usuario_crea: UUID = Field(..., description="ID del usuario que crea el tipo de habitación")
    id_usuario_edita: Optional[UUID] = Field(None, description="ID del usuario que edita el tipo de habitación")
    fecha_creacion: Optional[DateTime] = Field(None, description="Fecha de creación del tipo de habitación")
    fecha_edicion: Optional[DateTime] = Field(None, description="Fecha de edición del tipo de habitación")

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
    id_tipo: Optional[UUID] = None
    nombre_tipo: Optional[str] = None
    descripcion: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None
    fecha_edicion: Optional[DateTime] = None

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

class Tipo_HabitacionResponse(Tipo_HabitacionBase):
    id_tipo: UUID
    nombre_tipo: str
    descripcion: str
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
    fecha_creacion: DateTime
    fecha_edicion: Optional[DateTime] = None
    
    
    class Config:
        from_attributes = True
class Tipo_HabitacionListResponse(BaseModel):
    """Esquema para lista de tipos de habitación"""
    tipos_habitacion: List[Tipo_HabitacionResponse]
    
    class Config:
        from_attributes = True