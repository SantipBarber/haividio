# Montaje con tiempos de voz y verificación

*[English](editing-and-verification.en.md)*

Técnicas probadas al montar una demo de producto con voz clonada. El flujo completo está en el [workflow 5](workflows/05-product-demo.md).

## ffmpeg + HyperFrames

| | Calidad | Problema |
|---|---|---|
| Solo ffmpeg | Cortes limpios, rótulos estáticos | Sin zooms suaves. El ffmpeg de Homebrew puede no traer `drawtext` |
| Solo HyperFrames | La mejor | Mal sitio para recortar esperas: cada ajuste toca la composición |
| **ffmpeg + HyperFrames** | La mejor, con ajustes rápidos | Hay que preparar el vídeo para HyperFrames |

ffmpeg prepara una «placa» por escena (mp4 a 1080p30, `-g 30`, `crf` 16) y HyperFrames compone encima, con `<video muted>`. **Un fotograma clave por segundo es lo que evita congelaciones al buscar.** Comprobado: 1:13 se renderiza en 52 s con GPU.

## Sincronía: la voz manda

- **El movimiento del cursor nunca se acelera.** Solo se ajusta el tiempo quieto entre dos puntos: se recorta si sobra y se congela si falta (`tpad=stop_mode=clone`). Se nota mucho menos que un `setpts`.
- **Cada punto del cursor se empareja con una palabra** en un fichero de «beats». Con eso y las marcas de la toma se calcula cada tramo. Cuantiza sobre el tiempo acumulado para que no haya deriva.
- **Las pausas se añaden en el montaje**, sin gastar créditos: fin de frase, fin de párrafo, y un máximo para los silencios que ya trae la voz.

### Busca frases, no palabras

Es el error que más escenas estropeó:

- La primera aparición de una palabra suelta sin mayúsculas («Es», «Para») amontonó escenas enteras.
- Un rótulo enganchado a una palabra repetida entró 10 s antes de tiempo.
- Una pausa ligada a una palabra se aplicó en todas sus apariciones y metió 3 s a mitad de otra frase.

Busca una frase exacta, con mayúsculas, y **falla si aparece varias veces**, salvo que se indique cuál:

```python
def t(self, phrase, n=None):
    norm = lambda s: re.sub(r"[^\wáéíóúüñÁÉÍÓÚ-]", "", s)
    toks, ws = [norm(x) for x in phrase.split()], [norm(w["w"]) for w in self.words]
    hits = [i for i in range(len(ws) - len(toks) + 1) if ws[i:i + len(toks)] == toks]
    if not hits or (n is None and len(hits) > 1) or (n and len(hits) < n):
        raise SystemExit(f"«{phrase}» aparece {len(hits)} veces (n={n})")
    return self.words[hits[(n or 1) - 1]]["start"]
```

Comprobar que los beats están en orden no prueba que caigan donde toca: mira el fotograma de ese instante.

## Cortes de audio sin microcortes

- **El punto medio entre dos palabras no siempre es silencio.** 9 de 99 cortes cayeron en plena voz (−15 a −32 dB) y se oyeron. Busca el mínimo de nivel en ±90 ms y funde 15 ms a cada lado.
- **La voz no siempre para tras «:» o una coma:** 18 cortes en plena voz estaban ahí, casi todos tras los dos puntos.
- **Después de montar, mide:** `silencedetect` para silencios largos (−35 dB, 0,6 s) y [`scripts/detect_glitches.py`](../scripts/detect_glitches.py) para clics y huecos cortos. Da candidatos, no veredictos.
- **Y compara con el guion:** [`scripts/check_voice.py`](../scripts/check_voice.py) transcribe el vídeo final con WhisperX y lista las palabras perdidas, cambiadas o añadidas, con su instante. En un vídeo de 8 minutos con música tardó 3 minutos en un Mac con Apple Silicon y dejó 3 avisos que escuchar; los números («veinte» frente a «20») los separa aparte. Guarda también el instante real de cada palabra, para comprobar rótulos.
- **Lo que ninguna de las dos ve:** un corte limpio de 150 ms dentro de una palabra. En la prueba no dejó clic ni hueco, y la transcripción salió igual. Comparar la duración de las palabras tampoco sirve: el alineador mueve hasta 0,3 s el inicio de una palabra tras una pausa, en una copia sana.

## Mezcla y volumen

- Música muy baja bajo la voz: 0,07 en una demo, 0,14 en un explicativo con animaciones. Lo decide un oído. Una transcripción puede entender peor un nombre propio con música: es una señal para escucharlo.
- **Ducking:** [`scripts/duck_music.py`](../scripts/duck_music.py) baja la música solo mientras hay voz (`sidechaincompress` de ffmpeg, con la voz como señal de control) y mide, en ventanas de medio segundo, cuántos dB queda la música por debajo de la voz, antes y después. Lee los clips de voz de la composición raíz de HyperFrames:

```bash
uv run --with numpy scripts/duck_music.py --music assets/music/bed.mp3 \
  --hyperframes index.html --volume 0.25 --out assets/music/bed-ducked.mp3
```

  Después, apunta el `<audio>` de la música a `bed-ducked.mp3`. Como la música ya baja bajo la voz, admite más volumen (`data-volume`) y llena las pausas. En el vídeo de RAG, con volumen fijo de 0,14, la música quedaba solo 13 dB por debajo de la voz (mediana); con ducking y 0,25, 23 dB, y en las pausas sonaba 5 dB más alta. Los tramos que marca, por debajo de `--min-gap` (15 dB por defecto, por calibrar), son lo primero que hay que escuchar. Mide RMS, no LUFS: no decide si suena bien.
