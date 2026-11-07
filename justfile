# Recetas de Haividio. Lista: `just`

default:
    @just --list

# Publica site/ en haividio.dev (normalmente lo hace GitHub al fusionar en main)
deploy:
    npx -y wrangler@4 deploy

# Comprueba qué se publicaría, sin publicar
deploy-check:
    npx -y wrangler@4 deploy --dry-run
