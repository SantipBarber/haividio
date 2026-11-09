---
name: publish-youtube
description: Prepares and uploads a video to YouTube - title, description with chapters, tags, thumbnail and upload as private or unlisted with the youtubeuploader CLI (YouTube Data API v3). Use it when a video is finished or the user asks to publish. Also when the user writes in Spanish, e.g. "súbelo a YouTube", "publica el vídeo", "prepara el título y la descripción", "capítulos del vídeo".
---

# Publish to YouTube

Reply in the user's language. Title, description and tags go in the video's language.

## Prepare (`publishing.md`)

- **Title:** ≤ 60 characters, a clear promise, no misleading clickbait. Propose 3 options.
- **Description:** 2 hook lines, summary, chapters (`00:00 Intro`…) taken from the script or the transcript, sources and links.
- **Tags:** 5–10 relevant ones.
- **Thumbnail:** 1280×720, at most 4 words, with the channel's visual identity (skill `visual-identity`).

## Upload

1. Check that `youtubeuploader -version` works and that the credentials exist outside the repository (`~/.config/youtubeuploader/`). If not, guide the setup with `docs/workflows/04-publish-youtube.md`.
2. Prepare `publishing.json` (title, description with chapters, tags, language) from `publishing.md`.
3. **Ask for explicit confirmation** before uploading.
4. Upload with `-privacy private` (or `unlisted` if asked), with `-thumbnail` and `-caption` if available. Never straight to public.
5. Return the link and ask the user to review it in YouTube Studio: check the visibility (an unaudited project may leave it private and locked) and declare synthetic content if there is a cloned voice.

## When done

Write down the link and the date in the video's `README.md` and in the index `videos/README.md`.
