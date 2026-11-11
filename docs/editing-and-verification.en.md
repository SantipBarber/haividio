# Editing with voice timings and verification

*[Español](editing-and-verification.md)*

Techniques tested while editing a product demo with a cloned voice. The complete workflow is in [workflow 5](workflows/05-product-demo.en.md).

## ffmpeg + HyperFrames

| | Quality | Problem |
|---|---|---|
| ffmpeg only | Clean cuts, static titles | No smooth zooms. Homebrew's ffmpeg may not include `drawtext` |
| HyperFrames only | Best | Not a good place to trim waits: every adjustment changes the composition |
| **ffmpeg + HyperFrames** | Best, with quick adjustments | The video has to be prepared for HyperFrames |

ffmpeg prepares one «plate» per scene (mp4 at 1080p30, `-g 30`, `crf` 16), and HyperFrames composes over it using `<video muted>`. **One keyframe per second is what prevents freezes when seeking.** Tested: 1:13 renders in 52 s with GPU.

## Sync: the voice leads

- **Never speed up cursor movement.** Adjust only the idle time between two points: trim it if there is too much, freeze it if there is too little (`tpad=stop_mode=clone`). This is much less noticeable than `setpts`.
- **Pair each cursor point with a word** in a «beats» file. Use that and the take's timestamps to calculate each segment. Quantize against cumulative time to prevent drift.
- **Add pauses in the edit**, without spending credits: at the end of a sentence, at the end of a paragraph, and a maximum for pauses already in the voice.

### Search for phrases, not words

This error ruined the most scenes:

- The first occurrence of a standalone word («Es», «Para») shifted entire scenes together.
- A title tied to a repeated word appeared 10 s too early.
- A pause tied to a word applied to every occurrence and added 3 s in the middle of another sentence.

Search for an exact phrase, including capitalization, and **fail if it appears more than once**, unless a specific occurrence is given:

```python
def t(self, phrase, n=None):
    norm = lambda s: re.sub(r"[^\wáéíóúüñÁÉÍÓÚ-]", "", s)
    toks, ws = [norm(x) for x in phrase.split()], [norm(w["w"]) for w in self.words]
    hits = [i for i in range(len(ws) - len(toks) + 1) if ws[i:i + len(toks)] == toks]
    if not hits or (n is None and len(hits) > 1) or (n and len(hits) < n):
        raise SystemExit(f"«{phrase}» aparece {len(hits)} veces (n={n})")
    return self.words[hits[(n or 1) - 1]]["start"]
```

Checking that beats are in order does not prove they land in the right place: inspect the frame at that timestamp.

## Audio cuts without glitches

- **The midpoint between two words is not always silence.** 9 of 99 cuts landed in the middle of speech (−15 to −32 dB) and were audible. Find the lowest level within ±90 ms and crossfade 15 ms on each side.
- **The voice does not always stop after «:» or a comma:** 18 cuts in the middle of speech were there, almost all after colons.
- **After editing, measure:** `silencedetect` for long silences (−35 dB, 0.6 s) and [`scripts/detect_glitches.py`](../scripts/detect_glitches.py) for clicks and short gaps. They provide candidates, not verdicts.
- **Also compare with the script:** [`scripts/check_voice.py`](../scripts/check_voice.py) transcribes the final video with WhisperX and lists missing, changed or added words with their timestamps. On an 8-minute video with music, it took 3 minutes on an Apple Silicon Mac and produced 3 warnings to listen to; it lists numbers separately («veinte» versus «20»). It also saves the actual timestamp of each word, for checking titles.
- **What neither detects:** a clean 150 ms cut inside a word. In the test it caused no click or gap, and the transcript was unchanged. Comparing word duration does not work either: after a pause, the aligner can shift the start of a word by up to 0.3 s in an unedited copy.

## Mix and volume

