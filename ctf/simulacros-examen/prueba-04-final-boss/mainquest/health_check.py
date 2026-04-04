import os
import struct

# El directorio actual tiene permisos plenos. Un atacante puede crear struct.py.
# El administrador ejecuta esto periodicamente.

try:
    with open('/tmp/health_log.txt', 'a') as f:
        f.write("System OK.\n")
except:
    pass
