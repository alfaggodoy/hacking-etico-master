<h1 align="center">🧑‍💻 Simulacro 03: Web Dev — Writeup</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-Local_Docker-blue?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Dificultad-Medium-yellow.svg" alt="Medium">
  <img src="https://img.shields.io/badge/OS-Linux-informational?logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
  <img src="https://img.shields.io/badge/Estado-Pendiente-lightgrey.svg" alt="Pendiente">
</p>

<p align="center">
  <i>Tercer simulacro de examen en modalidad Caja Negra. Escenario centrado en vectores web: subida de ficheros sin restricciones, filtración de claves SSH en código fuente, y escalada mediante sudo con el binario <code>less</code>.</i>
</p>

---

> [!WARNING]
> **Aviso Legal.** Los contenidos de este repositorio han sido elaborados íntegramente con fines académicos en entornos locales controlados. Ninguna de las técnicas documentadas debe ser replicada fuera de un entorno con autorización explícita. El autor declina toda responsabilidad por el uso irresponsable de esta información.

---

> [!IMPORTANT]
> **Estado:** Writeup en elaboración. El escenario Docker está disponible y funcional. La documentación se publicará al completar el compromiso.

---

## 📑 Índice (Previsto)

1. Resumen Ejecutivo
2. Vectores de Ataque (OWASP / MITRE)
3. Herramientas Utilizadas
4. Fase 1 — Reconocimiento
5. Fase 2 — Subida de Fichero sin Restricciones (Unrestricted File Upload)
6. Fase 3 — Filtración de Clave SSH en Código Fuente
7. Fase 4 — Acceso SSH y Flag de Usuario
8. Fase 5 — Escalada Vertical: Sudo less
9. Flags Obtenidas y Conclusión

---

## 🎯 Vectores de Ataque Previstos (OWASP / MITRE)

| Vector | Clasificación | Descripción |
|:---|:---|:---|
| **Unrestricted File Upload** | OWASP A04 — Insecure Design | Subida de webshell PHP sin validación de tipo o extensión |
| **Source Code Disclosure** | OWASP A05 — Misconfiguration | Filtración de claves SSH en código fuente accesible |
| **Sudo Binary Exploitation** | MITRE T1548.003 | `less` con NOPASSWD → shell mediante escape de paginador |

---

<hr>
<p align="center">
  <i>Writeup elaborado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.</i>
  <br><br>
  <b>Gabriel Godoy Alfaro</b>
</p>
