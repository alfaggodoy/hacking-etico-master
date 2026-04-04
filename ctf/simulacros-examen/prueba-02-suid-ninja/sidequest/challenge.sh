#!/bin/bash
echo "Mini-Consola Restringida. Escribe el fichero que quieres leer:"
read input
# VULNERABILIDAD: Blind Command Injection
cat "$input" 2>/dev/null
