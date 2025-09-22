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
from datetime import date, timedelta, datetime
class SistemaGestion:
    def __init__(self):
        """Inicializar el sistema"""
        self.db = SessionLocal()
        self.usuario_crud = UsuarioCRUD(self.db)
        self.habitacion_crud = HabitacionCRUD(self.db)
        self.reserva_crud = ReservaCRUD(self.db)
        self.servicios_adicionales_crud = ServiciosAdicionalesCRUD(self.db)
        self.tipo_habitacion_crud = TipoHabitacionCRUD(self.db)
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
        Muestra el menú principal según el tipo de usuario autenticado (Administrador o Cliente).
        - Si el usuario es Administrador, presenta opciones para gestionar usuarios, habitaciones, reservas, servicios adicionales, ver y actualizar perfil, y cerrar sesión.
        - Si el usuario es Cliente, presenta opciones para reservar habitación, ver y cancelar reservas, ver y actualizar perfil, y cerrar sesión.
        - Valida la opción ingresada por el usuario y llama al método correspondiente según la selección.
        - Si el usuario no está autenticado, no muestra el menú.
        - Si el rol del usuario no es reconocido, muestra un mensaje de error.
        Returns:
            None
        """
        if not self.usuario_actual:
            return
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
            print("6. Actualizar perfil")
            print("7 Cerrar Sesión")
            while True:
                opcion = input("Elige una opción (1-7): ")
                if opcion.isdigit():  
                    opcion = int(opcion)  
                    if 1 <= opcion <= 7:
                        print("Opción válida:", opcion) 
                        break  
                    else:
                        print("El número debe estar entre 1 y 7.")
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
                self.mostrar_perfil()
            elif opcion == 6:
                self.actualizar_perfil()
            elif opcion == 7:
                print("\n¡Hasta luego!")
                self.usuario_actual = None  
                return
        elif self.usuario_actual.tipo_usuario == "Cliente":
            print("1. Reservar Habitación")
            print("2. Mostrar Mis Reservas")
            print("3. Cancelar Reserva")
            print("4. Mi Perfil")
            print("5. Actualizar perfil")
            print("6. Cerrar Sesión")
            while True:
                opcion = input("Elige una opción (1-6): ")
                if opcion.isdigit():  
                    opcion = int(opcion)  
                    if 1 <= opcion <= 6:
                        print("Opción válida:", opcion) 
                        break  
                    else:
                        print("El número debe estar entre 1 y 6.")
                else:
                    print("Debes ingresar un número válido.")
            if opcion == 1:
                self.reservar_habitacion()
            elif opcion == 2:
                self.mostrar_reservas()
            elif opcion == 3:
                self.cancelar_reserva()
            elif opcion == 4:
                self.mostrar_perfil()
            elif opcion == 5:
                self.actualizar_perfil()
            elif opcion == 6:
                print("\n¡Hasta luego!")
                self.usuario_actual = None 
                return
            else:
                print("Opción inválida.")
        else:
            print("ERROR: Rol no reconocido. Contacte al administrador.")
        print("=" * 50)
             
    def reservar_habitacion(self):
        """
        Permite a un usuario autenticado (cliente) reservar una habitación en el sistema.
        El método guía al usuario a través del proceso de reserva, solicitando el número de noches,
        número de personas, tipo de habitación, y la fecha de entrada. Calcula el costo total,
        muestra un resumen de la reserva y solicita confirmación antes de crear la reserva en la base de datos.
        Si la reserva es confirmada, marca la habitación como no disponible y ofrece la opción de agregar servicios adicionales.
        Requiere:
            - El usuario debe haber iniciado sesión como cliente.
            - Deben existir tipos de habitación y habitaciones disponibles en la base de datos.
        Entradas del usuario:
            - Número de noches (entero > 0)
            - Número de personas (entero > 0)
            - Selección de tipo de habitación
            - Fecha de entrada (formato AAAA-MM-DD, no anterior a hoy)
            - Confirmación de reserva (1 para sí, 2 para no)
            - Opción de agregar servicios adicionales (1 para sí, 2 para no)
        Efectos secundarios:
            - Crea una nueva reserva en la base de datos si es confirmada.
            - Marca la habitación reservada como no disponible.
            - Puede invocar la reserva de servicios adicionales.
        Mensajes de error:
            - Si el usuario no ha iniciado sesión como cliente.
            - Si no hay habitaciones disponibles del tipo seleccionado.
            - Si las entradas del usuario no son válidas.
        """
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
        tipos_disponibles = self.tipo_habitacion_crud.obtener_tipos_habitacion(self.db)
        print("Tipos de habitación disponibles:")
        for idx, t in enumerate(tipos_disponibles, start=1):
            print(f"{idx}. {t.nombre_tipo}")
        while True:
            tipo_input = input(f"Selecciona el tipo de habitación (1-{len(tipos_disponibles)}): ")
            if tipo_input.isdigit():
                tipo_input = int(tipo_input)
                if 1 <= tipo_input <= len(tipos_disponibles):
                    break
                print(f"Debes seleccionar entre 1 y {len(tipos_disponibles)}.")
            else:
                print("Debes ingresar un número válido.")
        tipo_seleccionado = tipos_disponibles[tipo_input - 1]  
        nombre_tipo = tipo_seleccionado.nombre_tipo  
        habitacion = self.db.query(Habitacion).filter_by(tipo=nombre_tipo, disponible=True).first()
        if not habitacion:
            print("No hay habitaciones disponibles de ese tipo.")
            return
        precio_noche = habitacion.precio
        total = precio_noche * noches
        while True:
            fecha_entrada_str = input("Ingrese la fecha de entrada (AAAA-MM-DD): ").strip()
            try:
                fecha_entrada = datetime.strptime(fecha_entrada_str, "%Y-%m-%d").date()
                if fecha_entrada < date.today():
                    print("La fecha de entrada no puede ser anterior a hoy.")
                else:
                    break
            except ValueError:
                print("Formato inválido. Usa AAAA-MM-DD.")
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
        id_habitacion = habitacion.id_habitacion
        reserva = Reserva(
            id_cliente=self.usuario_actual.id_usuario,
            id_habitacion=id_habitacion,
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
        while True:
            opcion_servicio = input("¿Deseas servicios adicionales? (1. Sí / 2. No): ").strip()
            if not opcion_servicio.isdigit():
                print("Debes ingresar un número válido (1 o 2).")
                continue
            opcion_servicio = int(opcion_servicio)
            if opcion_servicio == 1:
                print("Agregando servicios adicionales...")
                self.reservar_servicios() 
                break
            elif opcion_servicio == 2:
                print("No se agregaron servicios adicionales.")
                break
            else:
                print("Opción inválida. Solo puedes elegir 1 o 2.")
                
    def cancelar_reserva(self):
        """
        Cancela una reserva activa del usuario actual.
        Este método muestra todas las reservas activas del usuario actual, permitiéndole seleccionar una para cancelar.
        Solicita confirmación antes de proceder con la cancelación. Si se confirma, actualiza el estado de la reserva a "Cancelada",
        marca la habitación como disponible y registra la fecha y el usuario que realizó la edición.
        Entradas:
            - Solicita al usuario seleccionar el número de la reserva a cancelar.
            - Solicita confirmación para proceder con la cancelación.
        Salidas:
            - Mensajes informativos sobre el estado de la operación (éxito, error o cancelación abortada).
            - Actualización en la base de datos de la reserva y la habitación correspondiente.
        """
        reservas = self.db.query(Reserva).filter_by(
            id_cliente=self.usuario_actual.id_usuario, estado_reserva="Activa"
        ).all()
        if not reservas:
            print("No tienes reservas activas.")
            return
        print("Tus reservas activas:")
        for i, reserva in enumerate(reservas, 1):
            habitacion = self.db.query(Habitacion).filter_by(id_habitacion=reserva.id_habitacion).first()
            if habitacion: 
                print(f"{i}. Habitación {habitacion.numero} del {reserva.fecha_entrada} al {reserva.fecha_salida} - Total: ${reserva.costo_total:,.0f}")
            else:
                print(f"{i}. Habitación no encontrada para la reserva del {reserva.fecha_entrada} al {reserva.fecha_salida}")
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
            habitacion = self.db.get(Habitacion, reserva.id_habitacion)
            if habitacion:
                habitacion.disponible = True
            reserva.estado_reserva = "Cancelada"
            reserva.fecha_edicion = date.today()
            reserva.id_usuario_edita = self.usuario_actual.id_usuario
            self.db.commit()
            print("Reserva cancelada con éxito.")
        else:
            print("Cancelación abortada.")
    
    def mostrar_reservas(self):
        """
        Muestra todas las reservas registradas por el usuario actual.
        Consulta la base de datos para obtener las reservas asociadas al usuario actual.
        Si no existen reservas, informa al usuario. En caso contrario, imprime una lista
        de las reservas mostrando el número de habitación, la cantidad de noches y el estado
        de cada reserva.
        """
        reservas = self.db.query(Reserva).filter_by(id_cliente=self.usuario_actual.id_usuario).all()
        if not reservas:
            print("No tienes reservas registradas.")
            return
        print("\nTus reservas:")
        for r in reservas:
            print(f"Habitación {r.habitacion.numero} - {r.noches} noches - Estado: {r.estado_reserva}")
            
    def reservar_servicios(self):
        """
        Permite al usuario agregar servicios adicionales a una de sus reservas activas.
        El método realiza los siguientes pasos:
        1. Consulta y muestra las reservas activas del usuario actual.
        2. Permite seleccionar una reserva a la que se le agregarán servicios adicionales.
        3. Muestra los servicios adicionales disponibles.
        4. Permite seleccionar uno o varios servicios para agregar a la reserva.
        5. Agrega los servicios seleccionados a la reserva y actualiza el costo total.
        6. Maneja errores y realiza rollback en caso de excepción.
        Raises:
            Exception: Si ocurre un error al agregar los servicios a la reserva.
        """
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
        if not servicios:
            print("No hay servicios adicionales disponibles.")
            return
        print("\nServicios disponibles:")
        for i, s in enumerate(servicios, start=1):
            print(f"{i}. {s.nombre_servicio} - ${s.precio:,.0f} - {s.descripcion}")
        seleccion = input("Selecciona los servicios separados por coma (ej: 1,3): ")
        seleccion_indices = [int(x.strip())-1 for x in seleccion.split(",")]
        try:
            for i in seleccion_indices:
                servicio = servicios[i]
                subtotal = servicio.precio
                reserva_servicio = Reserva_Servicios(
                    id_reserva=reserva_seleccionada.id_reserva,
                    id_servicio=servicio.id_servicio,
                )
                self.db.add(reserva_servicio)
                reserva_seleccionada.costo_total += subtotal
            self.db.commit()
            print("Servicios agregados correctamente a tu reserva.")
        except Exception as e:
            self.db.rollback()
            print(f"Error al agregar servicios: {e}")

    def ejecutar(self) -> None:
        """Ejecutar el sistema principal con autenticación"""
        try:
            print("Iniciando Sistema de Gestión del Hotel...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")
            while True:
                if not self.usuario_actual:
                    if not self.mostrar_pantalla_login():
                        break
                self.mostrar_menu_principal_autenticado()
        except KeyboardInterrupt:
            print("\n\nSistema interrumpido por el usuario.")
        except Exception as e:
            print(f"\nError crítico: {e}")
        finally:
            self.db.close()
            
    def mostrar_menu_habitaciones(self) -> None:
        """
        Muestra el menú de gestión de habitaciones y gestiona la entrada del usuario.
        Este método presenta un menú con opciones para agregar, listar, actualizar o eliminar habitaciones,
        así como una opción para volver al menú principal. Valida la entrada del usuario para asegurar que se seleccione
        una opción válida y luego llama al método correspondiente según la elección del usuario.
        Retorna:
            None
        """
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
            print("Volviendo al menu principal...")
            self.mostrar_menu_principal_autenticado()

    def mostrar_menu_reservas(self) -> None:
        """
        Muestra el menú de gestión de reservas y gestiona la entrada del usuario.
        Solicita al usuario seleccionar una opción y valida la entrada.
        Ejecuta el método correspondiente según la elección del usuario.
        """
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("1. Listar reservas")
        print("2. Consultar reservas activas")
        print("3. Eliminar reserva")
        print("4. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-4): ")
            if opcion.isdigit():  
                opcion = int(opcion)  
                if 1 <= opcion <= 4:
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
            self.eliminar_reserva()
        elif opcion == 4:
            print("Volviendo al menu principal...")
            self.mostrar_menu_principal_autenticado()

    def mostrar_menu_servicios(self) -> None:
        """
        Muestra el menú de gestión de servicios adicionales y gestiona la entrada del usuario.
        Este método presenta un menú con opciones para agregar, listar, actualizar o eliminar servicios adicionales,
        así como una opción para volver al menú principal. Valida la entrada del usuario para asegurar que se seleccione
        una opción válida y luego llama al método correspondiente según la elección del usuariO
        """
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
            self.agregar_servicio()
        elif opcion == 2:                
            self.listar_servicios()
        elif opcion == 3:
            self.actualizar_servicio()
        elif opcion == 4:
            self.eliminar_servicio()
        elif opcion == 5:
            print("Volviendo al menu principal...")
            self.mostrar_menu_principal_autenticado()
 
    def mostrar_menu_usuarios(self) -> None:
        """
        Muestra el menú de gestión de usuarios y gestiona la selección del usuario.
        Solicita al usuario que seleccione una opción válida (1-5) y ejecuta la acción correspondiente.
        Si la opción ingresada no es válida, solicita nuevamente la entrada.
        """
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Eliminar usuario")
        print("4. Volver al menú principal")
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
            self.crear_usuario()
        elif opcion == 2:
            self.listar_usuarios()
        elif opcion == 3:
            self.eliminar_usuario()
        elif opcion == 4:
            print("Volviendo al menú principal...")
            self.mostrar_menu_principal_autenticado()

    def mostrar_perfil(self):
        """
        Muestra en consola la información del perfil del usuario actual.
        Imprime el nombre completo, número de teléfono (como usuario) y el rol del usuario actualmente autenticado.
        """
        print("\n--- MI PERFIL ---")
        print(f"Nombre: {self.usuario_actual.nombre} {self.usuario_actual.apellidos}")
        print(f"Usuario: {self.usuario_actual.telefono}")
        print(f"Rol: {self.usuario_actual.tipo_usuario}")
        
    def agregar_habitacion(self):
        """
        Agrega una nueva habitación al sistema solicitando al usuario el tipo de habitación y el precio por noche.
        El método realiza las siguientes acciones:
        - Muestra los tipos de habitación disponibles obtenidos desde la base de datos.
        - Solicita al usuario seleccionar un tipo de habitación por número.
        - Asigna automáticamente el número de habitación disponible dentro del rango correspondiente al tipo seleccionado.
        - Solicita al usuario el precio por noche de la habitación.
        - Crea una nueva instancia de `Habitacion` con los datos proporcionados y la guarda en la base de datos.
        - Informa al usuario si la habitación fue agregada exitosamente o si ocurrió un error.
        Maneja errores de entrada del usuario y excepciones generales durante el proceso de creación.
        """
        try:
            rangos = {
                "Estándar": range(101, 200),
                "Suite": range(201, 300),
                "Premium": range(301, 400)
            }
            tipos_disponibles = self.tipo_habitacion_crud.obtener_tipos_habitacion(self.db)
            print("Tipos de habitación disponibles:")
            for t in tipos_disponibles:
                print(f"- {t.nombre_tipo}")
            while True:
                opcion = input("Elige el número del tipo de habitación: ").strip()
                if opcion.isdigit():
                    opcion = int(opcion)
                    if 1 <= opcion <= len(tipos_disponibles):
                        tipo = tipos_disponibles[opcion - 1]                
                        break
                    else:
                        print("Número inválido. Debe estar en el rango mostrado.")
                else:
                    print("Debes ingresar un número válido.")      
            fecha_creacion = date.today()
            habitaciones_existentes = [h.numero for h in self.habitacion_crud.obtener_habitaciones(self.db)]
            numero_asignado = next((n for n in rangos[tipo.nombre_tipo] if n not in habitaciones_existentes), None)
            if not numero_asignado:
                print(f"No hay más habitaciones disponibles en el rango de {tipo.nombre_tipo}.")
                return
            while True:
                try:
                    precio = float(input("Precio por noche: "))
                    break
                except ValueError:
                    print("Debes ingresar un número válido para el precio.")
            nueva_habitacion = Habitacion(
                numero=numero_asignado,
                id_tipo=tipo.id_tipo,   
                tipo=tipo.nombre_tipo,       
                precio=precio,
                disponible=True,
                id_usuario_crea=self.usuario_actual.id_usuario,
                fecha_creacion = fecha_creacion
            )
            self.habitacion_crud.crear_habitacion(self.db, nueva_habitacion)
            print(f"Habitación {numero_asignado} ({tipo.nombre_tipo}) agregada exitosamente.")
        except Exception as e:
            print(f"Error al agregar habitación: {e}")

    def listar_habitaciones(self):
        """
        Lista todas las habitaciones registradas obteniéndolas de la base de datos y mostrando sus detalles.
        Este método recupera los registros de habitaciones usando la instancia habitacion_crud y muestra información
        formateada para cada habitación, incluyendo ID, número, tipo, precio, disponibilidad, IDs de usuario creador y editor, y fechas.
        Si no se encuentran habitaciones, notifica al usuario. Maneja e imprime cualquier excepción que ocurra durante el proceso.
        """
        try:
            habitaciones = self.habitacion_crud.obtener_habitaciones(self.db)
            if not habitaciones:
                print("No hay habitaciones registradas.")
            else:
                for h in habitaciones:
                    print(f"""
                    ============================
                    ID: {h.id_habitacion}
                    Número: {h.numero}
                    Tipo: {h.tipo} (ID tipo: {h.id_tipo})
                    Precio: ${h.precio}
                    Disponible: {"Sí" if h.disponible else "No"}
                    Usuario Creador: {h.id_usuario_crea}
                    Usuario Editor: {h.id_usuario_edita}
                    Fecha Creación: {h.fecha_creacion}
                    Fecha Edición: {h.fecha_edicion}
                    ============================
                    """)
        except Exception as e:
            print(f"Error al listar habitaciones: {e}")

    def actualizar_habitacion(self): 
        """
        Actualiza el precio de una habitación seleccionada por el usuario.
        Este método muestra una lista de habitaciones registradas, permite al usuario seleccionar una habitación
        y actualizar su precio. Registra la fecha de edición y el usuario que realiza la actualización.
        Si ocurre algún error durante el proceso, se imprime un mensaje de error y se revierte la transacción.
        Raises:
            Exception: Si ocurre un error durante la actualización de la habitación.
        """
        try:
            habitaciones = self.habitacion_crud.obtener_habitaciones(self.db)
            if not habitaciones:
                print("No hay habitaciones registradas.")
                return
            for i, u in enumerate(habitaciones, start=1):
                print(f"{i}. {u.numero} | ({u.tipo}) | | |")
            opcion = input("Elige el número de la habitación a actualizar: ").strip()
            if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(habitaciones):
                print("Opción inválida.")
                return
            habitacion_a_actualizar = habitaciones[int(opcion) - 1]
            nuevo_precio = float(input(f"Nuevo precio (actual: {habitacion_a_actualizar.precio}): "))
            fecha_edicion=date.today(),
            self.habitacion_crud.actualizar_habitacion(
                self.db,
                id_habitacion=habitacion_a_actualizar.id_habitacion,
                id_usuario_edita=self.usuario_actual.id_usuario,
                fecha_edicion = fecha_edicion,
                precio=nuevo_precio
            )
            print(f"Habitación '{habitacion_a_actualizar.numero}' actualizada exitosamente.")
        except Exception as e:
            print(f"Error al actualizar habitación: {e}")
            self.db.rollback()

    def eliminar_habitacion(self):
        """
        Elimina una habitación seleccionada por el usuario de la base de datos.
        Este método muestra una lista de habitaciones registradas, solicita al usuario que seleccione
        una habitación para eliminar y procede a eliminarla utilizando el CRUD correspondiente.
        Si no hay habitaciones registradas o la opción ingresada es inválida, muestra un mensaje de error.
        En caso de excepción durante el proceso, imprime el error y realiza un rollback en la base de datos.
        Raises:
            Exception: Si ocurre un error durante la eliminación de la habitación.
        """
        try:
            habitaciones = self.habitacion_crud.obtener_habitaciones(self.db)
            if not habitaciones:
                print("No hay habitaciones registradas.")
                return
            for i, u in enumerate(habitaciones, start=1):
                print(f"{i}. {u.numero} | ({u.tipo_habitacion}) | ")
            opcion = input("Elige el número del usuario a eliminar: ").strip()
            if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(habitaciones):
                print("Opción inválida.")
                return
            habitacion_a_eliminar = habitaciones[int(opcion) - 1]
            self.habitacion_crud.eliminar_habitacion(self.db, habitacion_a_eliminar.id_habitacion)
            print(f"Habitación '{habitacion_a_eliminar.numero}' eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la habitación: {e}")
            self.db.rollback()
    
    def listar_reservas(self):
        """
        Lista todas las reservas obtenidas de la base de datos.
        Este método intenta obtener todas las reservas usando el objeto reserva_crud.
        Si no se encuentran reservas, imprime un mensaje indicando que no hay reservas registradas.
        De lo contrario, imprime los detalles de cada reserva, incluyendo estado, fechas de entrada y salida,
        costo total, número de personas y número de noches.
        En caso de excepción, imprime un mensaje de error.
        Lanza:
            Exception: Si ocurre un error al obtener o listar las reservas.
        """
        try:
            reservas = self.reserva_crud.obtener_reservas(self.db)
            if not reservas:
                print("No hay habitaciones registradas.")
            else:
                for h in reservas:
                    print(f"¨{h} º {h.estado_reserva} | {h.fecha_entrada} | {h.fecha_salida} | {h.costo_total} | {h.numero_de_personas} | {h.noches} ")
        except Exception as e:
            print(f"Error al listar habitaciones: {e}")
            
    def listar_reservas_activas(self):
        """
        Lista todas las reservas activas obtenidas de la base de datos y muestra sus detalles.
        Este método intenta obtener todas las reservas activas usando el método `obtener_reservas_activas`
        del objeto `reserva_crud`. Si no hay reservas activas, notifica al usuario.
        De lo contrario, imprime los detalles de cada reserva activa, incluyendo ID de reserva, ID de cliente,
        ID de habitación, fechas de entrada y salida, y estado de la reserva.
        Maneja excepciones mostrando un mensaje de error si ocurre algún problema al obtener los datos.
        """
        try:
            reservas = self.reserva_crud.obtener_reservas_activas(self.db)
            if not reservas:
                print("No hay reservas activas.")
            else:
                for r in reservas:
                    print(f"Reserva {r.id_reserva} | Cliente: {r.id_cliente} | Habitación: {r.id_habitacion} | {r.fecha_entrada} → {r.fecha_salida} | Estado: {r.estado_reserva}")
        except Exception as e:
            print(f"Error al obtener reservas activas: {e}")
            
    def actualizar_perfil(self):
        """
        Permite al usuario actualizar su perfil interactuando por consola.
        Solicita al usuario los nuevos valores para su nombre, apellidos, teléfono,
        nombre de usuario y clave, mostrando los valores actuales y permitiendo mantenerlos
        si se deja el campo vacío. Valida que la nueva clave no exceda los 10 caracteres.
        Si se realizan cambios, actualiza el perfil del usuario en la base de datos y muestra
        un mensaje de confirmación. Si no hay cambios, informa al usuario. Maneja excepciones
        mostrando un mensaje de error y realiza rollback en caso de fallo.
        Returns:
            None
        """
        try:
            usuario = self.usuario_crud.actualizar_usuario(self.db, self.usuario_actual.id_usuario)
            if not usuario:
                print("Usuario no encontrado.")
                return
            print("\n=== ACTUALIZAR PERFIL ===")
            nuevo_nombre = input(f"Nuevo nombre (actual: {usuario.nombre}) [Enter para mantener]: ").strip()
            nuevos_apellidos = input(f"Nuevos apellidos (actual: {usuario.apellidos}) [Enter para mantener]: ").strip()
            nuevo_telefono = input(f"Nuevo teléfono (actual: {usuario.telefono}) [Enter para mantener]: ").strip()
            nuevo_usuario = input(f"Nuevo nombre de usuario (actual: {usuario.nombre_usuario}) [Enter para mantener]: ").strip()
            nueva_clave = input("Nueva clave (Enter para mantener): ").strip()
            fecha_edita = date.today()
            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevos_apellidos:
                cambios["apellidos"] = nuevos_apellidos
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono
            if nuevo_usuario:
                cambios["nombre_usuario"] = nuevo_usuario
            if nueva_clave:
                if len(nueva_clave) > 10:
                    print("La clave no puede exceder 10 caracteres.")
                    return
                cambios["clave"] = nueva_clave
            if cambios:
                self.usuario_crud.actualizar_usuario(
                    self.db,
                    id_usuario=self.usuario_actual.id_usuario,
                    id_usuario_edita=self.usuario_actual.id_usuario,
                    fecha_edicion = fecha_edita,
                    **cambios
                )
                print("Perfil actualizado correctamente.")
            else:
                print("No se realizaron cambios.")
        except Exception as e:
            print(f"Error al actualizar perfil: {e}")
            self.db.rollback()
            
    def crear_usuario(self):
        """
        Crea un nuevo usuario solicitando los datos necesarios por consola.
        Solicita al usuario los siguientes datos:
            - Nombre
            - Apellidos
            - Teléfono
            - Tipo de usuario (Administrador o Cliente)
            - Nombre de usuario
            - Clave (máximo 10 caracteres)
        Valida que el tipo de usuario sea válido. Crea una instancia de Usuario con los datos ingresados
        y la fecha de creación actual. Intenta guardar el usuario en la base de datos utilizando el CRUD
        correspondiente. Si ocurre un error, muestra un mensaje y realiza rollback en la base de datos.
        Raises:
            Exception: Si ocurre un error durante la creación del usuario.
        """
        try:
            print("\n=== CREAR USUARIO ===")
            nombre = input("Nombre: ").strip()
            apellidos = input("Apellidos: ").strip()
            telefono = input("Teléfono: ").strip()
            while True:
                tipo_usuario = input("Tipo de usuario (Administrador/Cliente): ").strip().capitalize()
                if tipo_usuario in ["Administrador", "Cliente"]:
                    break
                print("Opción inválida. Debes ingresar 'Administrador' o 'Cliente'.")
            nombre_usuario = input("Nombre de usuario: ").strip()
            clave = input("Clave (máx. 10 caracteres): ").strip()
            fecha_creacion = date.today()
            nuevo_usuario = Usuario(
                nombre=nombre,
                apellidos=apellidos,
                telefono=telefono,
                tipo_usuario=tipo_usuario,
                nombre_usuario=nombre_usuario,
                clave=clave,
                fecha_creacion = fecha_creacion
            )
            self.usuario_crud.crear_usuario(self.db, nuevo_usuario)
            print("Usuario creado exitosamente.")
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            self.db.rollback()
            
    def listar_usuarios(self):
        """
        Muestra una lista de usuarios registrados en el sistema.
        Obtiene los usuarios a través del método `obtener_usuarios` del objeto `usuario_crud`
        utilizando la conexión de base de datos `db`. Imprime la información de cada usuario
        en formato legible. Si no hay usuarios registrados, muestra un mensaje indicándolo.
        Maneja y muestra cualquier excepción que ocurra durante el proceso.
        Returns:
            None
        """
        try:
            print("\n=== LISTA DE USUARIOS ===")
            usuarios = self.usuario_crud.obtener_usuarios(self.db)
            if not usuarios:
                print("No hay usuarios registrados.")
                return
            for u in usuarios:
                print(f"- Usuario: {u.nombre_usuario} | Tipo: {u.tipo_usuario} | Nombre: {u.nombre} {u.apellidos}")
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            
    def eliminar_usuario(self):
        """
        Elimina un usuario del sistema.
        Muestra una lista de usuarios registrados, solicita al usuario seleccionar uno para eliminar,
        y elimina el usuario seleccionado de la base de datos. Si no hay usuarios registrados, informa al usuario.
        Maneja errores durante el proceso y revierte la transacción en caso de excepción.
        Raises:
            Exception: Si ocurre un error durante la eliminación del usuario.
        """
        try:
            print("\n=== ELIMINAR USUARIO ===")
            usuarios = self.usuario_crud.obtener_usuarios(self.db)
            if not usuarios:
                print("No hay usuarios registrados.")
                return
            for i, u in enumerate(usuarios, start=1):
                print(f"{i}. {u.nombre_usuario} ({u.tipo_usuario})")
            opcion = input("Elige el número del usuario a eliminar: ").strip()
            if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(usuarios):
                print("Opción inválida.")
                return
            usuario_a_eliminar = usuarios[int(opcion) - 1]
            self.usuario_crud.eliminar_usuario(self.db, usuario_a_eliminar.id_usuario)
            print(f"Usuario '{usuario_a_eliminar.nombre_usuario}' eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            self.db.rollback()
            
    def agregar_servicio(self):
        """
        Permite agregar un nuevo servicio adicional al sistema.
        Solicita al usuario el nombre, descricion y precio del servicio y lo guarda en la base de datos.
        """
        try:
            print("\n=== AGREGAR SERVICIO ADICIONAL ===")
            nombre_servicio = input("Nombre del servicio: ").strip()
            fecha_creacion = date.today()
            descripcion = input("Descripción del servicio: ").strip()
            if not nombre_servicio:
                print("El nombre es obligatorio.")
                return
            while True:
                try:
                    precio = float(input("Precio del servicio: "))
                    break
                except ValueError:
                    print("Debes ingresar un número válido para el precio.")
            servicio = Servicios_Adicionales(
                nombre_servicio=nombre_servicio,
                precio=precio,
                descripcion = descripcion,
                id_usuario_crea=self.usuario_actual.id_usuario,
                fecha_creacion = fecha_creacion
            )
            self.servicios_adicionales_crud.crear_servicio(self.db, servicio)
            print(f"Servicio '{servicio.nombre_servicio}' agregado exitosamente.")
        except Exception as e:
            print(f"Error al agregar servicio: {e}")
            self.db.rollback()

    def listar_servicios(self):
        """
        Muestra todos los servicios adicionales registrados en el sistema.
        """
        try:
            servicios = self.servicios_adicionales_crud.obtener_servicios(self.db)
            if not servicios:
                print("No hay servicios registrados.")
                return
            print("\n=== LISTA DE SERVICIOS ADICIONALES ===")
            for s in servicios:
                print(f"- ID: {s.id_servicio} | Nombre: {s.nombre_servicio} | Precio: ${s.precio}")
        except Exception as e:
            print(f"Error al listar servicios: {e}")

    def actualizar_servicio(self):
        """
        Permite actualizar un servicio adicional existente.
        Solicita al usuario seleccionar un servicio y luego modificar su nombre, descripcion o precio.
        """
        try:
            servicios = self.servicios_adicionales_crud.obtener_servicios(self.db)
            if not servicios:
                print("No hay servicios registrados.")
                return
            for i, s in enumerate(servicios, start=1):
                print(f"{i}. {s.nombre_servicio} - ${s.precio} - {s.descripcion}")
            opcion = input("Selecciona el número del servicio a actualizar: ").strip()
            if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(servicios):
                print("Opción inválida.")
                return
            servicio = servicios[int(opcion) - 1]
            nuevo_nombre = input(f"Nuevo nombre (actual: {servicio.nombre_servicio}) [Enter para mantener]: ").strip()
            nuevo_precio_input = input(f"Nuevo precio (actual: {servicio.precio}) [Enter para mantener]: ").strip()
            descripcion_nueva = input(f"Descripcion (actual: {servicio.descripcion}) [Enter para mantener]: ").strip()
            fecha_edita = date.today()
            id_usuario_edita = self.usuario_actual.id_usuario
            if nuevo_nombre:
                servicio.nombre_servicio = nuevo_nombre
            if nuevo_precio_input:
                try:
                    servicio.precio = float(nuevo_precio_input)
                except ValueError:
                    print("Precio inválido. Se mantiene el valor actual.")
            if descripcion_nueva:
                servicio.descripcion = descripcion_nueva
            self.servicios_adicionales_crud.actualizar_servicio(self.db, servicio, id_usuario_edita, fecha_edita)
            print("Servicio actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar servicio: {e}")
            self.db.rollback()

    def eliminar_servicio(self):
        """
        Elimina un servicio adicional seleccionado por el usuario.
        Este método obtiene la lista de servicios adicionales registrados, muestra al usuario
        las opciones disponibles y solicita que seleccione el número del servicio a eliminar.
        Si la opción es válida, elimina el servicio correspondiente de la base de datos.
        En caso de error, muestra un mensaje y realiza un rollback de la transacción.
        Raises:
            Exception: Si ocurre un error durante la eliminación del servicio.
        """
        try:
            servicios = self.servicios_adicionales_crud.obtener_servicios(self.db)
            if not servicios:
                print("No hay servicios registrados.")
                return
            for i, s in enumerate(servicios, start=1):
                print(f"{i}. {s.nombre_servicio} - ${s.precio}")
            opcion = input("Selecciona el número del servicio a eliminar: ").strip()
            if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(servicios):
                print("Opción inválida.")
                return
            servicio = servicios[int(opcion) - 1]
            self.servicios_adicionales_crud.eliminar_servicio(self.db, servicio.id_servicio)
            print(f"Servicio '{servicio.nombre_servicio}' eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar servicio: {e}")
            self.db.rollback()
            
    def eliminar_reserva(self):
        """
        Elimina una reserva seleccionada por el usuario.
        Este método muestra todas las reservas registradas, permite al usuario seleccionar una para eliminarla,
        solicita confirmación y, si se confirma, elimina la reserva de la base de datos. Si la reserva está asociada
        a una habitación, marca la habitación como disponible nuevamente.
        Pasos:
            1. Muestra la lista de reservas existentes.
            2. Solicita al usuario seleccionar una reserva por número.
            3. Solicita confirmación antes de eliminar.
            4. Marca la habitación como disponible si corresponde.
            5. Elimina la reserva de la base de datos.
        Maneja errores como selección inválida o problemas al eliminar la reserva.
        Raises:
            ValueError: Si ocurre un error al eliminar la reserva.
        """
        reservas = self.db.query(Reserva).all()
        if not reservas:
            print("No hay reservas registradas.")
            return
        print("=== Reservas registradas ===")
        for i, reserva in enumerate(reservas, 1):
            habitacion = self.db.get(Habitacion, reserva.id_habitacion)
            habitacion_num = habitacion.numero if habitacion else "No asignada"
            cliente = self.db.get(Usuario, reserva.id_cliente)
            cliente_nombre = f"{cliente.nombre} {cliente.apellidos}" if cliente else "Desconocido"
            print(f"{i}. Cliente: {cliente_nombre} | Habitación: {habitacion_num} | "
                f"Del {reserva.fecha_entrada} al {reserva.fecha_salida} - Total: ${reserva.costo_total:,.0f}")
        opcion = input("Selecciona el número de la reserva que deseas eliminar: ").strip()
        if not opcion.isdigit() or not (1 <= int(opcion) <= len(reservas)):
            print("Opción inválida.")
            return
        reserva_seleccionada = reservas[int(opcion) - 1]
        confirmar = input("¿Deseas confirmar la eliminación? (1. Sí / 2. No): ").strip()
        if confirmar != "1":
            print("Eliminación cancelada.")
            return
        if reserva_seleccionada.id_habitacion:
            habitacion = self.db.get(Habitacion, reserva_seleccionada.id_habitacion)
            if habitacion:
                habitacion.disponible = True
        try:
            self.reserva_crud.eliminar_reserva(self.db, reserva_seleccionada.id_reserva)
            print("Reserva eliminada exitosamente.")
        except ValueError as e:
            print(f"Error: {e}")
            
def main():
    """Función principal"""
    with SistemaGestion() as sistema:
        sistema.ejecutar()

if __name__ == "__main__":
    main()
