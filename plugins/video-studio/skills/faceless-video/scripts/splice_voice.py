#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Sustituye un trozo de una locución por una toma ya aprobada, sin gastar créditos de voz.

Trabaja con un mp3 y su .words.json al lado: {"text": ..., "duration": ..., "words": [{"w", "start", "end"}]}.

  splice_voice.py phrase <locución> <toma> "<primeras palabras>" "<última palabra>"
      Cambia una frase entera por la toma. Las primeras palabras deben aparecer una sola vez.

  splice_voice.py word <locución> <toma> "<palabras>" <apariciones> [--tail 0.34]
      Pega las mismas palabras de la toma en varias frases, para que suenen igual.
      <palabras> compara sin mayúsculas ni puntuación. <apariciones> empieza en 0: «0,2» o «all».
      Conviene incluir la palabra anterior («por api»): suele dar un corte más limpio.
      --tail: segundos de toma tras el inicio de la última palabra, ya en silencio.

<locución> y <toma> son rutas sin extensión. Hace una copia <locución>.bak.mp3 la primera vez.
Corta en el punto más silencioso de cada lado, iguala el nivel y funde 15 ms. Requiere ffmpeg.
"""
import argparse, array, json, math, shutil, subprocess, sys
from pathlib import Path

SR = 44100
FADE = 0.015


def load_pcm(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    pcm = array.array("h")
    pcm.frombytes(raw[: len(raw) // 2 * 2])
    return pcm


def rms_db(pcm, a, b):
    seg = pcm[max(int(a * SR), 0): max(int(b * SR), 0)]
    return 20 * math.log10(max(math.sqrt(sum(x * x for x in seg) / max(len(seg), 1)), 0.5) / 32768)


def quietest(pcm, a, b):
    """Instante más silencioso entre a y b: el alineado por palabras no siempre cae en el hueco real."""
    steps = max(int((b - a) / 0.002), 1)
    return min((a + i * 0.002 for i in range(steps + 1)), key=lambda t: rms_db(pcm, t - 0.005, t + 0.005))


def key(word):
    return word.lower().strip(".,;:¿?¡!…")


def read(stem):
    return json.loads(stem.with_suffix(".words.json").read_text(encoding="utf-8"))


def assemble(stem, take, a, b, p_a, p_b, gain):
    """Une locución[0, a] + toma[p_a, p_b] + locución[b, fin]. Sin a o sin b no hay ese tramo."""
    dur = p_b - p_a
    fades = (f"afade=t=in:d={FADE}," if a else "") + (f"afade=t=out:st={dur - FADE:.4f}:d={FADE}," if b is not None else "")
    fc, labels = [], []
    if a:
        fc.append(f"[0:a]atrim=0:{a:.4f},asetpts=PTS-STARTPTS,afade=t=out:st={a - FADE:.4f}:d={FADE}[h]")
        labels.append("[h]")
    fc.append(f"[1:a]atrim={p_a:.4f}:{p_b:.4f},asetpts=PTS-STARTPTS,volume={gain:.2f}dB,apad=whole_dur={dur:.4f},{fades}anull[m]")
    labels.append("[m]")
    if b is not None:
        fc.append(f"[0:a]atrim={b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d={FADE}[t]")
        labels.append("[t]")
    fc.append(f"{''.join(labels)}concat=n={len(labels)}:v=0:a=1[o]")
    tmp = stem.with_name(stem.name + ".tmp.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(stem.with_suffix(".mp3")), "-i", str(take.with_suffix(".mp3")),
                    "-filter_complex", ";".join(fc), "-map", "[o]", "-ar", str(SR), "-b:a", "192k", str(tmp)], check=True)
    tmp.replace(stem.with_suffix(".mp3"))


def write(stem, doc, words):
    doc.update(text=" ".join(w["w"] for w in words), duration=words[-1]["end"], words=words)
    stem.with_suffix(".words.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")


def moved(words, shift):
    return [{"w": w["w"], "start": round(w["start"] + shift, 3), "end": round(w["end"] + shift, 3)} for w in words]


def splice(stem, take, i, j, q0, q1, p_end, labels=None):
    """Cambia las palabras i..j de la locución por las palabras q0..q1 de la toma."""
    doc, W, P = read(stem), read(stem)["words"], read(take)["words"]
    pcm, ppcm = load_pcm(stem.with_suffix(".mp3")), load_pcm(take.with_suffix(".mp3"))
    a = quietest(pcm, W[i]["start"] - 0.12, W[i]["start"] + 0.04) if i else 0.0
    b = quietest(pcm, W[j]["end"] - 0.08, W[j + 1]["start"] + 0.02) if j + 1 < len(W) else None
    p_a = quietest(ppcm, P[q0]["start"] - 0.1, P[q0]["start"] + 0.03) if q0 else 0.0
    # Con palabras sueltas, la primera es la mejor referencia de cómo sonaba ese punto de la frase; con una frase, toda ella
    k = 0 if labels else j - i
    r = 0 if labels else q1 - q0
    gain = rms_db(pcm, W[i]["start"], W[i + k]["end"] + 0.05) - rms_db(ppcm, P[q0]["start"], P[q0 + r]["end"] + 0.05)
    assemble(stem, take, a, b, p_a, p_end, gain)
    dur = p_end - p_a
    mid = moved(P[q0:q1 + 1], a - p_a)
    for w in mid:
        w["end"] = min(w["end"], round(a + dur, 3))
    if labels:
        for w, label in zip(mid, labels):
            w["w"] = label
    tail = moved(W[j + 1:], a + dur - b) if b is not None else []
    write(stem, doc, W[:i] + mid + tail)
    print(f"cambiadas {j - i + 1} palabras: locución {a:.3f}–{b if b is None else round(b, 3)} s, "
          f"toma {p_a:.3f}–{p_end:.3f} s, nivel {gain:+.2f} dB, duración {doc['duration']:.2f} s")


def phrase(args):
    W, P = read(args.voice)["words"], read(args.take)["words"]
    head = args.first.split()
    hits = [k for k in range(len(W)) if [w["w"] for w in W[k:k + len(head)]] == head]
    if len(hits) != 1:
        sys.exit(f"«{args.first}» aparece {len(hits)} veces")
    i = hits[0]
    j = next(k for k in range(i, len(W)) if W[k]["w"] == args.last)
    splice(args.voice, args.take, i, j, 0, len(P) - 1, P[-1]["end"] + 0.1)


def word(args):
    wanted = [key(x) for x in args.words.split()]
    n = len(wanted)
    find = lambda W: [k for k in range(len(W) - n + 1) if [key(w["w"]) for w in W[k:k + n]] == wanted]
    P = read(args.take)["words"]
    q = find(P)
    if not q:
        sys.exit(f"«{args.words}» no está en la toma")
    total = len(find(read(args.voice)["words"]))
    which = range(total) if args.which == "all" else [int(x) for x in args.which.split(",")]
    # De atrás adelante: así los índices de las apariciones que quedan no cambian
    for m in sorted(which, reverse=True):
        if m >= total:
            sys.exit(f"solo hay {total} apariciones de «{args.words}»")
        W = read(args.voice)["words"]
        i = find(W)[m]
        # La palabra de la toma, con la puntuación que ya tenía la frase
        labels = [P[q[0] + k]["w"].rstrip(".,;:…") + W[i + k]["w"][len(W[i + k]["w"].rstrip(".,;:…")):] for k in range(n)]
        splice(args.voice, args.take, i, i + n - 1, q[0], q[0] + n - 1, P[q[0] + n - 1]["start"] + args.tail, labels)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("phrase")
    a.add_argument("voice", type=Path); a.add_argument("take", type=Path); a.add_argument("first"); a.add_argument("last")
    a.set_defaults(run=phrase)
    b = sub.add_parser("word")
    b.add_argument("voice", type=Path); b.add_argument("take", type=Path); b.add_argument("words"); b.add_argument("which")
    b.add_argument("--tail", type=float, default=0.34)
    b.set_defaults(run=word)
    args = ap.parse_args()
    backup = args.voice.with_name(args.voice.name + ".bak.mp3")
    if not backup.exists():
        shutil.copy(args.voice.with_suffix(".mp3"), backup)
        shutil.copy(args.voice.with_suffix(".words.json"), backup.with_suffix(".words.json"))
    args.run(args)


if __name__ == "__main__":
    main()
