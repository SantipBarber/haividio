# Workflow 4 — Publicar en YouTube

*[English](04-publish-youtube.en.md)*

Herramienta: [youtubeuploader](https://github.com/porjo/youtubeuploader) (Apache-2.0, YouTube Data API v3). Es una CLI, así que la usa cualquier agente sin configurar nada. Hay versión para Mac, Windows y Linux. Sube como **privado** por defecto, o como oculto (no listado), con miniatura, subtítulos SRT, lista de reproducción y título, descripción y etiquetas en un JSON.

Alternativa si prefieres un MCP: [youtube-uploader-mcp](https://github.com/anwerj/youtube-uploader-mcp) (MIT). Hace lo mismo, cambia la visibilidad de un vídeo ya subido y permite marcar el contenido como alterado o sintético. Tiene menos usuarios: revisa el código antes de darle acceso al canal.

## Instalar

| Mac | Windows |
|---|---|
| `brew install youtubeuploader` | Descarga `youtubeuploader_<versión>_Windows_amd64.zip` de [sus versiones](https://github.com/porjo/youtubeuploader/releases), descomprímelo y añade la carpeta al PATH. No está en winget |

## Configurar (una vez)

1. En Google Cloud Console: crea un proyecto y activa **YouTube Data API v3**.
2. Configura la pantalla de consentimiento OAuth y añade tu cuenta como usuario de prueba.
3. Crea credenciales: **ID de cliente OAuth**, tipo **aplicación web**, con la URI de redirección `http://localhost:8080/oauth2callback`.
4. Descarga el JSON y guárdalo **fuera del repositorio**, por ejemplo en `~/.config/youtubeuploader/client_secrets.json` (en Windows, `%APPDATA%\youtubeuploader\`).
5. La primera subida abre el navegador para autorizar el canal y guarda el permiso en el fichero que indiques con `-cache`. Guárdalo también fuera del repositorio.

Las credenciales y el token dan acceso a tu canal: nunca en git.

## Subir

```bash
Y=~/.config/youtubeuploader
youtubeuploader \
  -secrets $Y/client_secrets.json -cache $Y/request.token \
  -filename video.mp4 \
  -metaJSON publishing.json \
  -thumbnail miniatura.png \
  -caption subtitles.srt \
  -privacy private        # o unlisted
```

`publishing.json` lleva título, descripción con capítulos, etiquetas, idioma y, si quieres programarlo, la fecha de publicación (`publishAt`). Formato en el [README de la herramienta](https://github.com/porjo/youtubeuploader#metadata).

**Nunca público directamente.** Sube como privado u oculto y revísalo en YouTube Studio antes de publicarlo.

## Ojo: proyectos sin auditar

Según la referencia de `videos.insert`, los vídeos subidos por la API desde un proyecto de Google Cloud **sin auditar** (creado después del 28-07-2020) quedan **privados**, y la ayuda de YouTube dice que no se pueden cambiar: habría que volver a subirlos desde Studio o pedir la auditoría de la API, que es gratis. Una fuente de noviembre de 2026 dice que Google levantó esta restricción en octubre, pero no está confirmado ([issue](https://github.com/porjo/youtubeuploader/issues/86)).

Antes del primer vídeo de verdad, **sube uno corto de prueba como oculto** y mira en Studio cómo queda:

- Si queda oculto: la herramienta sirve para todo el flujo.
- Si queda privado y bloqueado: sube por la API solo lo que deba quedarse privado, y lo demás desde Studio con los textos ya preparados. O pide la auditoría.

## Contenido sintético

Si el vídeo usa voz clonada u otro contenido realista generado con IA, YouTube pide declararlo. Con youtubeuploader se marca en Studio al revisar; el MCP alternativo lo marca al subir (`contains_synthetic_media`).

## Checklist antes de publicar

- [ ] Título y descripción revisados (`videos/<carpeta>/publishing.md`)
- [ ] Miniatura final
- [ ] Subtítulos subidos o quemados
- [ ] Capítulos (timestamps) en la descripción
- [ ] Contenido sintético declarado, si lo hay
- [ ] Confirmación explícita de Santi para pasar a público
