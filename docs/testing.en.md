# How to test Haividio

*[Español](testing.md)*

Everything that goes into the plugin is tested before it is accepted, and how it was tested is written down, so that anyone (or any agent) can repeat it.

## Method

1. **With real material.** A finished video (the RAG one, `videos/2026-10-31-rag-2026/`, serves as the test bench) or a new one. Not with toy examples, except for edge cases.
2. **With a control that must fail.** A made-up label, an image with the wrong ratio, a cut inserted on purpose. If the control does not fail, the test proves nothing.
3. **Measured and compared** with what was there before: the hand-made version, the design PNG, the published SRT.
4. **What a script cannot see, the result says:** what has to be heard or seen in motion, and who does it.
5. **Written down:** the result goes in the PR description, what was learnt in `memory/learnings.md` and what is missing in `memory/backlog.md`. When ticking a box below, add the date and who tested it.

Paths are relative to the repository root; `RAG` is `videos/2026-10-31-rag-2026` and `RAGV`, `RAG/animations/rag-video`.

## Plugin 0.3.0 (PRs #25 to #29)

### Music ducking — `scripts/duck_music.py` (#25)

```bash
cd RAGV && uv run --with numpy ../../../../scripts/duck_music.py --music assets/music/bed.mp3 \
  --hyperframes index.html --volume 0.25 --out /tmp/bed-ducked.mp3
```

- [x] Reads the voice clips from the composition, including split ones with `data-media-start` (11-11, Claude).
- [x] Measures the voice-music gap before and after: 13 dB → 23 dB median (11-11, Claude).
- [ ] **Listen** to the one-minute A/B sample (0.14 without ducking versus 0.25 with ducking) and choose the volume and `--min-gap` (Santi).
- [ ] Render the RAG video with `bed-ducked.mp3`, listen to the flagged stretches and check that the music comes back without pumping after each sentence.
- [ ] Control: raise the volume to 0.6; many stretches must be flagged.

### HyperFrames blocks and `tokens.css` (#26)

- [x] `tokens.css` recolours a catalog component (`code-terminal-run`): snapshot with and without tokens (11-11, Claude).
- [ ] Mount one of the recommended transitions (`whip-pan-cut`, `directional-wipe`, `fade-through`) in a real scene and **watch it in motion**.
- [ ] Try `code-typing` and `code-diff` (blocks: they must be recoloured by hand) and `cursor-zoom-follow` with the marks JSON from workflow 5.
- [ ] `hyperframes check` with no warnings with 32 px and 40 px text (the identity's new minimum).

### Subtitles, chapters and thumbnail (#27)

```bash
cd RAGV && python3 ../../../../scripts/make_captions.py srt --hyperframes index.html \
  --words-dir ../../audio/voice -o /tmp/rag.srt
python3 scripts/make_captions.py chapters --timeline RAGV/timeline.json chapters.json
python3 scripts/check_publishing.py thumb RAG/miniatura.png --preview /tmp/thumbnail-mobile.png
```

- [x] The SRT has the same text as the hand-made one; no line over 42 characters; no one-word tails (11-11, Claude).
- [x] The chapters come out identical to the published ones (11-11, Claude).
- [x] `--pron` turns "oce erre" back into "OCR" and "Odú" into "Odoo" (11-11, Claude, with a prepared example).
- [x] `thumb` accepts the published thumbnail and rejects a 600×400 image (11-11, Claude).
- [ ] **Watch** the new SRT over the video (on YouTube as unlisted or in a player) and check that no subtitle comes early or lingers.
- [ ] Upload a 3840×2160 thumbnail through the API (the new 50 MB limit) on a test video.

### Visual review of the render — `scripts/check_render.py` (#28)

```bash
uv run --with "scenedetect[opencv]" --with rapidocr --with onnxruntime scripts/check_render.py \
  RAG/out/rag-video-v4.mp4 --out /tmp/review --timeline RAGV/timeline.json --expect labels.txt
```

- [x] Finds every expected label and not the made-up one (control); flags the grey struck-through label at 5:50 (11-11, Claude).
- [x] Without `--timeline`, the adaptive detector finds every cut between scenes in the first two minutes (11-11, Claude).
- [ ] Compare the shots detected over the whole video with `timeline.json`.
- [x] A label over two lines with another column beside it ("Busca lo más / cercano") counts as found; the made-up one still does not (11-11, Claude, with the draft of the Pencil storyboard).
- [ ] Cut-text control: render a scene with a label running off the frame; it must be flagged.
- [ ] Small-type control: a 20 px label must be flagged and a 32 px one must not.
- [ ] Try it on a talking-head video (workflow 1) and a screen demo (workflow 5), where the text is not ours.
- [ ] Try it on Windows (RapidOCR and PySceneDetect claim to work; not checked).

### Pencil → HyperFrames — `scripts/pencil_to_hyperframes.py` (#29)

- [x] One frame (KF 03 of the RAG video): `hyperframes check` with no errors and the snapshot differs from the Pencil PNG by 1 grey level out of 255 on average (11-11, Claude).
- [x] The `pencil-to-hyperframes` skill triggers from a request in Spanish (11-11, Claude).
- [x] **Real storyboard** (11-11, Claude): "KF 3b · Trocear", "KF 3b · Vectorizar" and "KF 03 · Buscar" from `scene3.pen`, exported together with an explicit `uri`. `states.json` captures the active step (01 → 02 → 03) and the footer; animated from it, snapshots at 1, 4 and 7 s match each PNG in the step bar (pills a few pixels narrower). The test surfaced three bugs, already fixed in #29: the unnamed canvas that wraps several frames, images relative to the `.pen`, and the missing HTML of entering layers.
- [x] Whole scene from the storyboard with `--draft --at 0,6,12` (11-11, Claude): `check` with no errors or reading warnings, an 18 s render, and `check_render.py` finds the 9 labels of the three states. It surfaced and fixed two more bugs: single-quoted `style` attributes and the transition to transparent going through green.
- [x] **Watched** the draft (`storyboard-draft.mp4`, no audio: voice and music go into the composition afterwards) in motion: it works as a starting point (11-11, Santi).
- [ ] A design with an image in an `<img>`, an SVG and a reusable component (instances).
- [ ] A font other than Geist.

## Before merging any PR

- `claude plugin validate .` passes.
- If it touches a skill: check that it triggers (method in `memory/learnings.md`, 08-11).
- If it adds a script: tested against real material and with a control that must fail.
- Guides in es and `.en.md`.
- What has not been heard or seen in motion, stated in the PR.

## Still pending from before

- Codex and Cursor with the skills (`docs/other-agents.md`).
- A real Windows machine (`docs/windows.md` has its checklist).
- A whole video made with an agent other than Claude Code.
