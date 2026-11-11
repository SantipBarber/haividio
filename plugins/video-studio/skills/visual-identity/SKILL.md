---
name: visual-identity
description: Applies the channel's visual identity (palette, typefaces, motion, signature) to animations, scenes and thumbnails so they look visual, bold and modern, not generic. Use it whenever you create an animation, scene, overlay or thumbnail. Also when the user writes in Spanish, e.g. "hazme una miniatura", "anima esta escena", "estilo del canal", "identidad visual", "que no parezca genérico".
---

# Visual identity

Reply in the user's language.

## Source of truth

Read `docs/style/identity.md` in the `haividio` repo. Copy `docs/style/tokens.css` to the project's `assets/` and link it from the HyperFrames root composition (or turn it into constants in Remotion). Besides the palette, it sets the theme tokens (`--bg`, `--surface`, `--fg`, `--brand`, `--accent`, `--font-body`…) that HyperFrames catalog components read, so they come out in the channel's colours and Geist instead of Inter. If the identity is still "direction to be chosen", ask the user which one to use before animating.

## Before delivering any scene, check

- [ ] Only palette colours, and the accent only for what matters (≤ 10 % of the screen).
- [ ] Only the guide's typefaces; no Inter, Poppins or Roboto.
- [ ] Nothing that looks like a generic template: real data and resources (docs/open-resources.md) are better than filler icons.
- [ ] Motion rhythm consistent with the chosen direction, without the same fade+slide repeated everywhere.
- [ ] ≤ 8 words of on-screen text at a time.
- [ ] The channel signature appears where it belongs (intro, chapter header, transition).
- [ ] Readable on mobile at 1080p: text that matters ≥ 32 px, the bottom subtitle 40 px, nothing under 28 px (the `hyperframes check` minimum), and enough contrast.
- [ ] Scenes joined by the video's transition, not by dry cuts (unless a hard cut is the point).

## Ready-made blocks and transitions

Before building a named effect, chart, transition or code/terminal scene, search the HyperFrames catalog (skill `hyperframes-registry`): `npx hyperframes catalog <words>`, then `npx hyperframes add <name>`.

- **Components** (`type component`) read the theme tokens from `tokens.css`. **Blocks** (`type block`) hard-code their colours and fonts: restyle them in the installed source.
- **Transitions:** pick one family for the whole video and keep it, so it works as part of the signature. Sober options that fit the dark modern direction: `whip-pan-cut`, `directional-wipe`, `fade-through`, and the `transitions-push`, `transitions-blur` and `transitions-scale` showcases as reference.
- **Off-identity, skip them:** `glitch`, `hologram`, `holographic`, `liquid-metal`, `glass-*`, neon captions and borders, and brand items such as `yt-*` or `heygen-*`.
- **Snapshot every installed item** with the tokens applied before using it: some do not lay out well as they come (`code-terminal-run`, in 0.9.33, pushes the command away from the prompt and runs off the bottom of the panel).

## Thumbnails

Same background and accent as the video, at most 4 words, a single dominant visual element. Make 2 variants for the user to choose from.

## Evolution

If the user corrects something about the style ("less red", "slower"), propose updating `docs/style/identity.md` so the correction also applies to the next videos.
