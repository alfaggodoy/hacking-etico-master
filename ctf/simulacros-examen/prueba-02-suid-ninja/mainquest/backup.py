import os
import random

# Este script importa random. Como el directorio /opt/scripts tiene permisos 777
# un atacante puede crear random.py en esta misma carpeta y será cargado en vez del módulo original.

try:
    numero = random.randint(1, 100)
    with open('/tmp/backup_log.txt', 'a') as f:
        f.write(f"Backup run id: {numero}\n")
except Exception as e:
    pass
