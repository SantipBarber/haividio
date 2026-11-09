# Open resources for videos

*[Español](open-resources.md)*

Sources of information, data and visual material that can be used as references or directly in videos. **Always check the license of the specific resource before using it, and cite it in the description.**

## Information and technical documentation

| Resource | What for | Notes |
|---|---|---|
| [Hugging Face Docs](https://huggingface.co/docs) | Transformers, embeddings, datasets, PEFT, TGI… | First-hand technical reference |
| [Hugging Face Papers](https://huggingface.co/papers) | Daily papers, with discussion and links to models | Good for "what's new" |
| [Hugging Face Learn](https://huggingface.co/learn) | Open courses (LLMs, agents, RAG, audio…) | Reusable teaching structure for scripts |
| [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | Embedding model rankings | Real data to compare on screen |
| [arXiv](https://arxiv.org) | Original papers | Figures have their own licenses: redraw them instead of copying |
| Official documentation for each tool | LangChain, LlamaIndex, Qdrant, Weaviate, pgvector, Anthropic, OpenAI… | Primary source for product claims |
| [Wikipedia](https://es.wikipedia.org) | Context and definitions | CC BY-SA |

## Real data to visualize

The best way to make a video look non-generic is to **show real data**:

- **Real embeddings:** use `sentence-transformers` and a Hugging Face dataset to calculate vectors for real sentences, project them into 2D (UMAP or PCA), and animate those points instead of invented ones.
- **Hugging Face datasets** ([huggingface.co/datasets](https://huggingface.co/datasets)): text, questions and answers, or benchmarks for specific examples.
- **Hugging Face Spaces:** interactive demos that can be screen-recorded as B-roll (respect the Space's license).
- **Benchmarks and leaderboards** (MTEB, Open LLM Leaderboard): real charts instead of invented figures.

## Visual material

| Resource | License | Use |
|---|---|---|
| [Google Fonts](https://fonts.google.com) / [Fontsource](https://fontsource.org) | OFL (most) | Typefaces (Geist, Inter, Space Grotesk…) |
| [Lucide](https://lucide.dev), [Tabler Icons](https://tabler.io/icons), [Phosphor](https://phosphoricons.com) | MIT | Icons |
| [Simple Icons](https://simpleicons.org) | CC0 (logos are still trademarks) | Technology logos; use them only to refer to those technologies |
| [Pexels](https://www.pexels.com), [Pixabay](https://pixabay.com), [Unsplash](https://unsplash.com) | Their own licenses, free to use | Stock photos and video (sparingly) |
| [Wikimedia Commons](https://commons.wikimedia.org) | Varies (CC) | Historical or technical images; check each one |
| HyperFrames registry | See repo | Ready-made animated components (`/hyperframes-registry`) |

## Audio

| Resource | License | Use |
|---|---|---|
| [Pixabay Music](https://pixabay.com/music/) | Pixabay License | Background music |
| [YouTube Audio Library](https://studio.youtube.com) | Free for YouTube | Music and sound effects |
| [Freesound](https://freesound.org) | CC (varies) | Sound effects; attribute when using CC BY |

## Practical rule

1. For data or a claim → link the primary source in the script and description.
2. For a figure from a paper → redraw it in our style and cite the paper.
3. For a logo → use it only to identify the technology, never as if it were ours.
