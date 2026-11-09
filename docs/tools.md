# Catálogo de herramientas (investigación de octubre 2026)

*[English](tools.en.md)*

Herramientas para editar y producir vídeo con Claude Code mediante MCP, skills o plugins. Las marcadas con ⚠️ no se pudieron verificar en su repositorio oficial.

## 1. Editores de escritorio con MCP (estilo pencil.dev: app con timeline + Claude Code la controla)

| Herramienta | Qué es | Precio | Mac | Notas |
|---|---|---|---|---|
| **Palmier Pro** ⚠️ | Editor nativo macOS (Swift). Abre un MCP local en `http://127.0.0.1:19789/mcp` mientras está abierto. | Editor, MCP y chat gratis (GPLv3). IA generativa (Seedance, Kling, Nano Banana) por créditos. | Requiere macOS 26 Tahoe + Apple Silicon | `claude mcp add --transport http palmier-pro http://127.0.0.1:19789/mcp` — [guía](https://tosea.ai/blog/palmier-pro-ai-video-editor-mac-guide) |
| **Velorn** ⚠️ | Editor open source multiplataforma, timeline multipista, Whisper local, FFmpeg, MCP local. | Gratis (GPLv3). Generación de vídeo opcional vía ComfyUI. | Sí | Proyecto de una sola persona — [repo](https://github.com/VelornLabs/velorn) |
| **DaVinci Resolve MCP** | MCP comunitario (32 herramientas). | Gratis, pero **requiere Resolve Studio 18+** (de pago); la versión free no permite scripting externo. | Sí | Poco maduro — [tooflex](https://github.com/tooflex/davinci-resolve-mcp), [lordhoell](https://github.com/lordhoell/davinci-resolve-mcp) |
| **Premiere Pro MCP** | Puente vía panel CEP/UXP. | MIT + suscripción Adobe | Sí | Instalación con Premiere real no verificada en CI — [repo](https://github.com/leancoderkavy/premiere-pro-mcp) |
| **fcp-mcp-server** | Final Cut Pro vía FCPXML: rough cut por transcripción, marcadores. | MIT | Sí | Exportar el timeline de FCP es manual — [PyPI](https://pypi.org/project/fcp-mcp-server/) |
| **Descript MCP** | MCP oficial (Settings → Descript MCP): importar, editar con Underlord, exportar SRT, publicar. | Nube de pago, gasta minutos/créditos | Sí | [docs](https://help.descript.com/api-and-mcp/mcp.md) |
| **Kdenlive MCP** | 60+ herramientas, control en vivo. | MIT | Sí | Requiere Kdenlive modificado con WebSocket. Experimental — [PyPI](https://pypi.org/project/kdenlive-mcp/) |
| OpenCut / CapCut ⚠️ | MCPs comunitarios muy verdes o no verificados. | — | — | No recomendados por ahora |
| OpusClip MCP | Nube: clips, subtítulos, reencuadre para shorts. | Pago | — | [blog](https://www.opus.pro/blog/claude-video-editing-mcp) |
| invideo MCP | Nube: timeline, generación y export desde Claude Code. | Pago | — | `claude mcp add --transport http --scope user invideo https://mcp.invideo.io/mcp` |

## 2. Skills y herramientas de código para Claude Code

| Herramienta | Para qué | Precio | Notas |
|---|---|---|---|
| **video-use** (browser-use) | Editar metraje en bruto → `edit/final.mp4`. Cortes, color, subtítulos, animaciones. | MIT. Requiere API key de ElevenLabs (Scribe) | Ver `workflows/01-talking-video.md` — [repo](https://github.com/browser-use/video-use) |
| **HyperFrames** (HeyGen) | HTML → MP4, pensado para agentes. App macOS con preview "Studio". | Apache 2.0, gratis | `claude plugin marketplace add heygen-com/hyperframes`. Requiere Node 22+ y FFmpeg — [repo](https://github.com/heygen-com/hyperframes) |
| **Remotion** | Vídeo programado en React, skills oficiales. | Gratis para individuos y equipos ≤3. Empresa: $25/mes por dev | `npx skills add remotion-dev/skills` — [docs](https://www.remotion.dev/docs/ai/skills), [licencia](https://www.remotion.dev/docs/license/faq) |
| videocut-skills ⚠️ | Quita muletillas y silencios >1 s, subtítulos con Whisper large-v3 local. | MIT, sin APIs de pago (~5 GB) | [ficha](https://www.sourcepulse.org/projects/22803490) |
| auto-editor + Whisper | Alternativa local y gratuita para cortar silencios. | Gratis | Claude Code los ejecuta directamente desde la terminal |
| claude-youtube-editor | Proyecto open source de flujo completo (corte, animaciones, miniatura, subida). | Repo gratis; algunos servicios de pago | [repo](https://github.com/hassancs91/claude-youtube-editor), [guía](https://learnwithhasan.com/guide/claude-code-video-editing/) |
| MCPs de FFmpeg | `mcp-ffmpeg`, `mcp-video` (`uvx mcp-video`) | Gratis | Normalmente innecesarios: Claude Code ya ejecuta ffmpeg |

## 3. Publicación en YouTube

| Herramienta | Qué hace | Notas |
|---|---|---|
| **[youtubeuploader](https://github.com/porjo/youtubeuploader)** (recomendada) | CLI: sube como privado u oculto, con miniatura, subtítulos SRT, lista de reproducción y metadatos en JSON | Apache-2.0, gratis. Mac (`brew`), Windows (zip) y Linux. OAuth de Google Cloud + YouTube Data API v3. v1.25.5, actividad en agosto de 2026 |
| [youtube-uploader-mcp](https://github.com/anwerj/youtube-uploader-mcp) | MCP: lo mismo, más cambiar la visibilidad después y marcar contenido sintético | MIT, gratis. Mac, Windows y Linux. v0.3.1 (31-10-2026), pocos usuarios: **revisar el código antes de dar acceso al canal** |

Un proyecto de Google Cloud sin auditar puede dejar privados y bloqueados los vídeos subidos por la API: prueba antes con un vídeo corto (ver [workflow 4](workflows/04-publish-youtube.md)).

## Recomendación de stacks

- **Vídeo hablado (talking-head):** video-use → (opcional) retoque en Palmier Pro / Velorn → youtubeuploader. Alternativa coste cero: auto-editor/videocut-skills + Whisper local.
- **Motion graphics, shorts y vídeos sin cara:** HyperFrames (o Remotion) + ElevenLabs TTS → youtubeuploader.

Demo de producto con grabación de pantalla: Playwright + ffmpeg + HyperFrames + ElevenLabs ([workflow 5](workflows/05-product-demo.md)). Voz: [cloned-voice.md](cloned-voice.md).

Windows: ver [docs/windows.md](windows.md).
