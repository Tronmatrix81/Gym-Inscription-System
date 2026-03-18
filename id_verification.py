def id_verification(qrScan):
    # --- Guard clause ---
    if not qrScan:
        return None
    # --------------------
    
    # Analizes the QR scan and validates legitimacy
    # Returns clean credentials, or None in case of falsification

    # Physical ID
    # Assumes it will always be 10 digits long, and first 6 are the matricula
    if len(qrScan)==11 and qrScan.lower().startswith('a') and qrScan[1:].isdigit():
        clean_matricula=qrScan[1:7]
        print("[Filtro] Credencial fisica detectada")
        return clean_matricula
    
    # Digital ID
    # Digital ID has a static link
    elif qrScan.startswith("https://verificacion.uach.mx/credencial/"):
        print("[Filtro] Credencial digital detectada")

        # Extract matricula from link
        clean_matricula=qrScan.split('/')[-1]

        # Verify it actually got a matricula
        if len(clean_matricula)==6 and clean_matricula.isdigit():
            return clean_matricula
        else:
            return None # Couldn't extract matricula

    # False ID
    else:
        return None