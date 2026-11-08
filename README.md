![Haividio: guion, voz, animación y publicación, dirigidos por tu agente de IA](docs/estilo/haividio-banner.png)

![Licencia MIT](https://img.shields.io/badge/licencia-MIT-D4FF3A?style=flat-square&labelColor=0F1116)
![Agentes: Claude Code, Codex, OpenCode, pi, Cursor](https://img.shields.io/badge/agentes-Claude_Code_%C2%B7_Codex_%C2%B7_OpenCode_%C2%B7_pi_%C2%B7_Cursor-D4FF3A?style=flat-square&labelColor=0F1116)
![Idiomas: español e inglés](https://img.shields.io/badge/idiomas-espa%C3%B1ol_%C2%B7_English-D4FF3A?style=flat-square&labelColor=0F1116)

[English version](README.en.md)

Un manual y un espacio de trabajo para producir vídeos con agentes de IA. Abres la terminal aquí y el agente ya sabe qué herramienta usar, cómo se trabaja y qué falló la última vez.

*Haividio* suena a «hay vídeo» en español y a «hi, video» en inglés.

**[haividio.dev](https://haividio.dev)** · [Elige tu vídeo](#elige-tu-vídeo) · [Empezar](#empezar) · [Skills](#skills) · [Guías](#guías) · [Estructura](#estructura)

## Elige tu vídeo

| Quieres hacer | Con | Guía |
|---|---|---|
| Vídeo hablado: quitar silencios, errores y muletillas | [video-use](https://github.com/browser-use/video-use) | [Workflow 1](docs/workflows/01-video-hablado.md) |
| Animaciones sobre tu explicación | video-use + HyperFrames o Remotion | [Workflow 2](docs/workflows/02-animaciones.md) |
| Explicativo sin cara, con voz en off | [HyperFrames](https://github.com/heygen-com/hyperframes) o [Remotion](https://www.remotion.dev/docs/ai/skills) + ElevenLabs | [Workflow 3](docs/workflows/03-video-sin-cara.md) |
| Demo de producto: pantalla y voz clonada | Playwright + ffmpeg + HyperFrames | [Workflow 5](docs/workflows/05-demo-de-producto.md) |
| Publicar en YouTube | [youtubeuploader](https://github.com/porjo/youtubeuploader) (YouTube Data API v3) | [Workflow 4](docs/workflows/04-publicar-youtube.md) |

Funciona con Claude Code, Codex, OpenCode, pi y Cursor. Lo único que se paga aparte es ElevenLabs.

## Empezar

```bash
git clone https://github.com/SantipBarber/haividio.git
cd haividio
claude    # o codex, opencode, pi, Cursor…
```

Tu agente lee `AGENTS.md` y encuentra las skills (en `.agents/skills`, o `.claude/skills` en Claude Code): no hay que instalar nada más. Dile qué vídeo quieres; elige el workflow y propone el plan antes de renderizar nada.

Para usar las skills en otros proyectos (plugin de Claude Code, `pi install` o `~/.agents/skills`) y ver qué se ha probado con cada agente: [docs/otros-agentes.md](docs/otros-agentes.md).

Claves (ElevenLabs, Google) en un `.env` en la raíz; está en `.gitignore`. Los vídeos y audios pesados no se suben al repositorio.

<details>
<summary>Instalación completa en Mac</summary>

```bash
# 1. Herramientas base
brew install ffmpeg node        # Node 22 o superior
git clone https://github.com/SantipBarber/haividio.git
cd haividio

# 2. Probar que la escena de ejemplo renderiza
cd videos/2026-10-31-rag-2026/animaciones/escena-03
npx hyperframes check
npx hyperframes preview          # vista previa en el navegador
npx hyperframes render -o ~/Desktop/escena-03.mp4

# 3. Abrir tu agente en la raíz del repositorio
cd ../../../.. && claude          # o codex, opencode, pi
```

</details>

<details>
<summary>Instalación completa en Windows</summary>

```powershell
# 1. Herramientas base (PowerShell)
winget install Git.Git
winget install GitHub.GitLFS
winget install OpenJS.NodeJS.LTS   # Node 22 o superior
winget install Gyan.FFmpeg
winget install Python.Python.3.12
# cerrar y abrir PowerShell para que se actualice el PATH
git lfs install
git clone https://github.com/SantipBarber/haividio.git
cd haividio

# 2. Probar que la escena de ejemplo renderiza
cd videos/2026-10-31-rag-2026/animaciones/escena-03
npx hyperframes check
npx hyperframes preview          # vista previa en Chrome o Edge
npx hyperframes render -o $HOME\Desktop\escena-03.mp4
```

El núcleo es multiplataforma, pero HyperFrames en Windows aún está por probar y hay herramientas solo de macOS. El resto, en [docs/windows.md](docs/windows.md).

</details>

## Skills

| Skill | Para qué |
|---|---|
| `elegir-herramienta-video` | Decide qué herramienta usar según el tipo de vídeo |
| `video-hablado` | Edita tomas: cortes, subtítulos y animaciones sincronizadas |
| `video-sin-cara` | Investigación, guion, voz, animación y render |
| `identidad-visual` | Aplica la identidad del canal y evita lo genérico |
| `publicar-youtube` | Título, capítulos, miniatura y subida como privado |

## Guías

- [Voz clonada](docs/voz-clonada.md): modelos, pronunciación, tomas y empalmes.
- [Montaje y verificación](docs/montaje-y-verificacion.md): sincronía, cortes limpios, mezcla y qué prueba cada comprobación.
- [Otros agentes](docs/otros-agentes.md): Codex, OpenCode, pi y Cursor, dentro y fuera del repositorio.
- [Catálogo de herramientas](docs/herramientas.md): editores, MCP y skills, con su coste.
- [Identidad visual](docs/estilo/identidad.md): paleta, tipografía y movimiento.
- [Recursos abiertos](docs/recursos-abiertos.md): documentación, iconos, fuentes y audio, con sus licencias.
- [Memoria](memoria/): aprendizajes y fallos, con fecha.

## Estructura

<details>
<summary>Ver carpetas</summary>

```text
AGENTS.md                    Instrucciones para cualquier agente
CLAUDE.md                    Punto de entrada para Claude Code
CONTRIBUTING.md              Cómo contribuir (también en inglés)
CODE_OF_CONDUCT.md           Código de conducta (Contributor Covenant 3.0)
.github/                     Plantillas de issues y PR, publicación de la página
README.en.md                 Este README en inglés
.agents/skills               Enlace a las skills para Codex, OpenCode, pi y Cursor
.claude/skills               Enlace a las skills para Claude Code
package.json                 Paquete de pi (pi install)
justfile                     Recetas: just deploy publica la página
wrangler.jsonc               Configuración de la página en Cloudflare
memoria/                     Aprendizajes, preferencias y pendientes
.claude-plugin/              Marketplace de plugins
plugins/video-studio/        Plugin de Claude Code con las skills
docs/
  estilo/identidad.md        Identidad visual (paleta, tipografía, movimiento)
  herramientas.md            Catálogo de herramientas
  voz-clonada.md             Modelos, pronunciación, tomas y empalmes
  montaje-y-verificacion.md  Sincronía, cortes, mezcla y comprobaciones
  recursos-abiertos.md       Recursos con sus licencias
  otros-agentes.md           Codex, OpenCode, pi y Cursor
  windows.md                 Instalación y límites en Windows
  workflows/                 Un flujo por tipo de vídeo
site/                        Página de haividio.dev, con /en en inglés (docs/web.md)
scripts/
  splice_voice.py            Sustituye frases o palabras de una locución sin regenerarla
  detect_glitches.py         Busca clics, huecos y congelaciones en un vídeo
  check_voice.py             Compara la voz con el guion (WhisperX, local)
videos/
  README.md                  Índice de vídeos
  _plantilla/                Copiar para cada vídeo nuevo
```

Para empezar un vídeo nuevo, copia `videos/_plantilla/` a `videos/AAAA-MM-DD-slug/` y dile al agente qué quieres hacer.

</details>

## Contribuir

Se agradecen sobre todo pruebas y aprendizajes con herramientas, agentes y sistemas, en español o en inglés. Lee [CONTRIBUTING.md](CONTRIBUTING.md) ([English](CONTRIBUTING.en.md)) antes de abrir un PR. Quien participa acepta el [código de conducta](CODE_OF_CONDUCT.md).

## Licencia

[MIT](LICENSE). La web usa la tipografía Geist, con licencia SIL OFL. Las herramientas y servicios citados tienen sus propias licencias.
