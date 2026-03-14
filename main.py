"""
Sistema de Control de Acceso para Gimnasio.

Este script gestiona la entrada de miembros validando una matrícula o código QR 
(leído a través de un escáner USB que emula un teclado) contra una base de datos 
local SQLite. Si el usuario está activo, simula el envío de una señal a una 
chapa magnética (maglock) para abrir la puerta.

"""

import sqlite3 # Database
import time

# Import our python files as if they were libraries
from qr_scanner import scan_qr

def connect_database():
    # Connects to the database
    return sqlite3.connect("gimnasio.db")

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
    else:
        name=result[0] # First part of the result
        active=result[1] # Second part of the result

        if active==1:
            print(f"Credencial correcta. Bienvenido {name}!")

            # Here goes some door mechanism logic #
        
        else:
            print(f"Acceso denegado {name}: tu credencial esta inactiva")


# PROGRAM START #
if __name__=="__main__":
    print("======================================================")
    print("  ▗▄▄▖▗▖  ▗▖▗▖  ▗▖     ▗▄▄▖▗▖  ▗▖▗▄▄▖▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖ ")
    print(" ▐▌    ▝▚▞▘ ▐▛▚▞▜▌    ▐▌    ▝▚▞▘▐▌     █  ▐▌   ▐▛▚▞▜▌ ")
    print(" ▐▌▝▜▌  ▐▌  ▐▌  ▐▌     ▝▀▚▖  ▐▌  ▝▀▚▖  █  ▐▛▀▀▘▐▌  ▐▌ ")
    print(" ▝▚▄▞▘  ▐▌  ▐▌  ▐▌    ▗▄▄▞▘  ▐▌ ▗▄▄▞▘  █  ▐▙▄▄▖▐▌  ▐▌ ")
    print("        Presiona Ctrl+C para salir del programa       ")                                                               
    print("======================================================")
                                                    
    # Infinite loop to keep the system online 24/7
    while True:
        try:
            # Awaits for any input
            # split() removes any invisible space inside the string
            matricula=scan_qr()

            if matricula:
                validate_access(matricula)

            time.sleep(2)
            
        except KeyboardInterrupt:
            # Detects admin input and exits the program
            print("\nCerrando el programa..")
            break