# Voz clonada con ElevenLabs: lo que hemos medido

Datos de noviembre de 2026, de un solo proyecto en español con una voz de clonación instantánea. Precios y modelos cambian: verifica antes de fiarte.

## Lo primero: Claude no puede oír

Ninguna medida sustituye a oírlo. Una transcripción dice si **las palabras** son las del guion, pero no cómo suenan.

| Comprobación | Sirve para | No sirve para |
|---|---|---|
| Transcripción contra el guion: [`scripts/check_voice.py`](../scripts/check_voice.py) (WhisperX, local y gratis) o Scribe | Palabras cambiadas, perdidas o que se entienden mal («Medí acierto» salía «Medía cierto»; se arregló cambiando el texto) | Acento: normaliza y escribe «API» o «Odoo» se digan como se digan. Avisa, eso sí, de una sigla escrita como palabra («Api») que dura demasiado y parece deletreada. Tampoco ve un corte limpio dentro de una palabra |
| Duración y nivel de cada palabra | Palabras truncadas, tiempos raros | Saber si una pronunciación es buena: 5 apariciones mal dichas no se distinguían de las otras 15 |
| Correlación contra la toma aprobada | Saber que la toma elegida es la que acabó en el vídeo | Juzgar si esa toma suena bien |
| Oído de una persona | Todo lo demás | — |

Por eso cada entrega lleva una lista de minutos para escuchar, y se dice con claridad qué no se ha oído.

## Elegir modelo

Comparar variantes con el **mismo texto** y que elija quien conoce la voz. Con 525 caracteres:

| Modelo | Palabras/min | Pausa máxima | Nota |
|---|---:|---:|---|
| `eleven_multilingual_v2` | 204 | 0,18 s | Sonó «un poco a robot» |
| v2 con `previous_text` y `next_text` | 175 | 0,6 s | |
| `eleven_v3` | 209 | — | Sin `<break>` |
| `eleven_v4` | 173 | 0,56 s | Elegido: el más real y parecido a la voz. Sin `<break>` |

- Todos costaron lo mismo: 210 créditos, también con contexto. La cabecera `character-cost` marcó 0,40 créditos por carácter, frente a 1 en las webs de precios: mira el panel.
- `GET /v1/models` dice qué modelos hay. v3 y v4 devuelven tiempos por carácter en `with-timestamps`.
- Calcula la duración con el ritmo medido de tu voz y tu modelo, no con las 140 palabras/min de siempre.
- Con v3 y v4, las pausas se añaden en el montaje: son gratis y no cambian lo aprobado.

## Clonación

- **Instantánea:** con 1:52 grabados y limpiados sonó natural (`highpass=70,afftdn=nr=18,loudnorm=TP=-3`).
- **Profesional:** plan Creator o superior, 30 minutos de audio como mínimo (recomiendan 1 hora o más), verificación y de 3 a 24 horas de entrenamiento, más cola. No sirve si quedan pocos días.

## Claves y créditos

- Una clave puede tener **su propio tope**, aparte del saldo. Al agotarlo responde `401 quota_exceeded`, que parece un fallo de autenticación: lee el cuerpo del error.
- Sin permiso `user_read`, la clave no lee el saldo. Suma `character-cost` y di que es un cálculo.
- Claves e ID de voz, en `.env`.

## Generar con tiempos por palabra

`POST /v1/text-to-speech/{voice}/with-timestamps` devuelve el audio y el tiempo de cada carácter; agrupados, dan el instante de cada palabra sin alineación aparte.

```python
words, cur = [], None
for c, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
    if c.isspace():
        if cur: words.append(cur); cur = None
    elif cur is None: cur = {"w": c, "start": s, "end": e}
    else: cur["w"] += c; cur["end"] = e
if cur: words.append(cur)
```

Guarda `{"text", "duration", "words"}` en un `.words.json` junto al mp3. Es lo que usa [`scripts/splice_voice.py`](../scripts/splice_voice.py).

## Pronunciación

**El guion no se toca.** Las grafías van en un mapa que solo se aplica al texto enviado a la voz, con excepciones por frase si hace falta. Si la frase de una excepción ya no aparece, el script debe parar antes de gastar créditos.

Lo que eligió de oído un hablante de español de España, como punto de partida y no como regla:

| En pantalla | A la voz | Nota |
|---|---|---|
| Odoo | Odú | |
| IA | í-a | No siempre: en dos frases sonó «I» y hubo que elegir por frase |
| API | Api | Como palabra, no letra a letra. Ganó de oído a la IPA (`/ˈapi/`), pero de tres tomas una salió deletreada: `check_voice.py` lo avisa |
| OCR | oce erre | «ocerre» no valió |
| CIF | zif | |
| NIF, IBAN | sin cambios | Con `language_code: es` no se deletrean |

**Lo que aprendimos, y costó créditos:**

1. **La misma grafía no garantiza el mismo sonido.** La voz cambia en cada generación y según la frase. De dos tomas con el mismo texto, se aprobó una y se rechazó la otra.
2. **Lo que se aprueba es la toma, no la grafía.** Una vez aprobada, se conserva el audio.
3. **Prueba en la frase real**, no en una muestra suelta. Genera 2 o 3 variantes de la frase que falla y que se elija de oído.
4. **Una palabra que se repite puede sonar distinta cada vez.** Tres frases generadas con la misma grafía sonaron diferentes, y el oyente lo notó más que cualquier fallo aislado. La solución es cortar una sola toma y pegarla en todas.

## Empalmar en vez de regenerar

Regenerar una escena cambia todo lo ya aprobado. [`scripts/splice_voice.py`](../scripts/splice_voice.py) sustituye solo lo necesario, sin gastar créditos:

```bash
# Una frase entera
scripts/splice_voice.py phrase audio/scene-3 audio/approved-take "Tardó unos" "cargada."
# Las mismas palabras de una toma, en varias frases
scripts/splice_voice.py word audio/scene-3 audio/approved-take "por api" all
```

- **Incluye la palabra anterior** si la palabra se pega a ella: en «por api», cortar antes de «por» cayó en silencio y cortar entre «por» y «api» no.
- **Límite:** una toma que venía seguida de coma, pegada al final de una frase, puede sonar en suspenso. Si molesta, se pide una toma con punto solo para esa frase.
- **Copia antes de empalmar.** Un primer intento dejó una escena con una sola frase, y solo se vio al compararla con el guion.
- **Comprueba** que la duración del `.words.json` coincide con la del mp3 (`ffprobe`), y que la toma está donde dicen los tiempos.
