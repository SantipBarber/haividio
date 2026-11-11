# Workflow 4 — Publicar en YouTube

*[English](04-publish-youtube.en.md)*

Herramienta: [youtubeuploader](https://github.com/porjo/youtubeuploader) (Apache-2.0, YouTube Data API v3). Es una CLI, así que la usa cualquier agente sin configurar nada. Hay versión para Mac, Windows y Linux. Sube como **privado** por defecto, o como oculto (no listado), con miniatura, subtítulos SRT, lista de reproducción, y título, descripción, etiquetas y declaraciones (para niños, contenido sintético) en un JSON.

Alternativa si prefieres un MCP: [youtube-uploader-mcp](https://github.com/anwerj/youtube-uploader-mcp) (MIT). Hace lo mismo y además cambia la visibilidad de un vídeo ya subido. Tiene menos usuarios: revisa el código antes de darle acceso al canal.

## Instalar

| Mac | Windows |
|---|---|
| `brew install youtubeuploader` | Descarga `youtubeuploader_<versión>_Windows_amd64.zip` de [sus versiones](https://github.com/porjo/youtubeuploader/releases), descomprímelo y añade la carpeta al PATH. No está en winget |

## Configurar (una vez)

1. En Google Cloud Console: crea un proyecto y activa **YouTube Data API v3**.
2. Configura la pantalla de consentimiento OAuth (tipo externo) y añade tu cuenta como usuario de prueba.
3. Crea credenciales: **ID de cliente OAuth**, tipo **aplicación web**, con la URI de redirección `http://localhost:8080/oauth2callback`.
4. Descarga el JSON y guárdalo **fuera del repositorio**, por ejemplo en `~/.config/youtubeuploader/client_secrets.json` (en Windows, `%APPDATA%\youtubeuploader\`).
5. La primera subida abre el navegador para autorizar el canal y guarda el permiso en el fichero que indiques con `-cache`. Guárdalo también fuera del repositorio.
6. **Publica la app** en **Google Auth Platform** → **Público** (estado **En producción**). No hace falta que Google la verifique, pero el botón sigue desactivado hasta completar **Información de la marca**: nombre de la app (sin «YouTube» ni «Google»), correo de asistencia, correo de contacto del desarrollador, página principal, enlace a una política de privacidad y el dominio de ambas como dominio autorizado, verificado en Search Console con la misma cuenta. Sin logotipo, que obliga a la verificación. Al pasar a producción, vuelve a autorizar: el permiso obtenido en pruebas sigue caducando a los 7 días. Mientras está **en pruebas**, Google hace caducar el permiso a los 7 días y hay que volver a autorizar cada semana. Al autorizar una app sin verificar sale un aviso: **Configuración avanzada** → **Ir a … (no seguro)**, con la cuenta del canal.

Las credenciales y el token dan acceso a tu canal: nunca en git.

**Si el permiso deja de valer** (falla al refrescar el token porque se revocó o cambió la contraseña de la cuenta): borra el fichero de `-cache` y la siguiente subida vuelve a pedir la autorización. El acceso se revoca desde la cuenta de Google del canal, en **Seguridad** → **Conexiones con terceros**.

## Privado u oculto

- **Privado:** solo lo ven las personas a las que invitas, una a una, con su cuenta de Google. Sirve para revisarlo antes de publicarlo.
- **Oculto (no listado):** no sale en el canal ni en las búsquedas, pero lo ve cualquiera que tenga el enlace. Sirve para mandarlo a alguien concreto.

Un enlace oculto se reenvía sin control: al revisar qué se ve, trátalo como si fuera público.

## Antes de subir: qué se ve

Revisa los fotogramas (un mosaico o el vídeo entero), los textos en pantalla y la locución. No puede salir:

- datos personales de personas reales: nombres, correos, teléfonos, documentos de identidad;
- importes o datos de negocio reales de un cliente, ni datos de otro cliente;
- claves, tokens, rutas personales o URLs internas en una terminal o un navegador.

Los datos inventados de una demo valen. Si sale algo que no debe, se vuelve a grabar o a renderizar con otros datos: un desenfoque se escapa en algún fotograma.

## Subir

`publishing.json` lleva título, descripción con capítulos, etiquetas, idioma, las declaraciones y, si quieres programarlo, la fecha de publicación (`publishAt`). Formato completo en el [README de la herramienta](https://github.com/porjo/youtubeuploader#metadata).

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

`containsSyntheticMedia` va a `true` si hay voz clonada u otro contenido realista generado con IA. La categoría 27 es Educación; la 28, Ciencia y tecnología.

1. **Valida la ficha** contra las reglas de YouTube y contra el vídeo real:

   ```bash
   python3 scripts/check_publishing.py meta publishing.json video.mp4
   ```

   Comprueba que el vídeo se lee entero; el título (una línea, 100 caracteres como máximo) y la descripción (5000 bytes), sin `<` ni `>`, que YouTube rechaza; las etiquetas (500 caracteres en total); los capítulos (el primero en 0:00, al menos 3, en orden y de 10 s o más, o YouTube no los muestra); que la visibilidad no es pública, y que están las dos declaraciones. Corrige lo que marque y repite hasta el ✔.

2. **Sube**, con confirmación explícita:

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

   `-notify=false` no avisa a los suscriptores, porque el vídeo aún no es público. La visibilidad sale del `privacyStatus` del JSON.

   **Miniatura personalizada:** solo funciona con el canal verificado por teléfono ([youtube.com/verify](https://www.youtube.com/verify)). Si no lo está, YouTube responde `403 … permissions to upload and set custom video thumbnails` y youtubeuploader **se para ahí: tampoco sube los subtítulos**, aunque el vídeo ya esté subido. Verifica el canal antes o quita `-thumbnail` y súbela después desde Studio.

3. **Comprueba la visibilidad** con la respuesta de YouTube:

   ```bash
   python3 scripts/check_publishing.py result upload-result.json --expect private   # o unlisted
   ```

   Si no coincide, no repartas el enlace (ver el apartado siguiente).

**Nunca público directamente.** Sube como privado u oculto y revísalo en YouTube Studio antes de publicarlo.

## Ojo: proyectos sin auditar

Según la referencia de `videos.insert`, los vídeos subidos por la API desde un proyecto de Google Cloud **sin auditar** (creado después del 28-07-2020) quedan **privados**, y la ayuda de YouTube dice que no se pueden cambiar: habría que volver a subirlos desde Studio o pedir la auditoría de la API, que es gratis. Una fuente de noviembre de 2026 dice que Google levantó esta restricción en octubre ([issue](https://github.com/porjo/youtubeuploader/issues/86)). Nuestra prueba lo confirma: el 10-11-2026, un proyecto recién creado y sin auditar subió un vídeo como oculto y otro como público, y los dos quedaron con esa visibilidad.

Antes del primer vídeo de verdad, **sube uno corto de prueba como oculto** y comprueba el resultado con `check_publishing.py result … --expect unlisted` y en Studio:

- Si queda oculto: la herramienta sirve para todo el flujo.
- Si queda privado y bloqueado: sube por la API solo lo que deba quedarse privado, y lo demás a mano desde Studio. O pide la auditoría.

## Subir a mano desde Studio

Si no hay acceso por la API, con la ficha ya validada, entra en [studio.youtube.com](https://studio.youtube.com) con la cuenta del canal:

1. **Crear** → **Subir vídeos** → el mp4.
2. **Detalles:** título y descripción de la ficha, miniatura y **No, no es contenido creado para niños**. En **Mostrar más**, el contenido alterado o sintético, si lo hay.
3. **Elementos del vídeo** → **Subtítulos:** el `.srt`, con su idioma.
4. **Visibilidad:** **Privado** u **Oculto** → **Guardar**.

## Checklist antes de publicar

- [ ] Revisado qué se ve: ningún dato que no deba salir
- [ ] Título y descripción revisados (`videos/<carpeta>/publishing.md`)
- [ ] `check_publishing.py meta` en ✔
- [ ] Miniatura final
- [ ] Subtítulos subidos o quemados
- [ ] Capítulos (timestamps) en la descripción
- [ ] Contenido sintético declarado, si lo hay
- [ ] `check_publishing.py result` con la visibilidad pedida
- [ ] Confirmación explícita de Santi para pasar a público
