# Aprendizajes

Lo más reciente arriba. Formato: `- AAAA-MM-DD · [tema] lo aprendido. Cómo aplicarlo.`

- 2026-11-08 · [plugin] Para comprobar qué skill se activa sin instalar la rama: `claude -p "<petición>" --plugin-dir <repo>/plugins/video-studio --settings s.json --output-format stream-json --verbose`, con `s.json` = `{"enabledPlugins":{"video-studio@haividio":false}}` para que no cargue la versión instalada, y buscar la llamada `"name":"Skill"`. Con nombres y cuerpo en inglés y frases de activación en español en la descripción, las seis peticiones de prueba (cinco en español, una en inglés) activaron la skill correcta.
- 2026-11-08 · [web] La publicación automática funciona: al fusionar un cambio de `site/`, el flujo tarda unos 25 s. El token de Cloudflare tiene que ser de edición (plantilla *Edit Cloudflare Workers*, limitada a la cuenta y a la zona); con solo lectura no publica. En el registro sale `npm error npx canceled due to missing packages`: es la acción comprobando si wrangler está instalado, no un fallo.
- 2026-11-08 · [web] Página bilingüe: `site/index.html` y `site/en/index.html`, enlazadas con `hreflang`. La onda de la portada sale de una toma real: en inglés se generó una frase con la voz clonada (`language_code: en`, 16 créditos por toma) y se midieron los tiempos con WhisperX (`--language en`; la primera vez descarga el alineador inglés). WhisperX junta «Claude Code» en una palabra: se separa por el mínimo de energía entre las dos.
- 2026-11-08 · [plugin] Si el plugin se instaló desde la carpeta local del repositorio, carga las skills de la rama que esté abierta: con una rama de vídeo antigua, la skill se queda atrás aunque `main` esté al día. Instalarlo desde GitHub (`claude plugin marketplace add SantipBarber/haividio` y `claude plugin install video-studio@haividio`) lo independiza de la rama.
- 2026-11-08 · [correo] Un correo del dominio (info@) sin servidor de correo: Email Routing de Cloudflare reenvía a una dirección ya verificada en la cuenta. Al activarlo crea solo los MX, SPF y DKIM, y se ve desde fuera en segundos. Para probarlo, escribe desde otra cuenta: Gmail puede ocultar lo que te envías a ti mismo.
- 2026-11-08 · [herramientas] Las capturas de chrome-devtools pueden colgarse (`Page.captureScreenshot timed out`) hasta que el navegador se reconecta. Mientras, la página se puede enseñar en una pane de herdr-app con `terminal-browser`, que también abre GitHub.
- 2026-11-07 · [voz] «API» con `eleven_v4`: la grafía «Api» ganó de oído a la IPA en línea (`/ˈapi/`, que no se lee en voz alta pero no mejoró), aunque de tres frases una salió deletreada. La transcripción escribe «API» en ambos casos; lo que la delata es la duración: 0,18 y 0,26 s dicha como palabra, 0,46 s deletreada. `check_voice.py` avisa cuando una palabra escrita como tal en el guion sale en mayúsculas a más de 0,12 s por letra; en 12 tomas de prueba, solo saltó en la mala.
- 2026-11-07 · [verificación] `scripts/check_voice.py` (WhisperX 3.8.6, `large-v3-turbo`, CPU int8) compara la voz con el guion. Probado: detecta una palabra quitada en el segundo exacto y deja limpia una copia recodificada; en un final de 8 min con música, 3 min de proceso y 3 avisos reales. No detecta un corte limpio de 150 ms dentro de una palabra (detect_glitches.py tampoco), y comparar duraciones de palabras con el alineador da hasta 0,3 s de ruido. Instalar en un entorno aparte: `uv venv ~/.local/share/haividio/whisperx --python 3.12` y `uv pip install whisperx==3.8.6` (unos 1 GB); los avisos de torchcodec al arrancar no afectan.

- 2026-11-07 · [web] `haividio.dev` es una página estática en `site/`, servida por un Worker de Cloudflare con la configuración de `wrangler.jsonc`. Se publica sola al fusionar en `main` (GitHub Actions, necesita los secretos de `docs/web.md`); a mano, `just deploy`.

- 2026-11-07 · [demo] Lo aprendido al hacer una demo de producto con voz clonada está en `docs/workflows/05-demo-de-producto.md`, `docs/voz-clonada.md` y `docs/montaje-y-verificacion.md`. Lo más caro: buscar palabras sueltas al sincronizar y regenerar voz ya aprobada en vez de empalmarla.

## HyperFrames

