from sqlalchemy import UUID, Column, Integer, String, Float, DateTime, Date, ForeignKey, func
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
    fecha_entrada: date
    fecha_salida: date
    estado_reserva: str = Field(..., min_length=1, max_length=50)
    numero_de_personas: int = Field(..., gt=0)
    noches: int = Field(..., gt=0)
    costo_total: float = Field(..., ge=0)
    
    @validator('estado_reserva')
    def estado_reserva_valido(cls, v):
        estados_validos = {"pendiente", "confirmada", "cancelada"}
        if v.strip().lower() not in estados_validos:
            raise ValueError(f"El estado de la reserva debe ser uno de {estados_validos}")
        return v.strip().lower()

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
    
class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(ReservaBase):
    estado_reserva: Optional[str] = None
    numero_de_personas: Optional[int] = None
    noches: Optional[int] = None
    costo_total: Optional[float] = None
    id_usuario_edita: Optional[uuid.UUID] = None
    fecha_edicion: Optional[datetime] = None
    fecha_salida: Optional[date] = None
    fecha_entrada: Optional[date] = None

    @validator('estado_reserva')
    def estado_reserva_valido(cls, v):
        estados_validos = {"pendiente", "confirmada", "cancelada"}
        if v.strip().lower() not in estados_validos:
            raise ValueError(f"El estado de la reserva debe ser uno de {estados_validos}")
        return v.strip().lower()

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
    

class ReservaResponse(ReservaBase):
    id_reserva: uuid.UUID
    fecha_entrada: date
    fecha_salida: date
    estado_reserva: str
    numero_de_personas: int
    noches: int
    costo_total: float
    id_cliente: uuid.UUID
    id_habitacion: uuid.UUID
    id_usuario_crea: uuid.UUID
    id_usuario_edita: Optional[uuid.UUID] = None
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


class ReservaListResponse(BaseModel):
    """Esquema para lista de reservas"""
    reservas: List[ReservaResponse]

    class Config:
        orm_mode = True
        from_attributes = True