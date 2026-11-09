# Guion — "¿RAG ha muerto? Cómo funciona y qué se usa de verdad en 2026"

- **Formato:** vídeo sin cara, explicativo animado, 1920×1080
- **Duración objetivo:** ~9:20 (≈1.400 palabras a 150 ppm)
- **Estado:** v2 aprobada (gancho A) a falta de la fuente primaria de la escena 1
- **Público:** alguien que no sabe qué es RAG tiene que acabar entendiéndolo. Didáctico, sin bajar a fórmulas. Fuentes en `sources.md`.
- **Firma «glosario»:** la primera vez que aparece un término (fragmento, vector, top-k, BM25, reranker, agente) sale una tarjeta pequeña abajo a la derecha con su definición en ≤ 6 palabras.
- **Visuales:** descritos de forma neutra; se adaptan a la dirección de estilo elegida (`docs/style/identity.md`)

---

### Escena 1 — Gancho (0:00–0:20)
**Voz:** "El equipo de Claude Code, una de las herramientas de IA más usadas para programar, probó la receta estándar para que un modelo encuentre información. Y la tiró. Desde entonces medio internet dice que esa receta, el RAG, ha muerto. Spoiler: no ha muerto. Ha cambiado de forma. Y en seis minutos vas a entender qué es y en qué se ha convertido."
**Visual:** una caja «receta estándar: base de datos vectorial» se tacha; aparece «¿RAG ha muerto?»; el signo de interrogación se convierte en una flecha que gira hacia «ha cambiado».
**Fuente:** ⚠️ pendiente de fuente primaria (post de Boris Cherny en X / entrevista de mayo de 2025). Secundarias: https://www.tabnews.com.br/kenimo49/construi-o-rag-que-mandaram-fazer-voyage-vector-db-busca-semantica-depois-deletei-tudo-o-grep-venceu · https://www.besthub.dev/articles/why-claude-code-and-cursor-abandoned-vector-databases-for-agentic-retrieval-9dad68e8f191
**Contexto (para la escena 9):** lo quitaron porque la búsqueda agéntica (grep, abrir ficheros) daba mejores resultados, no se desactualiza, no obliga a guardar una copia del código en un índice y tiene menos piezas.

### Escena 2 — El problema (0:20–0:50)
**Voz:** "Un modelo de lenguaje sabe muchísimo, pero no sabe nada de lo tuyo: tus contratos, tu documentación interna, el correo de ayer. Puedes pegárselo todo en el prompt, pero cuando son miles de documentos eso es caro y lento. RAG, generación aumentada con recuperación, resuelve justo eso: antes de responder, el sistema busca los trozos relevantes y se los pasa al modelo."
**Visual:** un modelo (forma simple, no un cerebro ni un robot) rodeado de documentos que no puede alcanzar; aparece una "mano" de búsqueda que trae 3 fichas al modelo.

### Escena 2b — La idea: examen a libro abierto (0:50–1:25)
**Voz:** "La idea viene de un artículo de Meta de 2020. Piensa en un examen. Un modelo normal lo hace a libro cerrado: solo con lo que memorizó al entrenarse. Con RAG lo hace a libro abierto: antes de contestar, consulta una biblioteca. En aquel primer experimento, la biblioteca era Wikipedia troceada en veintiún millones de fragmentos, y para cada pregunta consultaba cinco. Y lo mejor: si cambia la biblioteca, el modelo se entera al momento. No hay que volver a entrenarlo."
**Visual:** dos columnas: «libro cerrado · memoria» frente a «libro abierto · memoria + biblioteca». Contador que sube hasta 21.000.000 fragmentos; de ellos se encienden 5.
**Fuente:** https://huggingface.co/docs/transformers/model_doc/rag · https://huggingface.co/papers/2005.11401

### Escena 3a — Dos momentos: preparar y preguntar (1:25–1:40)
**Voz:** "Un RAG tiene dos momentos. Primero preparas la biblioteca, una sola vez. Después, cada vez que alguien pregunta, buscas en ella. Empecemos por la preparación."
**Visual:** línea de tiempo partida en dos: «Preparar · una vez» (pasos 01–02) | «Preguntar · cada vez» (pasos 03–04). La barra de pasos de la firma nace de aquí.

