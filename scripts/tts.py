#!/usr/bin/env python3
"""Genera voz con ElevenLabs y guarda el mp3 y los tiempos de cada palabra.

Escribe <salida>.mp3 y <salida>.words.json con el formato que usan check_voice.py,
splice_voice.py y make_captions.py: {"text", "duration", "words": [{"w", "start", "end"}]},
más el modelo, la voz, los ajustes y los créditos que costó.

Antes de mandar el texto aplica un mapa de pronunciación (solo a lo que oye la
voz; el guion no cambia):

    {"map": {"Odoo": "Odú", "IA": "í-a"},
     "phrases": [{"scene": "1", "from": "una IA acceso", "to": "una í-a, acceso"}]}

«phrases» va antes que «map» y solo en su escena: sirve para la frase en la que la
grafía general no suena bien. Si el guion cambia y la frase ya no aparece una sola
vez, se para antes de gastar créditos.

Uso:
    tts.py say <salida> "<texto>" [opciones]
    tts.py file <salida> <texto.txt> [opciones]

Opciones:
    --pron pronunciation.json   mapa de pronunciación
    --scene ID                  escena, para las «phrases» del mapa
    --model eleven_v4           modelo (eleven_v4 por defecto)
    --lang es                   idioma (es por defecto; sin él, la voz puede tirar a otro acento)
    --speed 1.0                 velocidad (0,7 a 1,2)
    --stability 0.5 --similarity 0.75 --style 0.0
    --voice-env ELEVENLABS_VOICE_ID   variable de .env con el id de la voz

Lee ELEVENLABS_API_KEY y la voz del entorno o de .env en la carpeta actual.
"""
import argparse, base64, json, os, re, sys, urllib.error, urllib.request
from pathlib import Path


def load_env():
    env = Path(".env")
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$", line)
            if m and m.group(1) not in os.environ:
                os.environ[m.group(1)] = m.group(2).strip().strip('"').strip("'")


def respell(text, pron, scene):
    if not pron:
        return text
    conf = json.loads(Path(pron).read_text(encoding="utf-8"))
    for ph in conf.get("phrases", []):
        if scene is None or str(ph["scene"]) != str(scene):
            continue
        n = text.count(ph["from"])
        if n != 1:
            sys.exit(f"escena {scene}: «{ph['from']}» aparece {n} veces; revisa «phrases» en {pron}")
        text = text.replace(ph["from"], ph["to"])
    for src, dst in conf.get("map", {}).items():
        text = re.sub(rf"(?<!\w){re.escape(src)}(?!\w)", dst, text)
    return text


def words_from(alignment):
    words, cur = [], None
    for c, s, e in zip(alignment["characters"], alignment["character_start_times_seconds"],
                       alignment["character_end_times_seconds"]):
        if c.isspace():
            if cur:
                words.append(cur)
                cur = None
        elif cur is None:
            cur = {"w": c, "start": round(s, 3), "end": round(e, 3)}
        else:
            cur["w"] += c
            cur["end"] = round(e, 3)
    if cur:
        words.append(cur)
    return words


def speak(text, out, a):
    voice = os.environ.get(a.voice_env) or sys.exit(f"falta {a.voice_env} en el entorno o en .env")
    key = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("falta ELEVENLABS_API_KEY en el entorno o en .env")
    settings = {"stability": a.stability, "similarity_boost": a.similarity, "style": a.style,
                "use_speaker_boost": True, "speed": a.speed}
    body = {"text": text, "model_id": a.model, "voice_settings": settings, "language_code": a.lang}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            cost = r.headers.get("character-cost")
            d = json.load(r)
    except urllib.error.HTTPError as e:
        # 401 quota_exceeded es el tope de créditos de la clave, no un fallo de autenticación
        sys.exit(f"{out.name}: HTTP {e.code} {e.read()[:400].decode(errors='replace')}")
    out.parent.mkdir(parents=True, exist_ok=True)
    Path(f"{out}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    words = words_from(d["alignment"])
    dur = d["alignment"]["character_end_times_seconds"][-1]
    Path(f"{out}.words.json").write_text(json.dumps(
        {"text": text, "duration": round(dur, 3), "words": words, "model_id": a.model,
         "voice_env": a.voice_env, "language_code": a.lang, "voice_settings": settings, "credits": cost},
        ensure_ascii=False, indent=1), encoding="utf-8")
    wpm = len(words) / dur * 60 if dur else 0
    print(f"{out.name}: {dur:.1f} s, {len(words)} palabras ({wpm:.0f}/min), {len(text)} caracteres, coste {cost}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["say", "file"])
    p.add_argument("out", help="ruta de salida sin extensión")
    p.add_argument("text", help="texto (say) o fichero de texto (file)")
    p.add_argument("--pron")
    p.add_argument("--scene")
    p.add_argument("--model", default="eleven_v4")
    p.add_argument("--lang", default="es")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--stability", type=float, default=0.5)
    p.add_argument("--similarity", type=float, default=0.75)
    p.add_argument("--style", type=float, default=0.0)
    p.add_argument("--voice-env", default="ELEVENLABS_VOICE_ID")
    a = p.parse_args()
    if not 0.7 <= a.speed <= 1.2:
        sys.exit("--speed va de 0,7 a 1,2")
    load_env()
    text = a.text if a.mode == "say" else Path(a.text).read_text(encoding="utf-8").strip()
    speak(respell(text, a.pron, a.scene), Path(a.out), a)


if __name__ == "__main__":
    main()
