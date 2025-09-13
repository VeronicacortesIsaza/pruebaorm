from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class Cliente(Base):
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    
    usuario = relationship("Usuario", back_populates="cliente")
    reservas = relationship("Reserva", back_populates="cliente")

class ClienteBase(BaseModel):
    id_usuario: int = Field(..., gt=0, description="Numero de documento del cliente")

    @validator('id_usuario')
    def id_usuario_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de usuario debe ser un número positivo')
        return v

class ClienteCreate(ClienteBase):
    pass 

class ClienteUpdate(BaseModel):
    id_usuario: Optional[int] = Field(None, gt=0)

    @validator('id_usuario')
    def id_usuario_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de usuario debe ser un número positivo')
        return v

class ClienteResponse(ClienteBase):
    id_cliente: int
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ClienteListResponse(BaseModel):
    """Esquema para lista de clientes"""
    clientes: List[ClienteResponse]

    class Config:
        from_attributes = True