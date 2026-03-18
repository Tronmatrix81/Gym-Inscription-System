import sqlite3
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import glob # Search for archives
from database_connect import connect_database

#--- Admin log ---

# Ensure logs folder exists
logsDirectory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(logsDirectory):
    os.makedirs(logsDirectory)

# Log rotation
adminLogDirectory=os.path.join(logsDirectory, "admin.log")

adminHandler=TimedRotatingFileHandler(
    filename=adminLogDirectory,
    when="midnight",
    interval=1,
    backupCount=100,
    encoding='utf-8'
)

# Format
adminFormat=logging.Formatter('%(asctime)s - [ADMIN] - [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S')
adminHandler.setFormatter(adminFormat)

# Activate admin logger
logger=logging.getLogger()
logger.setLevel(logging.INFO)

# Clear previous config
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(adminHandler)

#-----------------


connection=connect_database()

def register_user(matricula, nombre):
    # Register a new user (active by default)
    try:
        with connection:
            cursor=connection.cursor()
            cursor.execute("INSERT INTO miembros (matricula, nombre, activo) VALUES (?,?,1)", (matricula, nombre))
            connection.commit()

            print(f"Usuario {nombre} ({matricula}) ha sido dado de alta correctamente")
            logging.info(f"Usuario {nombre} ({matricula}) ha sido dado de alta correctamente.")
            return True
        
    except sqlite3.IntegrityError:
        print(f"Error: La matricula {matricula} ya existe en el sistema.")
        logging.error(f"No se pudo dar de alta la matricula {matricula}. Ya existe en el sistema.")

def alternate_user_status(matricula):
    # Changes the user status to active or inactive
    with connection:
        cursor=connection.cursor()
        cursor.execute("SELECT nombre, activo FROM miembros WHERE matricula = ?", (matricula,))
        result=cursor.fetchone()

        if result:
            name=result[0]
            status=result[1]

            newStatus=1 if status == 0 else 0
            status_str="ACTIVADO" if newStatus == 1 else "DESACTIVADO"

            cursor.execute("UPDATE miembros SET activo = ? WHERE matricula = ?", (newStatus, matricula))
            connection.commit()

            print(f"Usuario {name} ({matricula}) ha sido {status_str}")
            logging.info(f"Usuario {name} ({matricula}) ha sido {status_str}.")
        else:
            print(f"No se encontro la matricula {matricula}")
            logging.error(f"No se pudo actualizar el estado de la matricula {matricula}. Matricula no encontrada")

def list_users():
    # Prints the user list
    logging.info("El administrador leyo la lista de usuarios")
    print("\n--- DIRECTORIO DEL GIMNASIO ---")
    with connection:
        cursor=connection.cursor()
        cursor.execute("SELECT matricula, nombre, activo FROM miembros")
        for matricula, name, active in cursor.fetchall():
            status="Activo" if active==1 else "Inactivo"
            print(f"[{matricula}] {name} - {status}")
    print("-------------------------------\n")

def log_history(isAdmin=False):
    # Log history lookup

    logType = "ADMIN" if isAdmin else "REGISTRO_ACCESOS"
    print(f"\n--- HISTORIAL DE LOGS ({logType}) ---")

    logName="admin.log*" if isAdmin else "registro_accesos.log*"

    # Search for all logs in logs folder
    logsDirectory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", logName)
    foundFiles=glob.glob(logsDirectory)

    if not foundFiles:
        print("No se encontraron logs para mostrar")
        logging.warning(f"Intento de lectura: No se encontraron logs de {logType.lower()}.")
        return
    
    # Newer log shows first
    foundFiles.sort(key=os.path.getmtime, reverse=True)
    print("Fechas disponibles:")

    for index, filePath in enumerate(foundFiles):
        fileName=os.path.basename(filePath)
        
        # Easier naming
        baseName=f"{logType.lower()}+.log"
        if fileName==baseName:
            print(f"  {index+1}. Hoy (En curso)")
        else:
            # Remove filename and replace by date
            date=fileName.replace(f"{baseName}.", "")
            print(f"  {index+1}. {date}")
    
    option=input("\nElige el número del día que quieres revisar ('q' para salir): ").strip()
    if option.lower()=='q':
        return
    
    try:
        chosenFile=foundFiles[int(option)-1]
        logging.info(f"El administrador leyo el archivo {os.path.basename(chosenFile)}.")
        print(f"\n--- MOSTRANDO LOGS DE: {os.path.basename(chosenFile)} ---")

        with open(chosenFile, 'r', encoding='utf-8') as file:
            content=file.read()
            if content.strip()=="":
                print("[Archivo vacio]")
            else:
                print(content)
        print("---------------------------------\n")
    
    except (ValueError, IndexError):
        print("Opcion no valida, regresando al menu")

def delete_user(matricula):
    # Permanently removes a user from database
    with connection:
        cursor=connection.cursor()

        # Search for the user
        cursor.execute("SELECT nombre FROM miembros WHERE matricula = ?", (matricula,))
        result=cursor.fetchone()

        if result:
            name=result[0]

            # Security check before deleting user
            confirm=input(f"¿Estas seguro que deseas ELIMINAR a {name} ({matricula})? (S/N): ").strip().lower()

            if confirm=='s':
                cursor.execute("DELETE FROM miembros WHERE matricula = ?", (matricula,))
                connection.commit()

                print(f"Usuario {name} ({matricula}) ha sido eliminado permanentemente.")
                logging.info(f"Usuario {name} ({matricula}) ha sido eliminado permanentemente.")
            else:
                print("Operacion cancelada. El usuario no fue eliminado")
        else:
            # If no user was found during SELECT
            print(f"Error: Matrícula {matricula} no encontrada en el sistema.")
            logging.warning(f"Error: Matrícula {matricula} no encontrada en el sistema.")



# --- MENÚ DE TERMINAL (Para usarlo hoy) ---
if __name__ == "__main__":
    logging.info("La consola de admin ha sido abierta")
    try:
        while True:
            print("\n--- PANEL DE ADMINISTRACIÓN ---")
            print("1. Ver usuarios")
            print("2. Dar de alta nuevo usuario")
            print("3. Activar / Desactivar usuario")
            print("4. Ver historial de logs")
            print("5. Ver historial de logs (admin)")
            print("6. Dar de baja a un usuario")
            print("7. Salir")
            
            opcion = input("Elige una opción: ").strip()
            
            if opcion == '1':
                list_users()
            elif opcion == '2':
                matricula = input("Nueva matrícula: ").strip()
                name = input("Nombre del usuario: ").strip()
                register_user(matricula, name)
            elif opcion == '3':
                matricula = input("Matrícula a modificar: ").strip()
                alternate_user_status(matricula)
            elif opcion == '4':
                log_history()
            elif opcion=='5':
                log_history(True)
            elif opcion=='6':
                matricula=input("Matricula a dar de baja: ").strip()
                delete_user(matricula)
            elif opcion == '7':
                print("Cerrando terminal...")
                logging.info("La consola de admin ha sido cerrada")
                break

    except KeyboardInterrupt:
        print("\nCerrando el programa..")
        logging.info("La consola de admin fue apagada manualmente (Ctrl+C).")