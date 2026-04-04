#!/usr/bin/env python3
import os

print("""
===========================================
 Bienvenido a la Calculadora Remota Segura
===========================================
""")

while True:
    try:
        data = input("Introduce la operación matemática (o salir): ")
        if data.lower() == 'salir':
            print("Adios.")
            break
            
        # VULNERABILIDAD = eval() con user input directo sin __builtins__ limpiado
        resultado = eval(data)
        print("Resultado:", resultado)
    except Exception as e:
        print("Operación no válida:", e)
