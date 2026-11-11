---
name: choose-video-tool
description: Decides which tool to use for a video (editing takes, adding animations, faceless video, shorts, product demos, publishing to YouTube) and explains how to use it. Use it when starting any video or when the user asks "what do I make this with?". Also when the user writes in Spanish, e.g. "¿con qué hago este vídeo?", "quiero hacer un vídeo", "qué herramienta uso", "editar mis tomas", "hacer un short".
---

# Choose the video tool

Reply in the user's language.

Before recommending, ask at most two questions if it is not clear:
1. Is there the user's own footage (camera or voice), or does the video start from scratch?
2. Does it need visual review on a timeline, or is the final result enough?

## Decision tree

```
Is there recorded footage of someone talking?
├─ Yes → Only clean it up (silences, mistakes, filler words, subtitles)?
│        ├─ Yes → video-use                          → skill talking-video
│        └─ No, also animations on top
│               → video-use + HyperFrames/Remotion   → skill talking-video (animations section)
│        Wants to retouch by hand on a timeline?
│               → add Palmier Pro (macOS 26 + Apple Silicon) or Velorn
│
├─ Demo of an application with screen recording and a cloned voice?
│       → Playwright + ffmpeg + HyperFrames → docs/workflows/05-product-demo.md
│
└─ No → Explainer / diagrams / motion graphics / short?
         → HyperFrames (default) or Remotion + ElevenLabs voice → skill faceless-video
         Does the user record the voice? → clean it first with video-use

Always at the end → skill publish-youtube
Whenever there are animations → skill visual-identity
```

## HyperFrames vs Remotion

| Choose | When |
|---|---|
| **HyperFrames** | Diagrams, animated typography, explainer-style scenes, data charts, code and terminal scenes. Written in HTML/CSS, fast iteration, live preview, a catalog of ~450 blocks and components (`npx hyperframes catalog`). Apache 2.0. |
| **Remotion** | Highly programmatic animations and reusable templates in React. Free for individuals and teams of ≤3; companies need a licence. |

## Alternatives by constraint

| Constraint | Option |
|---|---|
| Zero cost, no APIs | auto-editor + local Whisper (or videocut-skills) instead of video-use |
| Already uses Final Cut | fcp-mcp-server (rough cut via FCPXML) |
| Already uses Premiere | premiere-pro-mcp (experimental) |
| Already uses DaVinci | davinci-resolve-mcp (requires Resolve **Studio**) |
| Wants everything in the cloud | Descript MCP, OpusClip MCP or invideo MCP (paid) |

## Quick install

```bash
# Editing takes
brew install ffmpeg
# Windows: winget install Gyan.FFmpeg  (see docs/windows.md)
git clone https://github.com/browser-use/video-use ~/tools/video-use
ln -s ~/tools/video-use ~/.claude/skills/video-use   # + ELEVENLABS_API_KEY in .env

# Animation
claude plugin marketplace add heygen-com/hyperframes   # Node 22+ and FFmpeg
npx skills add remotion-dev/skills

# Editor with MCP (with the app open)
claude mcp add --transport http palmier-pro http://127.0.0.1:19789/mcp   # macOS only
```

## Rules

- Check prices and requirements on the web if the information is more than a few months old: this ecosystem changes every month.
- Recommend a single main option and at most one alternative; do not list the whole catalogue.
- If the work is in the `haividio` repo, each tool is detailed in `docs/tools.md` and the workflows in `docs/workflows/`; every guide has an English version (`.en.md`) next to the Spanish one.
