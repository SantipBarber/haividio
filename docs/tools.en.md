# Tool catalogue (October 2026 research)

*[Español](tools.md)*

Tools for editing and producing video with Claude Code through MCP, skills or plugins. Those marked ⚠️ could not be verified against their official repository.

## 1. Desktop editors with MCP (pencil.dev style: an app with a timeline controlled by Claude Code)

| Tool | What it is | Price | Mac | Notes |
|---|---|---|---|---|
| **Palmier Pro** ⚠️ | Native macOS editor (Swift). Opens a local MCP at `http://127.0.0.1:19789/mcp` while running. | Editor, MCP and chat are free (GPLv3). Generative AI (Seedance, Kling, Nano Banana) uses credits. | Requires macOS 26 Tahoe + Apple Silicon | `claude mcp add --transport http palmier-pro http://127.0.0.1:19789/mcp` — [guide](https://tosea.ai/blog/palmier-pro-ai-video-editor-mac-guide) |
| **Velorn** ⚠️ | Open-source cross-platform editor, multi-track timeline, local Whisper, FFmpeg and local MCP. | Free (GPLv3). Optional video generation through ComfyUI. | Yes | One-person project — [repo](https://github.com/VelornLabs/velorn) |
| **DaVinci Resolve MCP** | Community MCP (32 tools). | Free, but **requires paid Resolve Studio 18+**; the free version does not allow external scripting. | Yes | Not very mature — [tooflex](https://github.com/tooflex/davinci-resolve-mcp), [lordhoell](https://github.com/lordhoell/davinci-resolve-mcp) |
| **Premiere Pro MCP** | Bridge through a CEP/UXP panel. | MIT + Adobe subscription | Yes | Installation with real Premiere not verified in CI — [repo](https://github.com/leancoderkavy/premiere-pro-mcp) |
| **fcp-mcp-server** | Final Cut Pro through FCPXML: transcript-based rough cuts, markers. | MIT | Yes | Exporting the FCP timeline is manual — [PyPI](https://pypi.org/project/fcp-mcp-server/) |
| **Descript MCP** | Official MCP (Settings → Descript MCP): import, edit with Underlord, export SRT and publish. | Paid cloud service; uses minutes/credits | Yes | [docs](https://help.descript.com/api-and-mcp/mcp.md) |
| **Kdenlive MCP** | 60+ tools, live control. | MIT | Yes | Requires Kdenlive modified with WebSocket. Experimental — [PyPI](https://pypi.org/project/kdenlive-mcp/) |
| OpenCut / CapCut ⚠️ | Very early or unverified community MCPs. | — | — | Not recommended for now |
| OpusClip MCP | Cloud: clips, subtitles and reframing for shorts. | Paid | — | [blog](https://www.opus.pro/blog/claude-video-editing-mcp) |
| invideo MCP | Cloud: timeline, generation and export from Claude Code. | Paid | — | `claude mcp add --transport http --scope user invideo https://mcp.invideo.io/mcp` |

## 2. Skills and code tools for Claude Code

| Tool | What for | Price | Notes |
|---|---|---|---|
| **video-use** (browser-use) | Edit raw footage → `edit/final.mp4`. Cuts, color, subtitles, animations. | MIT. Requires an ElevenLabs API key (Scribe) | See [workflow 1](workflows/01-talking-video.en.md) — [repo](https://github.com/browser-use/video-use) |
| **HyperFrames** (HeyGen) | HTML → MP4, designed for agents. macOS app with «Studio» preview. | Apache 2.0, free | `claude plugin marketplace add heygen-com/hyperframes`. Requires Node 22+ and FFmpeg — [repo](https://github.com/heygen-com/hyperframes) |
| **Remotion** | Programmatic video in React, official skills. | Free for individuals and teams of ≤3. Enterprise: $25/month per dev | `npx skills add remotion-dev/skills` — [docs](https://www.remotion.dev/docs/ai/skills), [license](https://www.remotion.dev/docs/license/faq) |
| videocut-skills ⚠️ | Removes filler words and silences >1 s, subtitles with local Whisper large-v3. | MIT, no paid APIs (~5 GB) | [listing](https://www.sourcepulse.org/projects/22803490) |
| auto-editor + Whisper | Free local alternative for cutting silences. | Free | Claude Code runs them directly from the terminal |
| claude-youtube-editor | Open-source end-to-end workflow (cuts, animations, thumbnail, upload). | Free repo; some paid services | [repo](https://github.com/hassancs91/claude-youtube-editor), [guide](https://learnwithhasan.com/guide/claude-code-video-editing/) |
| FFmpeg MCPs | `mcp-ffmpeg`, `mcp-video` (`uvx mcp-video`) | Free | Usually unnecessary: Claude Code can already run ffmpeg |

## 3. YouTube publishing

| Tool | What it does | Notes |
|---|---|---|
| **[youtubeuploader](https://github.com/porjo/youtubeuploader)** (recommended) | CLI: uploads as private or unlisted, with thumbnail, SRT subtitles, playlist, metadata and declarations (made for kids, synthetic content) in JSON | Apache-2.0, free. Mac (`brew`), Windows (zip) and Linux. Google Cloud OAuth + YouTube Data API v3. v1.25.5, active in August 2026 |
| [youtube-uploader-mcp](https://github.com/anwerj/youtube-uploader-mcp) | MCP: the same, plus changing visibility later | MIT, free. Mac, Windows and Linux. v0.3.1 (31-10-2026), few users: **review the code before granting access to your channel** |

An unaudited Google Cloud project may leave videos uploaded through the API private and blocked: test first with a short video (see [workflow 4](workflows/04-publish-youtube.en.md)).

## Recommended stacks

- **Talking-head video:** video-use → (optional) finishing in Palmier Pro / Velorn → youtubeuploader. Zero-cost alternative: auto-editor/videocut-skills + local Whisper.
- **Motion graphics, shorts and faceless videos:** HyperFrames (or Remotion) + ElevenLabs TTS → youtubeuploader.

Product demo with screen recording: Playwright + ffmpeg + HyperFrames + ElevenLabs ([workflow 5](workflows/05-product-demo.en.md)). Voice: [cloned-voice.en.md](cloned-voice.en.md).

Windows: see [docs/windows.en.md](windows.en.md).
