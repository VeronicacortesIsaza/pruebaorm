from database.config import SessionLocal, create_tables
from crud.reserva_crud import ReservaCRUD
from crud.tipo_habitacion_crud import TipoHabitacionCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.habitacion_crud import HabitacionCRUD
from crud.servicios_adicioneles_crud import ServiciosAdicionalesCRUD
from entities.servicios_adicionales import Servicios_Adicionales
from entities.reserva_servicios import Reserva_Servicios
from entities.usuario import Usuario
from entities.reserva import Reserva
from entities.habitacion import Habitacion
import getpass
from typing import Optional
from datetime import date, timedelta

class SistemaGestion:
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
        """
        Muestra el menú principal para el usuario autenticado según su rol (Administrador o Cliente).
        Dependiendo del tipo de usuario, despliega las opciones correspondientes y gestiona la selección del usuario.
        Permite acceder a los submenús de gestión, perfil, reservas, y cerrar sesión. Valida la entrada del usuario y
        redirige a la funcionalidad seleccionada. Si el rol no es reconocido, muestra un mensaje de error.
        Returns:
            None
        """
        print("\n" + "=" * 50)
        print("    SISTEMA DE GESTIÓN DEL HOTEL")
        print("=" * 50)
        print(f"Usuario: {self.usuario_actual.nombre} {self.usuario_actual.apellidos}")
        print(f"Rol: {self.usuario_actual.tipo_usuario}")
        print("=" * 50)

        if self.usuario_actual.tipo_usuario == "Administrador":
            print("1. Gestión de Usuarios")
            print("2. Gestión de Habitaciones")
            print("3. Gestión de Reservas")
            print("4. Gestión de Servicios Adicionales")
            print("5. Mi Perfil")
            print("6 Cerrar Sesión")
            while True:
                opcion = input("Elige una opción (1-7): ")
                if opcion.isdigit():  
                    opcion = int(opcion)  
                    if 1 <= opcion <= 7:
                        print("Opción válida:", opcion) 
                        break  
                    else:
                        print("El número debe estar entre 1 y 4.")
                else:
                    print("Debes ingresar un número válido.")
            if opcion == 1:
                self.mostrar_menu_usuarios()
            elif opcion == 2:
                self.mostrar_menu_habitaciones()
            elif opcion == 3:
                self.mostrar_menu_reservas()
            elif opcion == 4:
                self.mostrar_menu_servicios()
            elif opcion == 5:
                self.mostrar_menu_perfil()
            elif opcion == 6:
                print("Cerrando sesión...")
                self.usuario_actual = None
                return
        elif self.usuario_actual.tipo_usuario == "Cliente":
            print("1. Reservar Habitación")
            print("2. Mostrar Mis Reservas")
            print("3. Cancelar Reserva")
            print("4. Mi Perfil")
            print("5. Cerrar Sesión")
            while True:
                opcion = input("Elige una opción (1-5): ")
                if opcion.isdigit():  
                    opcion = int(opcion)  
                    if 1 <= opcion <= 5:
                        print("Opción válida:", opcion) 
                        break  
                    else:
                        print("El número debe estar entre 1 y 4.")
                else:
                    print("Debes ingresar un número válido.")
            if opcion == 1:
                self.reservar_habitacion()
            elif opcion == 2:
                self.cancelar_reserva()
            elif opcion == 3:
                self.mostrar_reservas()
            elif opcion == 4:
                self.mostrar_menu_perfil()
            elif opcion == 5:
                print("Saliendo...")
                self.usuario_actual = None
                return
            else:
                print("Opción inválida.")
        else:
            print("ERROR: Rol no reconocido. Contacte al administrador.")
        print("=" * 50)
    
    
        if input("¿Deseas servicios adicionales? (s/n): ").lower() == "s":
            Reserva_Servicios()
            
    def reservar_habitacion(self):
        if not self.usuario_actual:
            print("Debes iniciar sesión como cliente para reservar.")
            return

        while True:
            noches = input("Número de noches: ")
            if noches.isdigit():
                noches = int(noches)
                if noches > 0:
                    break
                else:     
                    print("Debe ser mayor a cero.")
            else:
                print("Debes ingresar un número válido.")
        while True:
            numero_de_personas = input("Número de personas: ")
            if numero_de_personas.isdigit():
                numero_de_personas = int(numero_de_personas)
                if numero_de_personas > 0:
                    break
                else:
                    print("Debe ser mayor a cero.")
            else:
                print("Debes ingresar un número válido.")


        print("\nTipos de habitación:")
        print("1. Estándar ($200000/noche)")
        print("2. Suite ($300000/noche)")
        print("3. Premium ($450000/noche)")

        while True:
            tipo = input("Selecciona el tipo de habitación (1-3): ")
            if tipo.isdigit():
                tipo = int(tipo)
                if 1 <= tipo <= 3:
                    break
                print("Debes seleccionar entre 1 y 3.")
            else:
                print("Debes ingresar un número válido.")
        opciones_tipo = {
            1: "Estándar",
            2: "Suite",
            3: "Premium"
        }
        tipo = opciones_tipo[tipo]
        habitacion = self.db.query(Habitacion).filter_by(tipo=tipo, disponible=True).first()
        if not habitacion:
            print("No hay habitaciones disponibles de ese tipo.")
            return

        precio_noche = habitacion.precio
        total = precio_noche * noches
        fecha_entrada = date.today()
        fecha_salida = fecha_entrada + timedelta(days=noches)
        fecha_creacion = date.today()

        print(f"\nFecha entrada: {fecha_entrada}")
        print(f"Fecha salida: {fecha_salida}")
        print(f"Total: {noches} noches x ${precio_noche:,} = ${total:,}")

    
        while True:
            confirmar = input("¿Desea confirmar la reserva? (1. Sí / 2. No): ")
            if confirmar.isdigit():
                confirmar = int(confirmar)
                if confirmar in (1, 2):
                    break
                else:
                    print("Opción inválida. Debe ser 1 o 2.")
            else:
                print("Debes ingresar un número válido.")

        if confirmar == 2:
            print("Reserva cancelada")
            return
    
        reserva = Reserva(
            id_cliente=self.usuario_actual.id_usuario,
            id_habitacion=habitacion.id_habitacion,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            estado_reserva="Activa",
            numero_de_personas=numero_de_personas,
            noches=noches,
            costo_total=total,
            id_usuario_crea=self.usuario_actual.id_usuario,
            fecha_creacion=fecha_creacion
        )
        
        self.reserva_crud.crear_reserva(self.db, reserva)
        habitacion.disponible = False
        self.db.commit()

          

        print(f"\nReserva creada para {self.usuario_actual.nombre} {self.usuario_actual.apellidos}")
        print(f"Habitación {habitacion.numero} - Total: ${total:,}")
        print(f"Del {fecha_entrada} al {fecha_salida}")
        
    def cancelar_reserva(self):
        reservas = self.db.query(Reserva).filter_by(
            id_cliente=self.usuario_actual.id_usuario, estado_reserva="Activa"
        ).all()

        if not reservas:
            print("No tienes reservas activas.")
            return

        print("Tus reservas activas:")
        for i, reserva in enumerate(reservas, 1):
            habitacion = self.db.query(Habitacion).get(reserva.id_habitacion)
            print(f"{i}. Habitación {habitacion.numero} del {reserva.fecha_entrada} al {reserva.fecha_salida} - Total: ${reserva.costo_total:,.0f}")

        opcion = input("Selecciona el número de la reserva que deseas cancelar: ")
        try:
            opcion = int(opcion)
            if opcion < 1 or opcion > len(reservas):
                print("Opción inválida.")
                return
        except ValueError:
            print("Debes ingresar un número.")
            return

        reserva = reservas[opcion - 1]
        
        while True:
            confirmar = input("¿Desea confirmar la reserva? (1. Sí / 2. No): ")
            if confirmar.isdigit():
                confirmar = int(confirmar)
                if confirmar in (1, 2):
                    break
                else:
                    print("Opción inválida. Debe ser 1 o 2.")
            else:
                print("Debes ingresar un número válido.")
                
        if confirmar == 1:
            habitacion = self.db.query(Habitacion).get(reserva.id_habitacion)
            habitacion.disponible = True

            reserva.estado_reserva = "Cancelada"
            reserva.fecha_edicion = date.today()
            reserva.id_usuario_edita = self.usuario_actual.id_usuario

            self.db.commit()
            print("Reserva cancelada con éxito.")
        else:
            print("Cancelación abortada.")

    
    def mostrar_reservas(self):
        reservas = self.db.query(Reserva).filter_by(id_cliente=self.usuario_actual.id_usuario).all()
        if not reservas:
            print("No tienes reservas registradas.")
            return

        print("\nTus reservas:")
        for r in reservas:
            print(f"Habitación {r.habitacion.numero} - {r.noches} noches - Estado: {r.estado_reserva}")
            
    def reservar_servicios(self):
        reservas = self.db.query(Reserva).filter_by(id_cliente=self.usuario_actual.id_usuario).all()
        if not reservas:
            print("No tienes reservas activas.")
            return

        print("\nTus reservas activas:")
        for i, r in enumerate(reservas, start=1):
            print(f"{i}. Habitación {r.habitacion.numero} del {r.fecha_entrada} al {r.fecha_salida}")

        idx = int(input("Selecciona la reserva a la que agregar servicios: ")) - 1
        reserva_seleccionada = reservas[idx]

        servicios = self.db.query(Servicios_Adicionales).all()
        print("\nServicios disponibles:")
        for i, s in enumerate(servicios, start=1):
            print(f"{i}. {s.nombre} - ${s.precio}")

        seleccion = input("Selecciona los servicios separados por coma (ej: 1,3): ")
        seleccion_indices = [int(x.strip())-1 for x in seleccion.split(",")]

        for i in seleccion_indices:
            servicio = servicios[i]
            cantidad = int(input(f"Ingrese la cantidad para {servicio.nombre}: "))
            subtotal = servicio.precio * cantidad

        reserva_servicio = Reserva_Servicios(
            id_reserva=reserva_seleccionada.id_reserva,
            id_servicio=servicio.id_servicio,
            cantidad=cantidad,
            subtotal=subtotal
        )
        self.db.add(reserva_servicio)
        reserva_seleccionada.costo_total += subtotal

        self.db.commit()
        print("Servicios agregados correctamente a tu reserva.")

    def ejecutar(self) -> None:
        """Ejecutar el sistema principal con autenticación"""
        try:
            print("Iniciando Sistema de Gestión del Hotel...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")

            if not self.mostrar_pantalla_login():
                print("Acceso denegado. ¡Hasta luego!")
                return

            while True:
                self.mostrar_menu_principal_autenticado()
        except KeyboardInterrupt:
            print("\n\nSistema interrumpido por el usuario.")
        except Exception as e:
            print(f"\nError crítico: {e}")
        finally:
            self.db.close()

    def mostrar_menu_habitaciones(self) -> None:
        print("\n--- GESTIÓN DE HABITACIONES ---")
        print("1. Agregar habitación")
        print("2. Listar habitaciones")
        print("3. Actualizar habitación")
        print("4. Eliminar habitación")
        print("5. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-5): ")
            if opcion.isdigit():  
                opcion = int(opcion)  
                if 1 <= opcion <= 5:
                    print("Opción válida:", opcion)                         
                    break  
                else:
                    print("El número debe estar entre 1 y 4.")
            else:
                print("Debes ingresar un número válido.")
        if opcion == 1:
            self.agregar_habitacion()
        elif opcion == 2:                
            self.listar_habitaciones()
        elif opcion == 3:
            self.actualizar_habitacion()
        elif opcion == 4:
            self.eliminar_habitacion()
        elif opcion == 5:
            print("Saliendo...")
            self.usuario_actual = None
            return      

    def mostrar_menu_reservas(self) -> None:
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("1. Listar reservas")
        print("2. Consultar reservas activas")
        print("3. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-5): ")
            if opcion.isdigit():  
                opcion = int(opcion)  
                if 1 <= opcion <= 5:
                    print("Opción válida:", opcion)                         
                    break  
                else:
                    print("El número debe estar entre 1 y 4.")
            else:
                print("Debes ingresar un número válido.")
        if opcion == 1:
            self.listar_reservas()
        elif opcion == 2:                
            self.listar_reservas_activas()
        elif opcion == 3:
            print("Saliendo...")
            self.usuario_actual = None
            return      



    def mostrar_menu_servicios(self) -> None:
        print("\n--- GESTIÓN DE SERVICIOS ADICIONALES ---")
        print("1. Agregar servicio")
        print("2. Listar servicios")
        print("3. Actualizar servicio")
        print("4. Eliminar servicio")
        print("5. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-5): ")
            if opcion.isdigit():  
                opcion = int(opcion)  
                if 1 <= opcion <= 5:
                    print("Opción válida:", opcion)                         
                    break  
                else:
                    print("El número debe estar entre 1 y 4.")
            else:
                print("Debes ingresar un número válido.")
        if opcion == 1:
            self.reservar_habitacion()
        elif opcion == 2:                
            self.cancelar_reserva()
        elif opcion == 3:
            self.mostrar_reservas()
        elif opcion == 4:
            self.mostrar_menu_perfil()
        elif opcion == 5:
            print("Saliendo...")
            self.usuario_actual = None
            return      

    
    def mostrar_menu_usuarios(self) -> None:
        print("\n--- CONSULTAS Y REPORTES ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Editar usuario")
        print("4. Eliminar usuario")
        print("5. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-5): ")
            if opcion.isdigit():  
                opcion = int(opcion)  
                if 1 <= opcion <= 5:
                    print("Opción válida:", opcion)                         
                    break  
                else:
                    print("El número debe estar entre 1 y 5.")
            else:
                print("Debes ingresar un número válido.")
        if opcion == 1:
            self.reservar_habitacion()
        elif opcion == 2:                
            self.cancelar_reserva()
        elif opcion == 3:
            self.mostrar_reservas()
        elif opcion == 4:
            self.mostrar_menu_perfil()
        elif opcion == 5:
            print("Saliendo...")
            self.usuario_actual = None
            return      


    
    def mostrar_menu_perfil(self):
        print("\n--- MI PERFIL ---")
        print(f"Nombre: {self.usuario_actual.nombre} {self.usuario_actual.apellidos}")
        print(f"Usuario: {self.usuario_actual.telefono}")
        print(f"Rol: {self.usuario_actual.tipo_usuario}")
        
    def agregar_habitacion(self):
        try:
            numero = input("Número de la habitación: ")
            tipo = input("Tipo de habitación (Sencilla/Doble/Suite): ")
            precio = float(input("Precio por noche: "))

            nueva_habitacion = Habitacion(
                numero=numero,
                tipo=tipo,
                precio=precio,
                disponible=True
            )
            self.habitacion_crud.crear_habitacion(nueva_habitacion)
            print("Habitación agregada exitosamente.")
        except Exception as e:
            print(f"Error al agregar habitación: {e}")


    def listar_habitaciones(self):
        try:
            habitaciones = self.habitacion_crud.obtener_todas()
            if not habitaciones:
                print("No hay habitaciones registradas.")
            else:
                for h in habitaciones:
                    estado = "Disponible" if h.disponible else "Ocupada"
                    print(f"Nº {h.numero} | {h.tipo} | ${h.precio} | {estado}")
        except Exception as e:
            print(f"Error al listar habitaciones: {e}")


    def actualizar_habitacion(self):
        try:
            habitacion_id = input("ID de la habitación a actualizar: ")
            habitacion = self.habitacion_crud.obtener_por_id(habitacion_id)

            if not habitacion:
                print("Habitación no encontrada.")
                return

            nuevo_precio = float(input(f"Nuevo precio (actual: {habitacion.precio}): "))
            habitacion.precio = nuevo_precio
            self.habitacion_crud.actualizar_habitacion(habitacion)
            print("Habitación actualizada correctamente.")
        except Exception as e:
            print(f"Error al actualizar habitación: {e}")


    def eliminar_habitacion(self):
        try:
            habitacion_id = input("ID de la habitación a eliminar: ")
            self.habitacion_crud.eliminar_habitacion(habitacion_id)
            print("Habitación eliminada correctamente.")
        except Exception as e:
            print(f"Error al eliminar habitación: {e}")
    
    def listar_reservas(self):
        try:
            reservas = self.reserva_crud.obtener_reservas()
            if not reservas:
                print("No hay habitaciones registradas.")
            else:
                for h in reservas:
                    estado = "Activa" if h.estado_reserva else "Cancelada"
                    print(f"Nº {estado} | {h.fecha_entrada} | {h.fecha_salida} | {h.costo_total} | {h.numero_personas} | {h.noches} ")
        except Exception as e:
            print(f"Error al listar habitaciones: {e}")
            
    def listar_reservas_activas(self):
        try:
            reservas = self.reserva_crud.obtener_reservas_activas()
            if not reservas:
                print("No hay reservas activas.")
            else:
                for r in reservas:
                    print(f"Reserva {r.id_reserva} | Cliente: {r.id_cliente} | Habitación: {r.id_habitacion} | {r.fecha_entrada} → {r.fecha_salida} | Estado: {r.estado_reserva}")
        except Exception as e:
            print(f"Error al obtener reservas activas: {e}")



def main():
    """Función principal"""
    with SistemaGestion() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()
