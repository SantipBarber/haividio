---
name: talking-video
description: Edits videos of someone talking to camera or in voice-over (talking-head, tutorials, interviews) with video-use - removing silences, mistakes, filler words and repetitions, colour correction, subtitles and animations synced with what is said. Also when the user writes in Spanish, e.g. "edita mis tomas", "quita los silencios", "quita las muletillas", "ponle subtítulos", "vídeo hablando a cámara".
---

# Talking video with video-use

Reply in the user's language.

## Check requirements

```bash
which ffmpeg && ls ~/.claude/skills/video-use && grep -q ELEVENLABS_API_KEY ~/tools/video-use/.env && echo OK
```

If something is missing, install it (see skill `choose-video-tool`) and ask the user for the ElevenLabs key. Never write it in the repo.

## Workflow

1. **Inventory.** List the takes in the folder, their length and what they are about (after transcribing).
2. **Propose a strategy** and wait for approval: target length, what gets removed, order, subtitle style, colour look, planned animations.
3. **Edit with video-use.** Cut on words and silences; with repeated takes, keep the most fluent one.
4. **Animations (optional).** Anchor them to specific phrases in the transcript: "when they say X, Y appears". Build each one with HyperFrames or Remotion applying the skill `visual-identity`.
5. **Self-review.** Check every cut (image jumps, clicks, subtitles covering things) before showing the result.
6. **Deliver** `edit/final.mp4` and summarise what was cut and why.

## Typical requests

- "Remove pauses longer than 0.7 s but let the important sentences breathe."
- "3-word subtitles, at the bottom, no capitals."
- "When I say 'vector database', show the embeddings diagram for 4 seconds."

## When done

Save in the video's folder in the repo: the `.srt` subtitles, the animation code and decision notes. No MP4 or WAV in git.
