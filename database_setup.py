import sqlite3

# Crear/Conectar a la base de datos
# Si no existe, Python crea el archivo automáticamente. 
# Si ya existe, simplemente se conecta a él.
conexion = sqlite3.connect("gimnasio.db")

# Crear el Cursor
# El cursor es como nuestra "mano virtual". Es el objeto que nos permite 
# mandar comandos SQL a la base de datos.
cursor = conexion.cursor()

# Diseñar y crear la tabla
# Usamos triple comilla (''') para poder escribir en varias líneas y que se lea limpio.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS miembros (
        matricula TEXT PRIMARY KEY,
        nombre TEXT,
        activo INTEGER
    )
''')
# PRIMARY KEY evita duplicados, como una contrasena
# activo INTEGER Es un booleano para saber si el usuario esta activo

# Confirmar y cerrar (¡La regla de oro!)
conexion.commit()  # Guarda los cambios en el archivo
conexion.close()   # Libera el archivo para que otros programas puedan usarlo

print("¡Base de datos y tabla creadas con éxito!")