<p align="center">
  <img src="docs/banner.webp" alt="HireWire — Remote Job Scout: un agente de IA que busca, filtra y sigue trabajos remotos" width="100%">
</p>

<p align="center">
  <a href="#-cómo-empezar"><img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="LICENSE"><img alt="Licencia: MIT" src="https://img.shields.io/badge/licencia-MIT-2f5d50"></a>
  <img alt="Funciona con Claude, Codex, OpenCode, Antigravity" src="https://img.shields.io/badge/funciona%20con-Claude%20·%20Codex%20·%20OpenCode%20·%20Antigravity-7fc2a8">
  <img alt="Sin claves de IA" src="https://img.shields.io/badge/claves%20de%20IA-ninguna-lightgrey">
</p>

<p align="center">
  <b>Encontrá trabajos remotos que <i>realmente</i> podés tomar desde tu país, ordenados según tu experiencia real,<br>con un CV a medida y apto para ATS para cada uno que elijas.</b>
</p>

<p align="center">
  <b>Español</b> · <a href="README.en.md">English</a>
</p>

---

## 📋 Contenido

- [🤔 Por qué HireWire](#-por-qué-hirewire)
- [✨ Cómo funciona](#-cómo-funciona)
- [🖥️ El tablero](#️-el-tablero)
- [🚀 Cómo empezar](#-cómo-empezar) (unos 10 minutos)
- [➕ Extra: sumá LinkedIn e Indeed](#-extra-sumá-linkedin-e-indeed) (opcional)
- [🧭 Uso diario](#-uso-diario)
- [💸 Cuánto cuesta](#-cuánto-cuesta)
- [🔎 Fuentes de avisos](#-fuentes-de-avisos)
- [🛡️ Qué lo hace distinto](#️-qué-lo-hace-distinto)
- [🔒 Tu privacidad](#-tu-privacidad)
- [🧰 Problemas frecuentes](#-problemas-frecuentes)
- [⚙️ Por dentro](#️-por-dentro)
- [👩‍💻 Autora](#-autora)

---

## 🤔 Por qué HireWire

Los portales de empleo están llenos de puestos "remotos" que no son remotos para vos:

- ❌ "Remote — US only"
- ❌ "Trabajá desde cualquier lugar"… y en la letra chica *"must be authorized to work in the United States"*
- ❌ Puestos híbridos o presenciales etiquetados como remotos

Si vivís fuera de EE. UU. o Europa, perdés horas leyendo avisos a los que nunca vas a poder acceder. Y cuando por fin aparece uno que encaja, reescribir el CV lleva otra hora, con la tentación de exagerar.

**HireWire lee por vos.** Solo te muestra trabajos que dicen, con sus propias palabras, que son remotos **y** que aceptan el lugar donde vivís. Después escribe un CV honesto, armado solo con hechos que confirmaste.

> 🙋 **Vos tenés el control.** HireWire nunca postula, nunca manda mensajes y nunca completa formularios. Busca, ordena y prepara. Vos decidís y postulás.

---

## ✨ Cómo funciona

<p align="center">
  <img src="docs/how-it-works.es.png" alt="Flujo de HireWire: instalación, perfil, rutas, búsqueda con filtro gratuito y clasificador de IA, tablero local, CV a medida, postulás vos" width="100%">
</p>

<sub>Versión interactiva: descargá <a href="docs/how-it-works.es.html"><code>docs/how-it-works.es.html</code></a> y abrilo en tu navegador. Diagrama hecho con <a href="https://github.com/tt-a1i/archify">Archify</a>.</sub>

| Paso | Vos hacés | HireWire hace |
| --- | --- | --- |
| **1. Perfil** | Compartís tu CV y respondés una entrevista corta (15–20 min). | Convierte tu experiencia en un **banco de evidencia**: cada hecho tiene un código y un límite (lo que hiciste y en lo que participaste, las herramientas que *no* usaste). |
| **2. Rutas** | Contás dónde vivís, dónde podés trabajar legalmente y si aceptás híbrido. | Propone 2 a 5 familias de puestos acordes a tu evidencia y arma la búsqueda: consultas, filtros y reglas de ubicación hechas para **tu** situación. |
| **3. Búsqueda** | Pedís una búsqueda cuando quieras. | Trae avisos de 5 portales gratis (y, si querés, de LinkedIn e Indeed), descarta gratis los repetidos y los falsos remotos, y la IA lee los más relevantes: prioridad A / B / C, con la frase exacta que prueba que podés postular. |
| **4. CV** | Marcás los avisos que te gustan y tocás **CV en español** o **CV en inglés**. | Vuelve a verificar el aviso original y escribe un **CV en formato Harvard** (DOCX + PDF) usando solo hechos de tu banco de evidencia. |

---

## 🖥️ El tablero

Corre en tu computadora, en `http://localhost:8765`. No se sube nada.

<p align="center">
  <img src="docs/dashboard.png" alt="Tablero de HireWire con avisos de ejemplo ficticios ordenados A y B, cada uno con evidencia de ubicación, ruta y motivo" width="100%">
</p>

<sub>Datos de ejemplo ficticios. El tablero tiene botón para cambiar a español.</sub>

**Recorrido:** Por revisar → Me interesa → CV listo → Aplicados. Cuando descartás un aviso elegís el motivo con un clic ("ventas o atención", "no es remoto de verdad"…), y el agente puede usar esos motivos para afinar las próximas búsquedas.

---

## 🚀 Cómo empezar

> 💡 **No necesitás ninguna clave de IA ni de API.** HireWire usa la IA del agente que ya tenés: sale de tu plan de Claude, ChatGPT o Google, no de una cuenta aparte. Para empezar tampoco hace falta Apify: las búsquedas usan portales gratuitos.

### Qué necesitás

1. **Un agente de IA.** Abajo te ayudamos a elegir.
2. **Python 3.10 o más nuevo.** No hace falta que lo instales vos: el agente lo revisa y, si falta, te pide permiso para instalarlo.

No hace falta saber programar.

### ¿Qué agente uso?

| Agente | Cómo se usa | ¿Sirve sin pagar? |
| --- | --- | --- |
| **Claude, app de escritorio** (pestaña Code) · ⭐ recomendado | Con clics, sin terminal | No. Necesita Claude Pro o un plan superior. |
| **[Antigravity](https://antigravity.google)** (Google) | Con clics, sin terminal | Sí. Plan gratis con una cuenta de Google, con límites semanales. |
| **[Codex](https://openai.com/codex/)** (OpenAI) | App de escritorio o terminal | Sí. Viene incluido en ChatGPT Free, con poco uso. |
| **[OpenCode](https://opencode.ai)** | Terminal | Sí, con sus modelos gratuitos (van cambiando). |

**Con un plan gratis** alcanza para la entrevista, las búsquedas y algunos CVs, pero los límites de uso se terminan antes. Pedile al agente que clasifique menos avisos por búsqueda (por ejemplo, 20). Los modelos gratuitos también se equivocan más: revisá con más cuidado las clasificaciones y cada CV antes de usarlo.

<sub>Planes vigentes en septiembre de 2026. Cambian seguido: confirmalos en la página de cada agente.</sub>

### Camino recomendado: la app de escritorio de Claude

Todo con clics, sin abrir una terminal.

1. Descargá la app desde **[claude.com/download](https://claude.com/download)** e iniciá sesión.
2. Abrí la pestaña **Code** y empezá una sesión nueva. Cuando te pida una carpeta, elegí **Documentos**.
3. Pegá esta frase y enviala:

   ```text
   Instalá HireWire desde https://github.com/mickybuilds/hirewire-remote_job_scout siguiendo su INSTALL.md.
   ```

   El agente crea la carpeta `HireWire`, descarga los archivos, revisa Python y **arranca la entrevista en la misma sesión**. Si necesita instalar algo, te pide permiso y te explica qué hace. Desde ahí te guía: entrevista, rutas, primera búsqueda y tablero.
4. **Las próximas veces**, empezá una sesión nueva eligiendo la carpeta **Documentos → HireWire** y escribí `/hirewire`: sigue donde quedaste. Así también funcionan los comandos con barra (`/search`, `/cv`…), que en la sesión de instalación pueden no andar.

<details>
<summary><b>Otras opciones: Antigravity, Codex, OpenCode y agentes de terminal</b></summary>

<br>

Con cualquier agente, el proceso es el mismo:

1. Abrí el agente en la carpeta donde quieras instalarlo (por ejemplo, Documentos) y pegale la frase de instalación de arriba. Instala y arranca la entrevista ahí mismo.
2. Las próximas veces, abrí la carpeta `HireWire` en el agente y escribí `/hirewire`, o *"empezar HireWire"* si tu agente no usa comandos con barra.

| Agente | Cómo abrir la carpeta `HireWire` las próximas veces |
| --- | --- |
| **Antigravity** (app) | Abrí la carpeta `HireWire` como espacio de trabajo (workspace). |
| **Codex** (app) | Elegí la carpeta `HireWire` como proyecto. |
| **Claude Code** (terminal) | Entrá a la carpeta con `cd` y ejecutá `claude`. |
| **Codex** (terminal) | Entrá a la carpeta con `cd` y ejecutá `codex`. |
| **OpenCode** | Entrá a la carpeta con `cd` y ejecutá `opencode`. |
| **Antigravity CLI** | Entrá a la carpeta con `cd` y ejecutá `agy`. |
| **Gemini CLI** (con plan pago de Google AI) | Entrá a la carpeta con `cd` y ejecutá `gemini`. |

</details>

---

## ➕ Extra: sumá LinkedIn e Indeed

Es opcional. Los portales gratis alcanzan para empezar; sumalo si después querés más volumen.

HireWire busca en LinkedIn e Indeed a través de **Apify**, un servicio que da USD 5 de crédito gratis por mes. Una búsqueda en Indeed cuesta centavos y una en LinkedIn, unos USD 0,40. Cada búsqueda tiene un tope de gasto, y el agente te pide OK antes de gastar crédito.

1. **Creá una cuenta gratis.** Entrá a **[apify.com](https://apify.com)** y hacé clic en **Sign up free**. Podés registrarte con Google, GitHub o un correo. No piden tarjeta.
2. **Copiá tu token.** En la consola de Apify: **Settings** (menú de la izquierda) → pestaña **API & Integrations** → **Personal API tokens** → ícono de **copiar**. El token empieza con `apify_api_`.
3. **Guardalo vos en el archivo `.env`.** Decile al agente: *"Abrí el archivo .env para pegar mi token de Apify"*. Te abre el archivo; pegás el token justo después del signo igual, guardás y cerrás:

   ```text
   APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxx
   ```

   > ⚠️ **No le pegues el token al agente en el chat.** El token funciona como una contraseña: va solo en el archivo `.env`, que queda en tu computadora y nunca se sube. Así no pasa por la IA.

4. **Activá las fuentes.** Decile al agente: *"Sumá Indeed y LinkedIn"*.

> ⚖️ **Sobre LinkedIn.** Extraer datos de LinkedIn va contra sus términos de uso, por eso HireWire lo deja apagado y te pide confirmación antes de activarlo. El servicio de Apify lee avisos públicos sin usar tu cuenta ni tu contraseña de LinkedIn, pero lo usás bajo tu responsabilidad. Si preferís no usarlo, Indeed se puede activar solo.

---

## 🧭 Uso diario

| Querés… | Decile a tu agente |
| --- | --- |
| Seguir donde quedaste | `/hirewire` o *"¿qué sigue?"* |
| Hacer una búsqueda nueva | `/search` o *"buscá trabajos"* |
| Abrir el tablero | *"abrí el tablero"* |
| Un CV para un aviso | Tocá **CV en español / CV en inglés** en el tablero y pegá el pedido copiado |
| Corregir avisos que no son remotos o no aceptan tu país | *"me aparecen trabajos que no son remotos"*: el agente encuentra el patrón y ajusta las reglas |
| Actualizar tu experiencia | `/profile` |
| Cambiar tipos de puesto, país o preferencias | `/routes` |

Si sumaste LinkedIn o Indeed, antes de cada búsqueda con esas fuentes el agente te dice el tope de gasto y espera tu OK.

---

## 💸 Cuánto cuesta

| Concepto | Costo |
| --- | --- |
| HireWire | Gratis y de código abierto (MIT) |
| Cinco portales gratuitos | Gratis, sin cuenta |
| Uso de IA | Sale del plan de tu agente, sin claves aparte. Cada búsqueda clasifica por defecto hasta 60 avisos, los más relevantes, después de los filtros gratuitos. |
| Indeed (opcional, vía Apify) | ≈ USD 0,05 por búsqueda completa |
| LinkedIn (opcional, vía Apify) | ≈ USD 0,40 por búsqueda completa |
| Plan gratis de Apify | USD 5 de crédito por mes → varias búsquedas completas |

Cada fuente de Apify tiene un tope de gasto (`max_spend_usd`), así que una búsqueda nunca lo puede superar.

---

## 🔎 Fuentes de avisos

| Fuente | Costo | Por qué está |
| --- | --- | --- |
| [Himalayas](https://himalayas.app) | gratis | Remotos filtrados por tu país |
| [Built In](https://builtin.com) | gratis | Remotos con la lista exacta de países que pueden aplicar |
| [We Work Remotely](https://weworkremotely.com) | gratis | Avisos pagos, casi sin spam; región por aviso |
| [Remotive](https://remotive.com) | gratis | Remotos curados; región por aviso |
| [Jobicy](https://jobicy.com) | gratis | Remotos filtrados por región |
| [Get on Board](https://www.getonbrd.com) | gratis, opcional | Tecnología en Latinoamérica |
| Indeed (vía Apify) | ≈ USD 0,05, opcional | Volumen extra del sitio de Indeed de tu país |
| LinkedIn (vía Apify) | ≈ USD 0,40, opcional | El mayor volumen. Apagado por defecto: [leé el aviso](#-extra-sumá-linkedin-e-indeed) |

Los repetidos entre fuentes se eliminan antes de que la IA lea nada. Después de cada búsqueda, el agente informa cuántos avisos A y B aportó cada fuente, así podés apagar las que no rinden. Cada aviso enlaza a su publicación original.

---

## 🛡️ Qué lo hace distinto

- **🌎 Detecta el falso remoto, adaptado a vos.** Un aviso es *elegible* solo con dos citas: una que pruebe que es remoto y otra que pruebe que acepta el lugar donde vivís o podés trabajar legalmente. "Remote" a secas queda como *dudoso*. Si el aviso no nombra ningún país, la IA lo lee entero buscando pistas ("401(k)" o "seguro médico de EE. UU." apuntan a solo EE. UU.; "contratamos por Deel" apunta a internacional).
- **🧾 Banco de evidencia contra CVs inventados.** Cada línea del CV tiene que rastrearse a un hecho confirmado, y cada hecho tiene sus propios límites. Nunca convierte una participación en liderazgo.
- **📄 CV formato Harvard sin relleno de IA.** Una columna, títulos estándar, fechas alineadas a la derecha, legible por filtros ATS. Una lista de frases prohibidas deja afuera "apasionada", "orientada a resultados", "amplia experiencia" y similares.
- **💰 Barato por diseño.** Los filtros gratuitos sacan la mayor parte del ruido antes de que la IA lea nada: en uso real, cerca del 60 % de los avisos irrelevantes, sin perder ninguno bueno.
- **🧠 Resistente a instrucciones escondidas.** Los avisos se tratan como datos. Si un aviso trae instrucciones escondidas para la IA, se ignoran y se marcan como alerta.
- **🌐 Bilingüe.** Entrevista, tablero y CVs en español o inglés.
- **📦 Sin dependencias.** Solo la biblioteca estándar de Python, incluido el generador de DOCX.

### 📊 Primera búsqueda real

Creado y probado por una profesional del derecho en Argentina que busca trabajo remoto con empleadores del exterior:

- ~1.100 avisos traídos en la primera búsqueda → 750 únicos tras eliminar repetidos
- 27 avisos A/B, cada uno con la frase de elegibilidad citada
- **USD 0,36** de crédito de Apify, con un tope de USD 1

---

## 🔒 Tu privacidad

Todo lo personal queda en tu computadora y está excluido de Git:

| Carpeta / archivo | Qué guarda |
| --- | --- |
| `profile/` | Tu CV, banco de evidencia, rutas y configuración de búsqueda |
| `data/` | Avisos, clasificaciones, tus estados y notas |
| `applications/` | Tus CVs a medida |
| `.env` | Tu token de Apify, si sumaste LinkedIn o Indeed |

HireWire no tiene servidor ni analíticas. Lo único que sale de tu computadora son las consultas a las fuentes que activás y tu propio agente de IA.

---

## 🧰 Problemas frecuentes

<details>
<summary><b>"python no se reconoce" / no encuentra Python</b></summary>

Pedile a tu agente que instale Python 3.10 o más nuevo. En Windows puede usar `winget install Python.Python.3.12`; en macOS, `brew install python`. En macOS y Linux el comando puede ser `python3` en lugar de `python`, y las instrucciones de HireWire ya lo contemplan.
</details>

<details>
<summary><b><code>/hirewire</code> no hace nada o dice que no existe</b></summary>

Los comandos con barra funcionan cuando el agente está abierto **dentro** de la carpeta de HireWire (ver el paso 4 del camino recomendado). Mientras tanto, pedilo con palabras: "empezar HireWire", "buscá trabajos".
</details>

<details>
<summary><b>Se me terminó el límite del plan gratis, o una búsqueda consume mucho</b></summary>

Decile al agente: *"clasificá solo 20 avisos por búsqueda"*. El resto espera a la búsqueda siguiente. Los límites de los planes gratis se renuevan solos (por día o por semana, según el agente).
</details>

<details>
<summary><b>El tablero no abre</b></summary>

Puede que otro programa esté usando el puerto 8765. Pedile al agente que abra el tablero en otro puerto (8766).
</details>

<details>
<summary><b>Me aparecen trabajos presenciales, híbridos o que no aceptan mi país</b></summary>

Decíselo a tu agente, con uno o dos ejemplos. Encuentra por qué se colaron, ajusta la regla, comprueba que no se pierda ningún aviso bueno y limpia el tablero.
</details>

<details>
<summary><b>"APIFY_TOKEN missing in .env"</b> (solo si sumaste LinkedIn o Indeed)</summary>

Revisá que el archivo se llame exactamente `.env` (no `.env.txt`), que esté en la carpeta de HireWire y que la línea diga `APIFY_TOKEN=` seguido de tu token, sin espacios.
</details>

<details>
<summary><b>Se me terminó el crédito de Apify</b></summary>

Las búsquedas siguen funcionando con las cinco fuentes gratis. Apify renueva el crédito gratis cada mes.
</details>

---

## ⚙️ Por dentro

<details>
<summary><b>Cómo se procesa una búsqueda</b></summary>

1. `fetch` consulta cada fuente activa, elimina repetidos (URL canónica y empresa + puesto) y aplica filtros gratuitos: empresas excluidas, exigencias de residencia o permiso de trabajo de otros países, avisos presenciales o híbridos que nunca dicen "remoto", títulos de otros rubros y avisos viejos.
2. `batch` ordena los avisos pendientes por relevancia (coincidencia de título, términos del rubro, fecha) y divide los mejores en lotes.
3. Un subagente de IA por lote aplica `config/criteria.md` con tu perfil y escribe una línea JSON por aviso.
4. `merge` valida cada línea (valores permitidos, tus rutas, una cita de ubicación para cada aviso *elegible*) e informa los errores para reintentar.
5. `sources` y `test-prefilter` miden el rendimiento de cada fuente y vuelven a pasar los filtros sobre clasificaciones anteriores, para ajustar reglas sin perder avisos buenos.
</details>

<details>
<summary><b>Estructura del proyecto</b></summary>

```text
.claude/skills/        punto de entrada y las cuatro etapas (/hirewire, /profile, /routes, /search, /cv)
AGENTS.md              instrucciones para cualquier agente (CLAUDE.md y GEMINI.md lo importan)
.agents/               regla y skills para Antigravity (apuntan a AGENTS.md y .claude/skills)
INSTALL.md             pasos de instalación que sigue el agente
config/criteria.md     reglas de clasificación: ubicación, ruta, nivel, prioridad, formato de salida
config/cv_style.md     formato del CV y reglas de redacción
templates/             punto de partida de los archivos de tu perfil
scripts/hirewire.py    pipeline: check, fetch, batch, merge, status, sources, refilter, test-prefilter
scripts/dashboard.py   servidor del tablero local
scripts/make_docx.py   Markdown → DOCX y PDF formato Harvard
web/                   tablero (modo local y demo)
docs/                  imágenes y el diagrama interactivo

profile/  data/  applications/  .env     tus datos privados, ignorados por Git
```
</details>

<details>
<summary><b>Comandos</b></summary>

```bash
python scripts/hirewire.py check          # valida tu carpeta de perfil
python scripts/hirewire.py fetch          # solo fuentes gratis
python scripts/hirewire.py fetch --with-apify   # también LinkedIn e Indeed, si están activas (gasta crédito de Apify)
python scripts/hirewire.py batch          # prepara los avisos más relevantes para la IA
python scripts/hirewire.py merge          # valida y guarda los resultados de la IA
python scripts/hirewire.py status         # en qué etapa estás y qué sigue
python scripts/hirewire.py sources        # rendimiento A/B/C por fuente
python scripts/dashboard.py               # abre el tablero en http://localhost:8765
```

Casi nunca los vas a necesitar: el agente los ejecuta por vos.
</details>

---

## 👩‍💻 Autora

Creado por **Micaela D. Asquini**, abogada tech a la que le gusta crear cosas: soluciones legales con IA, legal ops y legal tech. HireWire nació como su propia búsqueda laboral.

## 📄 Licencia

[MIT](LICENSE). Los avisos pertenecen a quienes los publican; HireWire enlaza a las publicaciones originales y no las republica.
