# Pendientes

## Haividio

- [ ] **Santi: revisar el vídeo de RAG en YouTube** (https://youtu.be/leo1j2YyT1w): pronunciación de «Claude», «RAG» y «Spoiler»; los 4 titulares inventados del gancho; los «tics» de la barra de arreglos.
- [ ] **Features del plugin (investigación del 11-11):** primera tirada aprobada por Santi y fusionada (#25–#29, #31): ducking de la música, bloques de HyperFrames en las skills (transiciones, terminal, código), revisión automática del render (PySceneDetect + RapidOCR + `freezedetect`), SRT, capítulos y miniatura desde los tiempos por palabra, y conversor de Pencil a HyperFrames. Un PR por tema. Siguen en cola: shorts verticales, voz local para borradores (Kokoro-82M, revisar licencia de las voces), versión en inglés, retención de YouTube por escena (exige reautorizar OAuth con `yt-analytics.readonly`), nube de embeddings reales, render por escena con manifiesto, música libre y transcripción local (whisper.cpp). Licencias por aclarar: Silero VAD, Parakeet v3, ACE-Step, Piper.
- [ ] **Probarlo todo** (Santi, 11-11): plan y método en `docs/testing.md`, con una casilla por prueba de la tirada 0.3.0 (PR #25–#29). Marcar fecha y quién al probar. Hechas el 11-11 las automáticas de cada PR y el borrador del storyboard (visto por Santi). Quedan: oír el A/B del ducking, ver el SRT y una transición en movimiento, los controles de texto cortado y letra pequeña, y Windows, Codex y Cursor. **Siguiente sesión:** esas pruebas o la siguiente tirada (shorts verticales, voz local, versión en inglés).
- [x] Documentar cómo instalarlo en Codex, OpenCode, pi y Cursor (07-11, `docs/other-agents.md`). pi y OpenCode encuentran las skills; Codex y Cursor sin probar.
- [ ] Producir un vídeo entero con un agente que no sea Claude Code y anotar qué falla.
- [x] Publicar con youtubeuploader (07-11, workflow 4): proyecto de Google Cloud creado y prueba como oculto hecha (10-11); el vídeo de RAG, publicado. Miniatura puesta el 11-11 tras verificar el canal (PR #19).
- [x] Publicar la app OAuth en Google Cloud (11-11): «En producción», con la marca y el sitemap; el token ya no caduca el 17-11 (PR #20, #21).
- [x] Subir la imagen como vista previa social en los ajustes de GitHub (07-11).
- [x] Publicar haividio.dev sola al fusionar en `main`, y `just deploy` a mano (07-11, `docs/web.md`).
- [x] Guía para contribuir, código de conducta (Contributor Covenant 3.0), plantillas de issue y PR, y avisos privados de seguridad (08-11). Contacto: info@haividio.dev, reenviado con Email Routing.
- [x] README y página en inglés (08-11): `README.en.md` y haividio.dev/en/.
- [x] Guías en inglés (09-11): los workflows, `windows`, `cloned-voice`, `editing-and-verification`, `other-agents`, `tools`, `style/identity` y `open-resources` tienen su `.en.md`. Sin traducir, a propósito: `clonify`, `ai-engineering-library`, `voice-sample-text` (es texto para leer en español) y `web` (interna).
- [ ] El perfil de comunidad de GitHub marca las plantillas de issue como ausentes aunque existen (son formularios `.yml`). Ver si basta con eso o hace falta otra cosa.
- [ ] Probar Codex y Cursor con las skills (siguen sin probar).
- [x] Mejoras pedidas por compañeros (08-11):
  - Demos de aplicaciones de gestión (un ERP) para clientes, con voz clonada o con la voz grabada de quien las presenta. Sirve el workflow 5; no se incorpora otro motor de grabación. Si la voz es grabada, se graba primero por escenas y la toma se ajusta a esas duraciones.
  - Skills en inglés y en español (hecho, 0.2.0).

## Verificación automática (investigación del 07-11)

Dos investigaciones independientes (un subagente de Claude y pi con gpt-6-luna) con el criterio de Santi: libre y gratis primero; ElevenLabs sigue siendo la voz principal. Ninguna medida decide si algo suena bien: sirven para saber qué escuchar primero.

Ya:
- [x] **WhisperX** ([repo](https://github.com/m-bain/whisperX), BSD-2, v3.8.6): `scripts/check_voice.py` compara la voz con el guion y guarda el instante real de cada palabra (07-11). Detectar cortes por duración de palabras no funcionó (ver aprendizajes).
- [ ] **Cortes limpios dentro de una palabra**: ni `check_voice.py` ni `detect_glitches.py` los ven. Probar a alinear el audio final con la toma original por MFCC y DTW: un corte debería verse como un salto en el camino. Caso de prueba: quitar 150 ms en mitad de una palabra de una toma aprobada.
- [x] **Pronunciación escrita en `eleven_v4`**: probada la IPA entre barras (`/ˈapi/`) con «API»; ganó la grafía «Api» (ver aprendizajes del 07-11). Queda por probar el alias en un diccionario de pronunciación ([guía](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)).

Después:
- [x] Revisión visual (11-11, `scripts/check_render.py`): un fotograma por escena con PySceneDetect o `timeline.json`, OCR con RapidOCR (Apache-2.0), rótulos esperados, texto cortado o pequeño y tramos quietos con `freezedetect`. La legibilidad a 360 px no se puede medir con OCR (lee mejor que una persona).
- [ ] Desfase rótulo-voz: OCR denso alrededor de cada rótulo esperado contra los tiempos de las palabras.
- [ ] Si el OCR se queda corto: [Qwen3-VL-4B](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) (Apache-2.0, local) como revisor de clips en movimiento. Ya está en caché la versión MLX de 4 bits.
- [x] Mezcla con *ducking* (11-11, `scripts/duck_music.py`): `sidechaincompress` con la voz como control y medida de voz frente a música por ventanas. Falta calibrar de oído `--min-gap` (15 dB) y el volumen (0,25 en la prueba de RAG).

Más adelante:
- [ ] Detector de pronunciación por fonemas: `wav2vec2-xlsr-53-espeak-cv-ft` (lo que suena) contra espeak-ng (lo esperado). Solo para la lista de términos difíciles; calibrar con tomas aprobadas y rechazadas. Licencia del modelo sin verificar.
- [ ] Similitud de timbre por frase contra la toma aprobada (WeSpeaker) y calidad con DNSMOS, para ordenar qué escuchar.
- [ ] Pedir 2 o 3 variantes solo de la frase difícil, ordenarlas con lo anterior y empalmar la buena con `splice_voice.py`.
- [ ] Limpiar la muestra de clonación con Resemble Enhance (MIT) o DeepFilterNet. No aplicarlo a lo que genera ElevenLabs.
- [ ] Borradores con voz local (VoxCPM2, Apache-2.0, o Qwen3-TTS) para cuadrar tiempos antes de gastar créditos.
- [ ] Shorts verticales: composición vertical en HyperFrames; para vídeo hablado, recorte con MediaPipe.
- [x] Subtítulos SRT y capítulos desde los `.words.json` (11-11, `scripts/make_captions.py`) y comprobación de la miniatura con vista previa a tamaño de móvil (`check_publishing.py thumb`). La miniatura ya se hace desde código, como composición de HyperFrames (vídeo de RAG).
- [ ] Probar títulos y miniaturas con «Test & Compare» de YouTube Studio.
- [ ] Documentar en `docs/other-agents.md` el MCP alojado de ElevenLabs (`https://api.elevenlabs.io/v1/mcp`, OAuth); el `elevenlabs-mcp` local está archivado desde el 20-08-2026.
- [ ] Validar las skills con `skills-ref` (Agent Skills).

Descartados: Chatterbox (retirado y con marca de agua), Fish Audio S2 (licencia de investigación), F5-TTS y XTTS v2 (pesos no comerciales), Gemini (de pago; como mucho segunda opinión), UTMOSv2 como único medidor (inestable).

## Ahora (en el Mac)

- [x] Clonar el repo e instalar el plugin `video-studio` (+ hyperframes, Chrome Headless Shell, whisper-cpp, Parakeet) (ver "Empezar en tu Mac" en el README).
- [x] Flujo **pencil.dev → HyperFrames** (11-11): `scripts/pencil_to_hyperframes.py`, skill `pencil-to-hyperframes` y `docs/workflows/06-pencil-to-hyperframes.md`. Probado con KF 03 del vídeo de RAG.
- [x] Modo storyboard con un export real de Pencil (11-11): Trocear, Vectorizar y Buscar del vídeo de RAG; los cambios de la barra de pasos y del pie animados desde `states.json` coinciden con los PNG.
- [x] Escena entera desde un storyboard con `--draft` (11-11). Falta que Santi vea el borrador en movimiento.
- [x] (01-11, clonación instantánea; ver `docs/cloned-voice.md`.) **Clonar la voz** en ElevenLabs: grabar audio limpio, crear la voz, comprobar requisitos actuales (clonación rápida vs profesional, plan necesario). Guardar el ID de la voz en `.env`, nunca en git.
- [ ] Elegir entre whisper-cpp y Parakeet para transcribir y **desinstalar el que no se use** (Santi, 31-10: el espacio en disco está creciendo mucho; npm y Playwright ya se limpiaron).
- [ ] Vídeo de RAG: **más pantallas** en el pen, con el conocimiento de `sources.md` (Hugging Face, LangChain Deep Agents…) explicado para usuarios no tan avanzados (petición de Santi, 31-10).

## Tarea: pasar nombres a inglés (pedida el 2026-10-31)

- [x] Renombrar **carpetas y ficheros** del repo de español a inglés: `memoria/` → `memory/`, `docs/estilo/` → `docs/style/`, `docs/herramientas.md` → `docs/tools.md`, `videos/_plantilla/` → `videos/_template/`, `guion.md` → `script.md`, `fuentes.md` → `sources.md`, `animaciones/escena-03` → `animations/scene-03`, skills del plugin `identidad-visual` → `visual-identity`, etc.
- [x] El **código** pasa a inglés (09-11, tras una auditoría con pi): plantillas de issue, ancla `#start` de la web, claves del informe de `check_voice.py` (`type`, `expected`, `heard`…) y la etiqueta del plugin. Los **comentarios** pueden seguir en español.
- [ ] Quedan dos cosas que no se pueden cambiar solo en git: los nombres de capa en español de `design/scene3.pen` (se cambian en Pencil y se vuelve a exportar `kf03.html`) y la pista local `A-pulso-tech-full.mp3` que espera `build_root.py` (renombrar el fichero y la constante a la vez).
- [ ] El **contenido** de los documentos y del vídeo sigue en español.
- [x] Hacerlo con `git mv` (conserva historial) y actualizar todas las referencias: CLAUDE.md, README, skills del plugin, marketplace.json, enlaces entre docs y la memoria de Claude. Al final: `claude plugin validate .` y reinstalar el plugin `video-studio`.
- [x] Buena candidata para delegar en pi (mecánica), con una lista de renombrados cerrada que apruebe Santi antes.

## Vídeo de RAG (`videos/2026-10-31-rag-2026/`)

- [x] Guion v1 con fuentes.
- [x] Prueba de la escena 3 en HyperFrames (26 s, sin voz).
- [x] Guion v2: bloque de fundamentos para principiantes (escenas 2b, 3a–3c, 8 ampliada) con fuentes de HF, LangChain y Anthropic (`sources.md`).
- [x] Guion v2 aprobado; gancho A (sin dar por sabido qué es Claude Code).
- [ ] **Fuente primaria de la escena 1**: post de Boris Cherny en X o entrevista (mayo 2025) donde cuenta que quitaron RAG + base vectorial. La URL de smartscope de la v1 ya no lo dice. Sin fuente primaria, no publicar esa afirmación tal cual.
- [x] Fotogramas en `design/scene3.pen`: 2b, 3a, 3b Trocear, 3b Vectorizar, 03 Buscar, 3c ¿Cuántos?, 04 Generar (fila 1) y 8a, 8b (fila 2). Componente reutilizable «Glosario». PNG en `design/export/`.
- [x] Revisión de Santi de los fotogramas (01-11: «bastante bien» como prueba de concepto).
- [x] Tramo de prueba 3b + 3c animado con voz en `animations/rag-steps/` (74 s, 5 escenas como subcomposiciones, voz de serie «Daniel» de ElevenLabs sincronizada por palabra). Pendiente: que Santi lo vea en la vista previa y apruebe antes de renderizar.
- [x] **Vídeo completo montado** en `animations/rag-video/` (18 composiciones, 7:58, voz de prueba «Daniel»). `build_root.py` regenera `index.html` y `timeline.json` desde las duraciones reales de la voz. Borrador renderizado en `out/rag-video-draft-v1.mp4` (fuera de git). Santi: «como POC está guay», mejorable en el ajuste final.
- [x] Música (estilo A «pulso tech», ElevenLabs Music, encadenada a 6:13) y 30 efectos (whoosh, pop, tic, golpe final), colocados desde `build_root.py`. Render v2 normalizado a −14 LUFS: `out/rag-video-v2.mp4`. Santi (01-11): «está perfecto para ser el primero»; la voz suena algo artificial.
- [x] Enviar la v2 para recoger opiniones (Google Drive, `Vídeos IA/RAG en 2026 - v2 (borrador para opiniones).mp4`). 03-11: **ha gustado bastante**. Siguiente paso: ajuste final (voz más natural, transiciones, ritmo de agentic y longcontext, `first_frame_empty`) y miniatura.
- [ ] Crear un client_id propio de Google Cloud para rclone (el compartido se retira en 2026) y aprovechar el proyecto para la API de YouTube.
- [ ] Ajustes conocidos: con la voz de Santi, 5 textos (ya resueltos con pausas de 1,2 s en search y topk) se ven poco tiempo (`line_unread` en search, topk y failures) porque las escenas «Buscar» (5,4 s) y «¿Cuántos?» (6,9 s) se han quedado cortas; «6 o más llamadas» (8b) no tiene fuente; música y efectos (sin créditos de ElevenLabs este mes); transiciones entre escenas (ahora cortes secos).
- [x] **Voz de Santi** (01-11): prueba A/B de la escena 1 entre ElevenLabs IVC (Starter), Qwen3-TTS 0.6B y Qwen3-TTS 1.7B, todas a la misma velocidad. Santi y Nerea eligieron **ElevenLabs**: entonación más natural y mejor manejo de pausas y silencios. Las 14 escenas ya están generadas con su voz (`ELEVENLABS_VOICE_ID_SANTI` en `.env`). El vídeo pasa de 7:58 a **6:11** y el gancho dice ahora «en seis minutos».
- [ ] Qwen3-TTS 1.7B: le vale la pena si llega a la calidad de ElevenLabs. Ideas para mejorarlo: generar párrafos (≤ 200 caracteres) en lugar de frases sueltas con pausas fijas, recortar los silencios de cada trozo y variar la pausa según la puntuación, y probar otra referencia. Ocupa 3,1 GB en la caché de HF (`models--mlx-community--Qwen3-TTS-12Hz-1.7B-Base-8bit`): borrarlo si se descarta.
- [ ] **Ritmo para que no canse** (Santi, 01-11: prioridad justo después de la voz): revisar escenas largas (8 agentic 52 s, 9 longcontext 42 s), meter cambios de plano y alguna pausa o pregunta al espectador.
- [ ] Afinar la escena 3: ritmo ajustado a la voz real, sonido (música de fondo + efecto en cada paso).
- [ ] Sustituir los puntos inventados por **embeddings reales** (sentence-transformers + dataset de Hugging Face, proyección UMAP/PCA).
- [x] Generar la voz por escenas con la voz clonada (01-11).
- [x] Animar el resto de escenas (`animations/rag-video/`, 18 composiciones).
- [ ] Miniatura y publicación como privado.

## Windows (03-11)

- [x] Adaptar el repo: `docs/windows.md` (winget, diferencias de comandos, herramientas solo de macOS), sección «Empezar en Windows» en el README, `encoding="utf-8"` en `build_root.py` (en el Mac genera el mismo `index.html`) y `.gitattributes` con `eol=lf`.
- [ ] **Probarlo en un Windows real** (Santi o alguien de su empresa): la lista de comprobación está en `docs/windows.md`. HyperFrames dice soportar Windows desde la v0.8.219, pero no lo hemos probado. Si falla el render nativo, usar WSL2. Para `rag-video` hay que pasar aparte los mp3 de `assets/`, que no están en git.

## Ideas

- **Biblioteca de vídeos de ingeniería de IA para la empresa de Santi** (01-11): `docs/ai-engineering-library.md`. Late chunking, para aplicarlo en sus proyectos: `videos/2026-10-31-rag-2026/apply-in-projects.md`.

- Crear una pequeña librería de componentes reutilizables (barra de pasos, tarjeta de fragmento, panel de dispersión, caja LLM) para no rehacerlos en cada vídeo.
- Añadir la clonación de voz a la skill `faceless-video`.
