# Ideas del vídeo para aplicar en proyectos reales

Notas para Santi, fuera del guion. Recogen técnicas del vídeo que pueden mejorar sistemas RAG que ya tenemos en marcha.

## Late chunking (prioridad: revisarlo en mis proyectos)

**Qué es.** En el RAG clásico, primero se trocea el documento y luego se vectoriza cada trozo por separado. Así, cada trozo pierde lo que dicen los demás: un trozo que dice «sus ingresos crecieron un 3 %» no sabe de qué empresa habla. El late chunking cambia el orden:

1. Pasa el documento entero (o una ventana grande) por un modelo de embeddings de contexto largo. Así cada token «ve» el resto del texto.
2. Corta **después**: agrupa los vectores de los tokens de cada trozo con *mean pooling* y obtiene un vector por trozo.

Los trozos son los mismos y se guardan igual que antes, pero sus vectores llevan el contexto del documento.

**Qué necesita.**
- Un modelo de embeddings de **contexto largo** que exponga los vectores por token y use *mean pooling*. Por ejemplo, jina-embeddings-v3 o posteriores, cuya API acepta `late_chunking: true` (verificar en su documentación antes de usarlo). Con sentence-transformers o Hugging Face se puede hacer a mano: `output_hidden_states` y agrupar por intervalos de tokens.
- No necesita reentrenar ni llamar a un LLM por trozo. Solo hay que volver a indexar.
- Límite: la ventana del modelo (p. ej., 8k tokens). Los documentos más largos se procesan en ventanas grandes que se solapan.

**Frente a la recuperación contextual de Anthropic.**

| | Late chunking | Recuperación contextual |
|---|---|---|
| Cómo da contexto | El modelo de embeddings ve todo el documento | Un LLM escribe una frase de contexto para cada trozo |
| Coste de indexar | Bajo (una pasada de embeddings) | Alto (una llamada al LLM por trozo; con prompt caching baja) |
| Calidad | Buena, algo menos completa | La mejor medida: −49 % de fallos con BM25, −67 % con reranker |
| Sirve para BM25 | No (solo cambia los vectores) | Sí (el texto de contexto también se indexa en BM25) |

Merola y Singh (2025) llegan a esta conclusión: la recuperación contextual mantiene mejor la coherencia, pero cuesta más. El late chunking es más eficiente, a cambio de perder algo de relevancia y de completitud.

**Cómo lo probaría en un proyecto.**
1. Preparar 30–50 preguntas reales cuya respuesta se sepa en qué trozo está.
2. Medir el recall@5 y el recall@20 con el índice actual.
3. Volver a indexar con late chunking, con el mismo troceado y un modelo que lo soporte, y repetir la medida.
4. Si mejora poco, probar la recuperación contextual solo en los documentos con más trozos huérfanos (informes, contratos, actas).

**Fuentes.**
- Günther et al., *Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models* (Jina AI), arXiv:2409.04701 — https://arxiv.org/abs/2409.04701
- Merola y Singh, *Reconstructing Context: Evaluating Advanced Chunking Strategies for RAG* (2025), arXiv:2504.19754 — https://arxiv.org/abs/2504.19754
- Anthropic, *Introducing Contextual Retrieval* — cifras en `sources.md`.

## Otras técnicas del vídeo que conviene revisar en los proyectos

- **Búsqueda híbrida** (vectores + BM25 con RRF): sirve para códigos, referencias y nombres propios, que los embeddings encuentran mal.
- **Reranker** sobre el top-50 → top-5: suele ser la mejora más barata después de la búsqueda híbrida.
- **Evaluar con un conjunto de preguntas fijo** antes de cambiar nada: sin eso no se sabe si una mejora es real.
