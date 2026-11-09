# Workflow 4 — Publishing to YouTube

*[Español](04-publish-youtube.md)*

Tool: [youtubeuploader](https://github.com/porjo/youtubeuploader) (Apache-2.0, YouTube Data API v3). It is a CLI, so any agent can use it without configuration. There are versions for Mac, Windows, and Linux. It uploads as **private** by default, or as unlisted, with a thumbnail, SRT subtitles, playlist, and title, description, and tags in a JSON file.

Alternative if you prefer an MCP: [youtube-uploader-mcp](https://github.com/anwerj/youtube-uploader-mcp) (MIT). It does the same, can change the visibility of an uploaded video, and lets you mark content as altered or synthetic. It has fewer users: review the code before giving it access to your channel.

## Install

| Mac | Windows |
|---|---|
| `brew install youtubeuploader` | Download `youtubeuploader_<versión>_Windows_amd64.zip` from [its releases](https://github.com/porjo/youtubeuploader/releases), unzip it, and add the folder to PATH. It is not on winget |

## Configure (once)

1. In Google Cloud Console: create a project and enable **YouTube Data API v3**.
2. Configure the OAuth consent screen and add your account as a test user.
3. Create credentials: **OAuth client ID**, type **web application**, with the redirect URI `http://localhost:8080/oauth2callback`.
4. Download the JSON and save it **outside the repository**, for example at `~/.config/youtubeuploader/client_secrets.json` (on Windows, `%APPDATA%\youtubeuploader\`).
5. The first upload opens a browser to authorize the channel and saves the permission in the file specified with `-cache`. Save that file outside the repository too.

The credentials and token grant access to your channel: never put them in git.

## Upload

```bash
Y=~/.config/youtubeuploader
youtubeuploader \
  -secrets $Y/client_secrets.json -cache $Y/request.token \
  -filename video.mp4 \
  -metaJSON publishing.json \
  -thumbnail miniatura.png \
  -caption subtitles.srt \
  -privacy private        # or unlisted
```

`publishing.json` contains the title, description with chapters, tags, language, and, if you want to schedule it, the publication date (`publishAt`). See the [tool README](https://github.com/porjo/youtubeuploader#metadata) for the format.

**Never publish directly.** Upload as private or unlisted and review it in YouTube Studio before publishing it.

## Warning: unaudited projects

According to the `videos.insert` reference, videos uploaded through the API from an **unaudited** Google Cloud project (created after 2020-07-28) remain **private**, and YouTube's help says their visibility cannot be changed: they would need to be uploaded again through Studio or the API audit requested, which is free. A November 2026 source says Google lifted this restriction in October, but this is unconfirmed ([issue](https://github.com/porjo/youtubeuploader/issues/86)).

Before your first real video, **upload a short test video as unlisted** and check its status in Studio:

- If it remains unlisted: the tool works for the whole workflow.
- If it is private and locked: use the API only for videos that should remain private, and upload the rest through Studio with the text already prepared. Or request the audit.

## Synthetic content

If the video uses a cloned voice or other realistic AI-generated content, YouTube requires you to disclose it. With youtubeuploader, mark it in Studio during review; the alternative MCP marks it during upload (`contains_synthetic_media`).

## Pre-publication checklist

- [ ] Title and description reviewed (`videos/<folder>/publishing.md`)
- [ ] Final thumbnail
- [ ] Subtitles uploaded or burned in
- [ ] Chapters (timestamps) in the description
- [ ] Synthetic content disclosed, if applicable
- [ ] Santi's explicit confirmation to make it public
