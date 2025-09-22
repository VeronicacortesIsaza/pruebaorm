from sqlalchemy.orm import Session
from entities.usuario import Usuario
from sqlalchemy.dialects.postgresql import UUID
class UsuarioCRUD:
    """
    Módulo CRUD para la entidad Usuario.

    Administra la creación, consulta, actualización, eliminación y autenticación
    de los usuarios que acceden al sistema.

    Funciones principales:
        - crear_usuario(db: Session, nuevo_usuario: Usuario) -> Usuario
        - obtener_usuario(db: Session, id_usuario: UUID) -> Usuario
        - obtener_usuario_por_nombre(db: Session, nombre_usuario: str) -> Usuario
        - obtener_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]
        - actualizar_usuario(db: Session, id_usuario: UUID, id_usuario_edita: UUID, **kwargs) -> Usuario
        - eliminar_usuario(db: Session, id_usuario: UUID) -> bool
        - autenticar_usuario(self, nombre_usuario: str, contrasena: str) -> Optional[Usuario]

    Notas:
        - Valida que el nombre de usuario sea único y no exceda 50 caracteres.
        - La contraseña no debe exceder 10 caracteres.
    """
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_usuario(db: Session, nuevo_usuario: Usuario):
        existente = (
            db.query(Usuario).filter(Usuario.nombre_usuario == nuevo_usuario.nombre_usuario).first()
        )
        if existente:
            raise ValueError(f"El nombre de usuario '{Usuario.nombre_usuario}' ya está en uso.")

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def obtener_usuario(db: Session, id_usuario: UUID):
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    @staticmethod
    def obtener_usuario_por_nombre(db: Session, nombre_usuario: str):
        return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario.strip()).first()

    @staticmethod
    def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Usuario).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar_usuario(db: Session, id_usuario: UUID, id_usuario_edita: UUID = None, **kwargs):
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            return None

        if "nombre_usuario" in kwargs:
            nuevo_nombre = kwargs["nombre_usuario"].strip()
            if len(nuevo_nombre) > 50:
                raise ValueError("El nombre de usuario no puede exceder 50 caracteres")
            existente = db.query(Usuario).filter(Usuario.nombre_usuario == nuevo_nombre).first()
            if existente and existente.id_usuario != id_usuario:
                raise ValueError("Ya existe un usuario con ese nombre")
            kwargs["nombre_usuario"] = nuevo_nombre

        if "clave" in kwargs and len(kwargs["clave"]) > 10:
            raise ValueError(status_code=400, detail="La clave no puede exceder 10 caracteres")

        usuario.id_usuario_edita = id_usuario_edita
        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)

        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def eliminar_usuario(db: Session, id_usuario: UUID) -> bool:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return True
        return False

    def autenticar_usuario(self, nombre_usuario: str, contrasena: str):
        """
        Autenticar un usuario usando nombre de usuario o email y contraseña en texto plano.
        """
        usuario = (
            self.db.query(Usuario)
            .filter(
                (Usuario.nombre_usuario == nombre_usuario)
                | (Usuario.nombre_usuario == nombre_usuario)
            )
            .first()
        )

        if usuario and usuario.clave == contrasena:
            return usuario
        return None