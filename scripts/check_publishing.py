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

Uso:
    python3 scripts/check_publishing.py meta publishing.json video.mp4
    python3 scripts/check_publishing.py result upload-result.json --expect unlisted

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
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
