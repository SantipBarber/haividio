# Workflow 6 — From Pencil to HyperFrames

*[Español](06-pencil-to-hyperframes.md)*

Tools: [Pencil](https://pen.dev) (pen.dev, with its MCP) + `scripts/pencil_to_hyperframes.py` + HyperFrames. Skill: `pencil-to-hyperframes`.

## Idea

Design a scene's key frames in Pencil, calmly and seeing them, and have the agent turn them into a HyperFrames composition that only needs animating. On the RAG video this was done by hand and worked well and fast; the script does the mechanical steps so they need not be repeated for every scene.

Pencil exports HTML with inline styles, absolute positions and each layer's name (`data-pencil-name`). Taking it into HyperFrames needs four more things, which the script adds:

| Missing | What the script does |
|---|---|
| Ids to animate | One id per named layer, from the path of names: `Tracker/Paso 01` → `#kf-tracker-paso-01`. Repeats get `-2`, `-3`… |
| Local fonts | Downloads the latin and latin-ext subsets from Google Fonts to `assets/fonts/` and declares them with `@font-face`. HyperFrames does not accept fonts from a CDN and Geist is not bundled. |
| Images | Copies the ones the design uses to `assets/pencil/` and rewrites the paths. It looks for them next to the exported HTML and next to the `.pen`. |
| Wrapper | `<template>`, `#root` with `data-composition-id` and an empty timeline registered in `window.__timelines`. |

With `--tokens docs/style/tokens.css`, every palette colour also becomes `var(--lime, #D4FF3A)`: if the identity changes, the imported scenes change too.

## Steps

1. **Design in Pencil** the scene's frames. Give layers meaningful names ("Tracker", "Paso 01", "Pregunta"): the ids come from them.
2. **Export** through the MCP, always with the explicit path of the `.pen` (if it does not exist, the MCP works on the open `.pen`, which may belong to another project):

   ```js
   Export(["<frame 1 id>", "<frame 2 id>"], "html-css", "<video>/design/export/search.html")
   Export(["<frame 1 id>", "<frame 2 id>"], "png", "<video>/design/export/")
   ```

3. **Convert:**

   ```bash
   python3 scripts/pencil_to_hyperframes.py <video>/design/export/search.html \
     --project <video>/animations/<project> --name search --prefix kf \
     --pen-dir <video>/design --tokens docs/style/tokens.css --duration 8
   ```

   It prints the layer → id list and the snippet to mount the scene in `index.html`.
4. **Check before animating:** `npx hyperframes check` and a `snapshot`, compared with the Pencil PNG.
5. **Animate** by id in the composition's timeline, with the `visual-identity` skill and the voice as in workflow 3.

## Several frames: states, not slides

If the export has several frames, the first one is the composition and the rest go to `<name>.states.json`: for each id, what changes compared with the first frame (styles and text), which layers enter and which leave. Animate from one state to the next; playing the frames back to back as stills is exactly what to avoid (HyperFrames' `figma` skill follows the same idea).

For this to work, the same element must have the same name and sit inside the same layer in every frame. The easiest way is to duplicate the frame in Pencil and change only what moves.

## Tested

With the "KF 03 · Buscar" frame of the RAG video: 96 layers with an id, 76 colours turned into variables, the background grid copied and Geist downloaded. `hyperframes check` with no errors or warnings, and the `snapshot` differs from the Pencil PNG by 1 grey level out of 255 on average (the other frames of the same design, by about 20). The state calculation was tested with two frames prepared by hand from the same export, not with a real Pencil storyboard.

## Watch out

- **The Pencil MCP** does not open files: if the path does not exist, it acts on the active `.pen`. Check `get_app_state` first and, if another project's file is open, ask before switching: another session may be working on it.
- **Do not edit a `.pen` by any means other than the MCP:** it gets corrupted.
- **Positions inside a flex layout** do not appear in the HTML as coordinates: if an element moves between frames because the layout changes, `states.json` reports it as a style change of the container, not as `left`/`top`. To move it precisely, measure it in the `snapshot`.
