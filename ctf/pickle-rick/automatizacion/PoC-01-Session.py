import requests as re

# Se inicia la variable sesion para guardar las cookies
sesion = re.Session()

# Defino las constantes del PoC de requests + session
LOGIN_ENDPOINT = 'http://10.128.167.86/login.php'
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

print('Imprimiendo contenido de la respuesta:')
print(respuesta.text)
