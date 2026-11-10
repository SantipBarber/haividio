# Workflow 4 — Publishing to YouTube

*[Español](04-publish-youtube.md)*

Tool: [youtubeuploader](https://github.com/porjo/youtubeuploader) (Apache-2.0, YouTube Data API v3). It is a CLI, so any agent can use it without configuration. There are versions for Mac, Windows, and Linux. It uploads as **private** by default, or as unlisted, with a thumbnail, SRT subtitles, playlist, and title, description, tags, and declarations (made for kids, synthetic content) in a JSON file.

Alternative if you prefer an MCP: [youtube-uploader-mcp](https://github.com/anwerj/youtube-uploader-mcp) (MIT). It does the same and can also change the visibility of an uploaded video. It has fewer users: review the code before giving it access to your channel.

## Install

| Mac | Windows |
|---|---|
| `brew install youtubeuploader` | Download `youtubeuploader_<versión>_Windows_amd64.zip` from [its releases](https://github.com/porjo/youtubeuploader/releases), unzip it, and add the folder to PATH. It is not on winget |

## Configure (once)

1. In Google Cloud Console: create a project and enable **YouTube Data API v3**.
2. Configure the OAuth consent screen (external type) and add your account as a test user.
3. Create credentials: **OAuth client ID**, type **web application**, with the redirect URI `http://localhost:8080/oauth2callback`.
4. Download the JSON and save it **outside the repository**, for example at `~/.config/youtubeuploader/client_secrets.json` (on Windows, `%APPDATA%\youtubeuploader\`).
5. The first upload opens a browser to authorize the channel and saves the permission in the file specified with `-cache`. Save that file outside the repository too.
6. **Publish the app** on the consent screen (status **In production**). Google does not need to verify it. While it is **in testing**, Google expires the permission after 7 days and you have to authorize again every week. When authorizing an unverified app you get a warning: **Advanced** → **Go to … (unsafe)**, with the channel's account.

The credentials and token grant access to your channel: never put them in git.

**If the permission stops working** (refreshing the token fails because it was revoked or the account password changed): delete the `-cache` file and the next upload asks for authorization again. Access is revoked from the channel's Google account, under **Security** → **Third-party connections**.

## Private or unlisted

- **Private:** only people you invite, one by one, with their Google account can see it. Use it to review the video before publishing.
- **Unlisted:** it does not appear on the channel or in search, but anyone with the link can see it. Use it to send the video to someone specific.

An unlisted link gets forwarded without control: when reviewing what is on screen, treat it as public.

## Before uploading: what is on screen

Review the frames (a contact sheet or the whole video), the on-screen text, and the voice-over. It must not show:

- personal data of real people: names, emails, phone numbers, ID documents;
- real amounts or business data of a client, or data of another client;
- keys, tokens, personal paths, or internal URLs in a terminal or browser.

Made-up demo data is fine. If something shows that should not, record or render again with other data: a blur slips through in some frame.

## Upload

`publishing.json` contains the title, description with chapters, tags, language, the declarations, and, if you want to schedule it, the publication date (`publishAt`). Full format in the [tool README](https://github.com/porjo/youtubeuploader#metadata).

```json
{
  "title": "Cómo funciona RAG en 2026",
  "description": "Dos frases de gancho.\n\nCapítulos:\n00:00 Intro\n00:20 El problema\n00:50 RAG clásico",
  "tags": ["RAG", "IA", "LLM"],
  "privacyStatus": "private",
  "madeForKids": false,
  "containsSyntheticMedia": true,
  "categoryId": "27",
  "language": "es"
}
```

`containsSyntheticMedia` is `true` if there is a cloned voice or other realistic AI-generated content. Category 27 is Education; 28, Science & Technology.

1. **Validate the metadata** against YouTube's rules and the actual video:

   ```bash
   python3 scripts/check_publishing.py meta publishing.json video.mp4
   ```

   It checks that the video can be read in full; the title (one line, at most 100 characters) and description (5000 bytes), without `<` or `>`, which YouTube rejects; the tags (500 characters in total); the chapters (the first at 0:00, at least 3, in order and 10 s or longer, or YouTube does not show them); that visibility is not public; and that both declarations are present. Fix what it flags and repeat until ✔.

2. **Upload**, with explicit confirmation:

   ```bash
   Y=~/.config/youtubeuploader
   youtubeuploader \
     -secrets $Y/client_secrets.json -cache $Y/request.token \
     -filename video.mp4 \
     -metaJSON publishing.json \
     -metaJSONout upload-result.json \
     -thumbnail miniatura.png \
     -caption subtitles.srt \
     -notify=false
   ```

   `-notify=false` does not notify subscribers, because the video is not public yet. Visibility comes from `privacyStatus` in the JSON.

   **Custom thumbnail:** it only works once the channel is phone-verified ([youtube.com/verify](https://www.youtube.com/verify)). Otherwise YouTube answers `403 … permissions to upload and set custom video thumbnails` and youtubeuploader **stops there: it does not upload the subtitles either**, although the video is already uploaded. Verify the channel first, or drop `-thumbnail` and add it later in Studio.

3. **Check the visibility** with YouTube's response:

   ```bash
   python3 scripts/check_publishing.py result upload-result.json --expect private   # or unlisted
   ```

   If it does not match, do not share the link (see the next section).

**Never publish directly.** Upload as private or unlisted and review it in YouTube Studio before publishing it.

## Warning: unaudited projects

According to the `videos.insert` reference, videos uploaded through the API from an **unaudited** Google Cloud project (created after 2020-07-28) remain **private**, and YouTube's help says their visibility cannot be changed: they would need to be uploaded again through Studio or the API audit requested, which is free. A November 2026 source says Google lifted this restriction in October ([issue](https://github.com/porjo/youtubeuploader/issues/86)). Our test confirms it: on 2026-11-10, a newly created, unaudited project uploaded one video as unlisted and another as public, and both kept that visibility.

Before your first real video, **upload a short test video as unlisted** and check the result with `check_publishing.py result … --expect unlisted` and in Studio:

- If it remains unlisted: the tool works for the whole workflow.
- If it is private and locked: use the API only for videos that should remain private, and upload the rest by hand through Studio. Or request the audit.

## Uploading by hand through Studio

If there is no API access, with the metadata already validated, go to [studio.youtube.com](https://studio.youtube.com) with the channel's account:

1. **Create** → **Upload videos** → the mp4.
2. **Details:** title and description from the metadata, thumbnail, and **No, it's not made for kids**. Under **Show more**, altered or synthetic content, if any.
3. **Video elements** → **Subtitles:** the `.srt`, with its language.
4. **Visibility:** **Private** or **Unlisted** → **Save**.

## Pre-publication checklist

- [ ] Reviewed what is on screen: no data that should not show
- [ ] Title and description reviewed (`videos/<folder>/publishing.md`)
- [ ] `check_publishing.py meta` shows ✔
- [ ] Final thumbnail
- [ ] Subtitles uploaded or burned in
- [ ] Chapters (timestamps) in the description
- [ ] Synthetic content disclosed, if applicable
- [ ] `check_publishing.py result` shows the requested visibility
- [ ] Santi's explicit confirmation to make it public
