from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from pydantic import BaseModel, validator
from typing import List, Optional
from entities.usuario import Usuario

class Administrador(Base):
    __tablename__ = "administrador"

    id_admin = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), primary_key=True, default=uuid.uuid4)

    usuario = relationship("Usuario", back_populates="administrador")

    def __repr__(self):
        return f"<Administrador(id={self.id_admin})>"

class AdministradorBase(BaseModel):
    id_admin: uuid.UUID

    @validator('id_admin')
    def validar_tipo_usuario_administrador(cls, v, values, **kwargs):
        if 'tipo_usuario' in values and values['tipo_usuario'] != 'administrador':
            raise ValueError('El usuario asociado debe ser de tipo administrador')
        return v

class AdministradorResponse(BaseModel):
    id_admin: uuid.UUID
    nombre: str
    apellidos: str
    telefono: Optional[str] = None
    fecha_creacion: str

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            uuid.UUID: str
        }
    }

class AdministradorListResponse(BaseModel):
    administradores: List[AdministradorResponse]

    class Config:
        orm_mode = True
        from_attributes = True

