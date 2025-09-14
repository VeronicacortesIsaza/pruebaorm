from database.config import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE cliente 
            DROP CONSTRAINT IF EXISTS cliente_id_cliente_fkey,
            ADD CONSTRAINT cliente_id_cliente_fkey
                FOREIGN KEY (id_cliente) REFERENCES usuario(id_usuario)
                ON DELETE CASCADE;
    """))

    conn.execute(text("""
        ALTER TABLE administrador
            DROP CONSTRAINT IF EXISTS administrador_id_admin_fkey,
            ADD CONSTRAINT administrador_id_admin_fkey
                FOREIGN KEY (id_admin) REFERENCES usuario(id_usuario)
                ON DELETE CASCADE;
    """))
    conn.commit()

print("Relaciones actualizadas en Neon correctamente ✅")
