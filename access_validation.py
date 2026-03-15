import logging
import time
from database_connect import connect_database

def validate_access(matricula):
    # Validates the password

    connection=connect_database() # Calls the quickconnect function
    cursor=connection.cursor() # Sets database as a cursor

    # Look for the password inside the database
    cursor.execute('''
        SELECT nombre, activo FROM miembros
        WHERE matricula = ?
    ''', (matricula,))

    # fetchone() brings only one result, or NONE if it doenst exist
    result=cursor.fetchone()
    connection.close() # Close database to free it

    # Time to decide
    if result is None:
        print("Acceso denegado: Matricula o codigo no encontrada en el sistema")
        logging.warning(f"Acceso denegado. Matricula no encontrada: {matricula}")
        
    else:
        name=result[0] # First part of the result
        active=result[1] # Second part of the result

        if active==1:
            print(f"Credencial correcta. Bienvenido {name}!")
            logging.info(f"Acceso concedido. Usuario: {name} (Matricula: {matricula})")

            # Here goes some door mechanism logic #
        
        else:
            print(f"Acceso denegado {name}: tu credencial esta inactiva")
            logging.warning(f"Acceso denegado (Inactivo). Usuario: {name} (Matricula {matricula})")
