# Sistema de Control de Acceso para Gimnasio 🏋️‍♂️🔐

Este es un sistema de control de acceso modular basado en Python y SQLite. Utiliza una cámara web o escáner USB para leer códigos QR, valida contra una base de datos local y mantiene un registro de auditoría con rotación de logs.

## 📁 Estructura del Proyecto

* `main.py`: El "cerebro" de la puerta. Se queda corriendo en bucle, enciende el escáner y valida el acceso.
* `qr_scanner.py`: Módulo de visión. Maneja la cámara web usando OpenCV y Pyzbar, tolerante a fallos de hardware.
* `admin_backend.py`: Panel de control (CRUD). Permite registrar usuarios, darlos de baja y leer el historial de la puerta.
* `database_connect.py` / `database_setup.py`: Archivos de configuración y conexión a la base de datos SQLite.
* `logs/`: Carpeta autogenerada que guarda el historial de accesos y de administrador (rotación de 100 días).
* `gimnasio.db`: Base de datos local (se genera automáticamente).

## 🛠️ Requisitos Previos e Instalación

Necesitas Python 3 instalado en tu sistema. Antes de correr el código, debes instalar las librerías de visión por computadora.

**Windows**

    \`\`\`bash
    pip install opencv-python-headless pyzbar
    \`\`\`

**Linux (Debian / Raspberry Pi OS)**

    \`\`\`bash
    sudo apt-get update
    sudo apt-get install libzbar0
    pip install opencv-python-headless pyzbar
    \`\`\`

## 🚀 Cómo usar el sistema

### 1. Preparar la Base de Datos (Solo la primera vez)
Para crear el archivo `gimnasio.db` y la estructura de tablas, corre el archivo de setup:

    \`\`\`bash
    python database_setup.py
    \`\`\`

### 2. Iniciar el Escáner de la Puerta
Este comando levanta la cámara y se queda esperando los códigos QR:

    \`\`\`bash
    python main.py
    \`\`\`
*(Para apagar el sistema de forma segura, presiona `Ctrl+C` en la terminal).*

### 3. Panel de Administrador
Abre una terminal nueva y ejecuta el panel para dar de alta usuarios o ver el historial:
    
    \`\`\`bash
    python admin_backend.py
    \`\`\`

## 📝 Notas de Hardware
* El sistema usa `cv2.CAP_DSHOW` en Windows para evitar crasheos al encender/apagar la cámara rápidamente. En Linux, OpenCV manejará los dispositivos de video nativos sin problema.
* Cuando se migre a hardware real (Raspberry Pi), la lógica de la chapa magnética (maglock) se integrará en `main.py` usando la librería `gpiozero`.
