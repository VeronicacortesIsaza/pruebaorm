import uuid
from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Cliente(Base):
    __tablename__ = 'cliente'

    id_cliente = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey('usuario.id_usuario'))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    
    usuario = relationship("Usuario", back_populates="cliente", uselist=False)
    reservas = relationship("Reserva", back_populates="cliente")

class ClienteBase(BaseModel):
    id_usuario: UUID = Field(..., description="ID único del usuario")

class ClienteCreate(ClienteBase):
    pass 

class ClienteUpdate(BaseModel):
    id_usuario: Optional[UUID] = Field(None)


class ClienteResponse(ClienteBase):
    id_cliente: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ClienteListResponse(BaseModel):
    """Esquema para lista de clientes"""
    clientes: List[ClienteResponse]

    class Config:
        from_attributes = True
        