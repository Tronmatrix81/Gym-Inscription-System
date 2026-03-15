"""
Sistema de Control de Acceso para Gimnasio.

Este script gestiona la entrada de miembros validando una matrícula o código QR 
(leído a través de un escáner USB que emula un teclado) contra una base de datos 
local SQLite. Si el usuario está activo, simula el envío de una señal a una 
chapa magnética (maglock) para abrir la puerta.

"""

import time
import logging # For logs

# Import our python files as if they were libraries
from qr_scanner import scan_qr
from access_validation import validate_access


# --- LOG STRUCTURE CONFIG ---
logging.basicConfig(
    filename='registro_accesos.log', # Log 
    level=logging.INFO, # Registers INFO and upper levels (Ignores debug)
    format='%(asctime)s - [%(levelname)s] - %(message)s', # Format: Date - Level - Message
    datefmt='%Y-%m-%d %H:%M:%S' # Date format: Year-Month-Day Hour:Minute:Second
)
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
            matricula=scan_qr()

            if matricula:
                validate_access(matricula)

            time.sleep(2)
            
        except KeyboardInterrupt:
            # Detects admin input and exits the program
            print("\nCerrando el programa..")
            logging.info("El sistema de acceso fue apagado manualmente (Ctrl+C).")
            break