import requests as re

respuesta = re.post('http://10.128.161.83/')

if respuesta.status_code == 200:
	print('Conexion establecida. Imprimiendo respuesta:')
	print(respuesta)
elif respuesta.status_code == 404:
	print('Error de conexion!')
