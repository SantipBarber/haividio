# Workflow 5 — Product demo: screen recording with a cloned voice

*[Español](05-product-demo.md)*

A 5–15-minute video about a real application: the screen is visible, a cursor points to what the voice is describing, and labels or diagrams explain what the screen does not show.

Tools: Playwright (recording), ElevenLabs (voice), ffmpeg (preparing the footage), and HyperFrames (compositing). Details in [cloned voice](../cloned-voice.en.md) and [editing and verification](../editing-and-verification.en.md).

## Work order

Each step closes out the previous one. Going back costs credits and time, especially if the voice has already been approved.

1. **Script by scene**, with narration separated from what is shown. Write for the ear: explain something once and do not force clarifications into the middle of a sentence.
2. **Choose the voice model and pronunciation** with short tests, before generating anything long.
3. **Rehearsal recording**, which does not write to any system, to check the steps and timing.
4. **Full voice-over** once the script is finalized. Check the text against a transcript and have a person listen to it.
5. **Timing for the recording:** use the voice-over to determine how long the cursor should stay at each point.
6. **Draft** with the rehearsal recording. Label anything that is not real on screen.
7. **Real recording**, once, and **final version** using it.
8. **Review list** with the timestamps to check (template in `videos/_template/REVIEW.md`).

## The screen recording

- **Playwright does not record the system cursor.** Draw it in the page as a fixed element and move it along a smooth curve, always at the same speed (0.6 s per movement worked well).
- **Capture with CDP instead of Playwright's recorder.** `Page.startScreencast` and one frame per n/30 keep small text sharper: SSIM was 0.971–0.990 with the recorder compared to a direct capture. Each frame must land at its actual timestamp; otherwise, the recording gradually drifts from the markers (0.4 s by the end was measured).
- **Keep a JSON of markers alongside the video:** when the cursor leaves and reaches each point, and when each wait starts and ends. Precise synchronization is not possible without these markers.
- **Record the screen at 1×.** Do not speed up or cut anything during recording: that is editing work.
- **Use synthetic data** whenever possible, and check what is readable on screen before showing it to anyone.
- **If the recording writes to a real system, a person runs it once.** There are two intentional modes: rehearsal (rejects writes) and real (approves them). Record the expected result and check it; if it fails after writing, do not run it again without reviewing. If a permission control blocks it, ask the person to decide rather than looking for another way around it.
- **Other heavy processes affect what is visible:** one read took more than twice as long while the machine was busy with the capture. Stop them before the real recording.

## What works on screen

- **What you explain must be visible.** If the voice says something was approved, show it approved and created in the destination system.
- **A fixed starting point.** Return to the same map or menu before each section to make the walkthrough easier to follow. If it gets long, shorten those openings first.
- **No gaps in the voice-over.** About 7–8 minutes without long silences works better than a shorter video with waits. Trim app waits from the footage and add the label «espera recortada» ("wait trimmed"); do not pause the voice-over.
- **The cursor must not cover what it points to:** place it below the word or number. It arrives about 0.3 s before it is mentioned.
- **Redraw diagrams using real data**, rather than enlarging a frame: see [redraw diagrams, don't enlarge](../editing-and-verification.en.md#diagrams-redraw-do-not-enlarge).
- **Cite figures and their scope.** If you show a bar, the label says what was measured and across how many cases.
- **Mark invented examples as such** («Correo de ejemplo», “Example email”).

## Two versions of the same video

A short version for people who just want to see it work and a longer training version can come from the same edit. The training version should include non-obvious details: how it was made internally and what is planned for improvement. Ask the audience what they want to learn more about and leave out the obvious.

1. Create standalone technical clips (animated diagrams with the same voice and visual identity) and approve them separately.
2. Insert them by cutting the approved video's picture frame by frame and **mixing the audio again from the voice tracks**, so the music does not jump at the joins.
3. Leave the short video untouched: verify with its SHA that nothing has changed.

Estimate the script using the actual speaking pace, not a general figure: one estimate of about 12 minutes ended up at 13:22. Compare the duration with the session time and have the short version ready in case it is cut down.

## Coordinate multiple sessions

This worked with several Claude sessions (app and recording, voice and editing, coordination):

- **One script**, in the app repository, with a fixed reference (`git show <commit>:script.md`): the local copy may be behind.
- **One session leads** and the others propose changes. Handoff notes with status, decisions, and what not to reopen prevent repeated discussions.
- **Freeze an approved video:** no one changes the voice or edit unless the person who approved it asks.
- **Before a heavy render**, check that no other measurement is running on the same machine.
