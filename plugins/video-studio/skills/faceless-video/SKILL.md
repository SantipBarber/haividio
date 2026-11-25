---
name: faceless-video
description: Produces faceless videos (animated explainers, technical outreach, shorts) from scratch - research, scene-by-scene script, voice-over, animations with HyperFrames or Remotion, render and subtitles. Use it too for a single step on a video that is already edited - lowering (ducking) background music under a voice-over, comparing a voice-over with its script, replacing a sentence of it with an approved take, or the visual review of a render (cut-off or small text, missing labels, still stretches). Not the review before publishing to YouTube (skill publish-youtube). Also when the user writes in Spanish, e.g. "vídeo sin cara", "vídeo explicativo", "hazme un short", "guion por escenas", "vídeo animado con voz en off", "baja la música cuando habla la voz", "busca textos cortados o tramos quietos en el render".
---

# Faceless video

Reply in the user's language. The script and the voice-over go in the language the user asks for the video.

**Paths:** `<skill-dir>` is the folder that contains this `SKILL.md`. Replace it with that folder's absolute path in every command, and run the commands from the user's project folder. Files in `references/` are in that folder too. If a script this skill names is missing, stop and tell the user which one, and suggest reinstalling the skill. Do not rewrite it, do not do its step by hand, and do not search for, download or use a copy from anywhere else (another folder, the repository, the web). Stop even if you cannot ask the user: end with that message. Scripts run with `uv run` declare their own dependencies ([uv](https://docs.astral.sh/uv/) installs them the first time, which needs network).

## Phases (do not skip the approval)

1. **Research.** Look for current sources on the topic; note the URLs in the script. Every concrete fact (figures, names, dates) needs a source.
2. **Scene-by-scene script** in `script.md`, with this format (headings in the video's language):

   ```markdown
   ### Scene N — Title (mm:ss–mm:ss)
   **Voice:** exact text to be spoken.
   **Visual:** what is shown and how it moves.
   **Source:** URL (if there is data).
   ```

   Pace: ~150 words per minute in Spanish (measure the real pace of the chosen voice). Hook in the first 15 s. One idea per scene.
3. **Script approval** by the user. Without it, do not generate voice or animations.
4. **Voice.** ElevenLabs TTS (the voice set in the project's identity, skill `visual-identity`, or the one the user chooses) or the user's recording cleaned with video-use. Generate one track per scene so you can adjust without redoing everything. Read `references/cloned-voice.md` first. With ElevenLabs:
   - `python3 "<skill-dir>/scripts/tts.py" file audio/voice/scene-3 scene-3.txt` writes the mp3 and its word timings (`--lang` for another language, `--pron` for a pronunciation map). It spends credits: say how many characters and wait for the user's approval.
   - `uv run "<skill-dir>/scripts/check_voice.py" scene-3.mp3 --words scene-3.words.json` compares the voice with the script (WhisperX, local; the first run downloads several GB: ask first; `--language` for a language other than Spanish). `--text script.txt` for a recording.
   - `python3 "<skill-dir>/scripts/splice_voice.py"` replaces a sentence or a word with an approved take instead of regenerating the scene, at no cost. `--help` has the syntax.
5. **Animation.** One composition per scene, as long as its voice track. Apply the skill `visual-identity` to all of them, and look in the HyperFrames catalog before building a chart, a transition or a code scene by hand. Try 1 scene first and show it before doing the rest.
6. **Assembly and render.** Join scenes, voice, music (optional) and subtitles. For music, run `uv run "<skill-dir>/scripts/duck_music.py"` so it dips under the voice and check the stretches it flags (see `references/editing-and-verification.md`, "Mix and volume"). Export 1920×1080 at 30 fps (or 1080×1920 for shorts); with HyperFrames, the final render goes with `-q delivery --video-bitrate 8M` (without the bitrate, flat dark scenes came out at 0.5 Mbps). Open on a cover (the title, like the thumbnail) for the first 1–2 s, not on an animation halfway through. Then run `uv run "<skill-dir>/scripts/check_render.py"` on the render (see `references/editing-and-verification.md`, "Visual review of the render"), look at its contact sheet and put what it flags in `REVIEW.md` before showing the video.
7. **Publishing.** Prepare `publishing.md` and move on to the skill `publish-youtube`.

## Tips

- Diagrams that build step by step with the voice beat long on-screen text.
- At most ~8 words of on-screen text at a time.
- Reuse components from previous videos (`videos/*/animations/`).
- **Tutorials of code or a terminal** (Claude Code, an agent, a script): HyperFrames already has `code-typing`, `code-diff`, `code-highlight`, `code-scroll`, `code-morph`, `code-terminal-run`, `agent-cursor` and `cursor-zoom-follow`. Use a real terminal recording (VHS) only when the output must be real.
- **Data:** `data-chart`, `chart-story`, `mk-line-graph`, `count-up`, `spain-map`. Real data from open sources, with the source on screen.
