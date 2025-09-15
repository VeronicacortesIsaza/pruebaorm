from login import login
from database.config import SessionLocal
from entities.habitacion import Habitacion
from entities.reserva import Reserva
from entities.reserva_servicios import Reserva_Servicios
from entities.servicios_adicionales import Servicios_Adicionales
from datetime import date, timedelta

def menu(usuario):
    session = SessionLocal()
    try:
        while True:
            print("\n===== SISTEMA DE RESERVAS DE HOTEL =====")
            print("1. Reservar habitación")
            print("2. Cancelar reserva")
            print("3. Mostrar reservas")
            print("4. Salir")

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
                reservar_habitacion(session, usuario)
            elif opcion == 2:
                cancelar_reserva(session, usuario)
            elif opcion == 3:
                mostrar_reservas(session, usuario)
            elif opcion == 4:
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
    finally:
        session.close()

def reservar_habitacion(session, usuario):
    if not usuario:
        print("Debes iniciar sesión como cliente para reservar.")
        return

    while True:
        noches = input("Número de noches: ")
        if noches.isdigit():
            noches = int(noches)
            if noches > 0:
                break
            print("Debe ser mayor a cero.")
        else:
            print("Debes ingresar un número válido.")
    while True:
        numero_de_personas = input("Número de personas: ")
        if numero_de_personas.isdigit():
            numero_de_personas = int(numero_de_personas)
            if numero_de_personas > 0:
                break
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
    habitacion = session.query(Habitacion).filter_by(tipo=tipo, disponible=True).first()
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
        id_cliente=usuario.id_usuario,
        id_habitacion=habitacion.id_habitacion,
        fecha_entrada=fecha_entrada,
        fecha_salida=fecha_salida,
        estado_reserva="Activa",
        numero_de_personas=numero_de_personas,
        noches=noches,
        costo_total=total,
        id_usuario_crea=usuario.id_usuario,
        fecha_creacion=fecha_creacion
    )

    habitacion.disponible = False
    session.add(reserva)
    session.commit()

    print(f"\nReserva creada para {usuario.nombre} {usuario.apellidos}")
    print(f"Habitación {habitacion.numero} - Total: ${total:,}")
    print(f"Del {fecha_entrada} al {fecha_salida}")

    if input("¿Deseas servicios adicionales? (s/n): ").lower() == "s":
        reservar_servicios(session, usuario)


def cancelar_reserva(session, usuario):
    reservas = session.query(Reserva).filter_by(
        id_cliente=usuario.id_usuario, estado_reserva="Activa"
    ).all()

    if not reservas:
        print("No tienes reservas activas.")
        return

    print("Tus reservas activas:")
    for i, reserva in enumerate(reservas, 1):
        habitacion = session.query(Habitacion).get(reserva.id_habitacion)
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

    confirm = input(f"¿Seguro que deseas cancelar la reserva de la habitación {habitacion.numero}? (s/n): ").lower()
    if confirm == "s":
        habitacion = session.query(Habitacion).get(reserva.id_habitacion)
        habitacion.disponible = True

        reserva.estado_reserva = "Cancelada"
        reserva.fecha_edicion = date.today()
        reserva.id_usuario_edita = usuario.id_usuario

        session.commit()
        print("Reserva cancelada con éxito.")
    else:
        print("Cancelación abortada.")

    
def mostrar_reservas(session, usuario):
    reservas = session.query(Reserva).filter_by(id_cliente=usuario.id_usuario).all()
    if not reservas:
        print("No tienes reservas registradas.")
        return

    print("\nTus reservas:")
    for r in reservas:
        print(f"Habitación {r.habitacion.numero} - {r.noches} noches - Estado: {r.estado_reserva}")


def reservar_servicios(session, usuario):
    reservas = session.query(Reserva).filter_by(id_cliente=usuario.id_usuario).all()
    if not reservas:
        print("No tienes reservas activas.")
        return

    print("\nTus reservas activas:")
    for i, r in enumerate(reservas, start=1):
        print(f"{i}. Habitación {r.habitacion.numero} del {r.fecha_entrada} al {r.fecha_salida}")

    idx = int(input("Selecciona la reserva a la que agregar servicios: ")) - 1
    reserva_seleccionada = reservas[idx]

    servicios = session.query(Servicios_Adicionales).all()
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
        session.add(reserva_servicio)
        reserva_seleccionada.costo_total += subtotal

    session.commit()
    print("Servicios agregados correctamente a tu reserva.")


if __name__ == "__main__":
    usuario = login()   
    if usuario:
        menu(usuario)   
    else:
        print("No se pudo iniciar sesión.")

