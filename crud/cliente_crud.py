from sqlalchemy.orm import Session
from entities.cliente import Cliente

class ClienteCRUD:
    @staticmethod
    def crear_cliente(db: Session, cliente: Cliente):
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def obtener_cliente(db: Session, id_cliente: int):
        return db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()

    @staticmethod
    def actualizar_cliente(db: Session, cliente: Cliente):
        db.merge(cliente)
        db.commit()
        return cliente

    @staticmethod
    def eliminar_cliente(db: Session, id_cliente: int):
        cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        if cliente:
            db.delete(cliente)
            db.commit()
        return cliente
