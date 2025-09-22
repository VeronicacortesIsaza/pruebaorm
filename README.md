# Sistema de Gestión de Hotel  

Este proyecto implementa un **sistema de gestión para un hotel** desarrollado en **Python 3.8** utilizando **SQLAlchemy** para la persistencia de datos.  
Incluye autenticación de usuarios, gestión de clientes, habitaciones, reservas y servicios adicionales, todo a través de una interfaz de consola.

---

## Estructura del Proyecto

```
pruebaorm/
│
├── crud/                         
│   ├── administrador_crud.py
│   ├── cliente_crud.py
│   ├── habitacion_crud.py
│   ├── reserva_crud.py
│   ├── reserva_servicios_crud.py
│   ├── servicios_adicionales_crud.py
│   ├── tipo_habitacion_crud.py
│   └── usuario_crud.py
│
├── database/                     
│   └── config.py                 
│
├── entities/                     
│   ├── __init__.py
│   ├── administrador.py
│   ├── cliente.py
│   ├── habitacion.py
│   ├── reserva_servicios.py
│   ├── reserva.py
│   ├── servicios_adicionales.py
│   ├── tipo_habitacion.py
│   └── usuario.py
│
├── entities/
│   ├── migrations/
│   │   └── __init__.py
│   ├── env.py
│   └── script.py.mako
│               
├── .env
├── .gitignore 
├── alembic.ini
├── main.py  
├── requirements.txt  
└── README.md                     
```

---

### Requisitos Previos
- Python 3.8 o superior  
- PostgreSQL (o el motor definido en `config.py`)  
- Paquetes necesarios (instalar con `pip`):

```bash
pip install sqlalchemy psycopg2-binary
```

> Opcional: si usas contraseñas cifradas, también se recomienda instalar `bcrypt`.


---

### Inicio de Sesión
- El sistema solicitará **nombre de usuario** y **contraseña**.  
- Se permite hasta **3 intentos fallidos** antes de bloquear el acceso.  
- Si es la primera vez, crea un usuario administrador con la opción del menú.

---

## Descripción de la Lógica de Negocio

El sistema cubre los siguientes procesos principales:

### Gestión de Usuarios
- Creación de usuarios (administradores y clientes).  
- Actualización, consulta y eliminación.  
- Cambio de contraseña y actualización de perfil.  

### Gestión de Habitaciones
- Registro de habitaciones con tipo, precio y disponibilidad.  
- Modificación y consulta de estado (disponible, reservada, mantenimiento).  

### Gestión de Reservas
- Creación de reservas asociadas a clientes y habitaciones.  
- Validación de fechas de entrada y salida.  
- Cálculo automático del número de noches y costo total.  
- Control de estados: **confirmada**, **cancelada**, **finalizada**.  

### Servicios Adicionales
- Registro y asociación de servicios (desayuno, spa, transporte, etc.) a una reserva.  
- Suma de costos adicionales a la cuenta final del cliente.  

### Autenticación
- Acceso mediante **nombre de usuario** y contraseña.  
- Distinción de roles:  
  - **Administrador**: acceso completo a todas las gestiones.  
  - **Cliente**: acceso restringido a su perfil y reservas.  

---

## Notas
- La lógica está implementada en la clase `SistemaGestion`, que controla los menús e interacción con el usuario.  
- Todos los accesos a base de datos se hacen mediante objetos CRUD, manteniendo la lógica separada de la persistencia.  
- Se utiliza **SQLAlchemy ORM** para mapear las entidades con la base de datos. 

---

## Cómo Ejecutar el Sistema
1. Abre una nueva terminal presionando **Control + shift + ñ"
2. Cambia de rama escribiendo git checkout Prod
3. Escribe en consola lo siguiente:

```bash
python main.py
```

En consola verás la pantalla de login:

```bash
==================================================
        SISTEMA DE GESTIÓN DE HOTEL
==================================================
INICIAR SESIÓN
==================================================

Intento 1 de 3
Nombre de usuario:
Contraseña:
```