- 2026-10-31 · [render] HyperFrames renderiza con **Chrome Headless Shell** (familia Chrome for Testing), no con Chrome normal ni Brave. `npx hyperframes browser ensure` lo descarga en `~/.cache/hyperframes/chrome/`. `npx hyperframes doctor` revisa todas las dependencias. Sustituye el truco del Chromium de Playwright.
- 2026-10-31 · [transcripción] HyperFrames usa whisper-cpp (`brew install whisper-cpp`) para `hyperframes transcribe`; para español pasar `-l es -m large-v3` (los modelos `.en` son solo inglés). Alternativa más rápida: `hyperframes models install parakeet`.
- 2026-10-31 · [render] Si no hay Chrome instalado, `render` falla. Apuntar al Chromium de Playwright: `HYPERFRAMES_BROWSER_PATH=$(node -e "console.log(require('playwright').chromium.executablePath())")`. En el Mac con Chrome instalado no hace falta.
- 2026-10-31 · [render] 26 s a 1080p30 tardan ~1 min con captura por software. 2026-11-01: con GPU, el vídeo completo (7:58, 1080p30) tarda 2 min 49 s y ocupa 32 MB. Para iterar, usar `npx hyperframes snapshot --at 1,5,10` y revisar el `contact-sheet.jpg` antes de renderizar.
- 2026-10-31 · [lint] No animar `left`/`top` con GSAP (error `gsap_non_transform_motion`, da tirones). Usar `x`/`y`.
- 2026-10-31 · [lint] No mezclar `transform` en CSS con tweens de `x`/`y` (error `gsap_css_transform_conflict`). Para centrar, `gsap.set(el, { xPercent: -50 })`.
- 2026-10-31 · [lint] Los estados iniciales ocultos van con `gsap.set(...)` fuera del timeline, no con `tl.set(..., 0)`, o el fotograma 0 sale mal.
- 2026-10-31 · [legibilidad] El check exige texto ≥ 28 px en 1080p (legible en móvil). Diseñar con ese mínimo desde el principio.
- 2026-10-31 · [assets] La plantilla carga GSAP y fuentes de CDN. En entornos sin red, copiarlos a `assets/` (gsap desde npm, fuentes desde `@fontsource/*`) y referenciarlos en local. Así además el render es reproducible.
- 2026-10-31 · [flujo] `npx hyperframes init <nombre> --example=blank --non-interactive` → editar `index.html` → `check` → `snapshot` → `render -o salida.mp4`.

- 2026-11-01 · [voz] Flujo voz → animación: `POST /v1/text-to-speech/{voice}/with-timestamps` devuelve el mp3 y el tiempo de cada carácter; agrupado en palabras (`audio/voice/scene-*.words.json`) da los instantes exactos para colocar cada animación. Sin alineación forzada aparte.
- 2026-11-01 · [preview] En **Safari** la vista previa de HyperFrames (`npx hyperframes preview`) no reproduce el audio; en Chrome sí. Abrir siempre la URL del Studio en Chrome.
- 2026-11-01 · [estructura] Un tramo = `index.html` raíz (fondo, barra de pasos, `<audio>` de voz, cada uno en su pista y con `data-duration` = duración real) + una subcomposición por escena en `compositions/`. Los ids deben ser únicos entre escenas (prefijo por escena). El check avisa de «dead_stretch» (>3 s sin cambios) y «line_unread» (texto que se va antes de poder leerse): útiles para ajustar el ritmo.

## ElevenLabs

- 2026-11-01 · [plan] El plan gratuito **no deja usar voces de la biblioteca (Voice Library) por API** (402 `paid_plan_required`): solo las de serie (inglesas/americanas, hablan español con algo de acento). Las castellanas nativas (Aaron Abad, David Martin, Eva Dorado, Carmelo) requieren Starter. 10.000 créditos/mes ≈ 10.000 caracteres.
- 2026-11-01 · [clave] Clave restringida «claude-video-studio»: TTS, STT, efectos, música, alineación forzada, modelos (acceso); voces (leído). Falta «Usuario» (`user_read`) para consultar créditos. Para clonar, voces → escribir.

## Pencil

- 2026-10-31 · [export] `Export(ids,"png",dir)` saca PNG por fotograma (nombre = id del nodo); `Export(ids,"html-css",fichero)` saca HTML con estilos inline, posiciones absolutas, `data-pencil-name` con el nombre de cada capa y fuentes de Google por CDN. Sirve de base para HyperFrames, pero hay que añadir ids, fuentes locales y copiar los assets (las URLs de imagen quedan relativas al .pen, no al HTML).
- 2026-10-31 · [diseño] Los puntos de un scatter se generan bien con JS dentro de `execute` (semilla determinista, la misma que luego usa la animación). No hay trazo discontinuo: el radio de búsqueda va como elipse con relleno lima al 6 % y borde al 40 %.
- 2026-10-31 · [diseño] La rejilla de puntos del fondo va como imagen (`design/assets/grid.png`, 1920×1080) en un fill de imagen; se reutiliza en HyperFrames.

- 2026-10-31 · [pencil] Los avisos `partially/fully clipped` que da `Get` en el mismo `execute` que crea los nodos suelen ser falsos (layout aún sin resolver). Recomprobar en otra llamada antes de corregir nada.
- 2026-10-31 · [pencil] Para la firma reutilizable (tarjeta de glosario) usar un componente `reusable: true` e instancias `ref` con `descendants` para cambiar término y definición.

## Claude Code / plugin

