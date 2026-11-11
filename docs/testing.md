# Cómo probar Haividio

*[English](testing.en.md)*

Todo lo que entra en el plugin se prueba antes de darlo por bueno, y se deja escrito cómo, para que cualquiera (o cualquier agente) pueda repetirlo.

## Método

1. **Con material real.** Un vídeo ya hecho (el de RAG, `videos/2026-10-31-rag-2026/`, sirve de banco de pruebas) o uno nuevo. No con ejemplos de juguete, salvo para casos límite.
2. **Con un control que deba fallar.** Un rótulo inventado, una imagen con proporción mala, un corte metido a propósito. Si el control no falla, la prueba no prueba nada.
3. **Medido y comparado** con lo que ya había: lo hecho a mano, el PNG del diseño, el SRT publicado.
4. **Lo que no ve un script, lo dice el resultado:** qué hay que oír o ver en movimiento, y quién lo hace.
5. **Se anota:** el resultado va en la descripción del PR, lo aprendido en `memory/learnings.md` y lo que falte en `memory/backlog.md`. Al marcar una casilla de abajo, poner la fecha y quién lo probó.

Las rutas son relativas a la raíz del repositorio; `RAG` es `videos/2026-10-31-rag-2026` y `RAGV`, `RAG/animations/rag-video`.

## Plugin 0.3.0 (PR #25 a #29)

### Ducking de la música — `scripts/duck_music.py` (#25)

```bash
cd RAGV && uv run --with numpy ../../../../scripts/duck_music.py --music assets/music/bed.mp3 \
  --hyperframes index.html --volume 0.25 --out /tmp/bed-ducked.mp3
```

- [x] Lee los clips de voz de la composición, incluidos los partidos con `data-media-start` (11-11, Claude).
- [x] Mide la distancia voz-música antes y después: 13 dB → 23 dB de mediana (11-11, Claude).
- [ ] **Oír** la muestra A/B de un minuto (0,14 sin ducking frente a 0,25 con ducking) y elegir volumen y `--min-gap` (Santi).
- [ ] Renderizar el vídeo de RAG con `bed-ducked.mp3`, oír los tramos que marca y comprobar que la música vuelve sin bombeo tras cada frase.
- [ ] Control: subir el volumen a 0,6; deben salir muchos tramos marcados.

### Bloques de HyperFrames y `tokens.css` (#26)

- [x] `tokens.css` tiñe un componente del catálogo (`code-terminal-run`): captura con y sin tokens (11-11, Claude).
- [ ] Montar en una escena real una transición de las recomendadas (`whip-pan-cut`, `directional-wipe`, `fade-through`) y **verla en movimiento**.
- [ ] Probar `code-typing` y `code-diff` (bloques: hay que recolorearlos a mano) y `cursor-zoom-follow` con el JSON de marcas del workflow 5.
- [ ] `hyperframes check` sin avisos con texto de 32 px y 40 px (el nuevo mínimo de la identidad).

### Subtítulos, capítulos y miniatura (#27)

```bash
cd RAGV && python3 ../../../../scripts/make_captions.py srt --hyperframes index.html \
  --words-dir ../../audio/voice -o /tmp/rag.srt
python3 scripts/make_captions.py chapters --timeline RAGV/timeline.json chapters.json
python3 scripts/check_publishing.py thumb RAG/miniatura.png --preview /tmp/miniatura-movil.png
```

- [x] El SRT tiene el mismo texto que el hecho a mano; ninguna línea pasa de 42 caracteres; sin colas de una palabra (11-11, Claude).
- [x] Los capítulos salen idénticos a los publicados (11-11, Claude).
- [x] `--pron` devuelve «oce erre» a «OCR» y «Odú» a «Odoo» (11-11, Claude, con un ejemplo preparado).
- [x] `thumb` acepta la miniatura publicada y rechaza una imagen de 600×400 (11-11, Claude).
- [ ] **Ver** el SRT nuevo sobre el vídeo (en YouTube como no listado o en un reproductor) y comprobar que ningún subtítulo se adelanta ni se queda colgado.
- [ ] Subir una miniatura de 3840×2160 por la API (el límite nuevo de 50 MB) en un vídeo de prueba.

### Revisión visual del render — `scripts/check_render.py` (#28)

```bash
uv run --with "scenedetect[opencv]" --with rapidocr --with onnxruntime scripts/check_render.py \
  RAG/out/rag-video-v4.mp4 --out /tmp/review --timeline RAGV/timeline.json --expect rotulos.txt
```

- [x] Encuentra todos los rótulos esperados y no el inventado (control); marca el rótulo gris tachado de 5:50 (11-11, Claude).
- [x] Sin `--timeline`, el detector adaptativo encuentra todos los cortes entre escenas de los dos primeros minutos (11-11, Claude).
- [ ] Comparar los planos detectados en el vídeo entero con `timeline.json`.
- [ ] Control de texto cortado: renderizar una escena con un rótulo que se salga del encuadre; debe marcarlo.
- [ ] Control de letra pequeña: un rótulo de 20 px; debe marcarlo y uno de 32 px no.
- [ ] Probarlo en un vídeo hablado (workflow 1) y en una demo de pantalla (workflow 5), donde el texto no es nuestro.
- [ ] Probarlo en Windows (RapidOCR y PySceneDetect dicen funcionar; sin comprobar).

### Pencil → HyperFrames — `scripts/pencil_to_hyperframes.py` (#29)

- [x] Un fotograma (KF 03 del vídeo de RAG): `hyperframes check` sin errores y la captura difiere del PNG de Pencil en 1 nivel de gris de 255 de media (11-11, Claude).
- [x] La skill `pencil-to-hyperframes` se activa con una petición en español (11-11, Claude).
- [x] **Storyboard real** (11-11, Claude): «KF 3b · Trocear», «KF 3b · Vectorizar» y «KF 03 · Buscar» de `scene3.pen`, exportados juntos con `uri` explícito. `states.json` recoge el paso activo (01 → 02 → 03) y el pie; animados desde ahí, las capturas en 1, 4 y 7 s coinciden con cada PNG en la barra de pasos (pastillas unos píxeles más estrechas). La prueba sacó tres fallos, ya arreglados en #29: el lienzo sin nombre que envuelve varios fotogramas, las imágenes relativas al `.pen` y que faltaba el HTML de las capas que entran.
- [ ] Animar la escena entera desde el storyboard, con las capas que entran y salen copiadas de `pencil/<nombre>/`, y **verla en movimiento**.
- [ ] Un diseño con imagen dentro de un `<img>`, un SVG y un componente reutilizable (instancias).
- [ ] Una fuente que no sea Geist.

## Antes de fusionar cualquier PR

- `claude plugin validate .` pasa.
- Si toca una skill: comprobar que se activa (método en `memory/learnings.md`, 08-11).
- Si añade un script: probado contra material real y con un control que deba fallar.
- Guías en es y `.en.md`.
- Lo que no se ha oído ni visto en movimiento, dicho en el PR.

## Pendiente de antes

- Codex y Cursor con las skills (`docs/other-agents.md`).
- Windows de verdad (`docs/windows.md` tiene su lista).
- Un vídeo entero con un agente que no sea Claude Code.
