from sqlalchemy import UUID, Column, Integer, String, Date, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid

class Reserva(Base):
    __tablename__ = 'reserva'

    id_reserva = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    id_cliente = Column(UUID(as_uuid=True), ForeignKey('cliente.id_cliente'))
    id_habitacion = Column(UUID(as_uuid=True), ForeignKey('habitacion.id_habitacion'))
    fecha_entrada = Column(Date)
    fecha_salida = Column(Date)
    estado_reserva = Column(String)
    numero_de_personas = Column(Integer)
    noches = Column(Integer)
    costo_total = Column(Float)
    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    

    cliente = relationship("Cliente", back_populates="reservas")
    habitacion = relationship("Habitacion", back_populates="reservas")
    servicios = relationship("Reserva_Servicios", back_populates="reserva")
    
class ReservaBase(BaseModel):
    id_reserva: int = Field(..., gt=0)
    id_servicio: int = Field(..., gt=0)
    fecha_entrada: DateTime
    fecha_salida: DateTime
    estado_reserva: str = Field(..., min_length=1, max_length=50)
    numero_de_personas: int = Field(..., gt=0)
    noches: int = Field(..., gt=0)
    costo_total: float = Field(..., ge=0)
    id_cliente: int = Field(..., gt=0)
    id_habitacion: int = Field(..., gt=0)
    

    @validator('id_reserva')
    def id_reserva_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de reserva debe ser un número positivo')
        return v

    @validator('id_servicio')
    def id_servicio_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de servicio debe ser un número positivo')
        return v
    
    @validator('estado_reserva')
    def estado_reserva_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El estado de la reserva no puede estar vacío')
        return v.strip()
    
    @validator('numero_de_personas')
    def numero_de_personas_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El número de personas debe ser un número positivo')
        return v
    
    @validator('noches')
    def noches_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El número de noches debe ser un número positivo')
        return v
    
    @validator('fecha_salida')
    def fecha_salida_despues_de_entrada(cls, v, values):
        if 'fecha_entrada' in values and v <= values['fecha_entrada']:
            raise ValueError('La fecha de salida debe ser posterior a la fecha de entrada')
        return v
    @validator('fecha_entrada')
    def fecha_entrada_no_pasada(cls, v):
        if v < DateTime.now().date():
            raise ValueError('La fecha de entrada no puede ser en el pasado')
        return v
    
class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(ReservaBase):
    id_reserva: Optional[int] = None
    id_servicio: Optional[int] = None
    estado_reserva: Optional[str] = None
    numero_de_personas: Optional[int] = None
    noches: Optional[int] = None
    costo_total: Optional[float] = None
    id_cliente: Optional[int] = None
    id_habitacion: Optional[int] = None
    fecha_salida: Optional[DateTime] = None
    fecha_entrada: Optional[DateTime] = None
    
    @validator('estado_reserva')
    def estado_reserva_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El estado de la reserva no puede estar vacío')
        return v.strip()
    
    @validator('numero_de_personas')
    def numero_de_personas_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El número de personas debe ser un número positivo')
        return v
    
    @validator('noches')
    def noches_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El número de noches debe ser un número positivo')
        return v
    
    @validator('fecha_salida')
    def fecha_salida_despues_de_entrada(cls, v, values):
        if 'fecha_entrada' in values and v <= values['fecha_entrada']:
            raise ValueError('La fecha de salida debe ser posterior a la fecha de entrada')
        return v
    @validator('fecha_entrada')
    def fecha_entrada_no_pasada(cls, v):
        if v < DateTime.now().date():
            raise ValueError('La fecha de entrada no puede ser en el pasado')
        return v

class Reserva_ServiciosResponse(ReservaBase):
    id_reserva: UUID
    id_servicio: UUID
    fecha_entrada: DateTime
    fecha_salida: DateTime
    estado_reserva: str
    numero_de_personas: int
    noches: int
    costo_total: float
    id_cliente: UUID
    id_habitacion: UUID
    fecha_creacion: DateTime
    fecha_edicion: Optional[DateTime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            DateTime: lambda v: v.isoformat()
        }


class Reserva_ServiciosListResponse(BaseModel):
    """Esquema para lista de reservas"""
    reservas: List[Reserva_ServiciosResponse]

    class Config:
        from_attributes = True