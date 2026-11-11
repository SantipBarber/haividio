---
name: publish-youtube
description: Prepares and uploads a video to YouTube - review of what is on screen, title, description with chapters, tags, thumbnail, validation against YouTube's rules and upload as private or unlisted with the youtubeuploader CLI (YouTube Data API v3). Use it when a video is finished or the user asks to publish it or share it by link. Also when the user writes in Spanish, e.g. "súbelo a YouTube", "publica el vídeo", "prepara el título y la descripción", "capítulos del vídeo", "quiero mandar el vídeo por enlace".
---

# Publish to YouTube

Reply in the user's language. Title, description and tags go in the video's language. Full guide: `docs/workflows/04-publish-youtube.md`.

## Rules

- **Never public.** Private to review it; unlisted to send the link to someone. An unlisted link gets forwarded without control: treat it as public.
- **Nothing is uploaded without the user's explicit OK**, after they have seen the metadata and what the review flagged.
- Credentials and token stay outside the repo (`~/.config/youtubeuploader/`).

## 1. Review what is on screen

Go through the frames (a contact sheet or the whole video), on-screen text and the voice-over. Flag real personal data (names, emails, phones, IDs), real client amounts or business data, data of another client, and keys, tokens, personal paths or internal URLs. Made-up demo data is fine. If something must not show, propose recording or rendering again with other data; do not blur it.

## 2. Prepare (`publishing.md`)

- **Title:** a clear promise, no misleading clickbait; aim for ≤ 60 characters (YouTube allows 100). Propose 3 options.
- **Description:** 2 hook lines, summary, chapters (`0:00 Intro`…), sources and links. Generate the chapter lines with `python3 scripts/make_captions.py chapters --timeline timeline.json chapters.json` when there is a HyperFrames timeline; otherwise take them from the script or the transcript. Chapters: the first at 0:00, at least 3, each ≥ 10 s; if the video is too short for that, no chapters.
- **Tags:** 5–10 relevant ones.
- **Thumbnail:** 16:9, 1280×720 or more (YouTube now recommends 3840×2160), at most 4 words, with the channel's visual identity (skill `visual-identity`). Run `python3 scripts/check_publishing.py thumb thumbnail.png --preview thumbnail-mobile.png` and look at the preview: it is the size it has on a phone.
- **Subtitles:** `python3 scripts/make_captions.py srt --hyperframes index.html --words-dir <folder of the .words.json> -o subtitles.srt` builds them from the voice's word timings, with the script's text (add `--pron` if there is a pronunciation map).
- **Declarations:** made for kids (normally no) and synthetic content (yes if there is a cloned voice or realistic AI-generated content).

## 3. Validate

Write `publishing.json` (title, description, tags, `privacyStatus`, `madeForKids`, `containsSyntheticMedia`, `categoryId`, `language`; example in the guide) and run:

```bash
python3 scripts/check_publishing.py meta publishing.json video.mp4
```

Fix what it flags and repeat until ✔.

## 4. Upload

1. Check that `youtubeuploader -version` works and that the credentials exist. If not, guide the setup with the guide, including publishing the OAuth app (in testing mode the token expires after 7 days).
2. Show the metadata and the review findings and **ask for explicit confirmation**.
3. Upload with `-metaJSON publishing.json -metaJSONout upload-result.json -notify=false`, plus `-thumbnail` and `-caption` if available. Custom thumbnails need a phone-verified channel: if YouTube answers 403 for the thumbnail, youtubeuploader stops before the subtitles, so add them afterwards (Studio or `captions.insert`).
4. Run `python3 scripts/check_publishing.py result upload-result.json --expect <private|unlisted>`. If YouTube left it with another visibility (unaudited project), say so and do not hand out the link.
5. Return the link and ask the user to review it in YouTube Studio.

Without API access, hand over the mp4, the `.srt` and the metadata with the guide's steps for uploading by hand through Studio.

## When done

Write down the link and the date in the video's `README.md` and in the index `videos/README.md`. Do not commit `upload-result.json`.
