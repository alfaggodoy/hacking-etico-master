#!/usr/bin/env python3
print("=== PYTHON JAILBREAK EXTREMO ===")
print("No puedes usar: os, system, eval, exec, import, open")
blacklist = ["os", "system", "eval", "exec", "import", "open"]

while True:
    try:
        user_input = input(">>> ")
        for word in blacklist:
            if word in user_input:
                print(f"Palabra prohibida detectada: {word}")
                break
        else:
            # Si no hay palabras prohibidas, lo evaluamos con eval. Pero eval, open y exec estan prohibidos, 
            # Hay que usar metodos builtins o de clases como: ().__class__.__bases__[0]...
            print(eval(user_input, {'__builtins__': {}}))
    except Exception as e:
        print(e)
