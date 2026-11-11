# Workflow 3 — Faceless video (animated explainer with voice-over)

*[Español](03-faceless-video.md)*

Example: "Cómo funciona RAG y qué tecnologías RAG son las más punteras ahora" ("How RAG works and which RAG technologies are at the cutting edge right now").

Tools: [HyperFrames](https://github.com/heygen-com/hyperframes) (or [Remotion](https://www.remotion.dev/docs/ai/skills)) + ElevenLabs TTS + youtubeuploader. video-use is only needed if you record the voice yourself (to clean it up and edit it).

## Install (once)

```bash
# HyperFrames (plugin for Claude Code). Requires Node 22+ and FFmpeg
claude plugin marketplace add heygen-com/hyperframes

# or Remotion (official skills)
npx skills add remotion-dev/skills
```

## Steps

1. **Research and script** → `videos/<folder>/script.md`. Claude researches the topic using current sources and writes a script split into scenes (voice-over text + visual description for each scene).
2. **Script approval.** Do not continue without it.
3. **Voice-over** with ElevenLabs TTS from the script (or record it yourself and clean it up with video-use).
4. **Animated scenes** synchronized with the voice: diagrams, data flows, comparisons, titles. Code in `videos/<folder>/animations/`.
5. **Render** to MP4. `.srt` subtitles and chapters from the timing of every word with `scripts/make_captions.py` (workflow 4).
6. **Thumbnail**, title, and description → `videos/<folder>/publishing.md`.
7. **Publish** (workflow 4).

## Scene template for the script

The sample voice-over in this scene is in Spanish: "Cuando haces una pregunta, el sistema la convierte en un vector..." ("When you ask a question, the system turns it into a vector..."). The visual description shows it becoming a numeric vector that searches a point cloud and highlights the 3 nearest points.

```markdown
### Escena 3 — Recuperación (0:45–1:10)
**Voz:** "Cuando haces una pregunta, el sistema la convierte en un vector..."
**Visual:** la pregunta se transforma en una flecha de números; la flecha busca en una nube de puntos y se iluminan los 3 más cercanos.
```
