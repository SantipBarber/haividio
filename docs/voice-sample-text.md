# Texto para grabar la muestra de voz (unos 2 minutos)

Léelo con el mismo tono que usarías en el vídeo: explicando a un compañero, tranquilo y sin prisa. No hace falta leerlo perfecto. Si te equivocas, haz una pausa y repite la frase entera; luego se recorta.

---

Imagina que le preguntas a un asistente por la política de devoluciones de tu empresa y te contesta con total seguridad… algo que se ha inventado. No es que mienta: es que nunca ha leído tus documentos. Para eso existe el RAG, la generación aumentada por recuperación.

La idea es sencilla. Primero troceas los documentos en fragmentos pequeños. Después conviertes cada fragmento en un vector, una lista de números que resume de qué habla. Cuando llega una pregunta, buscas los fragmentos más parecidos y se los das al modelo, con una instrucción clara: responde solo con esto, y di de dónde lo sacas.

¿Funciona siempre? No. A veces la búsqueda falla con códigos o nombres propios, como una referencia de pedido o el nombre de un cliente. Por eso hoy se combina la búsqueda por significado con la búsqueda por palabras clave, lo que se llama búsqueda híbrida, y se añade un reranker que vuelve a ordenar los resultados.

Hay más trucos: la recuperación contextual, el late chunking, GraphRAG o los agentes que deciden cuándo buscar y cuántas veces. Cada uno resuelve un problema distinto, y ninguno es gratis.

Entonces, ¿ha muerto el RAG ahora que los modelos leen un millón de tokens de golpe? Ni mucho menos. Pero sí ha cambiado. Y en los próximos minutos vamos a ver cómo, paso a paso, con ejemplos reales y sin dar nada por sabido.

Uno, dos, tres. Cuarenta y cinco días. El dos mil veintiséis. Embeddings, prompt, contexto, Claude Code.
