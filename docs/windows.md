# Windows

*[English](windows.en.md)*

Cómo producir vídeo con este repo desde Windows. El núcleo del flujo es el mismo que en macOS; aquí van las herramientas de instalación, las diferencias de comandos y qué hacer con lo que es solo de Mac.

## Qué funciona igual

El núcleo es multiplataforma:

- **Node 22+** con `npx hyperframes` (animaciones, renders).
- **ffmpeg / ffprobe** (mezcla de audio, subtítulos, normalización).
- **Python 3** para scripts auxiliares como `build_root.py`.
- **API de ElevenLabs** (voz clonada, música, efectos): es una API REST, funciona igual en cualquier sistema.
- **rclone** para subir el render a Google Drive.
- **Claude Code** funciona en Windows (instalación en PowerShell: `irm https://claude.ai/install.ps1 | iex`; necesita Git for Windows).

## Instalación con winget (PowerShell)

IDs verificados en microsoft/winget-pkgs (2026-11-03):

```powershell
winget install Git.Git
winget install GitHub.GitLFS
winget install OpenJS.NodeJS.LTS      # Node 22 o superior
winget install Gyan.FFmpeg            # incluye ffprobe
winget install Python.Python.3.12
winget install astral-sh.uv           # para video-use (uv sync)
winget install yt-dlp.yt-dlp          # solo para el workflow de vídeo hablado
winget install Rclone.Rclone          # subir a Google Drive
# youtubeuploader no está en winget: zip de https://github.com/porjo/youtubeuploader/releases
git lfs install
```

Tras instalar, cierra y abre la terminal para que el PATH se actualice; comprueba con `ffmpeg -version`, `node -v` (≥ 22) y `python --version`.

## Diferencias de comandos

- En Windows se usa `python` (o `py`) en vez de `python3`: `python build_root.py`.
- Rutas en PowerShell: `$HOME\Desktop\scene-03.mp4` en lugar de `~/Desktop/...`.
- Enlace simbólico de la skill video-use: en vez de `ln -s`, usa una unión de directorios (no requiere administrador):
  `New-Item -ItemType Junction -Path "$HOME\.claude\skills\video-use" -Target "$HOME\tools\video-use"`
- Skills del repositorio: `.agents/skills` y `.claude/skills` son enlaces simbólicos. Sin el Modo desarrollador, Git los clona como ficheros de texto. Actívalo y clona con `git clone -c core.symlinks=true ...`, o crea una unión: `New-Item -ItemType Junction -Path .agents\skills -Target plugins\video-studio\skills` (borra antes el fichero; lo mismo para `.claude\skills`). Detalles en [other-agents.md](other-agents.md).
- La vista previa de HyperFrames se abre en Chrome o Edge, que reproducen el audio.
- Finales de línea: el repo trae `.gitattributes` con `eol=lf`, no hace falta tocar `core.autocrlf`.

## HyperFrames en Windows (estado: sin probar por nosotros)

- Requisitos oficiales: Node.js 22+ y FFmpeg. La app de escritorio de HyperFrames tiene descarga para macOS, Windows y Linux.
- Las notas de versión recientes incluyen arreglos específicos de Windows (v0.8.207: instalación, check y preview en más configuraciones, `init` sin Modo desarrollador; v0.8.219: `check`, `snapshot` y `render` ya no fallan por un log de Chrome bloqueado). Usa una versión igual o posterior a la 0.8.219.
- Primeros pasos: `npx hyperframes doctor` y `npx hyperframes browser ensure` (descarga Chrome Headless Shell).
- Prueba mínima: renderizar `videos/2026-10-31-rag-2026/animations/scene-03` (comandos de la sección del README) y después el vídeo completo `rag-video`. Ojo: `rag-video` necesita los mp3 de voz, música y efectos en `assets/`, que no están en git; hay que copiarlos aparte o regenerarlos con ElevenLabs.
- Si falla el render nativo: usa **WSL2** (Ubuntu) y sigue las instrucciones de Linux (`sudo apt install ffmpeg`, Node 22 con nvm). Según las notas de versión, en WSL el render usa la GPU a través de Chrome completo.
- Aún no lo hemos probado en un Windows real. Casilla pendiente:

### Probado en Windows: pendiente

- [ ] `npx hyperframes doctor` pasa sin errores
- [ ] preview con audio suena
- [ ] render de scene-03 sale correcto
- [ ] render de rag-video sale correcto
- [ ] `python build_root.py` regenera `index.html` con las tildes correctas

## Solo macOS y alternativas en Windows

| Herramienta | Por qué no | Alternativa en Windows |
|---|---|---|
| Palmier Pro | Editor nativo de macOS 26 + Apple Silicon | Velorn u otro editor (comprobar plataforma), o DaVinci Resolve |
| mlx-audio + Qwen3-TTS | MLX solo funciona en Apple Silicon | Qwen3-TTS con PyTorch + CUDA (GPU NVIDIA), sin probar. La voz del canal se hace con ElevenLabs, que es una API y funciona igual |
| QuickTime (grabar la muestra de voz) | App de macOS | Grabadora de sonido de Windows o Audacity (`winget install Audacity.Audacity`). Después, la misma limpieza con ffmpeg |
| `brew install whisper-cpp` (transcribir con HyperFrames) | Homebrew | whisper.cpp publica binarios para Windows; o usar ElevenLabs Scribe. Sin probar |
