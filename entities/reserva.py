from sqlalchemy import UUID, Column, Integer, String, Float, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from database.config import Base
import uuid

class Reserva(Base):
    """""
    Representa la entidad de reserva.
    """
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
    
    usuario_crea = relationship(
        "Usuario",
        foreign_keys=[id_usuario_crea],
        overlaps="usuario_edita"   
    )

    usuario_edita = relationship(
        "Usuario",
        foreign_keys=[id_usuario_edita],
        overlaps="usuario_crea"
    )
    def __repr__(self):
        return (f"<Reserva(id={self.id_reserva}, cliente={self.id_cliente}, "
            f"habitacion={self.id_habitacion}, estado={self.estado_reserva}, "
            f"noches={self.noches}, costo_total={self.costo_total})>")

