from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from pydantic import BaseModel, validator
from typing import List, Optional
from entities.usuario import Usuario

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), primary_key=True, default=uuid.uuid4)

    usuario = relationship("Usuario", back_populates="cliente", uselist=False)
    reservas = relationship("Reserva", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id={self.id_cliente})>"
    
class ClienteBase(BaseModel):
    id_cliente: uuid.UUID
    
    @validator('id_cliente')
    def validar_tipo_usuario_cliente(cls, v, values, **kwargs):
        if 'tipo_usuario' in values and values['tipo_usuario'] != 'cliente':
            raise ValueError('El usuario asociado debe ser de tipo cliente')
        return v

class ClienteResponse(BaseModel):
    id_cliente: uuid.UUID
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

class ClienteListResponse(BaseModel):
    clientes: List[ClienteResponse]

    class Config:
        orm_mode = True
        from_attributes = True