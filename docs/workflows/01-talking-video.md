# Workflow 1 — Vídeo hablado: quitar errores, silencios y muletillas

Herramienta: [video-use](https://github.com/browser-use/video-use) (skill para Claude Code, MIT).

## Instalación (una vez)

Opción rápida: pegar en Claude Code el prompt de instalación del README de video-use. Claude clona el repo, instala dependencias, configura ffmpeg, registra la skill y pide la clave de ElevenLabs.

Opción manual (Mac):

```bash
brew install ffmpeg yt-dlp
git clone https://github.com/browser-use/video-use ~/tools/video-use
ln -s ~/tools/video-use ~/.claude/skills/video-use
cd ~/tools/video-use && uv sync        # o: pip install -e .
cp .env.example .env                   # poner ELEVENLABS_API_KEY
```

Opción manual (Windows, PowerShell):

```powershell
winget install Gyan.FFmpeg
winget install yt-dlp.yt-dlp
winget install astral-sh.uv
git clone https://github.com/browser-use/video-use $HOME\tools\video-use
New-Item -ItemType Junction -Path "$HOME\.claude\skills\video-use" -Target "$HOME\tools\video-use"
cd $HOME\tools\video-use; uv sync
copy .env.example .env                 # poner ELEVENLABS_API_KEY
```

## Cómo funciona

Pipeline: **Transcribir → Empaquetar → Razonar → EDL → Render → Autoevaluación**.

1. **Transcribe** cada toma con ElevenLabs Scribe: tiempo de cada palabra, quién habla, risas, suspiros.
2. **Empaqueta** todas las tomas en `takes_packed.md` (~12 KB). Claude decide leyendo el texto, no viendo el vídeo.
3. **Mira solo cuando duda:** `timeline_view` genera una imagen con fotogramas, forma de onda y palabras de un tramo.
4. **Corta** por límites de palabra y silencios: muletillas, arranques en falso, tiempos muertos, repeticiones (se queda con la mejor toma). Fundido de audio de 30 ms en cada corte.
5. **Etalona** cada segmento (cálido cinematográfico, neutro con contraste, o cadena ffmpeg propia).
6. **Subtítulos** quemados (por defecto 2 palabras en mayúsculas, personalizable).
7. **Autorrevisión:** revisa cada corte del render buscando saltos, chasquidos o subtítulos tapados; corrige y re-renderiza hasta 3 veces.

## Uso

```bash
cd ~/Videos/2026-11-xx-mi-video     # carpeta con las tomas en bruto
claude
> Monta estas tomas en un vídeo de YouTube de ~8 min. Quita errores y silencios. Subtítulos sí.
```

- Primero inventaría el material y propone una estrategia; no corta hasta que la apruebes.
- Salida: `edit/final.mp4`. Memoria de sesión en `edit/project.md` (para seguir otro día: "acorta la intro").

## Limitaciones

- Muy bueno para contenido hablado; menos fino en montajes puramente visuales.
- No hay timeline para ajustar a mano → si hace falta, retocar en Palmier Pro (solo macOS) o Velorn.
- Depende de ElevenLabs para transcribir (coste por uso).

## Al terminar

Copiar a `videos/<carpeta>/`: el `.srt` si se generó, notas de cortes y el `project.md` relevante. No el vídeo.