### Escena 3b — Preparar: trocear y vectorizar (1:40–2:30)
**Voz:** "Uno: trocear. En un tutorial de LangChain, catorce páginas de documentación acaban en setecientos ochenta y dos fragmentos de unos mil caracteres. Y cada trozo repite un poco del anterior, para que ninguna idea quede partida por la mitad. Dos: convertir cada trozo en un vector. Un vector es una lista de números, cientos de ellos, que resume de qué habla el texto. No hace falta entender los números: lo importante es que los textos que hablan de lo mismo acaban cerca."
**Visual:** un párrafo real se corta en trozos; la zona de solapamiento se marca en lima entre dos trozos. Contador «14 páginas → 782 fragmentos». Un fragmento se convierte en una tira de 384 casillas que se rellenan, y la tira se comprime en un punto del plano 2D, que cae junto a los de su tema.
**Fuente:** https://docs.langchain.com/oss/python/deepagents/rag · https://huggingface.co/learn/cookbook/advanced_rag

### Escena 3c — Preguntar: buscar y generar (2:30–3:15)
**Voz:** "Tres: llega una pregunta. También la conviertes en vector y buscas los trozos que quedan más cerca. ¿Cuántos? Depende: en el ejemplo de Hugging Face, cinco; Anthropic recomienda veinte. No hay número mágico, se mide. Cuatro: le das esos trozos al modelo con la pregunta y le pides que responda solo con eso y que diga de dónde lo saca. Si mañana cambia un documento, lo actualizas en la biblioteca y listo. Sin reentrenar nada."
**Visual:** fotogramas clave KF 03 · Buscar y KF 04 · Generar (`design/scene3.pen`). Entre medias, un rótulo «¿cuántos? 5 · 20 · mídelo».
**Fuente:** https://huggingface.co/learn/cookbook/advanced_rag · https://www.anthropic.com/news/contextual-retrieval

### Escena 4 — Por qué falla el RAG ingenuo (3:15–4:00)
**Voz:** "Y en la práctica, falla. Un trozo suelto pierde su contexto: 'los ingresos crecieron un 3 %'… ¿de qué empresa? ¿De qué trimestre? La búsqueda por significado se equivoca con nombres exactos, códigos de producto o identificadores. Y hay preguntas que ningún trozo responde solo: '¿cuáles son los temas principales de estos mil informes?' o preguntas que necesitan encadenar varios pasos. Para cada uno de estos fallos ha aparecido una solución."
**Visual:** tres tarjetas de fallo que aparecen con una marca roja: "trozo sin contexto", "nombres exactos", "preguntas globales o multipaso". Se quedan en pantalla como índice de lo que viene.

### Escena 5 — Arreglar la búsqueda: híbrida + reranker (4:00–5:00)
**Voz:** "Primer arreglo, y el que más rinde: búsqueda híbrida. Combinas la búsqueda por significado con la búsqueda clásica por palabras clave, la de toda la vida, BM25. Una encuentra lo parecido, la otra lo exacto, y fusionas los dos rankings. Hoy es el estándar en producción. Segundo arreglo: el reranker. Recuperas, por ejemplo, treinta candidatos rápido, y un modelo más preciso los lee uno a uno junto a la pregunta y se queda con los cinco mejores. Es como pasar de buscar en Google a que un experto te filtre los resultados."
**Visual:** dos columnas de resultados (vectores | palabras clave) que se funden en una sola lista; luego un embudo: 30 fichas entran, 5 salen ordenadas (cifras del cookbook de Hugging Face).
**Fuente:** https://daily.dev/agentic-ai-hub/rag-retrieval.md/ · https://www.callmissed.com/en/blog/rag-best-practices-2026

### Escena 6 — Darle contexto a cada trozo (5:00–5:45)
**Voz:** "Tercer arreglo, para los trozos huérfanos: recuperación contextual. Antes de indexar, un modelo escribe una frase que sitúa cada trozo: 'esto es del informe de Acme del segundo trimestre de 2023'. Parece poca cosa, pero Anthropic midió que, combinada con búsqueda híbrida, reduce los fallos de recuperación un 49 %, y con reranker, un 67 %. Hay una alternativa más barata, el late chunking, que genera los vectores viendo el documento entero antes de trocearlo."
**Visual:** el trozo "los ingresos crecieron un 3 %" recibe una etiqueta encima con su contexto; barra que baja de 5,7 % a 2,9 % y luego a 1,9 % de fallos.
**Fuente:** https://anthropic.com/news/contextual-retrieval · https://arxiv.org/html/2504.19754v1

