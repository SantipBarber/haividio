# Workflow 6 — De Pencil a HyperFrames

*[English](06-pencil-to-hyperframes.en.md)*

Herramientas: [Pencil](https://pen.dev) (pen.dev, con su MCP) + `scripts/pencil_to_hyperframes.py` + HyperFrames. Skill: `pencil-to-hyperframes`.

## Idea

Diseñar los fotogramas clave de una escena en Pencil, con calma y viéndolos, y que el agente los convierta en una composición de HyperFrames que solo falta animar. En el vídeo de RAG se hizo así a mano y funcionó bien y rápido; el script hace los pasos mecánicos para que no haya que repetirlos en cada escena.

Pencil exporta HTML con estilos en línea, posiciones absolutas y el nombre de cada capa (`data-pencil-name`). Al pasarlo a HyperFrames faltan cuatro cosas, y el script las añade:

| Falta | Qué hace el script |
|---|---|
| Ids para animar | Un id por capa con nombre, a partir de la ruta de nombres: `Tracker/Paso 01` → `#kf-tracker-paso-01`. Si se repite, lleva `-2`, `-3`… |
| Fuentes locales | Descarga de Google Fonts los subconjuntos latin y latin-ext a `assets/fonts/` y los declara con `@font-face`. HyperFrames no admite fuentes por CDN y Geist no viene incluida. |
| Imágenes | Copia las que usa el diseño a `assets/pencil/` y reescribe las rutas. Las busca junto al HTML exportado y junto al `.pen`. |
| Envoltorio | `<template>`, `#root` con `data-composition-id` y una línea de tiempo vacía registrada en `window.__timelines`. |

Con `--tokens docs/style/tokens.css`, además, cada color de la paleta pasa a `var(--lime, #D4FF3A)`: si cambia la identidad, cambia también lo importado.

## Pasos

1. **Diseñar en Pencil** los fotogramas de la escena. Nombra las capas con sentido («Tracker», «Paso 01», «Pregunta»): los ids salen de ahí.
2. **Exportar** por MCP, siempre con la ruta explícita del `.pen` (si no existe, el MCP trabaja sobre el `.pen` abierto, que puede ser de otro proyecto):

   ```js
   Export(["<id fotograma 1>", "<id fotograma 2>"], "html-css", "<vídeo>/design/export/buscar.html")
   Export(["<id fotograma 1>", "<id fotograma 2>"], "png", "<vídeo>/design/export/")
   ```

3. **Convertir:**

   ```bash
   python3 scripts/pencil_to_hyperframes.py <vídeo>/design/export/buscar.html \
     --project <vídeo>/animations/<proyecto> --name buscar --prefix kf \
     --pen-dir <vídeo>/design --tokens docs/style/tokens.css --duration 8
   ```

   Imprime la lista capa → id y el fragmento para montar la escena en `index.html`.
4. **Comprobar antes de animar:** `npx hyperframes check` y un `snapshot`, comparado con el PNG de Pencil.
5. **Animar** por id en la línea de tiempo de la composición, con la skill `visual-identity` y la voz como en el workflow 3.

## Varios fotogramas: estados, no diapositivas

Si el export trae varios fotogramas, el primero es la composición y los demás van a `<nombre>.states.json`: para cada id, qué cambia respecto al primero (estilos y texto), qué capas entran y cuáles salen. El HTML de cada fotograma, ya convertido y con los mismos ids, queda en `pencil/<nombre>/`: de ahí se copian las capas que entran. Pencil exporta varios fotogramas dentro de un lienzo sin nombre, cada uno desplazado a la derecha; el script lo quita. Se anima de un estado al siguiente; poner los fotogramas uno detrás de otro como imágenes es justo lo que hay que evitar (la skill `figma` de HyperFrames sigue la misma idea).

Para que funcione, el mismo elemento tiene que llamarse igual y estar dentro de la misma capa en todos los fotogramas. Lo más fácil es duplicar el fotograma en Pencil y cambiar solo lo que se mueve.

**Borrador de la escena entera (`--draft`):** mete en la composición los bloques de todos los fotogramas, ocultos hasta su momento, y escribe una línea de tiempo con un cambio por fotograma: salen los bloques que ya no están, entran los nuevos (de abajo arriba, escalonados) y las capas comunes pasan al estado siguiente (color, fondo, borde, tamaño, posición, texto). Con `--at 0,6,12` cada fotograma empieza cuando la voz lo nombra; sin él, tramos iguales. Es un punto de partida: dentro de cada estado no se mueve nada (`check` lo marca como `dead_stretch`) y las capas que entran dentro de un bloque que ya estaba hay que copiarlas a mano (el script dice cuántas).

## Probado

Con el fotograma «KF 03 · Buscar» del vídeo de RAG: 96 capas con id, 76 colores pasados a variables, la rejilla de fondo copiada y Geist descargada. `hyperframes check` sin errores ni avisos, y el `snapshot` se diferencia del PNG de Pencil en 1 nivel de gris de 255 de media (los demás fotogramas del mismo diseño, en unos 20). Storyboard real: «KF 3b · Trocear», «KF 3b · Vectorizar» y «KF 03 · Buscar», exportados juntos. `states.json` recoge lo que de verdad cambia entre ellos (el paso activo de la barra pasa de 01 a 02 y a 03, y el pie cambia de texto) y qué bloques entran y salen. Animando solo esos cambios en los segundos 3 y 6, las capturas en 1, 4 y 7 s muestran la barra igual que cada PNG de Pencil; las pastillas quedan unos píxeles más estrechas por cómo se dibuja el texto. Con `--draft --at 0,6,12 --duration 18`, la escena entera pasa `check` sin errores ni avisos de lectura, se renderiza en 11 s y `check_render.py` encuentra en el vídeo los 9 rótulos de los tres estados. La prueba sacó cuatro fallos, ya arreglados: el lienzo que envuelve varios fotogramas, las imágenes relativas al `.pen`, los `style` con comillas simples (perdían posición y color) y la transición a transparente, que pasaba por un verde: el borrador da siempre los dos extremos de cada cambio.

## Cuidado

- **El MCP de Pencil:** con la ruta explícita (`uri`) del `.pen`, `execute` lee y exporta ese fichero sin cambiar el que está abierto en la app (comprobado el 11-11 con otro proyecto abierto). Si la ruta no existe, actúa sobre el `.pen` activo: mira antes `get_app_state`.
- **No edites un `.pen` por otra vía** que no sea el MCP: se corrompe.
- **Las posiciones dentro de un layout flex** no salen en el HTML como coordenadas: si un elemento se mueve entre fotogramas porque cambia el layout, `states.json` lo dice como cambio de estilo del contenedor, no como `left`/`top`. Para moverlo con precisión, mídelo en el `snapshot`.
