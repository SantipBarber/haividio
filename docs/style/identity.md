# Identidad visual del canal

*[English](identity.en.md)*

> **Estado:** propuesta, pendiente de elegir dirección. Cuando se elija, se borran las otras dos y esta pasa a ser la guía oficial que aplica la skill `visual-identity`.

## Prioridad

Que el vídeo sea **visual, potente y moderno**. No pasa nada porque se note que está hecho con IA; lo que queremos es que no se vea genérico ni de plantilla. Mejor datos y recursos reales (ver `docs/open-resources.md`) que ilustraciones de relleno.

## D. Moderno oscuro (usado en la primera prueba, escena 3 del vídeo de RAG)

| Token | Valor |
|---|---|
| Fondo | `#07080B` con rejilla de puntos `#1C2029` |
| Paneles | `#0F1116`, borde `#232733` |
| Texto | `#F4F5F7`, secundario `#8B90A0` |
| Acento | Lima eléctrico `#D4FF3A` |
| Categorías | Cian `#5CE1E6`, violeta `#A78BFA`, coral `#FF6B4A` |
| Tipografía | Geist (títulos 800, texto 400–700) + Geist Mono (datos, etiquetas) |
| Movimiento | `expo.out` para entradas, `back.out` para elementos que "aterrizan", stagger corto |
| Firma | Barra de pasos superior (01–04) con el paso activo en lima; subtítulo explicativo abajo |
| Texto mínimo | 32 px en 1080p para lo que importa; el subtítulo explicativo de abajo, 40 px. 28 px es el mínimo que exige `hyperframes check`, no un objetivo: en un móvil en vertical se ve a unos 6 px |

Código de referencia: `videos/2026-10-31-rag-2026/animations/scene-03/` (HyperFrames).

Variables CSS: [`tokens.css`](tokens.css). Lleva la paleta con sus nombres (`--lime`, `--panel`…) y además los tokens de tema que leen los componentes del catálogo de HyperFrames (`--bg`, `--surface`, `--fg`, `--brand`, `--accent`, `--font-body`…). Cópialo a `assets/` de cada proyecto y enlázalo en la composición raíz: un componente instalado con `npx hyperframes add` sale entonces con la paleta y Geist, en vez de Inter y sus verdes por defecto. Los bloques no leen esos tokens: sus colores se cambian en el código instalado.

## Para no parecer de plantilla

- ❌ Degradados morado-azul-rosa, neones, glassmorphism, brillos.
- ❌ Inter, Poppins o Roboto como tipografía principal.
- ❌ Iconografía cliché: cerebros, robots, redes neuronales brillando, chips, "matrix".
- ❌ Imágenes de stock o generadas de relleno.
- ❌ Copys tipo "revolucionario", "desbloquea", "en el mundo actual…".
- ❌ Todo con la misma animación (fade-in + slide-up) y el mismo easing.
- ❌ Voz plana sin pausas ni énfasis; música corporativa genérica.
- ✅ Una paleta corta (3–4 colores) usada con disciplina.
- ✅ Una "firma" recurrente: intro de 3 s, numeración de capítulos, forma de dibujar flechas, sonido de transición.
- ✅ Imperfección intencionada: trazos a mano, textura, ritmo variable.
- ✅ Opinión propia en el guion: "yo haría esto", "esto está sobrevalorado".

## Tres direcciones propuestas

### A. Cuaderno de ingeniero

Explicar como en una pizarra o una libreta: cercano, artesanal, muy diferente de lo típico de IA.

| Token | Valor |
|---|---|
| Fondo | Papel cálido `#F3EEE3` con textura sutil |
| Tinta | `#1C1B19` |
| Acento | Naranja óxido `#D9481C` |
| Secundario | Azul lápiz `#2F5D8A` |
| Títulos | Young Serif |
| Etiquetas y código | IBM Plex Mono |
| Formas | Trazo irregular estilo rough.js, flechas dibujadas a mano, subrayados de rotulador |
| Movimiento | Los trazos se dibujan (stroke reveal), easing suave, pequeñas vibraciones del trazo |
| Firma | El título de cada capítulo se "escribe" a mano; esquina con número de página |

### B. Terminal ámbar

Estética de monitor de fósforo ámbar: técnica, con carácter, ideal para audiencia dev.

| Token | Valor |
|---|---|
| Fondo | Casi negro cálido `#0E0D0B` |
| Principal | Ámbar `#FFB000` |
| Secundario | Gris piedra `#8A857C` |
| Alerta | Rojo `#FF5A36` |
| Tipografía | JetBrains Mono para todo; títulos en mayúsculas |
| Formas | Cajas con bordes ASCII (`┌─┐`), barras de progreso de bloques |
| Movimiento | Texto que se teclea carácter a carácter, cortes secos (steps, sin easing), cursor parpadeante, scanlines muy sutiles |
| Firma | Prompt `$ ` antes de cada capítulo; sonido de tecla mecánica en transiciones |

### C. Editorial suizo

Revista de diseño: limpio, tipografía enorme, mucho espacio. Serio y premium.

| Token | Valor |
|---|---|
| Fondo | Blanco roto `#F5F4F0` |
| Texto | `#111111` |
| Acento | Rojo señal `#E63312` |
| Secundario | Gris `#9A9A96` |
| Tipografía | Archivo (títulos enormes, peso 800) + Archivo Narrow (etiquetas) |
| Formas | Rejilla de 12 columnas, rectángulos y flechas geométricas, números de capítulo gigantes ("03") |
| Movimiento | Deslizamientos sobre la rejilla, easing expo-out, entradas escalonadas |
| Firma | Número de capítulo enorme que entra desde el borde; línea roja que recorre la pantalla |

## Voz y sonido (común)

- Voz: la tuya grabada (recomendado para identidad) o una voz ElevenLabs clonada de la tuya. Si es una voz de catálogo, elegir una y usar siempre la misma.
- Ritmo ~150 palabras/minuto, pausas antes de las ideas clave.
- Música: una sola pista de fondo recurrente, a -18 dB bajo la voz.
- Sonido de transición propio y siempre el mismo.

## Formatos

- Vídeo largo: 1920×1080, 30 fps.
- Short: 1080×1920, zona segura de 150 px arriba y abajo.
- Miniatura: 1280×720, máximo 4 palabras, mismo fondo y acento que el vídeo.
