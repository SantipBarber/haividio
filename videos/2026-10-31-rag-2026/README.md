# ¿RAG ha muerto? Cómo funciona y qué se usa de verdad en 2026

- **Fecha:** 2026-10-31
- **Tipo:** sin-cara
- **Estado:** publicado el 10-11-2026 (público, con subtítulos en español; miniatura puesta el 11-11-2026, tras verificar el canal)
- **YouTube:** https://youtu.be/leo1j2YyT1w

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

## Archivos

- `script.md` — guion por escenas con fuentes
- `publishing.md` — título, descripción, tags, capítulos
- `animations/` — código de las animaciones
- `thumbnail/` y `miniatura.png` — miniatura
- `subtitles.srt` — subtítulos en español
