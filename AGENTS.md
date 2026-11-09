# Instrucciones para agentes de IA

Este repositorio, Haividio, es la base de conocimiento y el espacio de trabajo de Santi para producir vídeos con agentes de IA. Se ha usado de principio a fin con Claude Code; Codex, OpenCode, pi y Cursor encuentran las mismas skills en `.agents/skills`, y Claude Code en `.claude/skills` (ver `docs/otros-agentes.md`). Idioma de trabajo: español.

## Memoria (siempre)

Al empezar cualquier sesión, lee `memoria/aprendizajes.md`, `memoria/preferencias.md` y `memoria/pendientes.md`. Durante el trabajo, anota ahí lo que aprendas, lo que Santi decida y lo que quede pendiente (reglas en `memoria/README.md`).

## Antes de empezar cualquier vídeo

1. Lee `README.md` (tabla de herramientas) y `docs/herramientas.md`.
2. Identifica el caso de uso y lee el workflow correspondiente en `docs/workflows/`.
3. Revisa `videos/README.md` por si hay vídeos anteriores relacionados (reutiliza estilo, escenas, guiones).
4. Si hay animaciones o miniatura, aplica `docs/estilo/identidad.md` (skill `visual-identity`, en `plugins/video-studio/skills/`).
5. Crea la carpeta del vídeo copiando `videos/_plantilla/` → `videos/AAAA-MM-DD-slug/`.

## Reglas

- Propón el plan (guion, estructura, herramientas) y espera aprobación antes de renderizar o cortar.
- Nunca subas a YouTube sin confirmación explícita. Sube siempre como **privado** o **no listado** salvo que se pida lo contrario.
- No subas al repo archivos de vídeo/audio pesados (raw, renders). Solo guiones, código de animaciones, subtítulos (.srt), miniaturas finales y notas.
- Las claves (ElevenLabs, Google OAuth) van en `.env`, nunca en git.
- **El repositorio es público y acumula conocimiento general.** Antes de subir nada, quita nombres de clientes y empresas, datos, rutas personales, URLs internas y cualquier detalle de un proyecto privado. El material de un vídeo privado se queda en local, y lo que sirva a otros se generaliza en `docs/`.
- En cada entrega, deja una lista de qué revisar (`videos/_plantilla/REVIEW.md`). El agente no puede oír el audio: di qué no se ha oído ni visto en movimiento.
- Las herramientas evolucionan rápido: si algo de `docs/herramientas.md` tiene más de unos meses, verifica en la web antes de dar por bueno un precio, requisito o comando.

## Si contribuyes desde fuera

Sigue [CONTRIBUTING.md](CONTRIBUTING.md): un PR por tema, qué se probó y con qué, y la descripción breve y escrita por la persona.

## La página

`site/` es haividio.dev, en español (`site/index.html`) y en inglés (`site/en/index.html`): un cambio de texto va en las dos. Se publica sola al fusionar en `main`; si hace falta a mano, `just deploy`. Detalles en `docs/web.md`.

## Al terminar un vídeo

- Completa `videos/<carpeta>/README.md`: resumen, guion final, herramientas usadas, decisiones, problemas, enlace de YouTube.
- Añade una línea al índice `videos/README.md`.
- Si aprendiste algo útil sobre una herramienta (un fallo, un truco, un cambio de precio), actualízalo en `docs/`.
