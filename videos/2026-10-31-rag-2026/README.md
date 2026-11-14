# ¿RAG ha muerto? Cómo funciona y qué se usa de verdad en 2026

- **Fecha:** 2026-10-31
- **Tipo:** sin-cara
- **Estado:** v2 publicado el 14-11-2026 en el canal PildorIAs (público, con subtítulos en español). El v1 (10-11-2026) se retiró.
- **YouTube:** https://youtu.be/yOc2rTw593o

## Resumen

Explicación del RAG clásico (trocear, vectorizar, buscar, generar), por qué falla en la práctica y las soluciones actuales: búsqueda híbrida, reranker, recuperación contextual / late chunking, GraphRAG y agentic RAG. Cierra con el debate "contexto largo vs RAG" y un árbol de decisión práctico.

## Herramientas

- Guion: Claude Code + búsqueda web (fuentes en `sources.md` y en cada escena de `script.md`)
- Voz: clon instantáneo de la voz de Santi en ElevenLabs, modelo `eleven_v4`, comprobada con `scripts/check_voice.py`
- Animación: HyperFrames, estilo D «moderno oscuro» (`docs/style/identity.md`), 18 composiciones en `animations/rag-video/`
- Miniatura: composición de HyperFrames en `thumbnail/`
- Publicación: youtubeuploader, con `scripts/check_publishing.py` antes y después

## Decisiones y aprendizajes

- 2026-10-31: guion v1 escrito.
- 2026-10-31: prueba de la escena 3 (26 s, sin voz) en HyperFrames con estilo D "moderno oscuro". GSAP y fuentes Geist incluidos en `assets/` para que renderice sin red. Requiere `HYPERFRAMES_BROWSER_PATH` si no hay Chrome instalado.

- 2026-11-01: voz de Santi clonada; las animaciones se escribieron con la voz «Daniel» y `build_root.py` las resincroniza palabra a palabra con la voz actual.
- 2026-11-10: crítica de diseño con impeccable y pulido de las 18 escenas sin tocar los tiempos: textos mínimos de 32 px y pie de 40 px para el móvil, gris secundario `#A3A8B8`, segunda barra de pasos para los arreglos, el lima solo para la respuesta, escenas que antes dejaban medio encuadre vacío, gancho con titulares grandes y llamada a la acción final visible.
- 2026-11-10: locución regenerada con `eleven_v4` (mismo texto y voz): el vídeo pasa de 6:13 a 6:42. Capítulos recalculados desde `timeline.json`. Subtítulos `subtitles.srt` generados con los tiempos de cada palabra.
- 2026-11-10: fuente primaria del gancho: entrevista a Boris Cherny en The Pragmatic Engineer (04-03-2026).

- 2026-11-14: **v2.** Santi, al ver el v1: «vídeo» sonaba «vidéo», ritmo algo lento y faltaba algo de alegría. Cambios:
  - Voz entera nueva con `scripts/tts.py`: `language_code: es`, mapa de pronunciación (`pronunciation.json`: Clod, ía, rag, Espóiler, Graf rag, Eiyéntic) elegido de oído entre pruebas cortas, `style` 0,3 y tempo ×1,10 con `atempo` (`speed` no hace nada con `eleven_v4`). Pasa de 155 a ~169 palabras/min. Script: `audio/make_voice_v2.py`.
  - Portada de 2 s al empezar (la miniatura a pantalla completa) y fundido al gancho: antes el primer fotograma era la nube de puntos a medias.
  - Fundido corto a negro entre composiciones, en vez de cortes secos.
  - Música con ducking (`scripts/duck_music.py`, volumen 0,2, ratio 8): la voz queda ~22 dB por encima de la música.
  - Correcciones de la revisión: «medio internet» (la voz dijo «media») y la cifra de páginas que caben en contexto: de 500 a 300 páginas, con el matiz de modelos frontera frente a un modelo local de 128k (cuenta en `sources.md`). Se empalmaron solo esas frases con `scripts/splice_voice.py`.
  - La frase nueva tiene más palabras que la de la voz de referencia: se insertaron esas palabras en `audio/voice-daniel/scene-10.words.json` con tiempos dentro del hueco de la frase, para que `build_root.py` siga alineando palabra a palabra. Las animaciones que caen en ese hueco van ~11 veces más lentas: sus duraciones se escriben muy cortas (`compositions/choose.html`).
  - Render final con `-q delivery --video-bitrate 8M`: sin `--video-bitrate`, `delivery` dio 0,5 Mbps en estas escenas planas.
  - Revisión de Santi por minutos; detalles en `REVIEW.md`.

## Archivos

- `script.md` — guion por escenas con fuentes
- `publishing.md` — título, descripción, tags, capítulos
- `animations/` — código de las animaciones
- `thumbnail/` y `miniatura.png` — miniatura
- `subtitles.srt` — subtítulos en español
