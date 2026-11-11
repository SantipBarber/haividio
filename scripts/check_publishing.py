#!/usr/bin/env python3
"""Comprueba la ficha de un vídeo antes y después de subirlo a YouTube con youtubeuploader.

Antes de subir, valida el JSON que se le pasa con -metaJSON contra las reglas de
YouTube y contra el vídeo real:
- título de una línea y como máximo 100 caracteres; descripción de 5000 bytes como
  máximo; ninguno de los dos con < ni >, que YouTube rechaza;
- etiquetas de 500 caracteres en total como máximo (las que llevan espacios cuentan
  2 más, por las comillas);
- capítulos de la descripción: el primero en 0:00, al menos 3, en orden y de 10 s o
  más cada uno (si no se cumple, YouTube no los muestra);
- el vídeo se puede leer entero (ffprobe) y ningún capítulo empieza después del final;
- la visibilidad no es pública y están declarados madeForKids y containsSyntheticMedia.

Después de subir, lee el fichero de -metaJSONout y comprueba que YouTube ha dejado
el vídeo con la visibilidad pedida: un proyecto de Google Cloud sin auditar lo deja
en privado aunque se pida oculto.

La miniatura: JPG, PNG, GIF o BMP; 16:9 (9:16 en un Short) y 640 px como mínimo en el
lado corto; 50 MB como máximo por la API. Con --preview, guarda la imagen reducida al
tamaño en que se ve en el móvil (360 y 168 px de ancho), para mirar si se lee.

Uso:
    python3 scripts/check_publishing.py meta publishing.json video.mp4
    python3 scripts/check_publishing.py result upload-result.json --expect unlisted
    python3 scripts/check_publishing.py thumb miniatura.png --preview miniatura-movil.png

Sale con 1 si algo no vale. Solo necesita Python 3 y ffprobe.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TITLE_MAX = 100
DESCRIPTION_MAX_BYTES = 5000
TAGS_MAX = 500
CHAPTERS_MIN = 3
CHAPTER_MIN_SECONDS = 10
CHAPTER = re.compile(r"^\s*(?:(\d+):)?(\d{1,2}):(\d{2})\s+\S")


def video_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        sys.exit(f"✖ No se puede leer {path} (¿render cortado?): {r.stderr.strip()[:200]}")


def mmss(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def chapters(description: str) -> list[int]:
    starts = []
    for line in description.splitlines():
        m = CHAPTER.match(line)
        if m:
            starts.append(int(m.group(1) or 0) * 3600 + int(m.group(2)) * 60 + int(m.group(3)))
    return starts


def check_chapters(starts: list[int], duration: float) -> list[str]:
    if not starts:
        return []
    issues = []
    if starts[0] != 0:
        issues.append("el primer capítulo tiene que empezar en 0:00")
    if len(starts) < CHAPTERS_MIN:
        issues.append(f"hay {len(starts)} capítulos: YouTube pide al menos {CHAPTERS_MIN} (o ninguno)")
    if starts != sorted(starts):
        issues.append("los capítulos no van en orden")
    for start, end in zip(starts, starts[1:] + [duration]):
        if start >= duration:
            issues.append(f"el capítulo de {mmss(start)} empieza después del final ({mmss(duration)})")
        elif end - start < CHAPTER_MIN_SECONDS:
            issues.append(f"el capítulo de {mmss(start)} dura {end - start:.0f} s: mínimo {CHAPTER_MIN_SECONDS}")
    return issues


def check_meta(args) -> None:
    meta = json.loads(Path(args.meta).read_text())
    duration = video_duration(Path(args.video))
    title = meta.get("title", "")
    description = meta.get("description", "")
    tags = meta.get("tags", [])
    issues = []

    if not title:
        issues.append("falta el título (title)")
    elif len(title) > TITLE_MAX or "\n" in title:
        issues.append(f"el título tiene {len(title)} caracteres o varias líneas (máximo {TITLE_MAX}, una línea)")
    if not description:
        issues.append("falta la descripción (description)")
    elif len(description.encode()) > DESCRIPTION_MAX_BYTES:
        issues.append(f"la descripción ocupa {len(description.encode())} bytes (máximo {DESCRIPTION_MAX_BYTES})")
    for name, text in (("el título", title), ("la descripción", description)):
        if "<" in text or ">" in text:
            issues.append(f"{name} lleva < o >, que YouTube no admite")
    tags_length = sum(len(t) + (2 if " " in t else 0) for t in tags) + max(len(tags) - 1, 0)
    if tags_length > TAGS_MAX:
        issues.append(f"las etiquetas suman {tags_length} caracteres (máximo {TAGS_MAX})")

    starts = chapters(description)
    issues += check_chapters(starts, duration)

    privacy = meta.get("privacyStatus", "private")
    if privacy == "public" and not args.allow_public:
        issues.append("privacyStatus es public: sube como private o unlisted y publícalo tras revisarlo")
    for key in ("madeForKids", "containsSyntheticMedia"):
        if key not in meta:
            issues.append(f"falta {key} (true o false): YouTube lo pide declarar")

    for issue in issues:
        print(f"✖ {issue}")
    if issues:
        sys.exit(1)
    print(f"✔ Ficha válida: título de {len(title)} caracteres, {len(starts)} capítulos, "
          f"{len(tags)} etiquetas, vídeo de {mmss(duration)}, visibilidad {privacy}")


def check_result(args) -> None:
    video = json.loads(Path(args.result).read_text())
    privacy = video.get("status", {}).get("privacyStatus")
    video_id = video.get("id", "?")
    if privacy != args.expect:
        sys.exit(f"✖ YouTube ha dejado el vídeo en «{privacy}», no en «{args.expect}». Si el proyecto "
                 "de Google Cloud no está auditado, queda bloqueado en privado: no repartas el enlace "
                 f"y revísalo en Studio. https://youtu.be/{video_id}")
    print(f"✔ Visibilidad: {privacy}. https://youtu.be/{video_id}")


THUMB_MAX_BYTES = 50 * 1024 * 1024   # thumbnails.set desde el 14-09-2026 (antes, 2 MB)
THUMB_MOBILE_BYTES = 2 * 1024 * 1024  # límite al subirla desde la app del móvil
THUMB_FORMATS = {"png": "png", "mjpeg": "jpg", "gif": "gif", "bmp": "bmp"}


def check_thumb(args) -> None:
    path = Path(args.image)
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=codec_name,width,height", "-of", "json", str(path)],
                         capture_output=True, text=True)
    streams = json.loads(out.stdout or "{}").get("streams") or []
    if out.returncode or not streams:
        sys.exit(f"✖ No se puede leer la imagen: {path}")
    codec, w, h = streams[0]["codec_name"], streams[0]["width"], streams[0]["height"]
    size = path.stat().st_size
    issues, notes = [], []
    if codec not in THUMB_FORMATS:
        issues.append(f"formato {codec}: YouTube acepta JPG, PNG, GIF o BMP")
    ratio, want = w / h, (9 / 16 if args.short else 16 / 9)
    if abs(ratio - want) / want > 0.01:
        issues.append(f"{w}×{h} no es {'9:16' if args.short else '16:9'}")
    short_side = w if not args.short else h
    if short_side < 640:
        issues.append(f"{'ancho' if not args.short else 'alto'} de {short_side} px: mínimo 640")
    elif short_side < 1280:
        notes.append(f"{w}×{h}: se verá blanda en pantallas grandes; YouTube recomienda 3840×2160 (1280×720 como mínimo práctico)")
    if size > THUMB_MAX_BYTES:
        issues.append(f"{size / 1e6:.1f} MB: la API admite 50 MB como máximo")
    elif size > THUMB_MOBILE_BYTES:
        notes.append(f"{size / 1e6:.1f} MB: vale por la API, pero desde la app del móvil el límite es 2 MB")
    # Vistas previas al tamaño en que se ve en el móvil: si no se lee ahí, no se lee.
    if args.preview:
        widths = [360, 168] if not args.short else [180, 94]
        chain = ";".join(f"[0:v]scale={pw}:-2:flags=area,pad=iw+16:ih+16:8:8:color=0x202020[p{i}]"
                         for i, pw in enumerate(widths))
        chain += ";[p0][p1]xstack=inputs=2:layout=0_0|w0_0:fill=0x202020"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-filter_complex", chain,
                        "-frames:v", "1", args.preview], check=True)
        notes.append(f"vista previa a tamaño de móvil ({' y '.join(map(str, widths))} px de ancho): {args.preview}")
    for n in notes:
        print(f"· {n}")
    if issues:
        for i in issues:
            print(f"✖ {i}")
        sys.exit(1)
    print(f"✔ Miniatura: {codec}, {w}×{h}, {size / 1e6:.2f} MB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    meta = sub.add_parser("meta", help="valida el JSON de -metaJSON antes de subir")
    meta.add_argument("meta")
    meta.add_argument("video")
    meta.add_argument("--allow-public", action="store_true", help="admite privacyStatus public")
    meta.set_defaults(func=check_meta)
    result = sub.add_parser("result", help="comprueba la visibilidad con el JSON de -metaJSONout")
    result.add_argument("result")
    result.add_argument("--expect", default="private", choices=["private", "unlisted", "public"])
    result.set_defaults(func=check_result)
    thumb = sub.add_parser("thumb", help="valida la miniatura y saca una vista previa a tamaño de móvil")
    thumb.add_argument("image")
    thumb.add_argument("--short", action="store_true", help="miniatura vertical (9:16) de un Short")
    thumb.add_argument("--preview", help="PNG donde guardar la miniatura reducida a tamaño de móvil")
    thumb.set_defaults(func=check_thumb)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
