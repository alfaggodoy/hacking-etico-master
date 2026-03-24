<h1 align="center">🔓 Lab Local — HTTP RCE & Python Jailbreak</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white" alt="Python 3">
  <img src="https://img.shields.io/badge/Flask-REST%20API-black.svg?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
  <img src="https://img.shields.io/badge/Entorno-Local-informational?logo=linux&logoColor=white" alt="Local">
</p>

<p align="center">
  <i>Dos laboratorios locales de Hacking Ético diseñados para practicar explotación de RCE vía HTTP y evasión de un sistema de jailbreak Python con blacklist. Propuestos en el contexto del Máster en Ciberseguridad.</i>
</p>

---

> [!WARNING]
> **Aviso Legal.** Estos laboratorios son intencionalmente vulnerables y están diseñados para ejecutarse en un entorno local aislado con fines académicos. Nunca expongas estos servicios en una red pública. El autor declina cualquier responsabilidad por uso indebido.

---

## 📑 Índice

1. [Contexto y Origen](#-1-contexto-y-origen)
2. [Entorno y Despliegue](#-2-entorno-y-despliegue)
3. [Lab 1 — HTTP RCE API](#-3-lab-1--http-rce-api)
4. [Lab 2 — Python Jailbreak](#-4-lab-2--python-jailbreak)
5. [Estructura del Proyecto](#-5-estructura-del-proyecto)
6. [Writeups — Documentación por Lab](#-6-writeups--documentación-por-lab)

---

## 📌 1. Contexto y Origen

Este laboratorio engloba **dos retos locales** propuestos por el profesorado del módulo de Hacking Ético como ejercicios prácticos complementarios a los CTFs en plataformas externas. El objetivo es reproducir en local vulnerabilidades reales del mundo ofensivo:

- **HTTP RCE:** Explotación de un endpoint REST que ejecuta comandos del sistema sin sanitizar la entrada del usuario.
- **Python Jailbreak:** Evasión de un sistema de control de comandos (blacklist) implementado de forma defectuosa en Python.

Ambos escenarios están inspirados en vulnerabilidades documentadas en proyectos reales y plataformas CTF de la comunidad.

---

## 🛠️ 2. Entorno y Despliegue

### Requisitos

```bash
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Arrancar el Lab 1 (HTTP RCE API)

```bash
python3 api_rce.py
```

El servidor escucha en `http://127.0.0.1:5000`.

### Arrancar el Lab 2 (Python Jailbreak)

```bash
python3 jailbreak.py
```

Se abre una shell interactiva con el prompt `>>>`.

---

## 🌐 3. Lab 1 — HTTP RCE API

**Archivo:** `api_rce.py`

Una API REST construida con **Flask-RESTful** que expone un endpoint oculto. El servidor recibe comandos del sistema operativo como parámetro de la URL y los ejecuta directamente con `subprocess.run(shell=True)`, sin ningún tipo de validación ni sanitización.

### Vulnerabilidades presentes

| Vulnerabilidad | Descripción |
|:---|:---|
| **RCE (Remote Code Execution)** | El parámetro `<cmd>` se pasa sin filtrar a `subprocess.run(cmd, shell=True)` |
| **Secret key hardcodeada** | `app.secret_key = "EstoEstaDisenadoParaSerInseguro"` — fija en el código fuente |
| **Endpoint "secreto" predecible** | La ruta está en claro en el código fuente |
| **Sin autenticación** | Cualquiera con acceso al puerto puede ejecutar comandos |

### Endpoint objetivo

```
GET http://127.0.0.1:5000/supermegaultrasecretpath/sys/command/<cmd>
```

### Ejemplo de ataque

```bash
curl "http://127.0.0.1:5000/supermegaultrasecretpath/sys/command/whoami"
curl "http://127.0.0.1:5000/supermegaultrasecretpath/sys/command/cat%20/etc/passwd"
```

---

## 🧱 4. Lab 2 — Python Jailbreak

**Archivo:** `jailbreak.py`

Una shell interactiva Python que ejecuta los comandos del usuario mediante `os.system()`. Para "protegerse", implementa una **blacklist** de comandos peligrosos. Sin embargo, la lógica de comprobación tiene un fallo crítico de diseño que la hace trivialmente bypasseable.

### Blacklist aplicada

```python
["python", "python3", "bash", "sh", "php", "perl", "ruby",
 "ps", "kill", "cd", "ls", "pwd", "rm", "rmdir", "nc", "ncat",
 "xterm", "konsole", "mkdir", "touch", "sudo", "id", "su", "exec"]
```

### El fallo de diseño

La lógica solo comproba la **primera palabra** del comando cuando hay espacios — y después rompe el bucle inmediatamente sin comprobar el resto de palabras:

```python
for word in cmd.split(" "):
    if word in blacklist:
        print("Nope!")
        break
    else:
        os.system(cmd)   # ← ejecuta el comando completo
    break                # ← rompe tras el primer token siempre
```

Esto significa que comandos como `cat /etc/passwd` o `env; id` pueden ejecutarse libremente si la primera palabra no está en la lista.

### `exploit_jail.sh` — demostración de bypass por base64

```bash
#!/bin/bash
echo ZXhpdAo= | base64 -d | bash
# Decodifica "exit" y lo ejecuta a través de bash
```

Este script demuestra el concepto de evadir filtros de texto codificando el payload en base64, de forma similar a las técnicas usadas para eludir WAFs y filtros de input en entornos reales.

> [!TIP]
> `ZXhpdAo=` decodificado es simplemente `exit`. La clave del concepto está en el **método**, no en el payload concreto.

---

## 📁 5. Estructura del Proyecto

```text
httprce-jailbreak/
├── imagenes/           # Capturas y evidencias de los writeups
├── api_rce.py          # Lab 1 — Servidor Flask con endpoint RCE
├── jailbreak.py        # Lab 2 — Shell interactiva con blacklist defectuosa
├── exploit_jail.sh     # Script de demostración de bypass por base64
├── requirements.txt    # Dependencias Python (Flask, Flask-RESTful)
└── README.md
```

---

## 📝 6. Writeups — Documentación por Lab

> [!NOTE]
> Esta sección se completará con writeups detallados, capturas y técnicas de explotación empleadas.

---

### 🌐 Lab 1 — HTTP RCE API

**Categoría:** Remote Code Execution (RCE) | **Dificultad:** 🟢 Fácil

**Vector:** HTTP GET con parámetro de URL sin sanitizar ejecutado con `shell=True`.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá próximamente.*

*(Anexo Visual — `imagenes/lab1_rce.png`)*
<div align="center">
  <!-- <img src="imagenes/lab1_rce.png" alt="Explotación HTTP RCE" width="80%"/> -->
</div>

</details>

---

### 🧱 Lab 2 — Python Jailbreak

**Categoría:** Jailbreak / Evasión de filtros | **Dificultad:** 🟡 Media

**Vector:** Fallo lógico en la comprobación de la blacklist — solo se valida el primer token del comando.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá próximamente.*

*(Anexo Visual — `imagenes/lab2_jailbreak.png`)*
<div align="center">
  <!-- <img src="imagenes/lab2_jailbreak.png" alt="Bypass del Jailbreak Python" width="80%"/> -->
</div>

</details>

---

<hr>
<p align="center">
  <i>Documentado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.</i>
</p>
