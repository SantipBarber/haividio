# Workflow 3 — Vídeo sin cara (explicativo animado con voz en off)

*[English](03-faceless-video.en.md)*

Ejemplo: "Cómo funciona RAG y qué tecnologías RAG son las más punteras ahora".

Herramientas: [HyperFrames](https://github.com/heygen-com/hyperframes) (o [Remotion](https://www.remotion.dev/docs/ai/skills)) + ElevenLabs TTS + youtubeuploader. video-use solo entra si la voz la grabas tú (para limpiarla y cortarla).

## Instalación (una vez)

```bash
# HyperFrames (plugin para Claude Code). Requiere Node 22+ y FFmpeg
claude plugin marketplace add heygen-com/hyperframes

# o Remotion (skills oficiales)
npx skills add remotion-dev/skills
```

## Pasos

1. **Investigación y guion** → `videos/<carpeta>/script.md`. Claude investiga el tema con fuentes actuales y escribe el guion dividido en escenas (texto de voz + descripción visual de cada escena).
2. **Aprobación del guion.** No seguir sin ella.
3. **Voz en off** con ElevenLabs TTS a partir del guion (o grabarla tú y limpiarla con video-use).
4. **Escenas animadas** sincronizadas con la voz: diagramas, flujos de datos, comparativas, títulos. Código en `videos/<carpeta>/animations/`.
5. **Render** a MP4 (+ subtítulos `.srt` si se quiere).
6. **Miniatura**, título y descripción → `videos/<carpeta>/publishing.md`.
7. **Publicar** (workflow 4).

## Plantilla de escena en el guion

```markdown
### Escena 3 — Recuperación (0:45–1:10)
**Voz:** "Cuando haces una pregunta, el sistema la convierte en un vector..."
**Visual:** la pregunta se transforma en una flecha de números; la flecha busca en una nube de puntos y se iluminan los 3 más cercanos.
```
