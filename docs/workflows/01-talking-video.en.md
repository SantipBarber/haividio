# Workflow 1 — Talking-head video: removing mistakes, silences, and filler words

*[Español](01-talking-video.md)*

Tool: [video-use](https://github.com/browser-use/video-use) (skill for Claude Code, MIT).

## Install (once)

Quick option: paste the installation prompt from the video-use README into Claude Code. Claude clones the repo, installs dependencies, configures ffmpeg, registers the skill, and asks for the ElevenLabs key.

Manual option (Mac):

```bash
brew install ffmpeg yt-dlp
git clone https://github.com/browser-use/video-use ~/tools/video-use
ln -s ~/tools/video-use ~/.claude/skills/video-use
cd ~/tools/video-use && uv sync        # or: pip install -e .
cp .env.example .env                   # set ELEVENLABS_API_KEY
```

Manual option (Windows, PowerShell):

```powershell
winget install Gyan.FFmpeg
winget install yt-dlp.yt-dlp
winget install astral-sh.uv
git clone https://github.com/browser-use/video-use $HOME\tools\video-use
New-Item -ItemType Junction -Path "$HOME\.claude\skills\video-use" -Target "$HOME\tools\video-use"
cd $HOME\tools\video-use; uv sync
copy .env.example .env                 # set ELEVENLABS_API_KEY
```

## How it works

Pipeline: **Transcribe → Package → Reason → EDL → Render → Self-review**.

1. **Transcribe** each take with ElevenLabs Scribe: word-level timestamps, who is speaking, laughter, sighs.
2. **Package** all takes into `takes_packed.md` (~12 KB). Claude makes decisions by reading the text, not by watching the video.
3. **Look only when uncertain:** `timeline_view` generates an image with frames, waveform, and words from a section.
4. **Cut** at word boundaries and silences: filler words, false starts, dead time, repetitions (keep the best take). Add a 30 ms audio fade at each cut.
5. **Color-grade** each segment (cinematic warm, neutral with contrast, or a custom ffmpeg chain).
6. **Burn in subtitles** (2 uppercase words by default; customizable).
7. **Self-review:** inspect every cut in the render for jumps, clicks, or obscured subtitles; fix and re-render up to 3 times.

## Usage

```bash
cd ~/Videos/2026-11-xx-mi-video     # folder containing the raw takes
claude
> Assemble these takes into an ~8-minute YouTube video. Remove mistakes and silences. Subtitles: yes.
```

- First, it inventories the material and proposes a strategy; it does not cut until you approve.
- Output: `edit/final.mp4`. Session memory in `edit/project.md` (to continue another day: "shorten the intro").

## Limitations

- Very good for spoken content; less precise for purely visual edits.
- There is no timeline for manual adjustments → if needed, refine in Palmier Pro (macOS only) or Velorn.
- Depends on ElevenLabs for transcription (usage-based cost).

## When you're done

Copy to `videos/<folder>/`: the `.srt` if one was generated, cut notes, and the relevant `project.md`. Not the video.
