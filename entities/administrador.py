from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
class Administrador(Base):
    """
    Representa la entidad de administrador.
    """
    __tablename__ = "administrador"

    id_admin = Column(UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), primary_key=True, default=uuid.uuid4)

    usuario = relationship("Usuario", back_populates="administrador")

    def __repr__(self):
        return f"<Administrador(id={self.id_admin})>"

