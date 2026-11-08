#!/usr/bin/env python3
"""Comprueba una locución con WhisperX, en local y sin coste.

Transcribe el audio y lo compara palabra a palabra con el texto esperado:
marca palabras perdidas, cambiadas o añadidas, con su instante. Sustituye, sin
coste, a la ida y vuelta con Scribe.

Guarda además los tiempos reales de cada palabra (formato {"w","start","end"}),
que sirven para medir el desfase entre rótulos y voz en el vídeo final.

No decide si algo suena bien: la transcripción normaliza, y «API» dicha de dos
formas sale igual. Sí avisa de una sigla que debía decirse como palabra y
parece deletreada: el guion la escribe así («Api»), la transcripción la da en
mayúsculas («API») y dura demasiado para sus letras (en una prueba, «api» duró
0,18 y 0,26 s, y la toma deletreada, 0,46 s). Tampoco ve un corte limpio dentro de una palabra: en una
prueba, 150 ms quitados en mitad de «proveedor» no cambiaron la transcripción
(y comparar duraciones de palabras con el alineador dio hasta 0,3 s de ruido
en una copia sana, así que no sirve para eso).

Instalación (una vez, fuera del repositorio):
    uv venv ~/.local/share/haividio/whisperx --python 3.12
    uv pip install --python ~/.local/share/haividio/whisperx/bin/python whisperx==3.8.6

Uso:
    ~/.local/share/haividio/whisperx/bin/python scripts/check_voice.py voz.mp3 \\
        --words voz.words.json [--pron pronunciation.json]
    ... check_voice.py final.mp4 --text guion.txt

El texto esperado sale de --text (fichero) o del campo "text" de --words.
Con --pron, las grafías fonéticas enviadas a la voz («oce erre») se devuelven a
la escrita («OCR») antes de comparar.
"""
import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path


