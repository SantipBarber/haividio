---
name: faceless-video
description: Produces faceless videos (animated explainers, technical outreach, shorts) from scratch - research, scene-by-scene script, voice-over, animations with HyperFrames or Remotion, render and subtitles. Also when the user writes in Spanish, e.g. "vídeo sin cara", "vídeo explicativo", "hazme un short", "guion por escenas", "vídeo animado con voz en off".
---

# Faceless video

Reply in the user's language. The script and the voice-over go in the language the user asks for the video.

## Phases (do not skip the approval)

1. **Research.** Look for current sources on the topic; note the URLs in the script. Every concrete fact (figures, names, dates) needs a source.
2. **Scene-by-scene script** in `guion.md`, with this format (headings in the video's language):

   ```markdown
   ### Scene N — Title (mm:ss–mm:ss)
   **Voice:** exact text to be spoken.
   **Visual:** what is shown and how it moves.
   **Source:** URL (if there is data).
   ```

   Pace: ~150 words per minute in Spanish (measure the real pace of the chosen voice). Hook in the first 15 s. One idea per scene.
3. **Script approval** by the user. Without it, do not generate voice or animations.
4. **Voice.** ElevenLabs TTS (voice chosen in `docs/estilo/identidad.md`) or the user's recording cleaned with video-use. Generate one track per scene so you can adjust without redoing everything.
5. **Animation.** One composition per scene, as long as its voice track. Apply the skill `visual-identity` to all of them. Try 1 scene first and show it before doing the rest.
6. **Assembly and render.** Join scenes, voice, music (optional, -18 dB under the voice) and subtitles. Export 1920×1080 at 30 fps (or 1080×1920 for shorts).
7. **Publishing.** Prepare `publicacion.md` and move on to the skill `publish-youtube`.

## Tips

- Diagrams that build step by step with the voice beat long on-screen text.
- At most ~8 words of on-screen text at a time.
- Reuse components from previous videos (`videos/*/animaciones/`).
