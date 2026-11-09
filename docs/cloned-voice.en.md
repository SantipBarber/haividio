# Cloned voice with ElevenLabs: what we measured

*[Español](cloned-voice.md)*

Data from November 2026, from a single Spanish-language project using an Instant Voice Clone. Prices and models change: check before relying on them.

## First: Claude cannot hear

No measurement can replace listening. A transcript tells you whether **the words** match the script, but not how they sound.

| Check | What it can tell you | What it cannot tell you |
|---|---|---|
| Transcript against the script: [`scripts/check_voice.py`](../scripts/check_voice.py) (WhisperX, local and free) or Scribe | Changed, missing or misunderstood words («Medí acierto» was transcribed as «Medía cierto»; this was fixed by changing the text) | Accent: it normalizes and writes «API» or «Odoo» however they are pronounced. It does warn when an acronym written as a word («Api») lasts too long and sounds spelled out. It also cannot detect a clean cut inside a word |
| Duration and level of each word | Truncated words, unusual timings | Whether a pronunciation is good: 5 mispronounced instances were indistinguishable from the other 15 |
| Correlation against the approved take | Whether the selected take is the one that ended up in the video | Whether the take sounds good |
| A person listening | Everything else | — |

That is why every delivery includes a list of timestamps to listen to, and clearly states what has not been heard.

## Choosing a model

Compare variants with the **same text** and let someone who knows the voice choose. With 525 characters:

| Model | Words/min | Maximum pause | Note |
|---|---:|---:|---|
| `eleven_multilingual_v2` | 204 | 0.18 s | Sounded «un poco a robot» (a bit robotic) |
| v2 with `previous_text` and `next_text` | 175 | 0.6 s | |
| `eleven_v3` | 209 | — | No `<break>` |
| `eleven_v4` | 173 | 0.56 s | Chosen: most natural and closest to the voice. No `<break>` |

- They all cost the same: 210 credits, including with context. The `character-cost` header showed 0.40 credits per character, compared with 1 on the pricing pages: check the dashboard.
- `GET /v1/models` lists available models. v3 and v4 return per-character timings through `with-timestamps`.
- Estimate duration using the measured rate of your voice and model, not the usual 140 words/minute.
- With v3 and v4, pauses are added in the edit: they are free and do not change the approved take.

## Cloning

- **Instant:** 1:52 of recorded and cleaned audio sounded natural (`highpass=70,afftdn=nr=18,loudnorm=TP=-3`).
- **Professional:** Creator plan or higher, at least 30 minutes of audio (1 hour or more recommended), verification, and 3 to 24 hours of training, plus queue time. Not suitable if you only have a few days left.

## Keys and credits

- A key can have **its own limit**, separate from the balance. Once it is reached, the API returns `401 quota_exceeded`, which looks like an authentication failure: read the error body.
- Without `user_read` permission, the key cannot read the balance. Add up `character-cost` and say that it is an estimate.
- Keep keys and voice IDs in `.env`.

## Generate with word timings

`POST /v1/text-to-speech/{voice}/with-timestamps` returns the audio and the timing of each character; grouped together, they give the time of each word without separate alignment.

```python
words, cur = [], None
for c, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
    if c.isspace():
        if cur: words.append(cur); cur = None
    elif cur is None: cur = {"w": c, "start": s, "end": e}
    else: cur["w"] += c; cur["end"] = e
if cur: words.append(cur)
```

Save `{"text", "duration", "words"}` in a `.words.json` file next to the mp3. [`scripts/splice_voice.py`](../scripts/splice_voice.py) uses it.

## Pronunciation

**Do not change the script.** Put spellings in a map applied only to the text sent to the voice, with per-sentence exceptions if needed. If an exception's sentence no longer appears, the script should stop before spending credits.

What a speaker from Spain chose by ear, as a starting point rather than a rule:

| On screen | Spoken as | Note |
|---|---|---|
| Odoo | Odú | |
| IA | í-a | Not always: in two sentences it sounded like «I», so the choice had to be made per sentence |
| API | Api | As a word, not letter by letter. It sounded better by ear than the IPA (`/ˈapi/`), but one of three takes spelled it out: `check_voice.py` warns about this |
| OCR | oce erre | «ocerre» did not work |
| CIF | zif | |
| NIF, IBAN | unchanged | With `language_code: es`, they are not spelled out |

**What we learned, at the cost of credits:**

1. **The same spelling does not guarantee the same sound.** The voice changes with each generation and depending on the sentence. Of two takes with the same text, one was approved and the other rejected.
2. **The take is approved, not the spelling.** Once approved, keep the audio.
3. **Test it in the actual sentence**, not in an isolated sample. Generate 2 or 3 variants of the sentence that fails and let someone choose by ear.
4. **A repeated word can sound different each time.** Three sentences generated with the same spelling sounded different, and the listener noticed more than any isolated error. The solution is to cut one take and paste it into each instance.

## Splice instead of regenerating

Regenerating a scene changes everything already approved. [`scripts/splice_voice.py`](../scripts/splice_voice.py) replaces only what is needed, without spending credits:

```bash
# An entire phrase
scripts/splice_voice.py phrase audio/scene-3 audio/approved-take "Tardó unos" "cargada."
# The same words from one take in several sentences
scripts/splice_voice.py word audio/scene-3 audio/approved-take "por api" all
```

- **Include the previous word** if it runs into the target word: in «por api», cutting before «por» landed in silence, while cutting between «por» and «api» did not.
- **Limit:** a take that continues after a comma and is attached to the end of a sentence can sound unfinished. If it is distracting, request a take with a full stop for that sentence only.
- **Copy before splicing.** A first attempt left a scene with only one sentence; this was only noticed when it was compared with the script.
- **Check** that the `.words.json` duration matches the mp3 duration (`ffprobe`), and that the take is where the timings say it is.
