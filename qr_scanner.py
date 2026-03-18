import cv2 # To handle camera/scanner
from pyzbar.pyzbar import decode, ZBarSymbol # Handles qr scanner
import logging

def scan_qr():
    # Turns the camera on
    scan=cv2.VideoCapture(0)

    if not scan.isOpened():
        logging.error("No se detecto ninguna camara.")
        return None
    
    matricula=None

    try:
        # Infinite loop for the camera to stay on
        while True:
            worked, frame=scan.read()

            if not worked:
                logging.error("Se perdio la conexion con la camara de forma inesperada.")
                break

            # Analize frame for qr code
            codes=decode(frame, symbols=[ZBarSymbol.QRCODE])

            if codes:
                # Clean text
                matricula=codes[0].data.decode('utf-8').strip()
                break

    # Log if something goes wrong
    except Exception as e:
        logging.error(f"Error critico en el modulo de escaneo: {str(e)}")

    finally:
        if 'scan' in locals() and scan.isOpened():
            # Release camera
            scan.release()
        
    return matricula