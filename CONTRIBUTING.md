# Contribuir a Haividio

English version: [CONTRIBUTING.en.md](CONTRIBUTING.en.md)

Gracias por querer aportar. Haividio es una base de conocimiento para producir vídeos con agentes de IA, así que lo más valioso no siempre es código: también lo es una prueba con una herramienta, un fallo que te costó una tarde o un workflow que te funcionó.

## Qué aporta más

- **Lo que aprendiste usando una herramienta**: un fallo, un truco, un cambio de precio o de versión. Va en `docs/` y, en una línea, en `memoria/aprendizajes.md`.
- **Pruebas con otros agentes y sistemas.** Codex y Cursor están sin probar, y Windows casi. Cuéntalo en `docs/otros-agentes.md` o `docs/windows.md`.
- **Mejoras en skills, workflows y scripts**, con la prueba que hiciste.
- **Herramientas nuevas**, priorizando las de código abierto y gratuitas.

Para un arreglo pequeño (una errata, un comando que ha cambiado, un enlace roto), abre el PR directamente. Para algo grande (un workflow, una skill o una herramienta nueva, o un cambio de estructura), abre antes un issue con la plantilla «Propuesta», explica el problema y lo que propones, y espera respuesta: así nadie trabaja en algo que no va a entrar.

## Normas

1. **Todo es público y general.** Nada de nombres de clientes o empresas, datos reales, rutas personales (`/Users/tu-nombre/…`), URLs internas ni detalles de un proyecto privado. Si lo aprendiste en un proyecto privado, cuéntalo de forma que sirva a cualquiera.
2. **Ninguna clave en git.** Las claves van en `.env`, que está ignorado.
3. **Nada de vídeo ni audio pesado.** Sí guiones, código de animaciones, subtítulos, miniaturas finales y notas. Para enseñar un resultado, enlázalo.
4. **Di qué probaste y con qué.** Versión de la herramienta, sistema y agente. Si el agente generó audio o vídeo, di si lo escuchaste o viste: un agente no puede oír.
5. **Con fecha.** Las herramientas cambian rápido: un precio o un requisito sin fecha no sirve. En `memoria/aprendizajes.md`, sigue el formato `- AAAA-MM-DD · [tema] lo aprendido.`
6. **En español o en inglés**, en issues, PR y documentación. Si añades una guía en un idioma, no hace falta que la traduzcas: la otra versión puede llegar después.

## Usar IA para contribuir

Este proyecto se hace con agentes, así que usarlos para contribuir es lo normal. La condición es que entiendas lo que envías y lo hayas probado.

- Abre el agente en la raíz del repositorio para que lea `AGENTS.md`, y sigue sus reglas.
- Escribe la descripción del PR o del issue con tus palabras y breve. Si no cabe en una pantalla, probablemente el cambio es demasiado grande.
- Un PR generado sin revisar, o un issue que nadie ha comprobado, se cierra sin más.

## Cómo enviar un PR

1. Haz un fork y crea una rama con un nombre que diga qué cambia (`docs/whisperx-windows`, `skill/video-hablado-subtitulos`).
2. Un PR, un tema. Mejor dos PR pequeños que uno grande.
3. Si cambias una skill, sube la versión en `plugins/video-studio/.claude-plugin/plugin.json`.
4. Si cambias la página (`site/`), comprueba que se ve bien en el móvil. Se publica sola al fusionar.
5. Rellena la plantilla del PR: qué cambia, por qué y qué probaste.

Los mensajes de commit, en español o en inglés, dicen qué cambia («Comprobar la voz contra el guion con WhisperX»). No hace falta ningún formato especial ni firmar los commits.

## Qué no toca un PR

- `memoria/preferencias.md`: son los gustos del mantenedor para sus vídeos.
- `videos/`: son los vídeos del mantenedor. Si quieres enseñar uno tuyo hecho con Haividio, abre un issue y lo enlazamos.

## Problemas de seguridad

Si encuentras una clave filtrada o un dato privado, no abras un issue público: avisa con [un aviso privado de seguridad](https://github.com/SantipBarber/haividio/security/advisories/new).

## Licencia

Al contribuir, aceptas que tu aportación se publique con la [licencia MIT](LICENSE) del proyecto.

## Trato

Se critica el trabajo, no a las personas. Todo el que participa acepta el [código de conducta](CODE_OF_CONDUCT.md).
