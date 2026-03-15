import sqlite3
from database_connect import connect_database

# Conectarnos a la base de datos
conexion=connect_database()
cursor=conexion.cursor()

# Usuarios de prueba (dupla)
# Formato: (matricula, nombre, activo)
usuarios_dummy = [
    ("394350", "Justie", 1), # Activo - Deberia entrar
    ("394569", "Erik", 1),
    ("394468", "Caleb", 0) # Inactivo - No deberia entrar
]

# Insertar datos de forma segura (Forma correcta)
try:
    cursor.executemany('''
        INSERT INTO miembros (matricula, nombre, activo)
        VALUES (?, ?, ?)
    ''', usuarios_dummy)
    # 'executemany' Es como un ciclo for, pero mas optimizado para base de datos
    # '?' Es practica de seguridad para que no inyecten codigo malicioso

    conexion.commit() # Guardar cambios
    print(f"Se agregaron {cursor.rowcount} usuarios de prueba")

except sqlite3.IntegrityError:
    # Salta si intentas correr el script dos veces y las matrículas ya existen
    print("Error: Estas matrículas ya están registradas en la base de datos.")

conexion.close() # Cerrar sesion