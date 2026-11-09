# Usar Haividio con otros agentes

Haividio no depende de ningún agente concreto. Las instrucciones están en `AGENTS.md` y las skills siguen el formato abierto [Agent Skills](https://agentskills.io/specification), así que cualquier agente que lea ese formato puede usarlas.

Las skills viven en `plugins/video-studio/skills/`. El repositorio tiene dos enlaces simbólicos que apuntan a esa carpeta: `.agents/skills`, la ruta que buscan Codex, OpenCode, pi y Cursor, y `.claude/skills`, la que busca Claude Code. No hay que copiar nada.

## Dentro del repositorio (lo más sencillo)

Clona el repositorio y abre el agente en su raíz:

```bash
git clone https://github.com/SantipBarber/haividio.git
cd haividio
claude    # o codex, opencode, pi, Cursor…
```

El agente lee `AGENTS.md` (Claude Code, a través de `CLAUDE.md`) y encuentra las cinco skills sin instalar nada. pi solo carga las skills de un proyecto en el que confías: acepta cuando lo pregunte, o arráncalo con `pi --approve`.

## En cualquier proyecto (instalación global)

Para usar las skills fuera del repositorio, enlázalas en la carpeta global de cada agente. Hay que tener el repositorio clonado en algún sitio (aquí, `~/haividio`).

| Agente | Instalación global |
|---|---|
| pi | `pi install git:github.com/SantipBarber/haividio` |
| Codex, OpenCode y Cursor | `mkdir -p ~/.agents/skills && ln -s ~/haividio/plugins/video-studio/skills/* ~/.agents/skills/` |
| Claude Code | `claude plugin marketplace add SantipBarber/haividio` y `claude plugin install video-studio@haividio` |

pi instala el repositorio como paquete: lee el campo `pi` de `package.json`, que apunta a las skills. Para actualizar, `pi update`. Con el enlace simbólico, basta un `git pull` en el repositorio.

Fuera del repositorio, el agente tiene las skills pero no `AGENTS.md`, ni la memoria, ni las guías. Para producir un vídeo completo, trabaja dentro del repositorio.

## Qué se ha probado

| Agente | Estado |
|---|---|
| Claude Code | Probado: dentro del repositorio (`.claude/skills`) y con el plugin. |
| pi 1.3 | Probado: encuentra las cinco skills dentro del repositorio y con `pi install`. |
| OpenCode 2.2 | Probado: encuentra las cinco skills dentro del repositorio, una sola vez aunque lea las dos rutas. |
| Codex | Sin probar. Según su documentación, lee `.agents/skills` y `~/.agents/skills` y sigue los enlaces simbólicos. |
| Cursor | Sin probar. Según su documentación, lee `.agents/skills`, `~/.agents/skills` y también `.claude/skills`. |

Lo probado es que el agente encuentra las skills. Producir un vídeo entero solo se ha hecho con Claude Code. Si lo pruebas con otro agente, apunta en `memory/learnings.md` qué funcionó y qué no.

## Diferencias con Claude Code

- **Herramientas y MCP.** Las skills piden herramientas por su nombre (ffmpeg, HyperFrames, ElevenLabs, youtubeuploader). Las que son CLI funcionan igual en todos; los MCP, cada agente los configura a su manera.
- **Plugins de terceros.** Los workflows usan skills de otros proyectos, como HyperFrames o video-use. Cada uno explica cómo instalarlas fuera de Claude Code.
- **Windows.** Git en Windows puede clonar `.agents/skills` y `.claude/skills` como ficheros de texto en vez de como enlace. Mira [windows.md](windows.md).
