import cv2 # To handle camera/scanner
from pyzbar.pyzbar import decode, ZBarSymbol # Handles qr scanner
import logging

def scan_qr():

    matricula=None # Variable to store qr info

    try:
        # Turns the webcam on
        # '0' indicates main camera
        scan=cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not scan.isOpened():
            logging.error("Fallo de hardware: No se detecto ninguna camara o escaner USB conectado al iniciar.")
            return None

        while True:

            # Reads current frame
            # 'worked' tells us if the camera worked
            # 'frame' is the actual frame
            worked, frame=scan.read()

            if not worked:
                print("Error: No se pudo acceder a la camara")
                logging.error("FAllo de hardware: Se perdio la conexion con la camara de forma inesperada")
                break

            # This returns us a list of all codes scanned in said frame
            codes=decode(frame, symbols=[ZBarSymbol.QRCODE])
            for code in codes:
                # pyzbar returns codes in bytes
                # decode('utf-8') converts to human text
                # strip() removes all invisible characers
                matricula=(code.data.decode('utf-8').strip())[-6:]
                print(f"Matricula detectada: {matricula}")

            # Shows the frame in a corner for us to watch
            cv2.imshow('Escaner de acceso GYM', frame)
            
            # if matricula detected, break loop
            if matricula:
                cv2.waitKey(1000)
                break

            # Breaks loop if it detects keyboard input 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        logging.error(f"Error critico en el modulo de escaneo: {str(e)}")

    finally: # Finally always executes, even if no error was detected
        if 'scan' in locals() and scan.isOpened():
            scan.release() # Free cam for next use
        cv2.destroyAllWindows() # Closes all cam windows
    
    return matricula