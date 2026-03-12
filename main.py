"""
Sistema de Control de Acceso para Gimnasio.

Este script gestiona la entrada de miembros validando una matrícula o código QR 
(leído a través de un escáner USB que emula un teclado) contra una base de datos 
local SQLite. Si el usuario está activo, simula el envío de una señal a una 
chapa magnética (maglock) para abrir la puerta.
"""

import sqlite3 #Base de datos
import time

databaseTest = [394350, 394569, 394468]

matricula=input("Escribe tu matricula: ")
for i in range(databaseTest):
    if matricula==databaseTest[data]:
        print("Bienvenido")
    else:
        print("Matricula invalida :/")

#Todavia no es funcional, solo el concepto