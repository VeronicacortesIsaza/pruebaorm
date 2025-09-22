from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.cliente import Cliente

class ClienteCRUD:
    """
    Módulo CRUD para la entidad Cliente.

    Proporciona operaciones para administrar los clientes del hotel.
    Cada cliente debe estar asociado a un usuario existente.

    Funciones principales:
        - crear_cliente(db: Session, cliente: Cliente) -> Cliente
        - obtener_cliente(db: Session, id_cliente: UUID) -> Cliente
        - obtener_clientes(db: Session, skip: int = 0, limit: int = 100) -> List[Cliente]
        - eliminar_cliente(db: Session, id_cliente: UUID) -> bool
    """
    def __init__(self, db):
        self.db = db
        
    @staticmethod
    def crear_cliente(db: Session, cliente: Cliente):
        if not cliente.id_cliente:
            raise ValueError("El cliente debe estar asociado a un usuario")
        
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def obtener_cliente(db: Session, id_cliente: UUID):
        cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        if not cliente:
            raise ValueError("Cliente no encontrado")
        return cliente

    @staticmethod
    def obtener_clientes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Cliente).offset(skip).limit(limit).all()

    @staticmethod
    def eliminar_cliente(db: Session, id_cliente: UUID) -> bool:
        cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        if not cliente:
            raise ValueError("Cliente no encontrado")
        db.delete(cliente)
        db.commit()
        return True
