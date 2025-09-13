from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field, validator
from typing import Optional, List

Base = declarative_base()

class Usuario(Base):
    
    __tablename__ = "Usuario"

    id_usuario = Column(Integer, primary_key=True, index=True,autoincrement=False)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    tipo_usuario = Column(String(20), nullable=False) 
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    clave = Column(String(10), nullable=False)
    es_admin = Column(Boolean, default=False)
    fecha_creacion = Column(String, nullable=False)
    fecha_edicion = Column(String, nullable=True)

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nombre_usuario={self.nombre_usuario})>"
    
class UsuarioBase(BaseModel):
    id_usuario: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    tipo_usuario: str = Field(..., min_length=1, max_length=20)
    nombre_usuario: str = Field(..., min_length=1, max_length=50)
    clave: str = Field(..., min_length=1, max_length=10)

    @validator('id_usuario')
    def id_usuario_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de usuario debe ser un número positivo')
        return v

    @validator('telefono')
    def telefono_valido(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('El teléfono debe contener solo dígitos')
        return v

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    id_usuario: Optional[int] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    tipo_usuario: Optional[str] = None
    nombre_usuario: Optional[str] = None
    clave: Optional[str] = None

    @validator('id_usuario')
    def id_usuario_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de reserva debe ser un número positivo')
        return v

    @validator('telefono')
    def telefono_valido(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('El teléfono debe contener solo dígitos')
        return v

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    nombre: str
    apellidos: str
    telefono: Optional[str]
    tipo_usuario: str
    nombre_usuario: str
    clave: str
    fecha_creacion: Optional[str] = None
    fecha_edicion: Optional[str] = None
    

    class Config:
        orm_mode = True

class UsuarioListResponse(BaseModel):
    """Esquema para lista de usuarios"""
    usuarios: List[UsuarioResponse]
    
    class Config:
        from_attributes = True