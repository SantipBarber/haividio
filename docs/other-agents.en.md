# Using Haividio with other agents

*[Español](other-agents.md)*

Haividio does not depend on any particular agent. The instructions are in `AGENTS.md`, and the skills follow the open [Agent Skills](https://agentskills.io/specification) format, so any agent that reads that format can use them.

The skills live in `plugins/video-studio/skills/`. The repository has two symlinks pointing to that folder: `.agents/skills`, the path used by Codex, OpenCode, pi and Cursor, and `.claude/skills`, the path used by Claude Code. Nothing needs to be copied.

## Inside the repository (simplest)

Clone the repository and open the agent at its root:

```bash
git clone https://github.com/SantipBarber/haividio.git
cd haividio
claude    # or codex, opencode, pi, Cursor…
```

The agent reads `AGENTS.md` (Claude Code does so through `CLAUDE.md`) and finds the five skills without installing anything. pi only loads skills from a project you trust: accept when prompted, or start it with `pi --approve`.

## In any project (global installation)

To use the skills outside the repository, link them into each agent's global folder. You need to have the repository cloned somewhere (here, `~/haividio`).

| Agent | Global installation |
|---|---|
| pi | `pi install git:github.com/SantipBarber/haividio` |
| Codex, OpenCode and Cursor | `mkdir -p ~/.agents/skills && ln -s ~/haividio/plugins/video-studio/skills/* ~/.agents/skills/` |
| Claude Code | `claude plugin marketplace add SantipBarber/haividio` and `claude plugin install video-studio@haividio` |

pi installs the repository as a package: it reads the `pi` field in `package.json`, which points to the skills. Run `pi update` to update. With the symlink, just run `git pull` in the repository.

Outside the repository, the agent has the skills but not `AGENTS.md`, the memory or the guides. To produce a complete video, work inside the repository.

## What has been tested

| Agent | Status |
|---|---|
| Claude Code | Tested: inside the repository (`.claude/skills`) and with the plugin. |
| pi 1.3 | Tested: finds the five skills inside the repository and with `pi install`. |
| OpenCode 2.2 | Tested: finds the five skills inside the repository, once even when it reads both paths. |
| Codex | Untested. According to its documentation, it reads `.agents/skills` and `~/.agents/skills` and follows symlinks. |
| Cursor | Untested. According to its documentation, it reads `.agents/skills`, `~/.agents/skills` and `.claude/skills` too. |

What has been tested is whether the agent finds the skills. A complete video has only been produced with Claude Code. If you try another agent, note what worked and what did not in `memory/learnings.md`.

## Differences from Claude Code

- **Tools and MCP.** The skills request tools by name (ffmpeg, HyperFrames, ElevenLabs, youtubeuploader). CLI tools work the same in every agent; each agent configures MCPs in its own way.
- **Third-party plugins.** The workflows use skills from other projects, such as HyperFrames or video-use. Each explains how to install them outside Claude Code.
- **Windows.** Git on Windows may clone `.agents/skills` and `.claude/skills` as text files instead of symlinks. See [windows.en.md](windows.en.md).
