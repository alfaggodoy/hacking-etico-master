# Librerias neceasrias
import hashlib # <-- Para hashear (Por ej. sha256)

# Constantes necesarias
SALT = "s0m3_s4lt"
SECRET_PASSWORD = b"BRUTE_ME"
TOKEN_TRUNC = '9689a7'

# Hashear con la SALT y el TOKEN_TRUNC
with open("/usr/share/wordlists/rockyou.txt", "r", encoding="utf-8") as f:
    for linea in f:
        palabra = linea.strip()
        hash_palabra = hashlib.sha256(SALT.encode() + palabra.encode()).hexdigest()
        if hash_palabra[:6] == TOKEN_TRUNC:
            print(f"Encontrado: {palabra}")
            break
