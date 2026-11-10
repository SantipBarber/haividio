#!/usr/bin/env python3
"""Genera index.html (composición raíz) a partir de las duraciones reales de la voz.

Cada escena del guion tiene su mp3 y su words.json en ../../audio/voice/.
Las escenas largas se reparten en varias subcomposiciones (SPLITS): el corte
se hace en un instante de la voz, en segundos locales de la escena.
Uso: python3 build_root.py  (reescribe index.html y timeline.json)

Cambio de voz: las animaciones se escribieron con los tiempos de la voz de
referencia (AUTHORING, la voz «Daniel» en ../../audio/voice-daniel/). Si la voz
actual (../../audio/voice/) dice el mismo texto, el script calcula para cada
composición un mapa tiempo de referencia -> tiempo actual (un ancla por palabra)
y lo inyecta entre /* warp:start */ y /* warp:end */: una línea de tiempo
exterior que mueve la original a trozos lineales. Los números de las
composiciones siguen en tiempo de referencia: no hay que tocarlos.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
VOICE = HERE / "../../audio/voice"
AUTHORING = HERE / "../../audio/voice-daniel"   # voz con la que se escribieron los tiempos
GAP = 0.7      # silencio entre escenas
LEAD = 0.5     # el vídeo empieza medio segundo antes de la primera palabra
TAIL = 1.5     # cola tras la última palabra

# escena del guion -> [(id de la composición, inicio local en la voz)]
SPLITS = {
    "1": [("hook", 0)],
    "2": [("problem", 0)],
    "2b": [("openbook", 0)],
    "3a": [("twomoments", 0)],
    "3b": [("chunk", 0), ("embed", 18.3)],
    "3c": [("search", 0), ("topk", 7.4), ("generate", 18.2)],
    "4": [("failures", 0)],
    "5": [("hybrid", 0)],
    "6": [("contextual", 0)],
    "7": [("graphrag", 0)],
    "8": [("agentic", 0), ("warnings", 30.6)],
    "9": [("longcontext", 0)],
    "10": [("choose", 0)],
    "11": [("outro", 0)],
}

# Pausa extra (s) al final de una composición: la pantalla se queda quieta y la voz
# espera. Entre partes de una misma escena se corta el mp3 (data-media-start).
HOLD = {
    "search": 1.2,
    "topk": 1.2,
}

def words_of(folder, scene):
    return json.loads((folder / f"scene-{scene}.words.json").read_text(encoding="utf-8"))


def interp(x, xs, ys):
    """Interpolación lineal a trozos (xs creciente)."""
    if x <= xs[0]:
        return ys[0] + (x - xs[0])
    for i in range(1, len(xs)):
        if x <= xs[i]:
            f = (x - xs[i - 1]) / (xs[i] - xs[i - 1]) if xs[i] > xs[i - 1] else 0
            return ys[i - 1] + f * (ys[i] - ys[i - 1])
    return ys[-1] + (x - xs[-1])


def layout(folder, splits, hold):
    """Coloca composiciones y trozos de voz. Devuelve (escenas, clips de voz, total)."""
    scenes, clips, t = [], [], LEAD
    for scene, parts in splits.items():
        voice = round(words_of(folder, scene)["duration"], 2)
        shift = 0.0  # pausas acumuladas dentro de esta escena
        for i, (cid, local) in enumerate(parts):
            last = i + 1 == len(parts)
            nxt = voice if last else parts[i + 1][1]
            seg = t + local + shift
            start = seg if i else (0 if scene == "1" else t)
            h = hold.get(cid, 0)
            stop = (t + voice + shift + (GAP if scene != "11" else TAIL) + h) if last else (t + nxt + shift + h)
            clips.append({"id": f"voice-{scene}" + (f"-{i}" if len(parts) > 1 else ""), "scene": scene,
                          "start": round(seg, 2), "media": round(local, 2), "duration": round(nxt - local, 2)})
            scenes.append({"id": cid, "scene": scene, "start": round(start, 2),
                           "duration": round(stop - start, 2), "hold": h,
                           # tiempo local en la composición = tiempo de la palabra en words.json + word_to_local
                           "word_to_local": round(t + shift - start, 2)})
            if not last:
                shift += h
            else:
                t = stop
    return scenes, clips, round(t, 2)


def word_times(folder, scene):
    return [w["start"] for w in words_of(folder, scene)["words"]]


# Los cortes de SPLITS están en tiempo de la voz de referencia: se trasladan a la voz actual.
cur_splits = {}
for scene, parts in SPLITS.items():
    a, c = word_times(AUTHORING, scene), word_times(VOICE, scene)
    assert len(a) == len(c), f"escena {scene}: la voz actual no dice el mismo texto ({len(a)} vs {len(c)} palabras)"
    cw = words_of(VOICE, scene)["words"]

    def cut(local):
        # El corte va en el silencio antes de la primera palabra que empieza tras el corte de referencia.
        k = next(j for j, ta in enumerate(a) if ta >= local - 0.05)
        return round((cw[k - 1]["end"] + cw[k]["start"]) / 2, 2) if k else 0

    cur_splits[scene] = [(cid, cut(local) if i else 0) for i, (cid, local) in enumerate(parts)]

ref_scenes, _, _ = layout(AUTHORING, SPLITS, {})
scenes, clips, TOTAL = layout(VOICE, cur_splits, HOLD)

# Mapa de tiempos por composición: (tiempo de referencia, tiempo actual), un ancla por palabra.
WARP_JS = """/* warp:start (generado por build_root.py: no editar) */
      window.__timelines = window.__timelines || {{}};
      const warp = gsap.timeline({{ paused: true }});
      const W = {anchors};
      for (let i = 0; i < W.length - 1; i++) {{
        warp.fromTo(tl, {{ time: W[i][0] }}, {{ time: W[i + 1][0], duration: W[i + 1][1] - W[i][1], ease: "none", immediateRender: false }}, W[i][1]);
      }}
      window.__timelines["{cid}"] = warp;
      /* warp:end */"""
import re
WARPS = {}  # id -> (tiempos de referencia, tiempos actuales)
for ref, cur in zip(ref_scenes, scenes):
    a, c = word_times(AUTHORING, ref["scene"]), word_times(VOICE, cur["scene"])
    base = round(cur["duration"] - cur["hold"], 3)  # sin la pausa final
    pts = [(0.0, 0.0)]
    for ta, tc in zip(a, c):
        la, lc = ta + ref["word_to_local"], tc + cur["word_to_local"]
        if 0 < la < ref["duration"] and 0 < lc < base:
            pts.append((round(la, 3), round(lc, 3)))
    pts.append((ref["duration"], base))
    clean = [pts[0]]
    for p in pts[1:]:
        if p[0] - clean[-1][0] >= 0.05 and p[1] - clean[-1][1] >= 0.05:
            clean.append(p)
    clean[-1] = pts[-1]
    if cur["hold"]:
        clean.append((ref["duration"], cur["duration"]))  # pausa: el último estado se mantiene
    WARPS[cur["id"]] = ([p[0] for p in clean], [p[1] for p in clean])
    f = HERE / "compositions" / f"{cur['id']}.html"
    html = f.read_text(encoding="utf-8")
    block = WARP_JS.format(anchors=json.dumps([list(p) for p in clean], separators=(",", ":")), cid=cur["id"])
    if "/* warp:start" in html:
        html = re.sub(r"/\* warp:start.*?/\* warp:end \*/", lambda m: block, html, flags=re.S)
    else:
        old = re.search(r'window\.__timelines = window\.__timelines \|\| \{\};\s*window\.__timelines\["' + cur["id"] + r'"\] = tl;', html)
        assert old, f"{f.name}: no encuentro el registro de la línea de tiempo"
        html = html[:old.start()] + block + html[old.end():]
    f.write_text(html, encoding="utf-8")

# ── Efectos de sonido ────────────────────────────────────────────────────────
# Instante de referencia (segundo local de la composición, como en su código) -> segundo global actual.
START = {s["id"]: s["start"] for s in scenes}


def at(cid, local):
    xs, ys = WARPS[cid]
    return START[cid] + interp(local, xs, ys)


FRAME = 1 / 30
# Segundo del fichero en que suena el golpe (medido con `hyperframes audio --json`).
PEAK = {"whoosh-1": 0.10, "whoosh-2": 0.16, "whoosh-3": 0.18, "pop-1": 0.0, "pop-2": 0.0, "tick": 0.18, "impact": 0.49}
DUR = {"whoosh-1": 0.8, "whoosh-2": 0.8, "whoosh-3": 0.68, "pop-1": 0.48, "pop-2": 0.48, "tick": 0.48, "impact": 2.48}
VOL = {"whoosh": 0.22, "pop": 0.3, "tick": 0.35, "impact": 0.5}
# Pops: cifras y tarjetas clave, en tiempo de referencia de su composición.
POPS = [("chunk", 8.6), ("embed", 6.5), ("topk", 2.4), ("topk", 4.8), ("topk", 8.9),
        ("contextual", 26.0), ("contextual", 29.5), ("longcontext", 5.2)]
sfx = []  # (fichero, segundo global en que debe sonar el golpe)
for i, s_ in enumerate(scenes[1:]):
    sfx.append((f"whoosh-{i % 3 + 1}", s_["start"]))          # cada cambio de composición
for i, (cid, local) in enumerate(POPS):
    sfx.append((f"pop-{i % 2 + 1}", at(cid, local) + 0.05))
sfx.append(("impact", at("outro", 2.0) + 0.1))                 # «RAG ha madurado.»
# ── Música de fondo ──────────────────────────────────────────────────────────
# Pista de ElevenLabs Music (estilo A «pulso tech», 3:10) encadenada consigo misma
# con fundidos de 6 s hasta cubrir el vídeo. Se rehace si cambia la duración.
import subprocess
MUSIC_SRC = HERE / "../../audio/music/A-pulso-tech-full.mp3"
BED = HERE / "assets/music/bed.mp3"
MUSIC_VOL = 0.14


def media_duration(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                         capture_output=True, text=True).stdout.strip()
    return float(out) if out else 0.0


if MUSIC_SRC.exists() and (not BED.exists() or abs(media_duration(BED) - TOTAL) > 0.05):
    BED.parent.mkdir(parents=True, exist_ok=True)
    chain = ("[0:a]asplit=3[a][b][c];[a]atrim=0:182,asetpts=N/SR/TB[s1];[b]atrim=8:182,asetpts=N/SR/TB[s2];"
             "[c]atrim=8:120,asetpts=N/SR/TB[s3];[s1][s2]acrossfade=d=6:c1=tri:c2=tri[x];"
             "[x][s3]acrossfade=d=6:c1=tri:c2=tri[y];"
             f"[y]atrim=0:{TOTAL},afade=t=in:d=1.5,afade=t=out:st={TOTAL - 4}:d=4,loudnorm=I=-16:TP=-1:LRA=11")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(MUSIC_SRC),
                    "-filter_complex", chain, "-ar", "44100", "-b:a", "160k", str(BED)], check=True)
    print(f"música: {BED.name} rehecha ({TOTAL} s)")
music_tag = (f'      <audio id="music" class="clip" src="assets/music/bed.mp3" data-start="0" data-duration="{TOTAL}" '
             f'data-track-index="7" data-volume="{MUSIC_VOL}"></audio>') if BED.exists() else ""

tracker_from = next(s["start"] for s in scenes if s["id"] == "twomoments")
tracker_to = next(s["start"] + s["duration"] for s in scenes if s["id"] == "generate")
step_at = {i: next(s["start"] for s in scenes if s["id"] == cid)
           for i, cid in enumerate(["chunk", "embed", "search", "generate"])}


def word_at(scene, prefix):
    """Instante (raíz) de la primera palabra de la escena que empieza por prefix, en la voz actual."""
    comp = next(s for s in scenes if s["scene"] == scene)
    w = next(x for x in words_of(VOICE, scene)["words"] if x["w"].lower().startswith(prefix.lower()))
    return comp["start"] + w["start"] + comp["word_to_local"]


# Segunda barra: los arreglos, de la búsqueda híbrida al final del RAG agéntico.
fixes_from = next(s["start"] for s in scenes if s["id"] == "hybrid")
fixes_to = next(s["start"] + s["duration"] for s in scenes if s["id"] == "warnings")
fix_at = {0: fixes_from, 1: word_at("5", "segundo"), 2: word_at("6", "tercer"),
          3: next(s["start"] for s in scenes if s["id"] == "graphrag"),
          4: next(s["start"] for s in scenes if s["id"] == "agentic")}

for t_ in list(step_at.values()) + list(fix_at.values()):      # se enciende un paso de una barra
    sfx.append(("tick", t_ + 0.2))
sfx_tags = "\n".join(
    f'      <audio id="sfx-{i}" class="clip" src="assets/sfx/{name}.mp3" data-start="{round(hit + FRAME - PEAK[name], 2)}" '
    f'data-duration="{DUR[name]}" data-track-index="{5 + i % 2}" data-volume="{VOL[name.split("-")[0]]}"></audio>'
    for i, (name, hit) in enumerate(sorted(sfx, key=lambda x: x[1])))

hosts = "\n".join(
    f'      <div id="scene-{s["id"]}" class="host" data-composition-id="{s["id"]}" '
    f'data-composition-src="compositions/{s["id"]}.html"\n'
    f'        data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="1" '
    f'data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
    for s in scenes)
audios = "\n".join(
    f'      <audio id="{v["id"]}" class="clip" src="assets/audio/scene-{v["scene"]}.mp3" '
    f'data-start="{v["start"]}" data-duration="{v["duration"]}"'
    + (f' data-media-start="{v["media"]}"' if v["media"] else "")
    + f' data-track-index="{3 + i % 2}" data-volume="1"></audio>'
    for i, v in enumerate(clips))

html = f"""<!doctype html>
<html lang="es" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Geist"; src: url("assets/fonts/geist-sans-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
      @font-face {{ font-family: "Geist"; src: url("assets/fonts/geist-sans-latin-500-normal.woff2") format("woff2"); font-weight: 500; }}
      @font-face {{ font-family: "Geist"; src: url("assets/fonts/geist-sans-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
      @font-face {{ font-family: "Geist"; src: url("assets/fonts/geist-sans-latin-800-normal.woff2") format("woff2"); font-weight: 800; }}
      @font-face {{ font-family: "Geist Mono"; src: url("assets/fonts/geist-mono-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
      @font-face {{ font-family: "Geist Mono"; src: url("assets/fonts/geist-mono-latin-500-normal.woff2") format("woff2"); font-weight: 500; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #07080b; }}
      #root {{ position: relative; width: 1920px; height: 1080px; font-family: "Geist", sans-serif; color: #f4f5f7; }}
      #bg {{ position: absolute; inset: 0; background-image: radial-gradient(#1c2029 1.5px, transparent 1.5px); background-size: 40px 40px; }}
      .host {{ position: absolute; inset: 0; }}
      #tracker, #fixes {{ position: absolute; left: 120px; top: 70px; display: flex; gap: 14px; z-index: 10; }}
      .step {{ font-family: "Geist Mono", monospace; font-size: 30px; color: #a3a8b8; padding: 12px 22px; border: 2px solid #232733; border-radius: 999px; }}
      .step b {{ font-weight: 500; margin-right: 10px; }}
    </style>
  </head>
  <body>
    <!-- Vídeo completo de RAG (guion v2). GENERADO por build_root.py: no editar a mano. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <div id="bg" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0"></div>

{hosts}

      <!-- Firma del canal: barra de pasos 01–04, de la escena 3a al final de la 3c -->
      <div id="tracker" class="clip" data-start="{tracker_from}" data-duration="{round(tracker_to - tracker_from, 2)}" data-track-index="2">
        <div class="step" id="s1"><b>01</b>Trocear</div>
        <div class="step" id="s2"><b>02</b>Vectorizar</div>
        <div class="step" id="s3"><b>03</b>Buscar</div>
        <div class="step" id="s4"><b>04</b>Generar</div>
      </div>
      <div id="fixes" class="clip" data-start="{fixes_from}" data-duration="{round(fixes_to - fixes_from, 2)}" data-track-index="2">
        <div class="step" id="f1"><b>01</b>Híbrida</div>
        <div class="step" id="f2"><b>02</b>Reranker</div>
        <div class="step" id="f3"><b>03</b>Contextual</div>
        <div class="step" id="f4"><b>04</b>GraphRAG</div>
        <div class="step" id="f5"><b>05</b>Agéntico</div>
      </div>

{audios}

      <!-- Música de fondo -->
{music_tag}

      <!-- Efectos de sonido -->
{sfx_tags}
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
      const bars = {{ steps: ["#s1", "#s2", "#s3", "#s4"], fixes: ["#f1", "#f2", "#f3", "#f4", "#f5"] }};
      const activate = (idx, at, steps = bars.steps) => {{
        steps.forEach((s, i) => {{
          tl.to(s, {{
            color: i === idx ? "#11140a" : i < idx ? "#f4f5f7" : "#a3a8b8",
            backgroundColor: i === idx ? "#d4ff3a" : "rgba(212,255,58,0)",
            borderColor: i === idx ? "#d4ff3a" : i < idx ? "#3a3f4d" : "#232733",
            duration: 0.35, ease: "power2.out",
          }}, at);
        }});
      }};
      // La barra nace en la escena 3a, cuando la voz dice «Un RAG tiene dos momentos».
      tl.from("#tracker .step", {{ autoAlpha: 0, y: -20, stagger: 0.08, duration: 0.5, ease: "power3.out" }}, {tracker_from + 0.4});
{chr(10).join(f'      activate({i}, {round(at + 0.2, 2)});' for i, at in step_at.items())}
      // La barra de arreglos nace con «Primer arreglo» y se enciende con cada uno.
      tl.from("#fixes .step", {{ autoAlpha: 0, y: -20, stagger: 0.08, duration: 0.5, ease: "power3.out" }}, {fixes_from + 0.1});
{chr(10).join(f'      activate({i}, {round(at + 0.2, 2)}, bars.fixes);' for i, at in fix_at.items())}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(HERE / "index.html").write_text(html, encoding="utf-8")
(HERE / "timeline.json").write_text(json.dumps({"total": TOTAL, "scenes": scenes}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"index.html: {len(scenes)} escenas, {TOTAL} s")
