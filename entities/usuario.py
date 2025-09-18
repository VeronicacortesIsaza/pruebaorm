from sqlalchemy import String, Column, DateTime, func, ForeignKey
from database.config import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Usuario(Base):
    """
    Representa la entidad usuario
    """    
    __tablename__ = "usuario"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    tipo_usuario = Column(String(20), nullable=False) 
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    clave = Column(String(10), nullable=False)  
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    administrador = relationship("Administrador", back_populates="usuario", uselist=False)

    cliente = relationship("Cliente", back_populates="usuario", uselist=False)

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nombre_usuario={self.nombre_usuario}, tipo={self.tipo_usuario})>"