def norm(word):
    w = unicodedata.normalize("NFD", word.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    w = re.sub(r"[^a-z0-9ñ]", "", w)
    # En español la b y la v suenan igual: «IBAN» e «IVAN» no son un error.
    return w.replace("v", "b")


def tokens(text):
    out = []
    for raw in text.split():
        n = norm(raw)
        if n:
            out.append((raw, n))
    return out


def undo_pronunciation(text, pron):
    """Devuelve las grafías fonéticas a la forma escrita."""
    for ph in pron.get("phrases", []):
        text = text.replace(ph["to"], ph["from"])
    for written, spoken in sorted(pron.get("map", {}).items(), key=lambda kv: -len(kv[1])):
        text = re.sub(r"(?<!\w)" + re.escape(spoken) + r"(?!\w)", written, text)
    return text


_MODELS = {}


def transcribe(path, model_name, language):
    import whisperx

    if not _MODELS:
        _MODELS["asr"] = whisperx.load_model(model_name, device="cpu", compute_type="int8",
                                             language=language)
        _MODELS["align"] = whisperx.load_align_model(language_code=language, device="cpu")
    audio = whisperx.load_audio(str(path))
    result = _MODELS["asr"].transcribe(audio, batch_size=8, language=language)
    align_model, meta = _MODELS["align"]
    aligned = whisperx.align(result["segments"], align_model, meta, audio, "cpu",
                             return_char_alignments=False)
    words = []
    for w in aligned.get("word_segments", []):
        if "start" in w and "end" in w:
            words.append({"w": w["word"], "start": round(w["start"], 3),
                          "end": round(w["end"], 3), "score": round(w.get("score", 0), 3)})
    return words, len(audio) / 16000


# Segundos por letra a partir de los cuales una sigla parece deletreada. Dicha
# como palabra, «API» dio 0,06-0,09 s por letra; deletreada, 0,15.
SPELLED_SECONDS_PER_LETTER = 0.12


def spelled_acronyms(pairs):
    """Siglas escritas como palabra en el guion que suenan deletreadas."""
    out = []
    for raw_exp, word in pairs:
        heard_raw = re.sub(r"[^\wñÑ]", "", word["w"])
        if not (2 <= len(heard_raw) <= 5 and heard_raw.isupper() and heard_raw.isalpha()):
            continue
        if re.sub(r"[^\wñÑ]", "", raw_exp).isupper():
            continue  # el guion ya la escribe como sigla: deletrearla puede ser lo buscado
        dur = word["end"] - word["start"]
        if dur / len(heard_raw) > SPELLED_SECONDS_PER_LETTER:
            out.append({"tipo": "deletreada", "esperado": raw_exp, "oido": word["w"],
                        "t": word["start"], "duracion": round(dur, 3)})
    return out


def compare_text(expected, heard):
    exp = tokens(expected)
    got = [(w["w"], norm(w["w"]), w) for w in heard if norm(w["w"])]
    sm = difflib.SequenceMatcher(a=[e[1] for e in exp], b=[g[1] for g in got], autojunk=False)
    issues = []
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "equal":
            pairs = [(exp[a0 + k][0], got[b0 + k][2]) for k in range(a1 - a0)]
            issues.extend(spelled_acronyms(pairs))
            continue
        at = got[b0][2]["start"] if b0 < len(got) else (got[-1][2]["end"] if got else 0)
        heard_text = " ".join(g[0] for g in got[b0:b1])
        kind = {"replace": "cambiada", "delete": "perdida", "insert": "añadida"}[op]
        # La transcripción escribe en cifras lo que el guion dice en letras.
        if op == "replace" and re.search(r"\d", heard_text):
            kind = "número"
        issues.append({
            "tipo": kind,
            "esperado": " ".join(e[0] for e in exp[a0:a1]),
            "oido": heard_text,
            "t": at,
        })
    issues.sort(key=lambda x: x["t"])
    return issues, exp, got


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path, help="mp3, wav o vídeo")
    ap.add_argument("--text", type=Path, help="fichero con el texto esperado")
    ap.add_argument("--words", type=Path, help=".words.json: se usa su campo text")
    ap.add_argument("--pron", type=Path, help="pronunciation.json (map y phrases)")
    ap.add_argument("--model", default="large-v3-turbo")
    ap.add_argument("--language", default="es")
    ap.add_argument("--out", type=Path, help="informe JSON (por defecto, junto al audio)")
    args = ap.parse_args()

    if args.text:
        expected = args.text.read_text()
    elif args.words:
        expected = json.loads(args.words.read_text())["text"]
    else:
        sys.exit("Falta el texto esperado: --text o --words")
    if args.pron:
        expected = undo_pronunciation(expected, json.loads(args.pron.read_text()))

    heard, duration = transcribe(args.audio, args.model, args.language)
    issues, exp, got = compare_text(expected, heard)

    report = {"audio": str(args.audio), "duracion": round(duration, 3), "modelo": args.model,
              "palabras_esperadas": len(exp), "palabras_oidas": len(got), "texto": issues}
    report["palabras"] = heard

    out = args.out or args.audio.with_suffix(".check.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1))

    print(f"{args.audio.name}: {duration:.1f} s, {len(exp)} palabras esperadas, {len(got)} oídas")
    main_issues = [x for x in issues if x["tipo"] != "número"]
    numbers = [x for x in issues if x["tipo"] == "número"]
    print(f"Diferencias: {len(main_issues)}" + ("" if main_issues else " (ninguna)"))
    for x in main_issues:
        extra = f"  ({x['duracion']:.2f} s: escúchala)" if x["tipo"] == "deletreada" else ""
        print(f"  {x['t']:7.2f}s  {x['tipo']:10}  esperado «{x['esperado']}»  oído «{x['oido']}»{extra}")
    if numbers:
        print(f"Números escritos en cifras: {len(numbers)} (escúchalos solo si importa cómo se leen)")
        for x in numbers:
            print(f"  {x['t']:7.2f}s  «{x['esperado']}» → «{x['oido']}»")
    print(f"Informe: {out}")


if __name__ == "__main__":
    main()
