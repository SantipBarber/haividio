---
name: visual-identity
description: Applies the channel's visual identity (palette, typefaces, motion, signature) to animations, scenes and thumbnails so they look visual, bold and modern, not generic. Use it whenever you create an animation, scene, overlay or thumbnail. Also when the user writes in Spanish, e.g. "hazme una miniatura", "anima esta escena", "estilo del canal", "identidad visual", "que no parezca genérico".
---

# Visual identity

Reply in the user's language.

## Source of truth

Read `docs/estilo/identidad.md` in the `haividio` repo. If `docs/estilo/tokens.css` exists, import it in the HyperFrames compositions, or turn it into constants in Remotion. If the identity is still "direction to be chosen", ask the user which one to use before animating.

## Before delivering any scene, check

- [ ] Only palette colours, and the accent only for what matters (≤ 10 % of the screen).
- [ ] Only the guide's typefaces; no Inter, Poppins or Roboto.
- [ ] Nothing that looks like a generic template: real data and resources (docs/recursos-abiertos.md) are better than filler icons.
- [ ] Motion rhythm consistent with the chosen direction, without the same fade+slide repeated everywhere.
- [ ] ≤ 8 words of on-screen text at a time.
- [ ] The channel signature appears where it belongs (intro, chapter header, transition).
- [ ] Readable on mobile: text ≥ 42 px at 1080p and enough contrast.

## Thumbnails

Same background and accent as the video, at most 4 words, a single dominant visual element. Make 2 variants for the user to choose from.

## Evolution

If the user corrects something about the style ("less red", "slower"), propose updating `docs/estilo/identidad.md` so the correction also applies to the next videos.