- 2026-11-03 · [windows] IDs de winget verificados en microsoft/winget-pkgs: `Git.Git`, `GitHub.GitLFS`, `OpenJS.NodeJS.LTS`, `Gyan.FFmpeg`, `Python.Python.3.12`, `astral-sh.uv`, `yt-dlp.yt-dlp`, `Rclone.Rclone`, `Audacity.Audacity`. En Python, `read_text`/`write_text` siempre con `encoding="utf-8"`: en Windows el valor por defecto es cp1252.
- 2026-11-03 · [pi] `pi-task -v` solo funciona dentro de herdr. Desde una sesión de Claude Code fuera de herdr, lanzarlo con `-s <id>` para que quede la sesión y se pueda registrar el coste con `pi-usage`.

- 2026-10-31 · [plugin] `claude plugin marketplace add heygen-com/hyperframes` falla sin **git-lfs** (`brew install git-lfs && git lfs install`). Después queda un aviso de punteros LFS sin bajar: son vídeos de test del repo, no hace falta `lfs pull`. Plugin: `hyperframes@hyperframes`.
- 2026-10-31 · [pencil] El MCP de Pencil no crea ni abre ficheros: si `filePath` no existe, actúa sobre el `.pen` activo (¡riesgo de tocar otro proyecto!). Crear el fichero en la app (⌘N + guardar) y pasar siempre la ruta explícita. No abrir una segunda instancia de Pen: competirían por el MCP.
- 2026-10-31 · [plugin] Validar el marketplace con `claude plugin validate .` desde la raíz del repo antes de subir.
- 2026-10-31 · [github] Desde una sesión de Claude en la nube no se pueden crear repos; se crea vacío en GitHub y se da acceso a la app de Claude (github.com/apps/claude) para poder hacer push.

## Contenido

- 2026-10-31 · [fuentes] Las URLs de blogs de terceros cambian: smartscope.blog dejó de contener la cita sobre Claude Code y RAG. Para afirmaciones que abren un vídeo, buscar siempre la fuente primaria (post, transcripción) y guardarla.
- 2026-10-31 · [fuentes] Las cifras de recuperación contextual de Anthropic (−35 %, −49 % con BM25, −67 % con reranker; de 5,7 % a 1,9 % de fallos en top-20) están verificadas. Miden recuperación, no calidad final de respuesta: decirlo así en el vídeo.
- 2026-10-31 · [herramientas] Clonify no es un editor de vídeo (es una plataforma de formación online). Descartado.

- 2026-11-01 · [voz] Cambiar de voz sin rehacer animaciones: los tiempos de las composiciones se quedan en la voz de referencia (`audio/voice-daniel/`), y `build_root.py` inyecta en cada una un mapa de tiempos con un ancla por palabra (una línea de tiempo exterior que mueve `tl.time`). Requisito: que la voz nueva diga el mismo texto, palabra por palabra. HyperFrames lo acepta (`check` sin errores).
- 2026-11-01 · [voz] Clonación instantánea (IVC) de ElevenLabs con 1:52 de muestra grabada en QuickTime y limpiada con ffmpeg (`highpass=70, afftdn=nr=18, loudnorm TP=-3`; el ruido de fondo bajó de −51 a −62 dB): suena natural. Santi habla un 27 % más rápido que la voz «Daniel».
- 2026-11-01 · [voz] Qwen3-TTS en local (mlx-audio con uvx, parámetros de TranslateCall: referencia de unos 8 s con `ref_text` exacto, temp 0.7, top_p 0.95, rep 1.5, frase a frase): dice el texto exacto, pero las pausas fijas entre frases suenan peor que ElevenLabs. En el M4, el 0.6B va a RTF 0,53 y el 1.7B a RTF 0,72. ElevenLabs Scribe (STT) sirve para verificar lo generado y para transcribir la referencia.
- 2026-11-01 · [audio] Mezcla del render de HyperFrames: voz + música a 0,14 + efectos con el pico a −3 dB da −18 LUFS. Pasada final con ffmpeg `loudnorm` en dos pasadas a −14 LUFS y TP −1,5, copiando el vídeo: queda en −14,2 LUFS y pico de −1,2. Ojo, en zsh `"$var:linear"` aplica el modificador `:l`; hay que escribir `${var}`.
- 2026-11-01 · [audio] ElevenLabs Music: máximo 5 min por pista y a veces responde 429 «system_busy» (reintentar). Para cubrir 6 min, encadenar la pista consigo misma con `acrossfade` de 6 s.
- 2026-11-01 · [render] Vídeo de 6:13 con audio: 1 min 58 s con GPU.
- 2026-11-01 · [publicar] El conector de Google Drive de claude.ai no sirve para vídeos: el contenido viaja en base64 dentro de la llamada. Para ficheros grandes: rclone (`brew install rclone`), remoto `gdrive` con `scope=drive.file`, para que solo vea lo que sube él. Se sube con `rclone copyto <fichero> "gdrive:Vídeos IA/<nombre>.mp4"`. Aviso: el client_id compartido de rclone deja de funcionar en 2026; hay que crear uno propio en Google Cloud (el mismo proyecto puede servir para la API de YouTube).
