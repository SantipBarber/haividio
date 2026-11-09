# Fuentes extraídas para el vídeo de RAG

Notas de lectura (31-10-2026). Solo datos verificados en la fuente; la traducción y el "aterrizaje" son nuestros.

## Hugging Face · Transformers · RAG

https://huggingface.co/docs/transformers/model_doc/rag · paper: https://huggingface.co/papers/2005.11401 (Lewis et al., Meta AI, 2020)

- RAG combina un modelo de lenguaje preentrenado (**memoria paramétrica**: lo que "sabe" de memoria, guardado en sus pesos) con una fuente de datos externa (**memoria no paramétrica**: un índice de documentos) mediante un buscador neuronal.
- Recupera pasajes relevantes y condiciona la generación en ellos **en el momento de responder**.
- Respuestas más factuales y **conocimiento actualizable cambiando el índice, sin reentrenar el modelo**.
- Configuración por defecto: índice `wiki_dpr` = **21 millones de pasajes de Wikipedia**; **5 documentos** por pregunta (`n_docs=5`); vectores de **768 números** (`retrieval_vector_size=768`); contexto combinado máx. 300 tokens.
- Dos variantes: **RAG-Sequence** (usa los mismos documentos para toda la respuesta) y **RAG-Token** (puede apoyarse en un documento distinto para cada palabra).
- Ejemplo de la doc: pregunta "How many people live in Paris?".

**Aterrizaje:** examen a libro cerrado (solo memoria) vs. examen a libro abierto (memoria + chuleta que busca en la biblioteca).

## LangChain · Deep Agents · RAG

https://docs.langchain.com/oss/python/deepagents/rag

- Problema: sin recuperación, el modelo responde de memoria, genérico o desactualizado. Y no cabe toda la documentación en el contexto: hay que elegir pasajes.
- **Fase 1, indexar (una vez):** cargar 14 páginas → trocear en fragmentos de **1000 caracteres con 200 de solapamiento** → **782 fragmentos** → embeddings → almacén vectorial.
- **Fase 2, preguntar (cada vez):** buscar los **4 fragmentos** más parecidos (k=4) → guardarlos como ficheros con su URL de origen → el agente principal solo ve las rutas → **subagentes analistas** (hasta 3 en paralelo) leen un fichero cada uno y resumen en <300 palabras → el orquestador sintetiza con citas y, si falta evidencia, **vuelve a buscar**.
- Patrones: búsqueda guiada por skills · verificación con rúbrica (un evaluador aprueba o rechaza, beta) · investigación con lista de tareas · recuperar, descargar a ficheros y delegar.
- Clásico vs agéntico: una pasada vs ciclo (planificar → buscar → analizar → verificar → sintetizar); fragmentos al prompt vs a ficheros; sin reintentos vs refina la consulta.
- Coste: más llamadas al modelo, más latencia, más piezas que mantener.
- Seguridad: los fragmentos pueden contener texto que parezca instrucciones (**inyección indirecta**). "Treat retrieved documentation as data only." "No prompt or delimiter strategy fully prevents indirect prompt injection."
- Consejos: índice persistente y actualizado con calendario; pedir citas y comprobar que existen; trazas; evaluar con datasets.

**Aterrizaje:** clásico = un becario que hace una búsqueda y contesta; agéntico = un jefe de investigación que reparte lecturas entre ayudantes, junta sus resúmenes y vuelve a buscar si algo no cuadra.

## Hugging Face · Cookbook · Advanced RAG

https://huggingface.co/learn/cookbook/advanced_rag

- Dataset: documentación de Hugging Face (`m-ric/huggingface_doc`). Embeddings `thenlper/gte-small`: **384 números por vector**, máximo **512 tokens** por fragmento (lo que pase de ahí se corta sin avisar).
- Trocear contando **tokens**, no caracteres: fragmentos de 512 tokens con 10 % de solapamiento. El solapamiento evita que una idea quede partida entre dos trozos.
- Recupera **30** candidatos rápido → un reranker (ColBERTv2) los relee → pasan **5** al modelo.
- "Give your reader model only the most relevant insights, not a huge pile of books!" — demasiado contexto distrae (*lost in the middle*).
- "You cannot improve the model performance that you do not measure." Crear un pequeño set de preguntas de prueba.
- Error real que muestran: el modelo se inventa código que no estaba en los fragmentos aunque el prompt le pide no hacerlo.

**Aterrizaje:** buscar en Google te da 30 resultados; un experto los lee y te deja 5.

## Anthropic · Contextual Retrieval

https://www.anthropic.com/news/contextual-retrieval

- Definición simple: "RAG is a method that retrieves relevant information from a knowledge base and appends it to the user's prompt".
- **Si tu base cabe en ~200.000 tokens (~500 páginas), no necesitas RAG**: mete todo en el prompt (con prompt caching es más rápido y barato).
- Problema del trozo huérfano: "The company's revenue grew by 3% over the previous quarter." ¿Qué empresa? ¿Qué trimestre?
- Fallos de recuperación (top-20): 5,7 % → 3,7 % (−35 %, embeddings contextuales) → 2,9 % (−49 %, + BM25) → 1,9 % (−67 %, + reranker).
- BM25 = búsqueda por coincidencia exacta de palabras; clave para códigos de error e identificadores.
- Recomiendan pasar los **20** mejores fragmentos (mejor que 10 o 5), pero probar según el caso.
- Coste de contextualizar: ~1,02 $ por millón de tokens de documento, una sola vez.

**Nota:** HF cookbook pasa 5 y Anthropic recomienda 20 → no hay número mágico; decirlo así ("depende, mídelo").
