# Windows

*[Español](windows.md)*

How to produce video with this repo on Windows. The core workflow is the same as on macOS; this guide covers installation tools, command differences, and alternatives for Mac-only tools.

## What works the same

The core is cross-platform:

- **Node 22+** with `npx hyperframes` (animations, renders).
- **ffmpeg / ffprobe** (audio mixing, subtitles, normalization).
- **Python 3** for helper scripts such as `build_root.py`.
- **ElevenLabs API** (cloned voice, music, effects): it is a REST API and works the same on any system.
- **rclone** to upload the render to Google Drive.
- **Claude Code** works on Windows (PowerShell installation: `irm https://claude.ai/install.ps1 | iex`; requires Git for Windows).

## Install with winget (PowerShell)

IDs verified in microsoft/winget-pkgs (2026-11-03):

```powershell
winget install Git.Git
winget install GitHub.GitLFS
winget install OpenJS.NodeJS.LTS      # Node 22 or later
winget install Gyan.FFmpeg            # includes ffprobe
winget install Python.Python.3.12
winget install astral-sh.uv           # for video-use (uv sync)
winget install yt-dlp.yt-dlp          # talking-video workflow only
winget install Rclone.Rclone          # upload to Google Drive
# youtubeuploader is not on winget: download the zip from https://github.com/porjo/youtubeuploader/releases
git lfs install
```

After installing, close and reopen the terminal to update PATH; check with `ffmpeg -version`, `node -v` (≥ 22), and `python --version`.

## Command differences

- On Windows, use `python` (or `py`) instead of `python3`: `python build_root.py`.
- PowerShell paths: `$HOME\Desktop\scene-03.mp4` instead of `~/Desktop/...`.
- To symlink the video-use skill, use a directory junction instead of `ln -s` (no administrator rights required):
  `New-Item -ItemType Junction -Path "$HOME\.claude\skills\video-use" -Target "$HOME\tools\video-use"`
- Repository skills: `.agents/skills` and `.claude/skills` are symlinks. Without Developer Mode, Git checks them out as text files. Turn it on and clone with `git clone -c core.symlinks=true ...`, or create a junction: `New-Item -ItemType Junction -Path .agents\skills -Target plugins\video-studio\skills` (delete the file first; do the same for `.claude\skills`). Details in [other-agents.md](other-agents.en.md).
- Open the HyperFrames preview in Chrome or Edge; they play the audio.
- Line endings: the repo includes `.gitattributes` with `eol=lf`; there is no need to change `core.autocrlf`.

## HyperFrames on Windows (not tested by us)

- Official requirements: Node.js 22+ and FFmpeg. The HyperFrames desktop app is available for macOS, Windows, and Linux.
- Recent release notes include Windows-specific fixes (v0.8.207: installation, check, and preview in more configurations, `init` without Developer Mode; v0.8.219: `check`, `snapshot`, and `render` no longer fail because of a blocked Chrome log). Use version 0.8.219 or later.
- Getting started: `npx hyperframes doctor` and `npx hyperframes browser ensure` (downloads Chrome Headless Shell).
- Minimum test: render `videos/2026-10-31-rag-2026/animations/scene-03` (commands in the README section), then the full `rag-video`. Note: `rag-video` needs the voice, music, and effects mp3s in `assets/`, which are not in git; copy them separately or regenerate them with ElevenLabs.
- If native rendering fails: use **WSL2** (Ubuntu) and follow the Linux instructions (`sudo apt install ffmpeg`, Node 22 with nvm). According to the release notes, rendering in WSL uses the GPU through full Chrome.
- We have not tested this on a real Windows machine yet. Checklist:

### Tested on Windows: pending

- [ ] `npx hyperframes doctor` passes without errors
- [ ] preview audio plays
- [ ] scene-03 render is correct
- [ ] rag-video render is correct
- [ ] `python build_root.py` regenerates `index.html` with accents correct

## macOS only and Windows alternatives

| Tool | Why not | Windows alternative |
|---|---|---|
| Palmier Pro | Native macOS 26 + Apple Silicon editor | Velorn or another editor (check platform support), or DaVinci Resolve |
| mlx-audio + Qwen3-TTS | MLX only works on Apple Silicon | Qwen3-TTS with PyTorch + CUDA (NVIDIA GPU), untested. The channel voice uses ElevenLabs, which is an API and works the same |
| QuickTime (recording the voice sample) | macOS app | Windows Sound Recorder or Audacity (`winget install Audacity.Audacity`). Then use the same ffmpeg cleanup |
| `brew install whisper-cpp` (transcribe with HyperFrames) | Homebrew | whisper.cpp publishes Windows binaries; or use ElevenLabs Scribe. Untested |