### Escena 7 — GraphRAG: cuando importan las relaciones (5:45–6:35)
**Voz:** "Para las preguntas globales está GraphRAG, que popularizó Microsoft. En vez de solo trocear, extrae entidades y relaciones: personas, empresas, productos y cómo se conectan. Construye un grafo y lo agrupa en comunidades con resúmenes. Así puede responder '¿cuáles son los grandes temas?' o '¿qué proveedores dependen de esta pieza?'. El precio: construir y mantener ese grafo es bastante más caro. Úsalo cuando las relaciones sean el corazón del problema, no por moda."
**Visual:** los fragmentos se convierten en nodos con nombres; aparecen aristas; se forman 3 grupos coloreados con una etiqueta-resumen cada uno.
**Fuente:** https://futureagi.com/blog/rag-architecture-llm-2025/ · https://timewell.jp/en/columns/ai-rag-agi

### Escena 8 — Agentic RAG: del becario al jefe de investigación (6:35–7:50)
**Voz:** "Y el gran cambio de estos dos años: el RAG agéntico. El RAG clásico es como un becario: hace una búsqueda y contesta con lo que encuentra. El agéntico se parece más a un jefe de investigación. Planifica, busca, reparte los documentos entre varios ayudantes que los leen a la vez, junta sus resúmenes y, si algo no cuadra, vuelve a buscar, en documentos, en una base de datos o en la web. Dos avisos. Uno: es más lento y más caro, porque hay muchas más llamadas al modelo. Y dos: un documento puede llevar escondida una instrucción del tipo 'ignora todo y haz esto otro'. Por eso lo que se recupera se trata como datos, nunca como órdenes."
**Visual:** la tubería recta de la escena 3 (becario: buscar → responder) se dobla en un bucle: planificar → buscar → 3 ayudantes en paralelo → verificar → (¿suficiente?) → responder. Herramientas alrededor: documentos, SQL, web. Final: un fragmento con una línea en coral «ignora todo y…» y un sello «datos, no órdenes».
**Fuente:** https://docs.langchain.com/oss/python/deepagents/rag · https://c3.unu.edu/projects/ai/deepresearch/demo_research-report_searchengine1.html

### Escena 9 — ¿Y el contexto largo? (7:50–8:30)
**Voz:** "Volvamos al principio. Hoy hay modelos con un millón de tokens de contexto, y los agentes de programación como Claude Code ya no usan una base de datos vectorial: exploran el código con búsquedas de texto, abren archivos y deciden qué leer. Eso es lo que la gente llama 'la muerte del RAG'. Pero fíjate: siguen recuperando información antes de responder. Lo que ha muerto es la base de datos vectorial como paso obligatorio. Y meter un millón de tokens en cada pregunta sigue costando muchísimo más que recuperar cinco trozos buenos."
**Visual:** una ventana de contexto gigante llenándose de páginas, con un contador de coste subiendo; al lado, cinco fichas bien elegidas con un coste diminuto.
**Fuente:** https://akitaonrails.com/en/2026/04/06/rag-is-dead-long-context/ · https://www.callmissed.com/blog/rag-best-practices-2026 · https://hamel.dev/blog/posts/evals-faq/is-rag-dead.html

### Escena 10 — Cómo elegir (8:30–9:05)
**Voz:** "Mi recomendación práctica. ¿Pocos documentos, menos de unas quinientas páginas? Mételos en el contexto y olvídate. ¿Una base de conocimiento grande tipo FAQ o documentación? RAG con búsqueda híbrida y reranker: es lo que mejor relación esfuerzo-resultado tiene. ¿Muchas relaciones entre entidades? GraphRAG. ¿Tareas de varios pasos? Agentic RAG. Y sobre todo: empieza por lo más simple y sube de nivel solo cuando midas que te hace falta."
**Visual:** árbol de decisión de 4 ramas que se construye rama a rama; la rama "empieza simple" se resalta con el color de acento.
**Fuente:** https://gitcode.csdn.net/6a29183410ee7a33f27a54d3.html

### Escena 11 — Cierre (9:05–9:20)
**Voz:** "El RAG no ha muerto, ha madurado. Si quieres que en el próximo vídeo montemos uno de estos paso a paso, dímelo en los comentarios."
**Visual:** el "¿RAG ha muerto?" de la escena 1 vuelve y se transforma en "RAG ha madurado"; firma del canal.

---

## Notas para revisión

- Las cifras de la escena 6 (35 % / 49 % / 67 %, de 5,7 % a 1,9 %) vienen del benchmark de Anthropic de 2024: miden fallos de recuperación en el top-20, no la calidad final de la respuesta.
- "Bastante más caro" en GraphRAG es intencionadamente vago: una fuente habla de 3–5× pero no es primaria.
- La cita de la escena 1 viene de un artículo de terceros que recoge la frase del equipo de Claude Code; conviene enlazarla en la descripción.
- Las opiniones ("mi recomendación") son tuyas: cámbialas si no las compartes.
