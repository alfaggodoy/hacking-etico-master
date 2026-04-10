<h1 align="center">🎯 Simulacros de Examen — Hacking Ético</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-Local_Docker-red?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Dificultad-Progresiva-brightgreen.svg" alt="Dificultad">
  <img src="https://img.shields.io/badge/OS-Linux-informational?logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
</p>

<p align="center">
  <i>Simulacros de operación ofensiva en modalidad Caja Negra integral. Este repositorio alberga los laboratorios efímeros de entrenamiento personal y sus futuros writeups documentados. Su propósito es fortalecer la enumeración web, escalada de privilegios y persistencia de cara al examen final del módulo, estructurando las debilidades puras vistas en la teoría.</i>
</p>

---

> [!WARNING]
> **Aviso Legal.** Este directorio ha sido elaborado y preconfigurado con fallos deliberadamente inseguros con fines exclusivamente académicos. Las técnicas documentadas deben aplicarse únicamente localmente bajo un entorno confinado supervisado. El autor declina toda responsabilidad por extralimitaciones sobre esta base.

---

## 📑 Índice

1. [Resumen Ejecutivo](#-1-resumen-ejecutivo)
2. [Inventario de Simulacros (Dockers)](#-2-inventario-de-simulacros-dockers)
3. [Herramientas Utilizadas](#-3-herramientas-utilizadas)
4. [Instrucciones de Despliegue Técnico](#-4-instrucciones-de-despliegue-técnico)

---

## 📌 1. Resumen Ejecutivo

Esta sub-sección del repositorio es mi campo de pruebas definitivo previo al examen de Hacking Ético. He estructurado y orquestado cuatro escenarios Docker efímeros de complejidad ascendente donde ninguno regala el acceso directo. Tras el análisis de las Side Quests originales, se ha procedido a una limpieza de aquellas que carecían de contexto de examen (Jailbreaks extremos o inyecciones ciegas aisladas), manteniendo un enfoque 100% orientado a la metodología de auditoría real.

A lo largo de mis iteraciones de estudio, resolveré cada uno de estos escenarios publicando los *Writeups* definitivos. Plasmaré con total crudeza y capturas de pantalla desde los primeros sondeos en `nmap` y derrapes web infructuosos, hasta la exfiltración de la flag `root` definitiva.

---

## 📖 Manual de Operaciones (Cheatsheet)

Para afrontar estos Dockers con garantías y replicar las condiciones reales del examen local, apóyate en la **[Guía de Pentesting y Comandos](guia-pentesting.md)** que hemos estructurado. Contiene todo el arsenal estrictamente offline: enumeración, payloads locales, tty y *LoLBins*, descartando recursos online de los que no dispondremos el día de la prueba.

---

## 📁 2. Inventario de Simulacros (Dockers)

*Directorios de máquinas vulnerables enfocadas al asalto integral. Los enlaces a los Writeups mutarán de "Pendiente" a "Leer" a medida que complete los retos y su archivo fotográfico.*

| Entorno / CTF | Nivel | Vectores de Ataque | Estado | Writeup |
|:---|:---:|:---|:---:|:---:|
| 👊 **Prueba 1 — El Básico** | 🟢 Easy | FTP backdoor, RCE PHP, Cronjob hijack, Sudo wget | ✅ Completo | [📖 Leer Writeup](prueba-01-basico) |
| 🤷 **Prueba 2 — SUID Ninja** | 🟡 Med | Python Library Hijacking, Sudo find, SUID exploitation | ✅ Completo | [📖 Leer Writeup](prueba-02-suid-ninja) |
| 🧑‍💻 **Prueba 3 — Web Dev** | 🟡 Med | Unrestricted file upload, SSH keys leak, Source code leak, Sudo less | ⏳ Pendiente | [📁 Directorio](prueba-03-web-dev) |
| 👹 **Prueba Final — Boss Stage** | 🔴 Hard | FTP shell, LFI to SSH, Library Hijacking, Sudoers escalation | ⏳ Pendiente | [📁 Directorio](prueba-04-final-boss) |

---

## 🛠️ 3. Herramientas Utilizadas

Para afrontar estos simulacros bajo un régimen estricto de Caja Negra offline, se emplea un stack de utilidades calcadas a mi arsenal oficial de combate en la máquina atacante Kali:

| Herramienta | Propósito |
|:---|:---|
| `nmap` | Diagnóstico activo y barrido sintáctico de puertos perimetrales del contenedor. |
| `gobuster` | Fuzzing dinámico inyectado a los directorios de los servidores HTTP/Apache levantados. |
| `nc` (Netcat) | Emulador receptor instanciado localmente para captar las conexiones (Reverse Shells) y escupir payloads brutos. |
| `ssh` | Utilidad pilar para aplicar inicios de sesión legítimos inyectando llaves RSA previamente filtradas por LFI (Data Leakage). |
| `GTFOBins` | Bibliografía documental por excelencia (ahora desplegada 100% offline nativamente vía Docker) para certificar la ruta crítica cuando toque elevar privilegios. |
| `RevShells` | Entorno visual contenedorizado vía Docker para generar "on-the-fly" payloads de reverse shells encriptados y bypasses para Netcat o bash. |

---

## 🚀 4. Instrucciones de Despliegue Técnico

La infraestructura subyacente de cada prueba es 100% contenerizada, replicando cajas lógicas aisladas. Dado que este entorno se lanza desde una máquina atacante local (p. ej. Kali Linux), es crucial verificar las dependencias modernas de Docker V2:

**0. Requisitos Previos (Inicialización):**
Es necesario tener instalado el módulo oficial de compose y encender el demonio (Kali no arranca servicios por defecto):
```bash
sudo apt update && sudo apt install docker.io docker-compose-plugin
sudo systemctl start docker
```

**1. Levantar el laboratorio (Ejemplo Prueba 1):**
Mediante terminal atacante me dirijo a la ruta elegida y empujo la orquestación en *modo detached*.
```bash
cd prueba-01-basico
sudo docker compose up -d --build
```
*(Se adhiere incondicionalmente el flag `--build` asegurando la purga y digestión inmaculada de la imagen para que las vulnerabilidades sean siempre vírgenes al despliegue).*

**2. Localizar el Target (Targeting Activo):**
Para focalizar el arsenal directamente a la coraza del contenedor real sin apuntar al `localhost` del daemon anfitrión, saca primero el *NAME* exacto con `sudo docker ps` (¡fíjate en la última columna de la derecha!) y luego extrae su IP con un simple `grep`:
```bash
sudo docker inspect exam_mainquest | grep IPAddress
```
*(Si te fijas en tu `docker ps`, "prueba-01-basico-mainquest" es la IMAGEN, pero el "NAME" oficial del contenedor al final de la línea es `exam_mainquest`).*

**3. Anti-forense y Limpieza de Trazas (Modo Efímero):**
Concluido el reto de facto, purgo el entorno. Este comando es vital porque hace el entorno **100% efímero**: frena los contenedores, los aniquila físicamente, y con la flag `-v` destruye cualquier volumen o rastro de datos temporal. No deja ni las mijitas.
```bash
sudo docker compose down -v
```

---

<hr>
<p align="center">
  <i>Material diseñado y elaborado como parte operativa del módulo de Hacking Ético — Máster en Ciberseguridad.</i>
  <br><br>
  <b>Gabriel Godoy Alfaro</b>
</p>
