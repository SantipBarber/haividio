---
name: pencil-to-hyperframes
description: Turns frames designed in Pencil (pen.dev) into HyperFrames compositions ready to animate - stable ids from layer names, local fonts, copied images, palette colours as variables, and several frames read as states of one animation. Use it when the user has designed key frames or a storyboard in Pencil and wants them animated, or asks to bring a .pen design into a video. Also when the user writes in Spanish, e.g. "anima este diseño de Pencil", "pasa los fotogramas de Pencil a HyperFrames", "tengo el storyboard en pen.dev", "importa el .pen al vídeo".
---

# Pencil → HyperFrames

Reply in the user's language. Full guide: `docs/workflows/06-pencil-to-hyperframes.md` in the `haividio` repo.

## Safety with the Pencil MCP

- Always pass the `.pen` file's `uri` explicitly. If the path is wrong, the MCP acts on whatever `.pen` is active, which may belong to another project.
- Run `get_app_state` first. With the explicit `uri`, `execute` reads and exports that file without switching the canvas open in the app, so another project's open file is not touched.
- Only read and export. Never edit a `.pen` file by any other means than the MCP: it corrupts it.

## Steps

1. **List the frames** of the `.pen` with a `Get` visitor (top-level frames: id, name, size).
2. **Export** the frames to animate, in order, into the video folder:
   - `Export([ids], "html-css", "<video>/design/export/<scene>.html")`: one HTML with every frame.
   - `Export([ids], "png", "<video>/design/export/")`: the reference images.
3. **Convert:**

   ```bash
   python3 scripts/pencil_to_hyperframes.py <video>/design/export/<scene>.html \
     --project <video>/animations/<project> --name <scene> --prefix <short> \
     --pen-dir <video>/design --tokens docs/style/tokens.css --duration <s> [--draft --at 0,<s>,<s>]
   ```

   It writes `compositions/<scene>.html` with an id on every named layer (`Tracker/Paso 01` → `#<short>-tracker-paso-01`), Google fonts downloaded to `assets/fonts/` as `@font-face`, images copied to `assets/pencil/`, palette colours as `var(--name, #hex)` and an empty paused timeline registered under the scene's name. It prints the layer → id map and the mount snippet.
4. **Check before animating:** mount it, run `npx hyperframes check`, take a `snapshot` and compare it with the Pencil PNG. On the RAG video, the converted frame differed from the PNG by 1 grey level out of 255 on average.
5. **Animate** in the composition's timeline, by id, following the skill `visual-identity` (motion, rhythm) and syncing with the voice as in the skill `faceless-video`.

## Several frames: states, not slides

If the export has several frames, the first one is the composition and the others are written as `<scene>.states.json`: for each id, what changes compared with the first frame (styles, text) and which layers enter or leave. Each frame's converted HTML, with the same ids, is in `pencil/<scene>/`: copy entering layers from there. Animate from one state to the next: move, resize or recolour the shared elements, and bring in or take out the ones that appear in only one frame. Playing the frames back to back as stills is the failure mode.

For this to work, the same element must have the same layer name and parent in every frame. Ask the user to name layers meaningfully in Pencil: the ids come from those names.

To start from a working scene, add `--draft` (and `--at 0,<s>,<s>` with the second each frame should start, taken from the voice's word timings): the composition gets every frame's blocks and a draft timeline that plays the storyboard as state changes. Then refine it: builds within each state (`check` flags `dead_stretch`), rhythm, sound, and nested layers the script reports as not included.
