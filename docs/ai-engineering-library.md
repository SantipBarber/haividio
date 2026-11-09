# Biblioteca de vídeos de ingeniería de IA (idea, 2026-11-01)

Idea de Santi: el formato del vídeo de RAG (animaciones claras, voz y fundamentos para quien no sabe nada) puede servir de **biblioteca de formación interna**. La idea es que la gente de la empresa aprenda temas de ingeniería de IA.

## Por qué funciona

- El flujo ya está montado: guion con fuentes, voz por escena con tiempos por palabra, escenas en HyperFrames y `build_root.py`, que recalcula los tiempos. Un vídeo nuevo reutiliza el estilo y los componentes.
- El público es mixto. Cada vídeo empieza por los fundamentos, como el bloque 2b–3c del vídeo de RAG, y después va a lo práctico.
- Duración: unos 8–10 minutos como máximo. Santi: «no muy profundo, que aburre».

## Temas candidatos (por decidir)

1. RAG (hecho: `videos/2026-10-31-rag-2026/`).
2. Embeddings y búsqueda semántica en profundidad. Incluye late chunking: ver `videos/2026-10-31-rag-2026/apply-in-projects.md`.
3. Agentes: herramientas, bucle, subagentes, MCP.
4. Evaluación de sistemas con LLM (datasets, LLM como juez, métricas de recuperación).
5. Prompt caching, coste y latencia.
6. Seguridad: inyección de prompt directa e indirecta.
7. Fine-tuning frente a RAG frente a prompting.
8. Voz: STT, TTS y clonación (se puede apoyar en TranslateCall).

## Pendiente de decidir

- Dónde se publica: YouTube no listado, la intranet o una carpeta compartida.
- Si lleva la voz de Santi o una voz de serie.
- Formato: vídeo suelto o serie con cabecera común.
- Si conviene sacar la librería de componentes reutilizables (barra de pasos, glosario, caja LLM, mapa de puntos) antes del segundo vídeo.
