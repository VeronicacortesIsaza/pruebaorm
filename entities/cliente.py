from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Cliente(Base):
    """
    Representa la entidad Cliente.
    """
    __tablename__ = "cliente"

    id_cliente = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), primary_key=True, default=uuid.uuid4)

    usuario = relationship("Usuario", back_populates="cliente", uselist=False)
    reservas = relationship("Reserva", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id={self.id_cliente})>"
    