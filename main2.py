from database.config import SessionLocal, create_tables
from crud.reserva_crud import ReservaCRUD
from crud.tipo_habitacion_crud import TipoHabitacionCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.habitacion_crud import HabitacionCRUD
from crud.servicios_adicioneles_crud import ServiciosAdicionalesCRUD
from entities.servicios_adicionales import Servicios_Adicionales
from entities.usuario import Usuario
import getpass
from typing import Optional



class SistemaGestion:
    """Sistema principal de gestión de hotel con interfaz de consola y autenticación"""

    def __init__(self):
        """Inicializar el sistema"""
        self.db = SessionLocal()
        self.usuario_crud = UsuarioCRUD(self.db)
        self.habitacion_crud = HabitacionCRUD(self.db)
        self.reserva_crud = ReservaCRUD(self.db)
        self.servicios_adicionales_crud = ServiciosAdicionalesCRUD(self.db)
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
        print("        SISTEMA DE GESTIÓN DEL HOTEL")
        print("=" * 50)
        print("INICIAR SESIÓN")
        print("=" * 50)

        intentos = 0
        max_intentos = 3

        while intentos < max_intentos:
            try:
                print(f"\nIntento {intentos + 1} de {max_intentos}")
                nombre_usuario = input("Nombre de usuario: ").strip()

                if not nombre_usuario:
                    print("ERROR: El nombre de usuario es obligatorio")
                    intentos += 1
                    continue

                contrasena = getpass.getpass("Contraseña: ")

                if not contrasena:
                    print("ERROR: La contraseña es obligatoria")
                    intentos += 1
                    continue

                usuario = self.usuario_crud.autenticar_usuario(
                    nombre_usuario, contrasena
                )

                if usuario:
                    self.usuario_actual = usuario
                    print(f"\nÉXITO: ¡Bienvenido, {usuario.nombre}!")
                    if usuario.tipo_usuario == "Administrador":
                        print("INFO: Tienes privilegios de administrador")
                    return True
                else:
                    print("ERROR: Credenciales incorrectas o usuario inactivo")
                    intentos += 1

            except KeyboardInterrupt:
                print("\n\nINFO: Operación cancelada por el usuario")
                return False
            except Exception as e:
                print(f"ERROR: Error durante el login: {e}")
                intentos += 1

        print(
            f"\nERROR: Máximo de intentos ({max_intentos}) excedido. Acceso denegado."
        )
        return False

    def mostrar_menu_principal_autenticado(self) -> None:
        """Mostrar el menú principal para usuario autenticado"""
        print("\n" + "=" * 50)
        print("    SISTEMA DE GESTIÓN DEL HOTEL")
        print("=" * 50)
        print(f"Usuario: {self.usuario_actual.nombre}")
        print(f"Email: {self.usuario_actual.apellidos}")
        if self.usuario_actual.tipo_usuario == "Administrador":
            print("Administrador")
            print("=" * 50)
            print("1. Gestión de Usuarios")
            print("2. Gestión de Habitaciones")
            print("3. Gestión de Reservas")
            print("4. Gestión de Servicios Adicionales")
            print("5. Consultas y Reportes")
            print("6. Mi Perfil")
            print("0. Cerrar Sesión")
            print("=" * 50)

    def ejecutar(self) -> None:
        """Ejecutar el sistema principal con autenticación"""
        try:
            print("Iniciando Sistema de Gestión del Hotel...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")

            # Autenticación requerida
            if not self.mostrar_pantalla_login():
                print("Acceso denegado. ¡Hasta luego!")
                return

            # Menú principal autenticado
            while True:
                self.mostrar_menu_principal_autenticado()
                opcion = input("\nSeleccione una opción: ").strip()

                if opcion == "1":
                    self.mostrar_menu_usuarios()
                elif opcion == "2":
                    self.mostrar_menu_habitaciones()
                elif opcion == "3":
                    self.mostrar_menu_reservas()
                elif opcion == "4":
                    self.mostrar_menu_servicios()
                elif opcion == "5":
                    self.mostrar_menu_consultas()
                elif opcion == "6":
                    self.mostrar_menu_perfil()
                elif opcion == "0":
                    print("\n¡Hasta luego!")
                    break
                else:
                    print("ERROR: Opción inválida. Intente nuevamente.")

        except KeyboardInterrupt:
            print("\n\nSistema interrumpido por el usuario.")
        except Exception as e:
            print(f"\nError crítico: {e}")
        finally:
            self.db.close()

    # Métodos de habitaciones, reservas, servicios y consultas
    def mostrar_menu_habitaciones(self) -> None:
        print("\n--- GESTIÓN DE HABITACIONES ---")
        print("Funcionalidad de habitaciones (implementar CRUD según necesidad)")

    def mostrar_menu_reservas(self) -> None:
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("Funcionalidad de reservas (implementar CRUD según necesidad)")

    def mostrar_menu_servicios(self) -> None:
        print("\n--- GESTIÓN DE SERVICIOS ADICIONALES ---")
        print("Funcionalidad de servicios adicionales (implementar CRUD según necesidad)")

    def mostrar_menu_consultas(self) -> None:
        print("\n--- CONSULTAS Y REPORTES ---")
        print("Funcionalidad de consultas (implementar según necesidad)")


def main():
    """Función principal"""
    with SistemaGestion() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()
