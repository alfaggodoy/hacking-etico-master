<h1 align="center">🧩 Twisted CTF Challenges — 10 retos locales Twisted TCP</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/Framework-Twisted-darkblue.svg" alt="Twisted">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
</p>

<p align="center">
  <i>Batería de 10 desafíos CTF sobre protocolo TCP raw desarrollados con Twisted (Python). Retos de carácter académico propuestos por el profesorado del módulo de Hacking Ético, basados en recursos de la comunidad CTF y adaptados para entorno local con Docker.</i>
</p>

---

> [!NOTE]
> Estos retos son de **uso estrictamente académico y local**. Han sido desplegados en un entorno aislado (Docker) para practicar técnicas ofensivas de forma controlada dentro del marco del **Máster en Ciberseguridad**. No están pensados para ser expuestos en redes públicas.

---

## 📑 Índice

1. [Contexto y Origen](#-1-contexto-y-origen)
2. [Infraestructura y Despliegue](#-2-infraestructura-y-despliegue)
3. [Catálogo de Retos](#-3-catálogo-de-retos)
4. [Estructura del Proyecto](#-4-estructura-del-proyecto)
5. [Herramientas de Apoyo](#-5-herramientas-de-apoyo)
6. [Writeups — Documentación por Reto](#-6-writeups--documentación-por-reto)

---

## 📌 1. Contexto y Origen

Este repositorio contiene una batería de **10 desafíos CTF** de tipo *socket TCP* diseñados para practicar conceptos fundamentales de seguridad ofensiva:

- Criptografía clásica (Base64, XOR, César)
- Colisiones de hash y autenticación débil
- Inyección de comandos simulada
- Aritmética de bajo nivel (endianness, enteros grandes)
- **Jailbreak de sandboxes Python** (`eval` con `__builtins__=None`)
- Manipulación de protocolos (JSON, TCP raw)

Los retos fueron proporcionados por el profesorado del módulo de **Hacking Ético** y están basados en desafíos de la comunidad CTF disponibles en internet. El entorno de resolución, integración en Docker unificado y habilitación del reto 4 han sido realizados de forma propia.

---

## 🐳 2. Infraestructura y Despliegue

Todos los retos corren en un **único contenedor Docker** gestionado con Docker Compose. El servidor usa la librería **Twisted** para gestionar múltiples conexiones TCP concurrentes.

### Arrancar todos los retos

```bash
docker compose up --build
```

### Conectar a un reto

```bash
nc 127.0.0.1 <puerto>
```

### Parar los servicios

```bash
docker compose down
```

> [!TIP]
> Si modificas el código de algún reto, recuerda hacer `docker compose up --build` para reconstruir la imagen.

---

## 🎯 3. Catálogo de Retos

| # | Puerto | Nombre | Categoría | Dificultad |
|:-:|:------:|--------|-----------|:----------:|
| 1 | 9001 | Base64 Maze | Criptografía | 🟢 Fácil |
| 2 | 9002 | XOR Cipher | Criptografía | 🟢 Fácil |
| 3 | 9003 | Weak Hash Auth | Hashing / Brute Force | 🟡 Media |
| 4 | 9004 | Sandboxed REPL | Python Jailbreak | 🔴 Difícil |
| 5 | 9005 | CMD Injection | Inyección | 🟢 Fácil |
| 6 | 9006 | Caesar Shift | Criptografía | 🟢 Fácil |
| 7 | 9007 | Big Integer Sum | Aritmética | 🟢 Fácil |
| 8 | 9008 | Guess the Number | Algoritmia | 🟢 Fácil |
| 9 | 9009 | JSON Access | Manipulación de protocolo | 🟢 Fácil |
| 10 | 9010 | Endianness Puzzle | Bajo nivel | 🟡 Media |

---

## 📁 4. Estructura del Proyecto

```text
ctf/challs/
├── retos/                      # Módulo Python con los 10 retos (paquete importable)
│   ├── __init__.py
│   ├── c1.py                   # Reto 1 — Base64 Maze
│   ├── c2.py                   # Reto 2 — XOR Cipher
│   ├── c3.py                   # Reto 3 — Weak Hash Auth
│   ├── c4.py                   # Reto 4 — Sandboxed REPL (habilitado)
│   ├── c5.py                   # Reto 5 — CMD Injection
│   ├── c6.py                   # Reto 6 — Caesar Shift
│   ├── c7.py                   # Reto 7 — Big Integer Sum
│   ├── c8.py                   # Reto 8 — Guess the Number
│   ├── c9.py                   # Reto 9 — JSON Access
│   └── c10.py                  # Reto 10 — Endianness Puzzle
├── imagenes/                   # Capturas y evidencias de los writeups
├── server.py                   # Runner unificado — lanza los 10 retos
├── Dockerfile                  # Imagen Docker con Twisted
├── docker-compose.yml          # Orquestación del contenedor
├── solver_c3_bruteforce.py     # Script de fuerza bruta offline para el reto 3
├── solver_c7_bigsum.py         # Calculadora de suma de enteros grandes para el reto 7
└── README.md
```

---

## 🛠️ 5. Herramientas de Apoyo

### `solver_c3_bruteforce.py` — Bruteforce offline (Reto 3)

El reto 3 expone un token SHA256 truncado (primeros 6 dígitos en hex). Este script realiza la búsqueda offline contra `rockyou.txt` sin saturar el socket del servidor.

```bash
python3 solver_c3_bruteforce.py
```

> [!WARNING]
> Requiere tener `rockyou.txt` en `/usr/share/wordlists/rockyou.txt` (disponible por defecto en Kali/Parrot).

### `solver_c7_bigsum.py` — Suma de enteros grandes (Reto 7)

El reto 7 genera dos números aleatorios de 200 bits. Este script calcula la suma exacta de forma instantánea.

```bash
python3 solver_c7_bigsum.py
```

---

## 📝 6. Writeups — Documentación por Reto

> [!NOTE]
> Esta sección se irá completando progresivamente con writeups detallados, capturas y scripts de solución para cada reto.

---

### 🧩 Reto 1 — Base64 Maze `(puerto 9001)`

**Categoría:** Criptografía | **Dificultad:** 🟢 Fácil

**Descripción:** El servidor envía la flag codificada en base64 dos veces y representada en hexadecimal. El objetivo es decodificarla correctamente y devolvérsela al servidor.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c1_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c1_solucion.png" alt="Solución Reto 1" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 2 — XOR Cipher `(puerto 9002)`

**Categoría:** Criptografía | **Dificultad:** 🟢 Fácil

**Descripción:** El servidor cifra la flag con XOR usando una clave de un solo byte y devuelve el ciphertext en hex. Hay que encontrar la clave y enviarla en formato hexadecimal de dos dígitos.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c2_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c2_solucion.png" alt="Solución Reto 2" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 3 — Weak Hash Auth `(puerto 9003)`

**Categoría:** Hashing / Brute Force | **Dificultad:** 🟡 Media

**Descripción:** El servidor autentica comparando solo los primeros 6 dígitos hex del hash `SHA256(salt + password)`. Se filtra el token truncado. La solución pasa por un ataque de fuerza bruta offline con `rockyou.txt`.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c3_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c3_solucion.png" alt="Solución Reto 3" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 4 — Sandboxed REPL `(puerto 9004)`

**Categoría:** Python Jailbreak | **Dificultad:** 🔴 Difícil

**Descripción:** Un REPL Python "restringido" que evalúa expresiones con `eval(expr, {'__builtins__': None}, {})`. El objetivo es escapar el sandbox y leer el contenido del fichero `flag4.txt`.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c4_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c4_solucion.png" alt="Solución Reto 4" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 5 — CMD Injection `(puerto 9005)`

**Categoría:** Inyección | **Dificultad:** 🟢 Fácil

**Descripción:** Un buscador de ficheros que divide el input por `;`. El segundo token se interpreta como un comando de administrador. La inyección `search <cualquier_cosa>;reveal` revela la flag.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c5_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c5_solucion.png" alt="Solución Reto 5" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 6 — Caesar Shift `(puerto 9006)`

**Categoría:** Criptografía | **Dificultad:** 🟢 Fácil

**Descripción:** El servidor cifra la flag con un desplazamiento César aleatorio entre 1 y 25. Hay que probar los 25 posibles desplazamientos y enviar la flag en claro.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c6_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c6_solucion.png" alt="Solución Reto 6" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 7 — Big Integer Sum `(puerto 9007)`

**Categoría:** Aritmética | **Dificultad:** 🟢 Fácil

**Descripción:** El servidor genera dos enteros aleatorios de 200 bits y exige su suma exacta. Python maneja este tipo de aritmética de forma nativa sin desbordamiento.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c7_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c7_solucion.png" alt="Solución Reto 7" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 8 — Guess the Number `(puerto 9008)`

**Categoría:** Algoritmia | **Dificultad:** 🟢 Fácil

**Descripción:** El servidor elige un número entre 0 y 500 y responde con `higher` o `lower`. La búsqueda binaria lo resuelve en un máximo de 9 intentos.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c8_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c8_solucion.png" alt="Solución Reto 8" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 9 — JSON Access `(puerto 9009)`

**Categoría:** Manipulación de protocolo | **Dificultad:** 🟢 Fácil

**Descripción:** El servidor espera un objeto JSON con `username=admin` y `access=true` (booleano). Hay que enviar el JSON correctamente formado vía `nc`.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c9_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c9_solucion.png" alt="Solución Reto 9" width="80%"/> -->
</div>

</details>

---

### 🧩 Reto 10 — Endianness Puzzle `(puerto 9010)`

**Categoría:** Bajo nivel | **Dificultad:** 🟡 Media

**Descripción:** El servidor envía un valor de 32 bits representado en little-endian (hex). Hay que interpretarlo en big-endian y devolver el valor decimal resultante.

<details>
<summary><b>▸ Writeup (click para expandir)</b></summary>
<br>

> 📋 *Pendiente de documentar — Se añadirá la semana que viene.*

*(Anexo Visual — `imagenes/c10_solucion.png`)*
<div align="center">
  <!-- <img src="imagenes/c10_solucion.png" alt="Solución Reto 10" width="80%"/> -->
</div>

</details>

---

<hr>
<p align="center">
  <i>Documentado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.</i>
</p>
