"""
Sistema de Control de Acceso para Gimnasio.

Este script gestiona la entrada de miembros validando una matrícula o código QR 
(leído a través de un escáner USB que emula un teclado) contra una base de datos 
local SQLite. Si el usuario está activo, simula el envío de una señal a una 
chapa magnética (maglock) para abrir la puerta.

"""

import time
import logging # For logs
from logging.handlers import TimedRotatingFileHandler # For log rotation (Eliminates older logs when a new log is created)
import os

# Import our python files as if they were libraries
from qr_scanner import scan_qr
from access_validation import validate_access
from id_verification import id_verification

# --- LOG STRUCTURE CONFIG ---

# Make a log-dedicated folder
logsDirectory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(logsDirectory):
    os.makedirs(logsDirectory)

# Configure log rotation
logsPath=os.path.join(logsDirectory, "registro_accesos.log")

dailyHandler=TimedRotatingFileHandler(
    filename=logsPath, # Sets the file name
    when='midnight', # Ends log at midnight
    interval=1, # Each day
    backupCount=100, # Keeps the last 100 days
    encoding='utf-8' # Human text
)

# Format: Date - Level - Message, Year-Month-Day Hour:Minute:Second
format=logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S')
dailyHandler.setFormatter(format)

# Activate main logger
logger=logging.getLogger()
logger.setLevel(logging.INFO) # Registers INFO and upper levels (Ignores debug)
logger.addHandler(dailyHandler)

# ----------------------------


# --- PROGRAM START ---
if __name__=="__main__":
    logging.info("Sistema de acceso INICIADO.")
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
            rawMatricula=scan_qr()

            # Cleans matricula
            if rawMatricula:
                matricula=id_verification(rawMatricula)            
                if matricula:
                    validate_access(matricula)
                else:
                    print(f"Matricula falsa detectada")
                    logging.warning(f"Intento de acceso con credencial falsa: {rawMatricula}")

            time.sleep(2)
            
        except KeyboardInterrupt:
            # Detects admin input and exits the program
            print("\nCerrando el programa..")
            logging.info("El sistema de acceso fue apagado manualmente (Ctrl+C).")
            break