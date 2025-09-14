from sqlalchemy import String, Column, DateTime, func
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    tipo_usuario = Column(String(20), nullable=False) 
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    clave = Column(String(10), nullable=False)  
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    administrador = relationship("Administrador", back_populates="usuario", uselist=False)

    cliente = relationship("Cliente", back_populates="usuario", uselist=False)

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nombre_usuario={self.nombre_usuario})>"
    
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    tipo_usuario: str = Field(..., min_length=1, max_length=20)
    nombre_usuario: str = Field(..., min_length=1, max_length=50)
    clave: str = Field(..., min_length=1, max_length=10)
    
    @validator('tipo_usuario')
    def tipo_usuario_valido(cls, v):
        tipos_validos = {"cliente", "administrador"}
        if v.lower() not in tipos_validos:
            raise ValueError(f"El tipo_usuario debe ser uno de {tipos_validos}")
        return v.lower()

    @validator('telefono')
    def telefono_valido(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('El teléfono debe contener solo dígitos')
        return v
    
    @validator('clave')
    def clave_valida(cls, v):
        if not v.strip():
            raise ValueError('La clave no puede estar vacía')
        return v.strip()

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    nombre_usuario: Optional[str] = None
    clave: Optional[str] = None
    fecha_edicion: Optional[datetime] = None
    
    @validator('nombre_usuario')
    def nombre_usuario_valido(cls, v):
        if v is not None and len(v) > 40:
            raise ValueError('El nombre de usuario no puede exceder 40 caracteres')
        return v
    
    @validator('telefono')
    def telefono_valido(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('El teléfono debe contener solo dígitos')
        return v
    
    @validator('clave')
    def clave_valida(cls, v):
        if not v.strip():
            raise ValueError('La clave no puede estar vacía')
        return v.strip()

class UsuarioResponse(UsuarioBase):
    id_usuario: uuid.UUID
    nombre: str
    apellidos: str
    telefono: Optional[str] = None
    tipo_usuario: str
    nombre_usuario: str
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

class UsuarioListResponse(BaseModel):
    usuarios: List[UsuarioResponse]

    class Config:
        orm_mode = True
        from_attributes = True
