from login import login
from database.config import SessionLocal
from entities.habitacion import Habitacion
from entities.reserva import Reserva
from entities.reserva_servicios import Reserva_Servicios
from entities.servicios_adicionales import Servicios_Adicionales

def menu():
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
                reservar_habitacion(session)
            elif opcion == 2:
                cancelar_reserva(session)
            elif opcion == 3:
                mostrar_reservas(session)
            elif opcion == 4:
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
    finally:
        session.close()
from datetime import date, timedelta

def reservar_habitacion(session, sesion_actual):
    if not sesion_actual:
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
    habitacion = session.query(Habitacion).filter_by(tipo=tipo, disponible=True).first()
    if habitacion:
        precio_noche = habitacion.precio
        total = precio_noche * noches
    else:
        print("No hay habitaciones disponibles de ese tipo.")
        return

    fecha_entrada = date.today()
    fecha_salida = fecha_entrada + timedelta(days=noches)
    fecha_creacion = date.today()
    print(f"\nFecha entrada: {fecha_entrada}")
    print(f"Fecha salida: {fecha_salida}")
    print(f"Total: {noches} noches x ${precio_noche:,} = ${total:,}")

    confirmar = input("¿Desea confirmar la reserva? (s/n): ").lower()
    if confirmar != "s":
        print("Reserva cancelada.")
        return

    reserva = Reserva(
        id_cliente=sesion_actual.id_cliente,
        id_habitacion=habitacion.id_habitacion,
        fecha_entrada=fecha_entrada,
        fecha_salida=fecha_salida,
        estado_reserva="Activa",
        noches=noches,
        costo_total=total,
        id_usuario_crea=sesion_actual.id_cliente,
        fecha_creacion=fecha_creacion
    )

    habitacion.disponible = False
    session.add(reserva)
    session.commit()
    
    print("¿Deseas servicios adicionales? (Si/No)")
    sele = input().strip().lower()  

    if sele in {"si", "s"}:
        reservar_servicios(session, sesion_actual)
    elif sele in {"no", "n"}:
        print("No se agregarán servicios adicionales.")
    else:
        print("Respuesta inválida. Debes ingresar 'Si' o 'No'.")


    print(f"\nReserva creada para {sesion_actual.usuario.nombre} {sesion_actual.usuario.apellidos}")
    print(f"Habitación {habitacion.numero} - Total: ${total:,}")
    print(f"Del {fecha_entrada} al {fecha_salida}")

def cancelar_reserva(session):
    correo = input("Ingrese correo del cliente para cancelar la reserva: ")
    reserva = session.query(Reserva).filter_by(correo=correo).first()
    if reserva:
        reserva.habitacion.disponible = True
        session.delete(reserva)
        session.commit()
        print("Reserva cancelada.")
    else:
        print("No se encontró la reserva.")

def mostrar_reservas(session):
    reservas = session.query(Reserva).all()
    if not reservas:
        print("No hay reservas registradas.")
        return
    for r in reservas:
        print(f"{r.cliente} - {r.documento} - {r.habitacion.tipo} - {r.noches} noches")
    
def reservar_servicios(session, cliente_actual):
    if not cliente_actual:
        print("Debes iniciar sesión para reservar servicios.")
        return

    reservas = session.query(Reserva).filter_by(id_cliente=cliente_actual.id_cliente).all()
    if not reservas:
        print("No tienes reservas activas.")
        return

    print("\nTus reservas activas:")
    for i, r in enumerate(reservas, start=1):
        print(f"{i}. Habitación {r.habitacion.numero} del {r.fecha_entrada} al {r.fecha_salida}")

    idx = int(input("Selecciona la reserva a la que agregar servicios: ")) - 1
    reserva_seleccionada = reservas[idx]

    # Mostrar servicios disponibles
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
    if login():
        menu()
    else:
        print("No se pudo iniciar sesión.")
