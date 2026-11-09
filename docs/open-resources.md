# Recursos abiertos para los vídeos

Fuentes de información, datos y material visual que se pueden usar como referencia o directamente en los vídeos. **Comprueba siempre la licencia** del recurso concreto antes de usarlo y cítalo en la descripción.

## Información y documentación técnica

| Recurso | Para qué | Notas |
|---|---|---|
| [Hugging Face Docs](https://huggingface.co/docs) | Transformers, embeddings, datasets, PEFT, TGI… | Referencia técnica de primera mano |
| [Hugging Face Papers](https://huggingface.co/papers) | Papers del día con discusión y enlaces a modelos | Bueno para "qué es lo último" |
| [Hugging Face Learn](https://huggingface.co/learn) | Cursos abiertos (LLM, agentes, RAG, audio…) | Estructura didáctica reutilizable para guiones |
| [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | Ranking de modelos de embeddings | Datos reales para comparar en pantalla |
| [arXiv](https://arxiv.org) | Papers originales | Las figuras tienen licencia propia: redibújalas en vez de copiarlas |
| Documentación oficial de cada herramienta | LangChain, LlamaIndex, Qdrant, Weaviate, pgvector, Anthropic, OpenAI… | Fuente primaria para afirmaciones sobre producto |
| [Wikipedia](https://es.wikipedia.org) | Contexto y definiciones | CC BY-SA |

## Datos reales para visualizar

La forma más potente de que un vídeo no parezca genérico es **enseñar datos de verdad**:

- **Embeddings reales:** con `sentence-transformers` y un dataset de Hugging Face, calcula los vectores de frases reales, proyéctalos a 2D (UMAP o PCA) y anima esos puntos en lugar de puntos inventados.
- **Datasets de Hugging Face** ([huggingface.co/datasets](https://huggingface.co/datasets)): textos, preguntas y respuestas o benchmarks para ejemplos concretos.
- **Spaces de Hugging Face**: demos interactivas que se pueden grabar en pantalla como B-roll (respetando la licencia del Space).
- **Benchmarks y leaderboards** (MTEB, Open LLM Leaderboard): gráficos reales en lugar de cifras inventadas.

## Material visual

| Recurso | Licencia | Uso |
|---|---|---|
| [Google Fonts](https://fonts.google.com) / [Fontsource](https://fontsource.org) | OFL (casi todas) | Tipografías (Geist, Inter, Space Grotesk…) |
| [Lucide](https://lucide.dev), [Tabler Icons](https://tabler.io/icons), [Phosphor](https://phosphoricons.com) | MIT | Iconos |
| [Simple Icons](https://simpleicons.org) | CC0 (los logos siguen siendo marcas) | Logos de tecnologías; úsalos solo para referirte a ellas |
| [Pexels](https://www.pexels.com), [Pixabay](https://pixabay.com), [Unsplash](https://unsplash.com) | Licencias propias, uso gratuito | Fotos y vídeo de stock (con moderación) |
| [Wikimedia Commons](https://commons.wikimedia.org) | Variable (CC) | Imágenes históricas o técnicas; revisa cada una |
| Registro de bloques de HyperFrames | Ver repo | Componentes animados listos (`/hyperframes-registry`) |

## Audio

| Recurso | Licencia | Uso |
|---|---|---|
| [Pixabay Music](https://pixabay.com/music/) | Licencia Pixabay | Música de fondo |
| [YouTube Audio Library](https://studio.youtube.com) | Libre para YouTube | Música y efectos |
| [Freesound](https://freesound.org) | CC (variable) | Efectos de sonido; atribuye cuando sea CC BY |

## Regla práctica

1. Si es un dato o una afirmación → enlaza la fuente primaria en el guion y en la descripción.
2. Si es una figura de un paper → redibújala con nuestro estilo y cita el paper.
3. Si es un logo → solo para identificar la tecnología, nunca como si fuera nuestro.
