"""
Script para probar la conexión a PostgreSQL (Neon)
"""

import sys

from database.config import DATABASE_URL, engine
from sqlalchemy import text
from database.config import Base

def create_tables():
    Base.metadata.create_all(bind=engine)

def test_connection():
    """Probar la conexión a la base de datos"""
    print("=== PRUEBA DE CONEXION A POSTGRESQL (NEON) ===\n")
    print(f"URL de conexion: {DATABASE_URL}")
    print()

    try:
        # Intentar conectar
        with engine.connect() as connection:
            print("[OK] Conexion exitosa a PostgreSQL!")

            # Probar una consulta simple
            result = connection.execute(text("SELECT version() as version"))
            version = result.fetchone()
            print(f"[OK] Version de PostgreSQL: {version[0]}")

            # Verificar si la base de datos existe
            result = connection.execute(
                text(
                    "SELECT datname FROM pg_database WHERE datname = current_database()"
                )
            )
            db_exists = result.fetchone()

            if db_exists:
                print(f"[OK] Conectado a la base de datos: {db_exists[0]}")
            else:
                print("[WARNING] No se pudo verificar la base de datos actual")

            # Listar tablas disponibles
            print("\nTablas disponibles:")
            result = connection.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
            )
            tables = result.fetchall()
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  (No hay tablas creadas aun)")

    except Exception as e:
        print(f"[ERROR] Error de conexion: {e}")
        print("\nPosibles soluciones:")
        print("1. Verificar que la URL de conexion sea correcta")
        print("2. Verificar que la base de datos este activa en Neon")
        print("3. Verificar que las credenciales sean correctas")
        print("4. Verificar la conexion a internet")
        return False

    return True


def test_tables():
    """Probar la creacion de tablas"""
    print("\n=== PROBANDO CREACION DE TABLAS ===\n")

    try:
        from database.config import create_tables

        create_tables()
        print("[OK] Tablas creadas exitosamente")

    except Exception as e:
        print(f"[ERROR] Error creando las tablas: {e}")
        return False

    return True




if __name__ == "__main__":
    print("Iniciando prueba de conexion...\n")

    # Probar conexion
    if test_connection():
        print("\n" + "=" * 50)
        # Probar creacion de tablas
        if test_tables():
            print("\n" + "=" * 50)

        print("\n[SUCCESS] Configuracion completada!")
        print("Ahora puedes ejecutar:")
        print("  python main.py")
        print("  python ejemplo_basico.py")
    else:
        print("\n[ERROR] No se pudo establecer la conexion")
        sys.exit(1)
        
    with engine.connect() as connection:
        result = connection.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        ))
        print("Tablas en la BD Neon:")
        for row in result:
            print(" -", row[0])
