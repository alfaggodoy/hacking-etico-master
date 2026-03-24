<h1 align="center">🛡️ Hacking Ético — Máster en Ciberseguridad</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white" alt="Python 3">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
  <img src="https://img.shields.io/badge/Base-ASIR-informational?logo=linux&logoColor=white" alt="Base ASIR">
</p>

<p align="center">
  <i>Repositorio de prácticas, retos CTF y laboratorios del módulo de Hacking Ético. Incluye writeups documentados, herramientas de automatización propias y entornos de laboratorio local con Docker.</i>
</p>

---

## 📁 Estructura del Repositorio

```text
hacking-etico-master/
└── ctf/
    ├── challs/              🧩 10 retos TCP locales con Twisted — un único contenedor Docker
    ├── thm/                 🌐 Retos de TryHackMe
    │   └── easy/
    │       ├── pickle-rick/ 🥒 Writeup + Autopwn automatizado (Python puro)
    │       └── wgel-ctf/   🫠 Writeup completo con 19 capturas
    └── laboratorios/        🔬 Labs locales vulnerables para práctica ofensiva
        └── httprce-jailbreak/
```

---

## 🧩 CTF Challs — Retos TCP Twisted

> `ctf/challs/`

Batería de **10 retos CTF** sobre protocolo TCP raw usando la librería **Twisted**. Todos corren en un único contenedor Docker. Cubre criptografía clásica, hashing débil, inyección de comandos, aritmética de bajo nivel y Python jailbreak.

📄 [Ver README de Challs](ctf/challs/README.md)

---

## 🌐 TryHackMe

> `ctf/thm/`

### 🥒 Pickle Rick — Autopwn

Automatización total (0-clicks) del CTF *Pickle Rick* de TryHackMe. Desarrollada con Python nativo (sin Metasploit): autenticación HTTP, RCE vía reverse shell, escalada de privilegios y persistencia SSH.

📄 [Ver README de Pickle Rick](ctf/thm/easy/pickle-rick/README.md)

---

### 🫠 Wgel CTF

Writeup completo del CTF *Wgel* de TryHackMe. Enumeración en tres fases con `gobuster`, explotación de clave SSH expuesta y escalada de privilegios con `wget --post-file` vía GTFOBins.

📄 [Ver README de Wgel CTF](ctf/thm/easy/wgel-ctf/README.md)

---

## 🔬 Laboratorios Locales

> `ctf/laboratorios/`

### 🔓 HTTP RCE & Python Jailbreak

Dos labs locales intencionalmente vulnerables:
- **HTTP RCE API** — Flask REST API con ejecución de comandos sin sanitizar
- **Python Jailbreak** — Shell interactiva con blacklist bypasseable por diseño

📄 [Ver README de Laboratorios](ctf/laboratorios/httprce-jailbreak/README.md)

---

> [!NOTE]
> Este repositorio está en desarrollo activo. Los writeups de los retos CTF locales (`challs`) y los laboratorios se irán completando progresivamente.

<hr>
<p align="center">
  <i>Desarrollado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.</i>
</p>
