# Contributing to Haividio

Versión en español: [CONTRIBUTING.md](CONTRIBUTING.md)

Thanks for wanting to help. Haividio is a knowledge base for making videos with AI agents, so the most valuable contribution is not always code: a test of a tool, a bug that cost you an afternoon or a workflow that worked for you matter just as much.

## What helps most

- **What you learned using a tool**: a bug, a trick, a price or version change. It goes in `docs/` and, in one line, in `memory/learnings.md`.
- **Tests with other agents and systems.** Codex and Cursor are untested, and Windows barely tested. Write it up in `docs/other-agents.en.md` or `docs/windows.en.md`.
- **Improvements to skills, workflows and scripts**, with the test you ran.
- **New tools**, open source and free ones first.

For a small fix (a typo, a command that changed, a broken link), open the PR directly. For something bigger (a new workflow, skill or tool, or a change of structure), first open an issue with the "Proposal" template, explain the problem and what you suggest, and wait for a reply, so nobody works on something that will not go in.

## Rules

1. **Everything is public and general.** No client or company names, real data, personal paths (`/Users/your-name/…`), internal URLs or details of a private project. If you learned it on a private project, write it so it helps anyone.
2. **No keys in git.** Keys go in `.env`, which is ignored.
3. **No heavy video or audio.** Scripts, animation code, subtitles, final thumbnails and notes are fine. To show a result, link to it.
4. **Say what you tested and with what.** Tool version, operating system and agent. If the agent generated audio or video, say whether you listened to or watched it: an agent cannot hear.
5. **Dated.** Tools change fast: a price or requirement without a date is useless. In `memory/learnings.md`, follow the format `- YYYY-MM-DD · [topic] what you learned.`
6. **In Spanish or English**, for issues, PRs and docs. Most of the project is in Spanish today. If you add a guide in one language, you do not need to translate it: the other version can come later.

## Using AI to contribute

This project is built with agents, so using them to contribute is normal. The condition is that you understand what you send and have tested it.

- Open the agent at the root of the repository so it reads `AGENTS.md`, and follow its rules.
- Write the PR or issue description in your own words, and keep it short. If it does not fit on one screen, the change is probably too big.
- A PR generated without review, or an issue nobody has checked, is closed without discussion.

## How to send a PR

1. Fork the repository and create a branch whose name says what changes (`docs/whisperx-windows`, `skill/talking-video-subtitulos`).
2. One PR, one topic. Two small PRs are better than a big one.
3. If you change a skill, bump the version in `plugins/video-studio/.claude-plugin/plugin.json`.
4. If you change the website (`site/`), check that it looks right on a phone. It publishes itself on merge.
5. Fill in the PR template: what changes, why, and what you tested.

Commit messages, in Spanish or English, say what changes ("Check the voice against the script with WhisperX"). No special format or signed commits needed.

## What a PR does not touch

- `memory/preferences.md`: the maintainer's preferences for their own videos.
- `videos/`: the maintainer's videos. If you want to show one of yours made with Haividio, open an issue and we will link it.

## Security issues

If you find a leaked key or private data, do not open a public issue: report it with [a private security advisory](https://github.com/SantipBarber/haividio/security/advisories/new).

## License

By contributing, you agree that your contribution is published under the project's [MIT license](LICENSE).

## Conduct

Criticise the work, not the person. Everyone who takes part accepts the [code of conduct](CODE_OF_CONDUCT.en.md).
