# Qué revisar: vídeo de RAG v2 (14-11)

`out/rag-video-v5.mp4` · 6:07 (v1: 6:42) · −14,3 LUFS · pico −1,6 dB · 18 planos.

Revisado con fotogramas, OCR (`check_render.py`) y transcripción (`check_voice.py`). **Nadie lo ha oído ni visto en movimiento desde aquí.**

## Qué cambia respecto al v1

- **Voz nueva entera:** `language_code: es`, `style` 0,3 y tempo ×1,10 (169 palabras/min frente a 155). Mismo texto.
- **Grafías elegidas por Santi:** Clod, ía, rag, Espóiler; «vídeo» sin cambiar.
- **Transiciones:** fundido corto a negro en cada cambio de escena (0,2 s de bajada, 0,35 s de subida), con el «whoosh» de siempre. Antes eran cortes secos.
- **Música con ducking:** baja mientras se habla y sube en las pausas (volumen 0,2, ratio 8). La voz queda de mediana 22,5 dB por encima de la música; sin ducking, 6 dB.
- **Silencio entre escenas:** 0,7 → 0,6 s.

## Mira primero

1. **«Espóiler» (0:14):** la transcripción no lo oye. Puede que la voz se lo coma o lo diga muy flojo.
2. **Palabras difíciles:**
   - «Clod» en 0:01 y 5:06 (la transcripción oye «Cloud»).
   - «ía» en 0:03.
   - «rag» en 0:12 y 4:21 (oye «rack»).
   - «vídeo» en 6:02.
3. **Ritmo y alegría:** si ×1,10 con `style` 0,3 se nota bien en todo el vídeo o cansa en alguna escena larga (agentic, 4:19; contexto largo, 5:00).
4. **Transiciones:** si el fundido a negro queda bien o se hace repetitivo (hay 17).
5. **Música:** que se oiga en las pausas sin tapar la voz. Los tramos con menos distancia están entre 2:56 y 3:22 (reranker).
6. **Tramos quietos de 4 a 7 s** (la imagen no cambia mientras habla la voz): 0:44–0:51, 2:23, 3:26–3:32, 5:36–5:46. Ya estaban en el v1, pero ahora, con más ritmo, pueden notarse más.

## Sin cambios (ya revisado en el v1)

Diseño de las escenas, rótulos y textos (`check_render` encuentra todos los esperados), los cuatro titulares del gancho y los «tics» de la barra de arreglos.

## Capítulos nuevos

0:00 ¿RAG ha muerto? · 0:21 El problema que resuelve RAG · 1:12 RAG clásico en 4 pasos · 2:20 Por qué falla el RAG ingenuo · 2:47 Búsqueda híbrida y reranker · 3:19 Recuperación contextual · 3:50 GraphRAG · 4:19 Agentic RAG · 5:00 ¿Y el contexto largo? · 5:31 Cómo elegir

## Revisión de Santi (14-11) y qué se cambió

- Bien a la primera: «Espóiler», las palabras difíciles, el ritmo («rapidito, pero no acelerado») y el equilibrio de música y voz. Las 17 transiciones, sin comentarios.
- **Arranque:** el primer fotograma era la nube de puntos. → Portada de 2 s (la miniatura) y fundido al gancho.
- **0:14 «media internet»:** la voz cambió «medio» con el texto bien escrito, y la transcripción no lo detectó. → Empalme de la frase entera desde «Desde» (un primer empalme solo de «entonces medio» sonó «desdeente entonces»: el corte debe ir en el silencio antes de la frase).
- **«Agentic» con jota y «GraphRAG» muy británico** → grafías «Eiyéntic» y «Graf rag», elegidas de oído.
- **5:37 «menos de unas 500 páginas»:** la cifra de Anthropic (200.000 tokens ≈ 500 páginas) supone páginas cortas en inglés. → «trescientas páginas» con un modelo frontera, y menos de la mitad con un modelo local de 128k.

Versión publicada: `out/rag-video-v7.mp4` · 6:17 · −14,3 LUFS · pico −1,6 dB.
