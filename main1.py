"""
Sistema de gestion de productos con ORM SQLAlchemy y Neon PostgreSQL
Incluye sistema de autenticacion con login
"""

import getpass
from typing import Optional
from crud.habitacion_crud import HabitacionCRUD
from crud.reserva_crud import ReservaCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.servicios_adicioneles_crud import ServiciosAdicionalesCRUD
from database.config import SessionLocal, create_tables
from entities.reserva import Reserva
from entities.tipo_habitacion import Tipo_Habitacion
from entities.usuario import Usuario
from entities.habitacion import Habitacion
from entities.reserva_servicios import Reserva_Servicios
from entities.administrador import Administrador
from entities.cliente import Cliente
from entities.servicios_adicionales import Servicios_Adicionales


class SistemaGestion:
    """Sistema principal de gestion con interfaz de consola y autenticacion"""

    def __init__(self):
        """Inicializar el sistema"""
        self.db = SessionLocal()
        self.usuario_crud = UsuarioCRUD(self.db)
        self.habitacion_crud = HabitacionCRUD(self.db)
        self.reserva_crud = ReservaCRUD(self.db)
        self.servicios_adicioneles_crud = ServiciosAdicionalesCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.db.close()

    def mostrar_pantalla_login(self) -> bool:
        """Mostrar pantalla de login y autenticar usuario"""
        print("\n" + "=" * 50)
        print("        SISTEMA DE GESTION DE PRODUCTOS")
        print("=" * 50)
        print("INICIAR SESION")
        print("=" * 50)

        intentos = 0
        max_intentos = 3

        while intentos < max_intentos:
            try:
                print(f"\nIntento {intentos + 1} de {max_intentos}")
                nombre_usuario = input("Nombre de usuario o email: ").strip()

                if not nombre_usuario:
                    print("ERROR: El nombre de usuario es obligatorio")
                    intentos += 1
                    continue

                contrasena = getpass.getpass("Contrasena: ")

                if not contrasena:
                    print("ERROR: La contrasena es obligatoria")
                    intentos += 1
                    continue

                usuario = self.usuario_crud.autenticar_usuario(
                    nombre_usuario, contrasena
                )

                if usuario:
                    self.usuario_actual = usuario
                    print(f"\nEXITO: ¡Bienvenido, {usuario.nombre}!")
                    if usuario.es_admin:
                        print("INFO: Tienes privilegios de administrador")
                    return True
                else:
                    print("ERROR: Credenciales incorrectas o usuario inactivo")
                    intentos += 1

            except KeyboardInterrupt:
                print("\n\nINFO: Operacion cancelada por el usuario")
                return False
            except Exception as e:
                print(f"ERROR: Error durante el login: {e}")
                intentos += 1

        print(
            f"\nERROR: Maximo de intentos ({max_intentos}) excedido. Acceso denegado."
        )
        return False

    def mostrar_menu_principal_autenticado(self) -> None:
        """Mostrar el menu principal para usuario autenticado"""
        print("\n" + "=" * 50)
        print("    SISTEMA DE GESTION DE PRODUCTOS")
        print("=" * 50)
        print(f"Usuario: {self.usuario_actual.nombre}")
        print(f"Email: {self.usuario_actual.email}")
        if self.usuario_actual.es_admin:
            print("Administrador")
        print("=" * 50)
        print("1. Gestion de Usuarios")
        print("2. Gestion de Categorias")
        print("3. Gestion de Productos")
        print("4. Consultas y Reportes")
        print("5. Configuracion del Sistema")
        print("6. Mi Perfil")
        print("0. Cerrar Sesion")
        print("=" * 50)

    def mostrar_menu_perfil(self) -> None:
        """Mostrar menu de perfil del usuario"""
        while True:
            print("\n" + "-" * 30)
            print("   MI PERFIL")
            print("-" * 30)
            print("1. Ver Informacion Personal")
            print("2. Actualizar Informacion")
            print("3. Cambiar Contrasena")
            print("0. Volver al menu principal")

            opcion = input("\nSeleccione una opcion: ").strip()

            if opcion == "1":
                self.ver_informacion_personal()
            elif opcion == "2":
                self.actualizar_informacion_personal()
            elif opcion == "3":
                self.cambiar_contrasena()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opcion invalida. Intente nuevamente.")

    def ver_informacion_personal(self) -> None:
        """Ver informacion personal del usuario"""
        try:
            print(f"\n--- INFORMACION PERSONAL ---")
            print(f"Nombre: {self.usuario_actual.nombre}")
            print(f"Nombre de usuario: {self.usuario_actual.nombre_usuario}")
            print(f"Email: {self.usuario_actual.email}")
            print(f"Telefono: {self.usuario_actual.telefono or 'No especificado'}")
            print(f"Estado: {'Activo' if self.usuario_actual.activo else 'Inactivo'}")
            print(
                f"Rol: {'Administrador' if self.usuario_actual.es_admin else 'Usuario'}"
            )
            print(f"Fecha de creacion: {self.usuario_actual.fecha_creacion}")

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def actualizar_informacion_personal(self) -> None:
        """Actualizar informacion personal del usuario"""
        try:
            print(f"\n--- ACTUALIZAR INFORMACION PERSONAL ---")
            print("Deje en blanco para mantener el valor actual")

            nuevo_nombre = input(
                f"Nombre actual ({self.usuario_actual.nombre}): "
            ).strip()
            nuevo_nombre_usuario = input(
                f"Nombre de usuario actual ({self.usuario_actual.nombre_usuario}): "
            ).strip()
            nuevo_email = input(f"Email actual ({self.usuario_actual.email}): ").strip()
            nuevo_telefono = input(
                f"Telefono actual ({self.usuario_actual.telefono or 'No especificado'}): "
            ).strip()

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_nombre_usuario:
                cambios["nombre_usuario"] = nuevo_nombre_usuario
            if nuevo_email:
                cambios["email"] = nuevo_email
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono

            if cambios:
                usuario_actualizado = self.usuario_crud.actualizar_usuario(
                    self.usuario_actual.id, **cambios
                )
                if usuario_actualizado:
                    self.usuario_actual = usuario_actualizado
                    print(f"EXITO: Informacion actualizada exitosamente")
                else:
                    print("ERROR: Error al actualizar la informacion")
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def cambiar_contrasena(self) -> None:
        """Cambiar contrasena del usuario"""
        try:
            print(f"\n--- CAMBIAR CONTRASENA ---")

            contrasena_actual = getpass.getpass("Contrasena actual: ")
            if not contrasena_actual:
                print("ERROR: La contrasena actual es obligatoria")
                return

            nueva_contrasena = getpass.getpass("Nueva contrasena: ")
            if not nueva_contrasena:
                print("ERROR: La nueva contrasena es obligatoria")
                return

            confirmar_contrasena = getpass.getpass("Confirmar nueva contrasena: ")
            if nueva_contrasena != confirmar_contrasena:
                print("ERROR: Las contrasenas no coinciden")
                return

            if self.usuario_crud.cambiar_contrasena(
                self.usuario_actual.id, contrasena_actual, nueva_contrasena
            ):
                print("EXITO: Contrasena cambiada exitosamente")
            else:
                print("ERROR: Error al cambiar la contrasena")

        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def mostrar_menu_usuarios(self) -> None:
        """Mostrar menu de gestion de usuarios"""
        while True:
            print("\n" + "-" * 30)
            print("   GESTION DE USUARIOS")
            print("-" * 30)
            print("1. Crear Usuario")
            print("2. Listar Usuarios")
            print("3. Buscar Usuario por Email")
            print("4. Buscar Usuario por Nombre de Usuario")
            print("5. Actualizar Usuario")
            print("6. Eliminar Usuario")
            print("7. Crear Usuario Administrador")
            print("0. Volver al menu principal")

            opcion = input("\nSeleccione una opcion: ").strip()

            if opcion == "1":
                self.crear_usuario()
            elif opcion == "2":
                self.listar_usuarios()
            elif opcion == "3":
                self.buscar_usuario_por_email()
            elif opcion == "4":
                self.buscar_usuario_por_nombre_usuario()
            elif opcion == "5":
                self.actualizar_usuario()
            elif opcion == "6":
                self.eliminar_usuario()
            elif opcion == "7":
                self.crear_usuario_admin()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opcion invalida. Intente nuevamente.")

    def crear_usuario(self) -> None:
        """Crear un nuevo usuario"""
        try:
            print("\n--- CREAR USUARIO ---")
            nombre = input("Nombre completo: ").strip()
            nombre_usuario = input("Nombre de usuario: ").strip()
            email = input("Email: ").strip()
            contrasena = getpass.getpass("Contrasena: ")
            telefono = input("Telefono (opcional): ").strip() or None
            es_admin = input("¿Es administrador? (s/n): ").strip().lower() == "s"

            usuario = self.usuario_crud.crear_usuario(
                nombre=nombre,
                nombre_usuario=nombre_usuario,
                email=email,
                contrasena=contrasena,
                telefono=telefono,
                es_admin=es_admin,
            )

            print(f"EXITO: Usuario creado exitosamente: {usuario}")

        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def listar_usuarios(self) -> None:
        """Listar todos los usuarios"""
        try:
            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("INFO: No hay usuarios registrados.")
                return

            print(f"\n--- USUARIOS ({len(usuarios)}) ---")
            for i, usuario in enumerate(usuarios, 1):
                admin_text = " (ADMIN)" if usuario.es_admin else ""
                activo_text = "Activo" if usuario.activo else "Inactivo"
                print(
                    f"{i}. {usuario.nombre} ({usuario.nombre_usuario}) - {usuario.email} - {activo_text}{admin_text}"
                )

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def buscar_usuario_por_email(self) -> None:
        """Buscar usuario por email"""
        try:
            email = input("\nIngrese el email a buscar: ").strip()
            usuario = self.usuario_crud.obtener_usuario_por_email(email)

            if usuario:
                admin_text = " (ADMIN)" if usuario.es_admin else ""
                activo_text = "Activo" if usuario.activo else "Inactivo"
                print(f"EXITO: Usuario encontrado:")
                print(f"   Nombre: {usuario.nombre}")
                print(f"   Nombre de usuario: {usuario.nombre_usuario}")
                print(f"   Email: {usuario.email}")
                print(f"   Telefono: {usuario.telefono or 'No especificado'}")
                print(f"   Estado: {activo_text}{admin_text}")
            else:
                print("ERROR: Usuario no encontrado.")

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def buscar_usuario_por_nombre_usuario(self) -> None:
        """Buscar usuario por nombre de usuario"""
        try:
            nombre_usuario = input("\nIngrese el nombre de usuario a buscar: ").strip()
            usuario = self.usuario_crud.obtener_usuario_por_nombre_usuario(
                nombre_usuario
            )

            if usuario:
                admin_text = " (ADMIN)" if usuario.es_admin else ""
                activo_text = "Activo" if usuario.activo else "Inactivo"
                print(f"EXITO: Usuario encontrado:")
                print(f"   Nombre: {usuario.nombre}")
                print(f"   Nombre de usuario: {usuario.nombre_usuario}")
                print(f"   Email: {usuario.email}")
                print(f"   Telefono: {usuario.telefono or 'No especificado'}")
                print(f"   Estado: {activo_text}{admin_text}")
            else:
                print("ERROR: Usuario no encontrado.")

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def actualizar_usuario(self) -> None:
        """Actualizar un usuario"""
        try:
            email = input("\nIngrese el email del usuario a actualizar: ").strip()
            usuario = self.usuario_crud.obtener_usuario_por_email(email)

            if not usuario:
                print("ERROR: Usuario no encontrado.")
                return

            print(f"\nActualizando usuario: {usuario.nombre}")
            print("Deje en blanco para mantener el valor actual")

            nuevo_nombre = input(f"Nombre actual ({usuario.nombre}): ").strip()
            nuevo_nombre_usuario = input(
                f"Nombre de usuario actual ({usuario.nombre_usuario}): "
            ).strip()
            nuevo_email = input(f"Email actual ({usuario.email}): ").strip()
            nuevo_telefono = input(
                f"Telefono actual ({usuario.telefono or 'No especificado'}): "
            ).strip()

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_nombre_usuario:
                cambios["nombre_usuario"] = nuevo_nombre_usuario
            if nuevo_email:
                cambios["email"] = nuevo_email
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono

            if cambios:
                usuario_actualizado = self.usuario_crud.actualizar_usuario(
                    usuario.id, **cambios
                )
                print(f"EXITO: Usuario actualizado: {usuario_actualizado}")
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def eliminar_usuario(self) -> None:
        """Eliminar un usuario"""
        try:
            email = input("\nIngrese el email del usuario a eliminar: ").strip()
            usuario = self.usuario_crud.obtener_usuario_por_email(email)

            if not usuario:
                print("ERROR: Usuario no encontrado.")
                return

            confirmacion = (
                input(f"¿Esta seguro de eliminar a {usuario.nombre}? (s/n): ")
                .strip()
                .lower()
            )
            if confirmacion == "s":
                if self.usuario_crud.eliminar_usuario(usuario.id):
                    print("EXITO: Usuario eliminado exitosamente.")
                else:
                    print("ERROR: Error al eliminar el usuario.")
            else:
                print("INFO: Operacion cancelada.")

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def crear_usuario_admin(self) -> None:
        """Crear usuario administrador por defecto"""
        try:
            admin = self.usuario_crud.obtener_admin_por_defecto()
            if admin:
                print("INFO: Ya existe un usuario administrador por defecto.")
                return

            admin = self.usuario_crud.crear_usuario(
                nombre="Administrador del Sistema",
                nombre_usuario="admin",
                email="admin@system.com",
                contrasena=contrasena_admin,
                es_admin=True,
            )
            print(f"EXITO: Usuario administrador creado: {admin}")
            print(f"INFO: Contrasena temporal: {contrasena_admin}")
            print(
                "ADVERTENCIA:  IMPORTANTE: Cambie esta contrasena en su primer inicio de sesion"
            )

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def ejecutar(self) -> None:
        """Ejecutar el sistema principal con autenticacion"""
        try:
            print("Iniciando Sistema de Gestion de Productos...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")

            # Autenticacion requerida
            if not self.mostrar_pantalla_login():
                print("Acceso denegado. Hasta luego!")
                return

            # Menu principal autenticado
            while True:
                self.mostrar_menu_principal_autenticado()
                opcion = input("\nSeleccione una opcion: ").strip()

                if opcion == "1":
                    self.mostrar_menu_usuarios()
                elif opcion == "2":
                    self.mostrar_menu_categorias()
                elif opcion == "3":
                    self.mostrar_menu_productos()
                elif opcion == "4":
                    self.mostrar_menu_consultas()
                elif opcion == "5":
                    self.configurar_sistema()
                elif opcion == "6":
                    self.mostrar_menu_perfil()
                elif opcion == "0":
                    print("\n¡Hasta luego!")
                    break
                else:
                    print("ERROR: Opcion invalida. Intente nuevamente.")

        except KeyboardInterrupt:
            print("\n\nSistema interrumpido por el usuario.")
        except Exception as e:
            print(f"\nError critico: {e}")
        finally:
            self.db.close()

    # Metodos de categorias, productos y consultas (simplificados para el ejemplo)
    def mostrar_menu_categorias(self) -> None:
        print("\n--- GESTION DE CATEGORIAS ---")
        print("Funcionalidad de categorias (implementar segun necesidad)")

    def mostrar_menu_productos(self) -> None:
        print("\n--- GESTION DE PRODUCTOS ---")
        print("Funcionalidad de productos (implementar segun necesidad)")

    def mostrar_menu_consultas(self) -> None:
        print("\n--- CONSULTAS Y REPORTES ---")
        print("Funcionalidad de consultas (implementar segun necesidad)")

    def configurar_sistema(self) -> None:
        print("\n--- CONFIGURACION DEL SISTEMA ---")
        print("Funcionalidad de configuracion (implementar segun necesidad)")


def main():
    """Funcion principal"""
    with SistemaGestion() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()