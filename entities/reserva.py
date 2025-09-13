from sqlalchemy import UUID, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from database.config import Base
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid
from datetime import date, datetime

class Reserva(Base):
    __tablename__ = 'reserva'

    id_reserva = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_cliente = Column(UUID(as_uuid=True), ForeignKey('cliente.id_cliente'))
    id_habitacion = Column(UUID(as_uuid=True), ForeignKey('habitacion.id_habitacion'))
    fecha_entrada = Column(date)
    fecha_salida = Column(date)
    estado_reserva = Column(String)
    numero_de_personas = Column(Integer)
    noches = Column(Integer)
    costo_total = Column(Float)
    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(date(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(date(timezone=True), onupdate=func.now(), nullable=True)
    

    cliente = relationship("Cliente", back_populates="reservas")
    habitacion = relationship("Habitacion", back_populates="reservas")
    servicios = relationship("Reserva_Servicios", back_populates="reserva")
    
class ReservaBase(BaseModel):
    id_reserva: UUID 
    id_servicio: UUID 
    fecha_entrada: date
    fecha_salida: date
    estado_reserva: str = Field(..., min_length=1, max_length=50)
    numero_de_personas: int = Field(..., gt=0)
    noches: int = Field(..., gt=0)
    costo_total: float = Field(..., ge=0)
    id_cliente: UUID 
    id_habitacion: UUID 
    fecha_creacion: datetime = Field(None, description="Fecha de creación de la reserva")
    fecha_edicion: Optional[datetime] = None
    
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
        if v < date.today():
            raise ValueError('La fecha de entrada no puede ser en el pasado')
        return v
    
class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(ReservaBase):
    id_reserva: Optional[UUID] = None
    id_servicio: Optional[UUID] = None
    estado_reserva: Optional[str] = None
    numero_de_personas: Optional[int] = None
    noches: Optional[int] = None
    costo_total: Optional[float] = None
    id_cliente: Optional[UUID] = None
    id_habitacion: Optional[UUID] = None
    fecha_salida: Optional[date] = None
    fecha_entrada: Optional[date] = None
    
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
        if v < date.today():
            raise ValueError('La fecha de entrada no puede ser en el pasado')
        return v

class Reserva_ServiciosResponse(ReservaBase):
    id_reserva: UUID
    id_servicio: UUID
    fecha_entrada: date
    fecha_salida: date
    estado_reserva: str
    numero_de_personas: int
    noches: int
    costo_total: float
    id_cliente: UUID
    id_habitacion: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }


class Reserva_ServiciosListResponse(BaseModel):
    """Esquema para lista de reservas"""
    reservas: List[Reserva_ServiciosResponse]

    class Config:
        from_attributes = True