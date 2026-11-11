#!/usr/bin/env python3
"""Subtítulos SRT y capítulos de YouTube a partir de los tiempos de cada palabra.

Las voces de ElevenLabs se guardan con un `.words.json` al lado (formato
{"words": [{"w", "start", "end"}]}) y la composición raíz de HyperFrames dice en qué
instante del vídeo suena cada clip. Con eso no hace falta transcribir nada: el texto
es el del guion y los tiempos son los reales.

    python3 scripts/make_captions.py srt --hyperframes index.html \\
        --words-dir ../../audio/voice [--pron pronunciation.json] -o subtitles.srt
    python3 scripts/make_captions.py chapters --timeline timeline.json chapters.json

srt
    Lee los <audio class="clip"> de voz de la composición (id que empieza por
    «voice»; respeta data-start, data-media-start y data-duration) y busca para cada
    uno `<nombre>.words.json`, junto al audio o en --words-dir. También se puede dar
    a mano: --words escena.words.json@inicio_en_s (repetible).
    Corta en frases de una línea de hasta --max-chars caracteres (42) y --max-dur
    segundos (6), mejor tras un signo de puntuación o en una pausa, y alarga cada
    subtítulo hasta 20 ms antes del siguiente si están cerca. Con --pron, las grafías
    fonéticas enviadas a la voz («oce erre») vuelven a la escrita («OCR»), como en
    check_voice.py.

chapters
    chapters.json es una lista de {"title": "...", "at": <id de escena del timeline.json
    o segundos>}. Escribe las líneas «0:00 Título» para la descripción, con el primero
    en 0:00 aunque el timeline no empiece ahí. Valídalas después con
    check_publishing.py (mínimo 3 capítulos de 10 s o más).

Solo necesita Python 3.
"""
import argparse
import html.parser
import json
import re
import sys
import unicodedata
from pathlib import Path

PUNCT_END = (".", "?", "!", "…", ":", ";")
PUNCT_SOFT = (",",)


class VoiceClips(html.parser.HTMLParser):
    """Lee los <audio class="clip"> de voz de una composición de HyperFrames."""

    def __init__(self, base, prefix):
        super().__init__()
        self.base, self.prefix, self.clips = base, prefix, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "audio" and "clip" in (a.get("class") or "").split() and (a.get("id") or "").startswith(self.prefix):
            self.clips.append({"src": self.base / a["src"], "start": float(a.get("data-start", 0)),
                               "media_start": float(a.get("data-media-start", 0)),
                               "duration": float(a["data-duration"]) if a.get("data-duration") else None})


def words_file(src, words_dir):
    name = Path(src).with_suffix(".words.json").name
    for folder in ([Path(words_dir)] if words_dir else []) + [Path(src).parent]:
        if (folder / name).exists():
            return folder / name
    sys.exit(f"No encuentro {name} (ni junto a {src} ni en --words-dir)")


def timed_words(clips):
    """Palabras con su instante en el vídeo, en orden."""
    out = []
    for c in clips:
        data = json.loads(Path(c["words"]).read_text(encoding="utf-8"))
        lo = c["media_start"]
        hi = lo + c["duration"] if c["duration"] else float("inf")
        for w in data["words"]:
            if w["start"] >= lo - 0.01 and w["start"] < hi - 0.01:
                out.append({"w": w["w"], "start": round(c["start"] + w["start"] - lo, 3),
                            "end": round(c["start"] + min(w["end"], hi) - lo, 3)})
    return sorted(out, key=lambda w: w["start"])


def norm(word):
    w = unicodedata.normalize("NFD", word.lower())
    return re.sub(r"[^a-z0-9ñ]", "", "".join(ch for ch in w if unicodedata.category(ch) != "Mn"))


def undo_pronunciation(words, pron):
    """Junta las palabras de una grafía fonética («oce erre») en la escrita («OCR»), conservando la puntuación final."""
    forms = [(written, [norm(t) for t in spoken.split()]) for written, spoken in pron.get("map", {}).items()]
    forms += [(ph["from"], [norm(t) for t in ph["to"].split()]) for ph in pron.get("phrases", [])]
    forms.sort(key=lambda f: -len(f[1]))
    out, i = [], 0
    while i < len(words):
        for written, toks in forms:
            seg = words[i:i + len(toks)]
            if toks and [norm(w["w"]) for w in seg] == toks:
                tail = re.search(r"[^\w]*$", seg[-1]["w"]).group(0)
                out.append({"w": written + tail, "start": seg[0]["start"], "end": seg[-1]["end"]})
                i += len(toks)
                break
        else:
            out.append(words[i])
            i += 1
    return out