- Keep music very low under the voice: 0.07 in a demo, 0.14 in an animated explainer. Use your ears. A transcript may have more trouble recognizing a proper name when there is music: treat that as a cue to listen.
- **Ducking:** [`scripts/duck_music.py`](../scripts/duck_music.py) lowers the music only while there is voice (ffmpeg's `sidechaincompress`, with the voice as the control signal) and measures, in half-second windows, how many dB the music sits below the voice, before and after. It reads the voice clips from the HyperFrames root composition:

```bash
uv run --with numpy scripts/duck_music.py --music assets/music/bed.mp3 \
  --hyperframes index.html --volume 0.25 --out assets/music/bed-ducked.mp3
```

  Then point the music `<audio>` at `bed-ducked.mp3`. Since the music already dips under the voice, it can take more volume (`data-volume`) and fill the pauses. In the RAG video, with a fixed volume of 0.14, the music sat only 13 dB below the voice (median); with ducking at 0.25, 23 dB, and it was 5 dB louder in the pauses. The stretches it flags, below `--min-gap` (15 dB by default, to be calibrated), are the first thing to listen to. It measures RMS, not LUFS: it does not decide whether it sounds good.
- If a track is too short, loop it into itself (`acrossfade=d=6`).
- Normalize in two passes with `loudnorm` to −14 LUFS and TP −1.5, and copy the video if it has not changed:

```bash
ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -    # measure
ffmpeg -i in.mp4 -c:v copy -c:a aac -b:a 192k -movflags +faststart \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=…:measured_TP=…:measured_LRA=…:measured_thresh=…:offset=…:linear=true,aresample=44100" out.mp4
ffmpeg -i out.mp4 -af ebur128=peak=true -f null -    # verify
```

- When reading that JSON from a script, extract the text between the first and last brace: ffmpeg writes more text after it.
- In zsh, `"$var:linear"` applies the `:l` modifier. Write `${var}:linear` instead.

## Visual review of the render

The agent does not see the video moving. [`scripts/check_render.py`](../scripts/check_render.py) gives it something to look at and a place to start, all locally:

```bash
uv run --with "scenedetect[opencv]" --with rapidocr --with onnxruntime \
  scripts/check_render.py out/video.mp4 --out out/review \
  --timeline animations/<project>/timeline.json --expect labels.txt
```

- **One frame per scene**, at its end, once everything has appeared (from `timeline.json`, or by detecting shots with PySceneDetect when there is none), plus one every 10 s, or every 2 s when looking for labels. It saves them with the warnings marked in red, and a contact sheet.
- **On-screen text** with RapidOCR, which reads Spanish well (accents, «», ¿?), at half a second per frame on an Apple Silicon Mac. It flags text touching the edge (cut off?), type under about 28 px at 1080p (estimated from the box height, which in Geist is 1 to 1.2 times the type size) and doubtful readings.
- **Expected labels** (`--expect`, one per line): which ones do not appear in any frame. A label over several lines counts if its words appear in order in the same frame, even when OCR reads another column in between; so a label made of words already on screen may be taken as found.
- **Still stretches** of 4 s or more (`freezedetect`): in an explainer, the first thing to look at if the pace drags.

On the RAG video (6:42) it took 2 minutes for 218 frames. It found every label except one made up as a control, two still stretches over 6 s, and a grey, struck-through, small mono label that is hard to read. It does not decide whether something reads well: OCR still read 28 px type with the frame scaled down to 360 px wide. Nor does it see motion or the offset between a label and the voice. With PySceneDetect, the default detector found no cut between similar dark scenes; the adaptive one with a low threshold, which the script uses, found them all.

## Insert clips into an already approved video

1. Cut the **picture by frame** at scene boundaries using `trim=start_frame`, then concatenate.
2. **Mix the audio again from the voice tracks**, each in its new position (`adelay`), with continuous music. If you cut the final audio, the music jumps at every join.
3. Normalize the mix and check:
   - picture: SSIM for several sections against the original (measured 0.998–0.999);
   - voice: correlation against the original to calculate the offset (measured 0–1 ms);
   - original unchanged: `shasum -a 256`.

## Diagrams: redraw, do not enlarge

A frame from a low-bitrate recording enlarged 1.5 times looks blurry, even if it seems fine in the take. Extract the data from the source (read-only) and draw layered SVG: it stays sharp and can be animated.

- **Highly connected graphs:** force-directed algorithms (`spring_layout`, ForceAtlas2) crowded the center. A custom layout worked better: place each node in a group in a spiral around its main node.
- **If the layout does not match the screen, say so.** The data is real; the arrangement is not.
- Keep **extracted data** outside git if it comes from a real application.
- **Marks on text:** put them on a layer above the text, always visible. Animating highlighted text leaves gaps before each mark.

## What each check proves

| Check | What it proves | What it does not prove |
|---|---|---|
| `hyperframes check` | Composition rules, readable text | That it looks good |
| `snapshot --at` or individual frames | What is there at that moment | The motion, the smoothness |
| Transcript | The words | How they sound |
| `ebur128`, `ffprobe` | Volume, peaks, duration | The voice/music balance |
| `duck_music.py` | Where the music gets close to the voice | That the mix sounds good |
| SSIM, correlation, SHA | That something did not change, or which take is present | That it is good |
| `check_render.py` | What text each scene shows, whether it touches the edge, whether it is small, where the picture stays still | That it reads well on a phone, motion |

**Check the check itself.** A correlation of 0.35 looked like a failure; loading the whole audio instead of trimming with `-ss` on every attempt brought it up to 0.93–0.99. Add a control that should score low: an unrelated word scored 0.10. And measure before reporting a number: a 33 ms offset came from our own rounding.

## HyperFrames

- To iterate: use `snapshot --at 1,5,10` before rendering. It is much faster than a render.
- Individual clips: one composition per clip, with its GSAP timeline paused, and run `check` on each one.
- Renders on a Mac mini M4 with GPU: 8 minutes in about 3 minutes; a 52-second clip with normalization in 24 seconds.
