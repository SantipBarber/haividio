# Workflow 2 — Animaciones y efectos sobre tu explicación

Herramientas: video-use + HyperFrames o Remotion.

## Idea

Como video-use tiene la transcripción con el tiempo de cada palabra, puede colocar overlays justo cuando dices algo. Ejemplo:

> "Cuando digo 'base de datos vectorial', pon encima un diagrama animado de embeddings entrando en la base de datos."

Cada animación la genera un subagente en paralelo con HyperFrames, Remotion, Manim o PIL, y luego se compone sobre el vídeo.

## Pasos

1. Hacer primero el corte limpio (workflow 1).
2. Pedir las animaciones indicando la frase o el momento y qué debe mostrarse.
3. Revisar el render; iterar ("más lento", "colores de la marca", "que no tape la cara").
4. Guardar el código de las animaciones en `videos/<carpeta>/animations/` para reutilizarlas en otros vídeos.

## Consejos

- Definir una vez una paleta y tipografía de marca y guardarla en `videos/_template/estilo.md` para que todas las animaciones sean coherentes.
- Las animaciones de tipo diagrama (flujos, cajas, flechas) salen mejor en HyperFrames (HTML/CSS); las muy programáticas o con datos, en Remotion.