- Si una pista no llega, se encadena consigo misma (`acrossfade=d=6`).
- Normaliza con `loudnorm` en dos pasadas a −14 LUFS y TP −1,5, y copia el vídeo si no cambia:

```bash
ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -    # mide
ffmpeg -i in.mp4 -c:v copy -c:a aac -b:a 192k -movflags +faststart \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=…:measured_TP=…:measured_LRA=…:measured_thresh=…:offset=…:linear=true,aresample=44100" out.mp4
ffmpeg -i out.mp4 -af ebur128=peak=true -f null -    # comprueba
```

- Al leer ese JSON desde un script, recorta entre la primera y la última llave: ffmpeg escribe texto después.
- En zsh, `"$var:linear"` aplica el modificador `:l`. Escribe `${var}:linear`.

## Revisión visual del render

El agente no ve el vídeo en movimiento. [`scripts/check_render.py`](../scripts/check_render.py) le da qué mirar y por dónde empezar, todo en local:

```bash
uv run --with "scenedetect[opencv]" --with rapidocr --with onnxruntime \
  scripts/check_render.py out/video.mp4 --out out/review \
  --timeline animations/<proyecto>/timeline.json --expect rotulos.txt
```

- **Un fotograma por escena**, al final, cuando ya ha aparecido todo (de `timeline.json`, o detectando los planos con PySceneDetect si no lo hay), más uno cada 10 s, o cada 2 s si se buscan rótulos. Los guarda con los avisos marcados en rojo y en una hoja de contactos.
- **Texto en pantalla** con RapidOCR, que lee bien el español (tildes, «», ¿?), a medio segundo por fotograma en un Mac con Apple Silicon. Avisa de texto pegado al borde (¿cortado?), de letra de menos de unos 28 px en 1080p (la estima por la altura de la caja, que en Geist es de 1 a 1,2 veces la letra) y de lecturas dudosas.
- **Rótulos esperados** (`--expect`, uno por línea): cuáles no salen en ningún fotograma.
- **Tramos quietos** de 4 s o más (`freezedetect`): en un explicativo, lo primero que mirar si el ritmo cansa.

En el vídeo de RAG (6:42) tardó 2 minutos con 218 fotogramas. Encontró todos los rótulos menos uno inventado como control, dos tramos quietos de más de 6 s y un rótulo gris, tachado y en mono pequeña que se lee mal. No decide si algo se lee bien: el OCR siguió leyendo letra de 28 px con la imagen reducida a 360 px de ancho. Tampoco ve el movimiento ni el desfase entre rótulo y voz. Con PySceneDetect, el detector por defecto no vio ningún corte entre escenas oscuras parecidas; el adaptativo con umbral bajo, que es el que usa el script, los vio todos.

## Insertar clips en un vídeo ya aprobado

1. Corta la **imagen por fotogramas** en los límites de escena, con `trim=start_frame`, y concatena.
2. **Vuelve a mezclar el audio desde las pistas de voz**, cada una en su nuevo sitio (`adelay`), con la música continua. Si cortas el audio final, la música salta en cada unión.
3. Normaliza la mezcla y comprueba:
   - imagen: SSIM de varios tramos contra el original (se midió 0,998-0,999);
   - voz: correlación contra el original para calcular el desfase (se midió 0-1 ms);
   - original intacto: `shasum -a 256`.

## Esquemas: redibujar, no ampliar

Un fotograma de grabación a baja tasa de bits ampliado 1,5 veces se ve borroso, aunque en la toma parezca bien. Saca los datos de la fuente (en modo lectura) y dibuja SVG por capas: queda nítido y se puede animar.

- **Grafos muy conectados:** los algoritmos de fuerzas (`spring_layout`, ForceAtlas2) amontonaron el centro. Funcionó mejor una colocación propia: cada nodo de un grupo en espiral alrededor de su nodo principal.
- **Si la colocación no es la de la pantalla, dilo.** Los datos son reales, la disposición no.
- **Los datos extraídos**, fuera de git si son de una aplicación real.
- **Marcas sobre texto:** ponlas como capa encima del texto, siempre visible. Animar el texto marcado deja huecos antes de cada marca.

## Qué prueba cada comprobación

| Comprobación | Qué demuestra | Qué no demuestra |
|---|---|---|
| `hyperframes check` | Reglas de composición, texto legible | Que quede bien |
| `snapshot --at` o fotogramas sueltos | Lo que hay en ese instante | El movimiento, la fluidez |
| Transcripción | Las palabras | Cómo suenan |
| `ebur128`, `ffprobe` | Volumen, picos, duración | El balance voz-música |
| `duck_music.py` | Dónde la música queda cerca de la voz | Que la mezcla suene bien |
| SSIM, correlación, SHA | Que algo no cambió, o qué toma hay | Que sea bueno |
| `check_render.py` | Qué texto hay en cada escena, si toca el borde, si es pequeño, dónde se queda quieto | Que se lea bien en el móvil, el movimiento |

**Comprueba la propia comprobación.** Una correlación de 0,35 parecía un fallo; al cargar el audio entero en vez de recortarlo con `-ss` en cada intento, subió a 0,93-0,99. Añade un punto de control que deba dar bajo: una palabra ajena dio 0,10. Y mide antes de dar una cifra: un desfase de 33 ms venía de un redondeo propio.

## HyperFrames

- Para iterar: `snapshot --at 1,5,10` antes de renderizar. Es mucho más rápido que un render.
- Clips sueltos: una composición por clip, con su línea de tiempo GSAP pausada, y `check` en cada una.
- Renders en un Mac mini M4 con GPU: 8 min en unos 3 min; un clip de 52 s con normalización en 24 s.
