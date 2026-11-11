#!/usr/bin/env python3
"""Baja la música cuando habla la voz (ducking) y mide si la tapa.

Hace dos cosas:
1. Con --out, escribe la música con el ducking aplicado: `sidechaincompress` de
   ffmpeg, con la voz como señal de control. La música baja solo mientras hay voz
   y vuelve a subir en las pausas. El nivel general no cambia: el volumen de la
   mezcla (data-volume en HyperFrames) se sigue poniendo aparte.
2. Siempre, un informe: en ventanas de medio segundo con voz, cuántos dB queda la
   música por debajo de la voz, antes y después del ducking, al volumen de mezcla
   de --volume. Marca los tramos en que la distancia baja de --min-gap.

Mide RMS, no sonoridad percibida (LUFS): sirve para saber qué escuchar primero, no
para decidir si suena bien. El umbral de --min-gap hay que calibrarlo de oído.

La voz sale de la composición raíz de HyperFrames (--hyperframes index.html: los
<audio class="clip"> cuyo id empieza por «voice», con data-start, data-duration y
data-media-start) o se da a mano: un fichero, o varios clips con su instante de
inicio en el vídeo («escena.mp3@23.52»).

Uso:
    uv run --with numpy scripts/duck_music.py --music assets/music/bed.mp3 \\
        --hyperframes index.html --volume 0.14 --out assets/music/bed-ducked.mp3
    uv run --with numpy scripts/duck_music.py --music bed.mp3 \\
        --voice scene-1.mp3@0 --voice scene-2.mp3@23.52 --volume 0.14 [--report informe.json]

Ajustes del compresor (valores de partida): --threshold 0.02 (−34 dBFS de voz),
--ratio 4, --attack 20 ms, --release 400 ms. Más ratio, más baja la música.
Sale con 1 si queda algún tramo por debajo de --min-gap.
"""
import argparse
import html.parser
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