def cues(words, max_chars, max_dur, pause):
    out, cur = [], []

    def flush():
        if cur:
            out.append({"start": cur[0]["start"], "end": cur[-1]["end"], "text": " ".join(w["w"] for w in cur)})
            cur.clear()

    for i, w in enumerate(words):
        if cur:
            text = " ".join(x["w"] for x in cur + [w])
            gap = w["start"] - cur[-1]["end"]
            too_long = len(text) > max_chars or w["end"] - cur[0]["start"] > max_dur
            if gap > pause or too_long:
                # Si hay una coma en la segunda mitad, corta ahí en vez de a mitad de sintagma.
                if too_long and gap <= pause:
                    cut = max((k for k, x in enumerate(cur[:-1]) if x["w"].endswith(PUNCT_SOFT + PUNCT_END)
                               and k >= len(cur) // 2), default=None)
                    if cut is not None:
                        rest = cur[cut + 1:]
                        del cur[cut + 1:]
                        flush()
                        cur.extend(rest)
                        if len(" ".join(x["w"] for x in cur + [w])) > max_chars:
                            flush()
                    else:
                        flush()
                else:
                    flush()
        cur.append(w)
        if w["w"].endswith(PUNCT_END):
            flush()
    flush()
    out = rebalance(out, words, max_chars)
    for a, b in zip(out, out[1:]):
        if b["start"] - a["end"] < 0.5:
            a["end"] = round(b["start"] - 0.02, 3)
    return out


def rebalance(out, words, max_chars, short=15):
    """Evita colas huérfanas («2020.»): si un subtítulo corto cierra una frase que empezó en el anterior,
    le pasa palabras del final del anterior hasta igualarlos, sin pasar de max_chars."""
    for a, b in zip(out, out[1:]):
        if len(b["text"]) >= short or a["text"].endswith(PUNCT_END + PUNCT_SOFT) or b["start"] - a["end"] > 0.7:
            continue
        aw, bw = a["text"].split(" "), b["text"].split(" ")
        while len(aw) > 1 and len(" ".join([aw[-1]] + bw)) <= max_chars and len(" ".join(aw[:-1])) >= len(" ".join([aw[-1]] + bw)):
            bw.insert(0, aw.pop())
        if len(bw) == len(b["text"].split(" ")):
            continue
        # Recalcula los tiempos con las palabras reales: el corte cae al final de la última que se queda en a.
        seq = [w for w in words if a["start"] <= w["start"] <= b["end"]]
        a["text"], b["text"] = " ".join(aw), " ".join(bw)
        a["end"] = seq[len(aw) - 1]["end"]
        b["start"] = seq[len(aw)]["start"]
    return out


def ts(t, sep=","):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def mmss(t):
    t = int(round(t))
    h, rem = divmod(t, 3600)
    return f"{h}:{rem // 60:02d}:{rem % 60:02d}" if h else f"{rem // 60}:{rem % 60:02d}"


def cmd_srt(a):
    clips = []
    if a.hyperframes:
        parser = VoiceClips(Path(a.hyperframes).parent, a.voice_prefix)
        parser.feed(Path(a.hyperframes).read_text(encoding="utf-8"))
        for c in parser.clips:
            c["words"] = words_file(c["src"], a.words_dir)
        clips += parser.clips
    for spec in a.words:
        path, start = spec.rsplit("@", 1) if "@" in spec else (spec, "0")
        clips.append({"words": path, "start": float(start), "media_start": 0.0, "duration": None})
    if not clips:
        sys.exit("Falta la voz: usa --hyperframes o --words.")
    words = timed_words(clips)
    if a.pron:
        words = undo_pronunciation(words, json.loads(Path(a.pron).read_text(encoding="utf-8")))
    out = cues(words, a.max_chars, a.max_dur, a.pause)
    text = "\n".join(f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n" for i, c in enumerate(out, 1))
    if a.output:
        Path(a.output).write_text(text, encoding="utf-8")
        print(f"{len(out)} subtítulos, {len(words)} palabras → {a.output}")
    else:
        sys.stdout.write(text)


def cmd_chapters(a):
    scenes = {s["id"]: s["start"] for s in json.loads(Path(a.timeline).read_text(encoding="utf-8"))["scenes"]} \
        if a.timeline else {}
    lines = []
    for i, ch in enumerate(json.loads(Path(a.chapters).read_text(encoding="utf-8"))):
        at = ch["at"]
        if isinstance(at, str):
            if at not in scenes:
                sys.exit(f"«{at}» no está en el timeline (escenas: {', '.join(scenes)})")
            at = scenes[at]
        lines.append(f"{mmss(0 if i == 0 else at)} {ch['title']}")
    print("\n".join(lines))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("srt", help="subtítulos desde los .words.json")
    s.add_argument("--hyperframes", help="composición raíz de HyperFrames")
    s.add_argument("--voice-prefix", default="voice", help="prefijo del id de los <audio> de voz")
    s.add_argument("--words-dir", help="carpeta de los .words.json, si no están junto al audio")
    s.add_argument("--words", action="append", default=[], help="fichero.words.json@inicio_en_s (repetible)")
    s.add_argument("--pron", help="pronunciation.json (map y phrases)")
    s.add_argument("--max-chars", type=int, default=42)
    s.add_argument("--max-dur", type=float, default=6.0)
    s.add_argument("--pause", type=float, default=0.7, help="s de silencio que cierran un subtítulo")
    s.add_argument("-o", "--output")
    c = sub.add_parser("chapters", help="líneas de capítulos para la descripción")
    c.add_argument("--timeline", help="timeline.json con las escenas y su inicio")
    c.add_argument("chapters", help="lista JSON de {title, at}")
    a = p.parse_args()
    cmd_srt(a) if a.cmd == "srt" else cmd_chapters(a)


if __name__ == "__main__":
    main()
