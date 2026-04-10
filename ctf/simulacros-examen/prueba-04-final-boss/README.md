<h1 align="center">👹 Simulacro 04: Final Boss — Writeup</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-Local_Docker-blue?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Dificultad-Hard-red.svg" alt="Hard">
  <img src="https://img.shields.io/badge/OS-Linux-informational?logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
  <img src="https://img.shields.io/badge/Estado-Pendiente-lightgrey.svg" alt="Pendiente">
</p>

<p align="center">
  <i>Cuarto y último simulacro de examen en modalidad Caja Negra. El escenario de mayor complejidad, que replica las condiciones de un examen real combinando múltiples vectores de compromiso: FTP shell, LFI hacia acceso SSH, Library Hijacking y escalada mediante sudoers.</i>
</p>

---

> [!WARNING]
> **Aviso Legal.** Los contenidos de este repositorio han sido elaborados íntegramente con fines académicos en entornos locales controlados. Ninguna de las técnicas documentadas debe ser replicada fuera de un entorno con autorización explícita. El autor declina toda responsabilidad por el uso irresponsable de esta información.

---

> [!IMPORTANT]
> **Estado:** Writeup en elaboración. El escenario Docker está disponible y funcional. Este es el simulacro de mayor dificultad del módulo, que sirve como preparación directa para el examen final.

---

## 📑 Índice (Previsto)

1. Resumen Ejecutivo
2. Vectores de Ataque (OWASP / MITRE)
3. Herramientas Utilizadas
4. Fase 1 — Reconocimiento
5. Fase 2 — FTP Shell (Acceso Inicial)
6. Fase 3 — Local File Inclusion (LFI)
7. Fase 4 — Acceso SSH mediante LFI y Flag de Usuario
8. Fase 5 — Escalada Lateral: Python Library Hijacking
9. Fase 6 — Escalada Vertical: Sudoers Exploitation
10. Flags Obtenidas y Conclusión

---

## 🎯 Vectores de Ataque Previstos (OWASP / MITRE)

| Vector | Clasificación | Descripción |
|:---|:---|:---|
| **FTP Anonymous / Shell** | OWASP A05 — Misconfiguration | Acceso anónimo FTP + explotación de servicio mal configurado |
| **Local File Inclusion** | OWASP A01 — Broken Access Control / MITRE T1083 | LFI para exfiltrar ficheros sensibles del sistema (claves SSH) |
| **Python Library Hijacking** | MITRE T1574.006 | Inyección de librería maliciosa en ruta resoluble por Python |
| **Sudo Escalation** | MITRE T1548.003 | Abuso de entrada sudoers para elevar a root |

---

<hr>
<p align="center">
  <i>Writeup elaborado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.</i>
  <br><br>
  <b>Gabriel Godoy Alfaro</b>
</p>