SR = 16000
WIN = 0.5  # s por ventana del informe


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def duration(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


class VoiceClips(html.parser.HTMLParser):
    """Lee los <audio class="clip"> de voz de una composición de HyperFrames."""

    def __init__(self, base, prefix):
        super().__init__()
        self.base, self.prefix, self.clips = base, prefix, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "audio" and "clip" in (a.get("class") or "").split() and (a.get("id") or "").startswith(self.prefix):
            self.clips.append({"path": str(self.base / a["src"]), "start": float(a.get("data-start", 0)),
                               "media_start": float(a.get("data-media-start", 0)),
                               "duration": float(a["data-duration"]) if a.get("data-duration") else None})


def parse_spec(spec):
    path, start = spec.rsplit("@", 1) if "@" in spec else (spec, "0")
    return {"path": path, "start": float(start), "media_start": 0.0, "duration": None}


def build_voice(clips, length, dest):
    """Coloca cada clip de voz en su instante y lo mezcla en una sola pista de `length` s."""
    inputs, chains = [], []
    for i, c in enumerate(clips):
        inputs += ["-i", c["path"]]
        trim = f"atrim=start={c['media_start']}" + (f":duration={c['duration']}" if c["duration"] else "")
        ms = int(round(c["start"] * 1000))
        chains.append(f"[{i}:a]{trim},asetpts=N/SR/TB,aformat=channel_layouts=mono,aresample=44100,"
                      f"adelay={ms}:all=1[v{i}]")
    mix = "".join(f"[v{i}]" for i in range(len(clips)))
    graph = ";".join(chains) + f";{mix}amix=inputs={len(clips)}:normalize=0,apad,atrim=0:{length}[out]"
    ffmpeg(*inputs, "-filter_complex", graph, "-map", "[out]", "-ar", "44100", str(dest))


def duck(music, voice, dest, a):
    graph = (f"[1:a]aformat=channel_layouts=mono[key];"
             f"[0:a][key]sidechaincompress=threshold={a.threshold}:ratio={a.ratio}:"
             f"attack={a.attack}:release={a.release}:makeup=1[out]")
    ffmpeg("-i", str(music), "-i", str(voice), "-filter_complex", graph, "-map", "[out]",
           "-ar", "44100", "-b:a", "192k", str(dest))


def pcm(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def rms_db(x):
    n = int(SR * WIN)
    frames = x[: len(x) // n * n].reshape(-1, n)
    return 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)


def gaps(voice_db, music_db, voice_floor):
    k = min(len(voice_db), len(music_db))
    active = voice_db[:k] > voice_floor
    return active, voice_db[:k] - music_db[:k]


def intervals(mask, min_len):
    """Agrupa ventanas seguidas marcadas en tramos [inicio, fin] en segundos; descarta los más cortos que min_len.

    Una ventana suelta suele ser el principio o el final de una frase, con poca voz: no avisa de nada."""
    out, start = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and start is None:
            start = i
        elif not m and start is not None:
            if (i - start) * WIN >= min_len:
                out.append([round(start * WIN, 1), round(i * WIN, 1)])
            start = None
    return out


def summary(gap, active):
    g = gap[active]
    return {"median_db": round(float(np.median(g)), 1), "p10_db": round(float(np.percentile(g, 10)), 1)}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--music", required=True, help="pista de música (ya con la duración del vídeo)")
    p.add_argument("--voice", action="append", default=[], help="fichero de voz, o clip@inicio_en_s (repetible)")
    p.add_argument("--hyperframes", help="composición raíz de HyperFrames de la que leer los clips de voz")
    p.add_argument("--voice-prefix", default="voice", help="prefijo del id de los <audio> de voz")
    p.add_argument("--volume", type=float, default=1.0, help="volumen de la música en la mezcla (data-volume)")
    p.add_argument("--out", help="dónde escribir la música con ducking")
    p.add_argument("--report", help="guardar el informe en JSON")
    p.add_argument("--min-gap", type=float, default=15.0, help="dB mínimos de la voz sobre la música (por calibrar)")
    p.add_argument("--min-length", type=float, default=1.0, help="s mínimos de un tramo para avisar de él")
    p.add_argument("--voice-floor", type=float, default=-40.0, help="dBFS a partir de los que una ventana tiene voz")
    p.add_argument("--threshold", type=float, default=0.02)
    p.add_argument("--ratio", type=float, default=4.0)
    p.add_argument("--attack", type=float, default=20.0)
    p.add_argument("--release", type=float, default=400.0)
    a = p.parse_args()

    clips = [parse_spec(v) for v in a.voice]
    if a.hyperframes:
        parser = VoiceClips(Path(a.hyperframes).parent, a.voice_prefix)
        parser.feed(Path(a.hyperframes).read_text(encoding="utf-8"))
        clips += parser.clips
    if not clips:
        sys.exit("Falta la voz: usa --hyperframes o --voice.")
    length = duration(a.music)
    with tempfile.TemporaryDirectory() as tmp:
        voice = Path(tmp) / "voice.wav"
        build_voice(clips, length, voice)
        ducked = Path(a.out) if a.out else Path(tmp) / "ducked.wav"
        duck(a.music, voice, ducked, a)
        v = rms_db(pcm(voice))
        gain = 20 * np.log10(a.volume)
        before = rms_db(pcm(a.music)) + gain
        after = rms_db(pcm(ducked)) + gain

    active, gap_before = gaps(v, before, a.voice_floor)
    _, gap_after = gaps(v, after, a.voice_floor)
    if not active.any():
        sys.exit("No se ha encontrado voz: revisa --voice y --voice-floor.")
    low = intervals(active & (gap_after < a.min_gap), a.min_length)
    report = {
        "music": a.music, "volume": a.volume, "min_gap_db": a.min_gap,
        "voice_seconds": round(float(active.sum() * WIN), 1),
        "gap_before": summary(gap_before, active),
        "gap_after": summary(gap_after, active),
        "music_in_pauses_dbfs": round(float(np.median(after[: len(active)][~active])), 1) if (~active).any() else None,
        "low_gap": low,
        "compressor": {"threshold": a.threshold, "ratio": a.ratio, "attack": a.attack, "release": a.release},
    }
    print(f"voz: {report['voice_seconds']} s · música a volumen {a.volume}")
    print(f"distancia voz-música sin ducking: mediana {report['gap_before']['median_db']} dB, "
          f"peor 10 % {report['gap_before']['p10_db']} dB")
    print(f"distancia voz-música con ducking: mediana {report['gap_after']['median_db']} dB, "
          f"peor 10 % {report['gap_after']['p10_db']} dB")
    if report["music_in_pauses_dbfs"] is not None:
        print(f"música en las pausas de la voz: mediana {report['music_in_pauses_dbfs']} dBFS")
    if low:
        print(f"{len(low)} tramos con la música a menos de {a.min_gap} dB de la voz (escuchar primero):")
        for s, e in low[:30]:
            print(f"  {int(s // 60)}:{s % 60:04.1f} – {int(e // 60)}:{e % 60:04.1f}")
    else:
        print(f"ningún tramo con la música a menos de {a.min_gap} dB de la voz")
    if a.out:
        print(f"música con ducking: {a.out}")
    if a.report:
        Path(a.report).write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    sys.exit(1 if low else 0)


if __name__ == "__main__":
    main()
