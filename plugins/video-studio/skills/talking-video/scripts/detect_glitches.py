#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Detecta microcortes en un vídeo: saltos y caídas de audio, y congelaciones de imagen. Solo lee.

Da candidatos para revisar, no veredictos. Uso: uv run detect_glitches.py <vídeo>. Requiere ffmpeg.
"""
import argparse
import re
import subprocess

import numpy as np

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("video")
V = ap.parse_args().video
SR = 16000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(raw, dtype=np.float32)
print(f"audio {len(a) / SR:.1f} s")

# Clics: salto de muestra muy por encima de su entorno
d = np.abs(np.diff(a))
win = SR // 50
env = np.convolve(d, np.ones(win) / win, mode="same") + 1e-5
idx = np.where((d / env > 25) & (d > 0.02))[0]
clicks = sorted({round(i / SR, 1) for i in idx})
print("clics:", len(clicks), clicks[:60])

# Huecos: caída de nivel de menos de 120 ms entre dos tramos con voz
hop = SR // 100
rms = np.sqrt(np.convolve(a * a, np.ones(hop) / hop, mode="same"))[::hop] + 1e-9
db = 20 * np.log10(rms)
music = np.median(db[db < np.percentile(db, 30)])
gaps = []
i = 0
while i < len(db):
    if db[i] < -45:
        j = i
        while j < len(db) and db[j] < -45:
            j += 1
        if 1 <= j - i <= 12 and i > 3 and j < len(db) - 3 and db[i - 3] > -30 and db[j + 2] > -30:
            gaps.append((round(i / 100, 2), (j - i) * 10))
        i = j
    else:
        i += 1
print(f"huecos cortos entre voz (suelo {music:.0f} dB):", len(gaps), gaps[:40])

# Caídas relativas, con música de fondo: bajón brusco de más de 15 dB y vuelta en menos de 100 ms
drops = []
for k in range(3, len(db) - 10):
    if db[k - 2] > -28 and db[k] < db[k - 2] - 15 and np.max(db[k + 1 : k + 10]) > db[k - 2] - 5:
        drops.append(round(k / 100, 2))
print("caídas relativas:", len(drops), sorted(set(round(x, 1) for x in drops))[:60])

# Imagen: congelaciones y saltos
out = subprocess.run(["ffmpeg", "-hide_banner", "-i", V, "-vf", "scale=480:-1,freezedetect=n=0.0008:d=0.12,metadata=print:file=-", "-an", "-f", "null", "-"], capture_output=True, text=True)
txt = out.stdout + out.stderr
starts = [float(x) for x in re.findall(r"freeze_start[=: ]+([\d.]+)", txt)]
durs = [float(x) for x in re.findall(r"freeze_duration[=: ]+([\d.]+)", txt)]
pairs = list(zip(starts, durs))
print("congelaciones de imagen >=0,12 s:", len(pairs), [(round(s, 2), round(d, 2)) for s, d in pairs if d < 3][:40])
