# Changelog

[English](CHANGELOG.en.md)

Qué se añade a Haividio y qué queda pendiente. Lo más reciente, arriba. Las versiones son las del plugin `video-studio` (`plugins/video-studio/.claude-plugin/plugin.json`); entre una versión y otra, los cambios van en «Sin publicar».

Cada PR fusionado añade aquí una línea. El detalle de cada prueba está en [docs/testing.md](docs/testing.md) y las ideas sin empezar, en [memory/backlog.md](memory/backlog.md).

## Sin publicar

### Añadido

- Este changelog, en español e inglés (#33, #34).
- `scripts/tts.py`: voz con ElevenLabs, `language_code`, mapa de pronunciación y tiempos por palabra. `speed` no hace nada con `eleven_v4`: el tempo se cambia con `atempo` (#35).

### Pendiente

Pruebas de la 0.3.0 que faltan (casillas en `docs/testing.md`):

- [ ] Oír el A/B del ducking y elegir el volumen de la música y `--min-gap`.
- [ ] Ver el SRT generado por `make_captions.py` sobre el vídeo.
- [ ] Ver en movimiento una transición de HyperFrames montada en una escena.
- [ ] `check_render.py`: controles de texto cortado y de letra de 20 px frente a 32 px.
- [ ] `duck_music.py`: el control a volumen 0,6, que debe fallar.
- [ ] `pencil_to_hyperframes.py`: un diseño con `<img>`, SVG, instancias y una fuente que no sea Geist.
- [ ] Windows, Codex y Cursor.

Revisión del vídeo de RAG publicado (https://youtu.be/leo1j2YyT1w):

- [ ] Pronunciación de «Claude», «RAG» y «Spoiler».
- [ ] Los cuatro titulares inventados del gancho.
- [ ] Los «tics» de la barra de arreglos.

Siguiente tirada posible: shorts verticales, voz local para borradores (Kokoro-82M), versión en inglés de un vídeo, retención de YouTube por escena, render por escena, música libre y transcripción local con whisper.cpp.

## 0.3.0 — 2026-11-11

### Añadido

- `scripts/duck_music.py`: baja la música cuando habla la voz (`sidechaincompress`) y mide la diferencia entre voz y música por ventanas (#25).
- Catálogo de bloques de HyperFrames en las skills (transiciones, terminal, código) y `docs/style/tokens.css` con los colores del canal (#26).
- `scripts/make_captions.py`: subtítulos SRT y capítulos de YouTube desde los tiempos por palabra; `check_publishing.py thumb` comprueba la miniatura a tamaño de móvil (#27).
- `scripts/check_render.py`: revisa el render fotograma a fotograma por escena con PySceneDetect, RapidOCR y `freezedetect` (rótulos esperados, texto cortado o pequeño, tramos quietos) (#28, #31).
- Plan de pruebas en `docs/testing.md`: todo lo que entra en el plugin se prueba con material real y un control que deba fallar (#30).
- Pencil → HyperFrames: `scripts/pencil_to_hyperframes.py`, la skill `pencil-to-hyperframes` y el workflow 06, con modo storyboard y borrador de escena (`--draft --at`) (#29, #32).
- Miniatura puesta en el vídeo de RAG tras verificar el canal (#19).
- Página de privacidad de haividio.dev (es/en) y `sitemap.xml`, y guía de lo que pide Google para publicar la app OAuth de YouTube (#20, #21).

### Cambiado

- Texto mínimo unificado en 32, 40 y 28 px según el formato (#26).
- El botón de la estrella de la web lleva a la página del repositorio (#22).

## 0.2.2 — 2026-11-10

### Añadido

- Primer vídeo publicado: «¿RAG ha muerto?», con escenas pulidas, voz con `eleven_v4`, subtítulos y miniatura (#18).

## 0.2.1 — 2026-11-10

### Añadido

- Publicar en YouTube: revisar qué se ve en pantalla, validar la ficha y comprobar la visibilidad tras la subida (#17).

## 0.2.0 — 2026-11-09

### Cambiado

- Skills con nombre en inglés y activación en español y en inglés (#14).
- Carpetas, ficheros y código con nombres en inglés (#15).

### Añadido

- Guías en inglés (`.en.md`) junto a las españolas (#16).
- README y página en inglés (#12).
- Guía para contribuir, código de conducta y plantillas de issue y PR (#11).

## 0.1.0 — 2026-10-31 a 2026-11-08

### Añadido

- Base de conocimiento: herramientas, workflows, plantilla de vídeo, memoria del proyecto y plugin `video-studio`.
- Identidad visual del canal y prueba de escena en HyperFrames.
- Adaptación a Windows (`docs/windows.md`).
- Guía de demos de producto con voz clonada.
- Nombre Haividio, instrucciones comunes en `AGENTS.md` e instalación en Codex, OpenCode, pi y Cursor.
- haividio.dev, que se publica sola al fusionar en `main` (#9).
- `scripts/check_voice.py`: compara la voz con el guion con WhisperX y avisa de siglas deletreadas (#10).
- Publicar con youtubeuploader en vez del MCP de YouTube (#8).
