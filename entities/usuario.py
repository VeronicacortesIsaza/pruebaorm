from sqlalchemy import String, Column, func
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "Usuario"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    tipo_usuario = Column(String(20), nullable=False) 
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    clave = Column(String(10), nullable=False)
    fecha_creacion = Column(datetime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(datetime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nombre_usuario={self.nombre_usuario})>"
    
class UsuarioBase(BaseModel):
    id_usuario: uuid.UUID = Field(..., description="ID único del usuario")
    nombre: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    tipo_usuario: str = Field(..., min_length=1, max_length=20)
    nombre_usuario: str = Field(..., min_length=1, max_length=50)
    clave: str = Field(..., min_length=1, max_length=10)
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    @validator('telefono')
    def telefono_valido(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('El teléfono debe contener solo dígitos')
        return v

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    id_usuario: Optional[UUID] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    tipo_usuario: Optional[str] = None
    nombre_usuario: Optional[str] = None
    clave: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    @validator('telefono')
    def telefono_valido(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('El teléfono debe contener solo dígitos')
        return v

class UsuarioResponse(UsuarioBase):
    id_usuario: uuid.UUID
    nombre: str
    apellidos: str
    telefono: Optional[str]
    tipo_usuario: str
    nombre_usuario: str
    clave: str
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UsuarioListResponse(BaseModel):
    """Esquema para lista de usuarios"""
    usuarios: List[UsuarioResponse]
    
    class Config:
        from_attributes = True