import uuid
from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Administrador(Base):
    __tablename__ = 'administrador'

    id_administrador = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey('usuario.id_usuario'))
    
    usuario = relationship("Usuario", back_populates="administrador")

class AdministradorBase(BaseModel):
    id_usuario: UUID = Field(..., description="ID único del usuario administrador")


class AdministradorCreate(AdministradorBase):
    pass

class AdministradorUpdate(BaseModel):
    id_usuario: Optional[UUID] = Field(None)


class AdministradorResponse(AdministradorBase):
    id_administrador: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
class AdministradorListResponse(BaseModel):
    """Esquema para lista de administradores"""
    administradores: List[AdministradorResponse]
    
    class Config:
        from_attributes = True

