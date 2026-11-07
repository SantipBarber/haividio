# La página haividio.dev

La página son los ficheros estáticos de `site/`, servidos por un Worker de Cloudflare. La configuración está en `wrangler.jsonc`: nombre, carpeta y dominios.

## Publicar

- **Sola:** al fusionar en `main` un cambio de `site/` o de `wrangler.jsonc`, GitHub Actions la publica (`.github/workflows/web.yml`). También se puede lanzar a mano desde la pestaña *Actions*, con *Run workflow*.
- **A mano:** `just deploy` desde la raíz, con una sesión de Wrangler abierta (`npx wrangler login`). `just deploy-check` enseña qué se subiría, sin subir nada.

## Configurar la publicación automática (una vez)

1. En Cloudflare: *My Profile → API Tokens → Create Token*, con la plantilla **Edit Cloudflare Workers**. Limítalo a tu cuenta y, en la zona, a `haividio.dev`.
2. En GitHub: *Settings → Secrets and variables → Actions → New repository secret*:
   - `CLOUDFLARE_API_TOKEN`: el token.
   - `CLOUDFLARE_ACCOUNT_ID`: el ID de la cuenta (`npx wrangler whoami` lo muestra).
3. Lanza el flujo a mano una vez (*Actions → Publicar haividio.dev → Run workflow*) y comprueba la página.

Sin el token, el flujo no falla: avisa de que falta y no publica.
