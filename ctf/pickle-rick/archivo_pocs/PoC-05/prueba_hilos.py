import threading
import time

# Esta es la tarea que simulará ser nuestro Netcat (se queda bloqueada)
def escuchar_puerto(puerto):
    print(f"[HILO SECUNDARIO] Abriendo el puerto {puerto}...")
    print(f"[HILO SECUNDARIO] Me quedo esperando conexiones (bloqueado 5 segundos)...")
    
    # time.sleep(5) congela este hilo durante 5 segundos
    time.sleep(5) 
    
    print(f"[HILO SECUNDARIO] ¡Conexión recibida! Termino mi trabajo.")

# --- PROGRAMA PRINCIPAL ---
print("[PROGRAMA PRINCIPAL] Arrancando el ataque...")

# 1. Preparamos el Hilo (Contratamos a un ayudante)
# target = la función que va a ejecutar
# args = los parámetros que le pasamos a esa función (IMPORTANTE: la coma al final es obligatoria si es un solo argumento)
hilo_listener = threading.Thread(target=escuchar_puerto, args=(4445,))

# 2. Arrancamos el Hilo (Le decimos al ayudante que empiece)
hilo_listener.start()

# 3. Nuestro programa principal sigue su camino INMEDIATAMENTE sin esperar
print("[PROGRAMA PRINCIPAL] El ayudante está escuchando. Yo voy a disparar el exploit.")
print("[PROGRAMA PRINCIPAL] 3... 2... 1... ¡Pum! Exploit enviado.")
print("[PROGRAMA PRINCIPAL] Mi trabajo principal ha terminado. Esperando a que el ayudante acabe...")

# Esta línea no es obligatoria, pero le dice al programa principal 
# que no se cierre del todo hasta que el hilo_listener termine su trabajo.
hilo_listener.join()

print("[PROGRAMA PRINCIPAL] Todo finalizado. ¡Adiós!")
