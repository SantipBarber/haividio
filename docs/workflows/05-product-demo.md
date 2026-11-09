# Workflow 5 — Demo de producto: grabación de pantalla con voz clonada

Vídeo de 5 a 15 minutos sobre una aplicación real: se ve la pantalla, un cursor señala lo que cuenta la voz y unos rótulos o esquemas explican lo que la pantalla no enseña.

Herramientas: Playwright (toma), ElevenLabs (voz), ffmpeg (preparar la imagen) y HyperFrames (componer). Detalle en [voz clonada](../cloned-voice.md) y [montaje y verificación](../editing-and-verification.md).

## Orden de trabajo

Cada paso cierra el anterior. Volver atrás cuesta créditos y tiempo, sobre todo si la voz ya está aprobada.

1. **Guion por escenas**, con la locución separada de lo que se ve. Se escribe para el oído: una aclaración se da una vez y no se fuerzan aclaraciones a mitad de frase.
2. **Elegir modelo de voz y pronunciación** con pruebas cortas, antes de generar nada largo.
3. **Toma de ensayo**, que no escribe en ningún sistema, para comprobar puntos y tiempos.
4. **Voz completa** cuando el guion esté cerrado. Se revisa el texto con una transcripción y una persona la escucha.
5. **Tiempos para la toma:** de la voz sale cuánto tiene que quedarse el cursor en cada punto.
6. **Borrador** con la toma de ensayo. Lo que aún no sea real se marca en pantalla con un rótulo.
7. **Toma real**, una sola vez, y **versión final** con ella.
8. **Lista de revisión** con los minutos que hay que mirar (plantilla en `videos/_template/REVIEW.md`).

## La toma de pantalla

- **Playwright no graba el cursor del sistema.** Hay que dibujarlo en la página con un elemento fijo y moverlo con una curva suave, siempre a la misma velocidad (0,6 s por movimiento funcionó bien).
- **Captura por CDP en vez del grabador de Playwright.** `Page.startScreencast` y un fotograma por instante n/30 dejan la letra pequeña más nítida: SSIM de 0,971-0,990 con el grabador frente a una captura directa. Cada fotograma debe caer en su instante real; si no, la toma se retrasa poco a poco respecto a las marcas (se midieron 0,4 s al final).
- **Junto al vídeo, un JSON de marcas:** cuándo sale y llega el cursor a cada punto, y cuándo empieza y acaba cada espera. Sin esas marcas no hay sincronía fina.
- **La imagen se graba a 1×.** No se acelera ni se corta nada al grabar: eso es trabajo del montaje.
- **Datos sintéticos** siempre que se pueda, y comprobar qué se lee en pantalla antes de enseñarlo a nadie.
- **Si la toma escribe en un sistema real, la lanza una persona, una sola vez.** Dos modos a propósito: ensayo (rechaza las escrituras) y real (aprueba). Se anota el resultado esperado para comprobarlo; si falla tras escribir, no se repite sin revisar. Si un control de permisos la bloquea, se le pasa la decisión a la persona, sin buscar otra vía.
- **Otros procesos pesados alteran lo que se ve:** una lectura tardó más del doble con la máquina ocupada por la captura. Mejor pararlos antes de la toma real.

## Qué funciona en pantalla

- **Lo que se explica tiene que verse.** Si la voz dice que algo se aprueba, se ve aprobado y creado en el sistema de destino.
- **Un punto de partida fijo.** Volver al mismo mapa o menú antes de cada parte hace didáctico el recorrido. Si se hace largo, esas entradas son lo primero que se acorta.
- **Sin huecos de voz.** Unos 7-8 minutos sin silencios largos funcionan mejor que un vídeo más corto con esperas. Las esperas de la app se recortan de la imagen, con un rótulo «espera recortada»; no se para la voz.
- **El cursor no tapa lo que señala:** debajo de la palabra o la cifra. Llega unos 0,3 s antes de que se nombre.
- **Los esquemas se dibujan con datos reales**, no con un fotograma ampliado: ver [redibujar](../editing-and-verification.md#esquemas-redibujar-no-ampliar).
- **Cifras con su fuente y su alcance.** Si se enseña una barra, el rótulo dice qué se midió y sobre cuántos casos.
- **Ejemplos inventados, marcados como tales** («Correo de ejemplo»).

## Dos versiones del mismo vídeo

Una versión corta para quien solo quiere verlo funcionar y una larga para formación pueden salir del mismo montaje. En la formación aporta lo que no es obvio: cómo se hizo por dentro y qué se planea mejorar. Conviene preguntar al público qué quiere ampliar y descartar lo evidente.

1. Se hacen clips técnicos sueltos (esquemas animados con la misma voz e identidad) y se aprueban aparte.
2. Se insertan cortando la imagen del vídeo aprobado por fotogramas y **volviendo a mezclar el audio desde las pistas de voz**, para que la música no salte en las uniones.
3. El vídeo corto se queda intacto: se comprueba con su SHA que nada lo ha tocado.

Se estima el guion con el ritmo real de la voz, no con una cifra general: una estimación de unos 12 minutos acabó en 13:22. Hay que comparar la duración con el tiempo de la sesión y tener lista la versión corta por si la recortan.

## Coordinar varias sesiones

Con varias sesiones de Claude (app y toma, voz y montaje, coordinación) funcionó así:

- **Un solo guion**, en el repositorio de la app, con una referencia fija (`git show <commit>:script.md`): la copia local puede ir por detrás.
- **Una sesión manda** y las demás le proponen cambios. Las notas de traspaso con estado, decisiones y qué no reabrir ahorran repetir discusiones.
- **Un vídeo aprobado se congela:** nadie toca voz ni montaje salvo que lo pida quien lo aprobó.
- **Antes de un render pesado**, comprobar que no haya otra medición en marcha en la misma máquina.
