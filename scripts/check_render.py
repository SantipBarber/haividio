#!/usr/bin/env python3
"""Revisión visual de un render: qué texto hay en pantalla, si se corta, si es pequeño y dónde se queda quieto.

El agente no ve el vídeo en movimiento. Este script le da algo que mirar y una lista
de sitios a los que ir primero:

1. Planos: toma las escenas de timeline.json (--timeline) o detecta los cambios de
   plano (PySceneDetect), y saca un fotograma al final de cada uno, cuando ya ha
   aparecido todo, más uno cada --every segundos.
2. Texto: lee cada fotograma con OCR (RapidOCR, local) y avisa de
   - texto pegado al borde del encuadre (posible texto cortado),
   - texto pequeño: estima el tamaño de letra por la altura de la caja de OCR (en
     Geist, entre 1 y 1,2 veces la letra; se toma 1, así que la estimación no se
     queda corta) y avisa por debajo de --min-text (28 px, el mínimo de
     docs/style/identity.md), con lo que mediría en un móvil de 360 px de ancho,
   - lectura dudosa (confianza baja: texto borroso, cortado o tapado).
3. Rótulos esperados (--expect, uno por línea): cuáles no aparecen en ningún fotograma.
4. Tramos quietos: la imagen no cambia en --static segundos o más (freezedetect de
   ffmpeg). En un explicativo, un plano quieto mucho rato cansa.

Guarda en --out un informe JSON, los fotogramas con los avisos marcados en rojo y una
hoja de contactos (contact-sheet.jpg) para mirarla de un vistazo.

No decide si algo queda bien: el OCR lee mejor que una persona (a 360 px de ancho
seguía leyendo letra de 28 px), así que «se lee» no es «se lee bien en el móvil».
Tampoco ve el movimiento ni mide el desfase entre rótulo y voz.

Uso:
    uv run --with "scenedetect[opencv]" --with rapidocr --with onnxruntime \\
        scripts/check_render.py out/video.mp4 --out out/review \\
        [--timeline animations/<proyecto>/timeline.json] [--expect rotulos.txt]

Sale con 1 si hay texto cortado o rótulos esperados que no aparecen.
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import cv2
import numpy as np

BOX_TO_FONT = 1.0  # caja de OCR / tamaño de letra: de 1,0 a 1,2 medido con Geist Mono a 32 px


def shots(video, threshold):
    """Planos con el detector adaptativo y umbral bajo: con fondos oscuros parecidos entre escenas,
    ContentDetector a 27 no vio ningún corte en un vídeo de 18 escenas; este los vio todos."""
    from scenedetect import AdaptiveDetector, detect

    det = AdaptiveDetector(adaptive_threshold=threshold, min_content_val=5, min_scene_len=15)
    return [(s.seconds, e.seconds) for s, e in detect(str(video), det)]


def timeline_shots(path):
    scenes = json.loads(Path(path).read_text(encoding="utf-8"))["scenes"]
    return [(sc["start"], sc["start"] + sc["duration"]) for sc in scenes]


def freezes(video, seconds, noise):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-map", "0:v:0",
                          "-vf", f"freezedetect=n={noise}:d={seconds}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", err)]
    return [[round(s, 1), round(e, 1)] for s, e in zip(starts, ends + [None] * (len(starts) - len(ends))) if e]


def frame_at(cap, t):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, img = cap.read()
    return img if ok else None


def norm(text):
    t = unicodedata.normalize("NFD", text.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ%]+", " ", t).strip()


def found(expected, lines, joined):
    e = norm(expected)
    return e in joined or any(difflib.SequenceMatcher(None, e, norm(l)).ratio() >= 0.85 for l in lines)


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("--out", required=True, help="carpeta para el informe, los fotogramas y la hoja de contactos")
    p.add_argument("--expect", help="fichero con los rótulos que deben salir, uno por línea")
    p.add_argument("--every", type=float, help="s entre fotogramas fijos, además de uno por plano (0: no). "
                   "Por defecto 10, o 2 con --expect: un rótulo puede salir y quitarse dentro de un plano")
    p.add_argument("--min-text", type=float, default=28.0, help="px de letra en 1080p por debajo de los que avisa")
    p.add_argument("--edge", type=int, default=6, help="px al borde del encuadre que cuentan como texto cortado")
    p.add_argument("--min-score", type=float, default=0.8, help="confianza del OCR por debajo de la que avisa")
    p.add_argument("--static", type=float, default=4.0, help="s sin cambios en la imagen para avisar")
    p.add_argument("--freeze-noise", default="0.003", help="tolerancia de freezedetect")
    p.add_argument("--timeline", help="timeline.json de HyperFrames: usa sus escenas en vez de detectar planos")
    p.add_argument("--threshold", type=float, default=1.5, help="umbral adaptativo de cambio de plano de PySceneDetect")
    a = p.parse_args()

    from rapidocr import RapidOCR

    if a.every is None:
        a.every = 2.0 if a.expect else 10.0
    out = Path(a.out)
    (out / "frames").mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    scale = 1080 / min(height, width)  # a 1080p, también en vertical

    print("planos…", flush=True)
    cuts = timeline_shots(a.timeline) if a.timeline else shots(a.video, a.threshold)
    times = {round(max(s, e - 0.25), 2) for s, e in cuts} or {round(duration - 0.25, 2)}
    if a.every > 0:
        times |= {round(t, 2) for t in np.arange(a.every, duration, a.every)}
    times = sorted(t for t in times if 0 <= t < duration)

    print(f"texto en {len(times)} fotogramas…", flush=True)
    engine = RapidOCR()
    frames, all_lines, issues = [], [], []
    for t in times:
        img = frame_at(cap, t)
        if img is None:
            continue
        r = engine(img)
        h, w = img.shape[:2]
        items, flagged = [], False
        for box, txt, score in zip(r.boxes if r.boxes is not None else [], r.txts or [], r.scores or []):
            xs, ys = [q[0] for q in box], [q[1] for q in box]
            font = (max(ys) - min(ys)) * scale / BOX_TO_FONT
            item = {"text": txt, "score": round(float(score), 2), "font_px": round(font),
                    "box": [round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys))]}
            warn = []
            symbol = len(re.sub(r"[^\w]", "", txt)) < 2  # «●», «]», «+»: iconos, no texto
            if min(xs) <= a.edge or min(ys) <= a.edge or max(xs) >= w - a.edge or max(ys) >= h - a.edge:
                warn.append("cut")
            if font < a.min_text and not symbol:
                warn.append("small")
            if score < a.min_score and not symbol:
                warn.append("unsure")
            if warn:
                item["warn"] = warn
                flagged = True
                cv2.polylines(img, [np.array(box, dtype=np.int32)], True, (40, 40, 255), 4)
                for k in warn:
                    issues.append({"t": t, "type": k, "text": txt, "font_px": item["font_px"]})
            items.append(item)
            all_lines.append(txt)
        name = f"t{t:07.2f}.jpg"
        cv2.putText(img, mmss(t), (24, 64), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (40, 40, 255) if flagged else (200, 200, 200), 4)
        cv2.imwrite(str(out / "frames" / name), img, [cv2.IMWRITE_JPEG_QUALITY, 82])
        frames.append({"t": t, "file": f"frames/{name}", "text": items})

    # Hoja de contactos: 5 columnas de 384 px.
    tiles = [cv2.resize(cv2.imread(str(out / f["file"])), (384, int(384 * height / width))) for f in frames]
    if tiles:
        cols = 5
        blank = np.zeros_like(tiles[0])
        rows = [np.hstack(tiles[i:i + cols] + [blank] * (cols - len(tiles[i:i + cols]))) for i in range(0, len(tiles), cols)]
        cv2.imwrite(str(out / "contact-sheet.jpg"), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 80])

    missing = []
    if a.expect:
        joined = " ".join(norm(l) for l in all_lines)
        expected = [l.strip() for l in Path(a.expect).read_text(encoding="utf-8").splitlines() if l.strip()]
        missing = [e for e in expected if not found(e, all_lines, joined)]

    print("tramos quietos…", flush=True)
    still = freezes(a.video, a.static, a.freeze_noise)

    report = {"video": a.video, "duration": round(duration, 1), "shots": len(cuts), "frames": frames,
              "issues": issues, "missing": missing, "static": still,
              "settings": {"min_text": a.min_text, "edge": a.edge, "min_score": a.min_score, "static": a.static}}
    (out / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"\n{mmss(duration)} · {len(cuts)} planos · {len(frames)} fotogramas leídos")
    labels = {"cut": "texto pegado al borde (¿cortado?)", "small": f"letra de menos de unos {a.min_text:.0f} px",
              "unsure": "lectura dudosa"}
    for kind, label in labels.items():
        hits = [i for i in issues if i["type"] == kind]
        if hits:
            print(f"{label}: {len(hits)}")
            seen = set()
            for i in hits:
                if i["text"] in seen:
                    continue
                seen.add(i["text"])
                extra = f" · {i['font_px']} px (en un móvil, {i['font_px'] * 360 / 1080:.0f} px)" if kind == "small" else ""
                print(f"  {mmss(i['t'])}  «{i['text']}»{extra}")
                if len(seen) >= 12:
                    print(f"  … y más en {out / 'report.json'}")
                    break
    if a.expect:
        print(f"rótulos esperados que no salen: {len(missing)}" + "".join(f"\n  «{m}»" for m in missing))
    if still:
        print(f"tramos quietos de {a.static:.0f} s o más: {len(still)}")
        for s, e in still[:20]:
            print(f"  {mmss(s)} – {mmss(e)} ({e - s:.1f} s)")
    print(f"\nhoja de contactos: {out / 'contact-sheet.jpg'}")
    sys.exit(1 if missing or any(i["type"] == "cut" for i in issues) else 0)


if __name__ == "__main__":
    main()
