# Channel visual identity

*[Español](identity.md)*

> **Status:** proposal, pending a choice of direction. Once one is chosen, remove the other two and make this the official guide used by the `visual-identity` skill.

## Priority

Make the video **visual, bold and modern**. It is fine if it looks AI-made; what we want to avoid is a generic or templated look. Real data and resources are better than filler illustrations (see `docs/open-resources.md`).

## D. Dark modern (used in the first test, scene 3 of the RAG video)

| Token | Value |
|---|---|
| Background | `#07080B` with `#1C2029` dot grid |
| Panels | `#0F1116`, border `#232733` |
| Text | `#F4F5F7`, secondary `#8B90A0` |
| Accent | Electric lime `#D4FF3A` |
| Categories | Cyan `#5CE1E6`, violet `#A78BFA`, coral `#FF6B4A` |
| Typeface | Geist (headings 800, body 400–700) + Geist Mono (data, labels) |
| Motion | `expo.out` for entrances, `back.out` for elements that "land", short stagger |
| Signature | Top step bar (01–04) with the active step in lime; explanatory subtitle below |
| Minimum text size | 32 px at 1080p for anything that matters; the explanatory subtitle at the bottom, 40 px. 28 px is the minimum `hyperframes check` enforces, not a target: on a phone held upright it looks about 6 px tall |

Reference code: `videos/2026-10-31-rag-2026/animations/scene-03/` (HyperFrames).

CSS variables: [`tokens.css`](tokens.css). It holds the palette under its own names (`--lime`, `--panel`…) plus the theme tokens read by components from the HyperFrames catalog (`--bg`, `--surface`, `--fg`, `--brand`, `--accent`, `--font-body`…). Copy it to each project's `assets/` and link it from the root composition: a component installed with `npx hyperframes add` then comes out in the palette and Geist instead of Inter and its default greens. Blocks do not read those tokens: change their colours in the installed code.

## Avoiding a templated look

- ❌ Purple-blue-pink gradients, neon, glassmorphism, glows.
- ❌ Inter, Poppins or Roboto as the primary typeface.
- ❌ Cliché iconography: brains, robots, glowing neural networks, chips, "the Matrix".
- ❌ Filler stock or AI-generated images.
- ❌ Copy such as «revolucionario» (revolutionary), «desbloquea» (unlock) or «en el mundo actual…» (in today's world…).
- ❌ Using the same animation everywhere (fade-in + slide-up) and the same easing.
- ❌ Flat voice with no pauses or emphasis; generic corporate music.
- ✅ A short palette (3–4 colors), used with discipline.
- ✅ A recurring "signature": a 3-second intro, chapter numbers, a way of drawing arrows, a transition sound.
- ✅ Intentional imperfection: hand-drawn strokes, texture, varied rhythm.
- ✅ A point of view in the script: «yo haría esto» (I'd do this), «esto está sobrevalorado» (this is overrated).

## Three proposed directions

### A. Engineer's notebook

Explain things as if on a whiteboard or in a notebook: approachable, handmade, and very different from typical AI content.

| Token | Value |
|---|---|
| Background | Warm paper `#F3EEE3` with subtle texture |
| Ink | `#1C1B19` |
| Accent | Rust orange `#D9481C` |
| Secondary | Pencil blue `#2F5D8A` |
| Headings | Young Serif |
| Labels and code | IBM Plex Mono |
| Shapes | Irregular rough.js-style strokes, hand-drawn arrows, marker underlines |
| Motion | Strokes draw on (stroke reveal), smooth easing, slight stroke jitter |
| Signature | Each chapter title is "handwritten"; page number in the corner |

### B. Amber terminal

Amber phosphor monitor aesthetic: technical, distinctive, ideal for a developer audience.

| Token | Value |
|---|---|
| Background | Warm near-black `#0E0D0B` |
| Primary | Amber `#FFB000` |
| Secondary | Stone gray `#8A857C` |
| Alert | Red `#FF5A36` |
| Typeface | JetBrains Mono throughout; headings in uppercase |
| Shapes | Boxes with ASCII borders (`┌─┐`), block progress bars |
| Motion | Character-by-character typing, hard cuts (steps, no easing), blinking cursor, very subtle scanlines |
| Signature | `$ ` prompt before each chapter; mechanical key sound on transitions |

### C. Swiss editorial

A design magazine: clean, oversized typography, lots of space. Serious and premium.

| Token | Value |
|---|---|
| Background | Off-white `#F5F4F0` |
| Text | `#111111` |
| Accent | Signal red `#E63312` |
| Secondary | Gray `#9A9A96` |
| Typeface | Archivo (oversized headings, weight 800) + Archivo Narrow (labels) |
| Shapes | 12-column grid, geometric rectangles and arrows, oversized chapter numbers ("03") |
| Motion | Grid-aligned slides, expo-out easing, staggered entrances |
| Signature | Oversized chapter number enters from the edge; red line sweeps across the screen |

## Voice and sound (shared)

- Voice: your own recorded voice (recommended for identity) or an ElevenLabs clone of your voice. If using a catalog voice, choose one and use it every time.
- Pace: ~150 words/minute, with pauses before key ideas.
- Music: one recurring background track, at −18 dB under the voice.
- A distinctive transition sound, always the same.

## Formats

- Long video: 1920×1080, 30 fps.
- Short: 1080×1920, safe area of 150 px at the top and bottom.
- Thumbnail: 1280×720, maximum 4 words, same background and accent as the video.
