import socket

print("[*] Arrancando listener en el puerto 4445...")

# 1. Configuramos el conducto de red
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 2. Le decimos que escuche en nuestra máquina local (127.0.0.1), puerto 4445
s.bind(('127.0.0.1', 4445))
s.listen(1)

print("[*] Esperando a que alguien se conecte... (El script se pausa aquí)")

# 3. EL BLOQUEO: Python se detiene hasta que alguien llame
conexion, direccion = s.accept()
print(conexion)

# 4. Si pasa de aquí, es que alguien se ha conectado
print(f"[+] ¡ÉXITO! Alguien se ha conectado desde: {direccion}")

# Cerramos para no dejar basura
conexion.close()
s.close()
