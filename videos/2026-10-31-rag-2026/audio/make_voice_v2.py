#!/usr/bin/env python3
"""Locución v2 del vídeo de RAG: mismas frases que la v1, con las grafías y el ritmo elegidos de oído (14-11).

- Pronunciación: pronunciation.json (Clod, ía, rag, Espóiler).
- style 0,3 en ElevenLabs y tempo ×1,10 con atempo (speed no hace nada con eleven_v4).
- words.json vuelve a la grafía del guion, para que build_root.py y make_captions.py casen con el texto.

Uso (desde la raíz del repo): python3 videos/2026-10-31-rag-2026/audio/make_voice_v2.py [escena ...]
Lee el texto de voice-v1/ y escribe en voice/.
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TEMPO = 1.10
STYLE = 0.3
SCENES = ["1", "2", "2b", "3a", "3b", "3c", "4", "5", "6", "7", "8", "9", "10", "11"]


def make(scene):
    src = json.loads((HERE / f"voice-v1/scene-{scene}.words.json").read_text(encoding="utf-8"))
    text = src["text"]
    raw = HERE / f"voice-v2-raw/scene-{scene}"
    raw.parent.mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/tts.py"), "say", str(raw), text,
                    "--pron", str(HERE.parent / "pronunciation.json"), "--scene", scene,
                    "--style", str(STYLE), "--voice-env", "ELEVENLABS_VOICE_ID_SANTI"], check=True, cwd=ROOT)
    spoken = json.loads(Path(f"{raw}.words.json").read_text(encoding="utf-8"))
    script_words = text.split()
    if len(script_words) != len(spoken["words"]):
        sys.exit(f"escena {scene}: {len(script_words)} palabras en el guion y {len(spoken['words'])} en la voz")
    out = HERE / f"voice/scene-{scene}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{raw}.mp3", "-filter:a", f"atempo={TEMPO}",
                    "-b:a", "128k", f"{out}.mp3"], check=True)
    words = [{"w": w, "start": round(x["start"] / TEMPO, 3), "end": round(x["end"] / TEMPO, 3)}
             for w, x in zip(script_words, spoken["words"])]
    data = {"scene": scene, "voice_id": src.get("voice_id"), "model_id": spoken["model_id"], "text": text,
            "spoken_text": spoken["text"], "duration": round(spoken["duration"] / TEMPO, 3), "words": words,
            "voice_settings": spoken["voice_settings"], "tempo": TEMPO, "credits": spoken["credits"]}
    Path(f"{out}.words.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    for s in sys.argv[1:] or SCENES:
        make(s)
