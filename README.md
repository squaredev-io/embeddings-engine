# Embeddings engine

Squaredev embeddings engine is an API first product that simplifies the process of creating and storing embeddings.
It also, enables features like semantic search, recommendations, RAG, image-to-image search, etc through a simple API and SQK.

Embedding engine is based in Python and Postgres making it reliable, scalable and easy to deploy.

## Features

### Text

- 🟦 Embeddings creation and storage through open source state of the art models.
- 🟦 Semantic search
- 🟦 Recommendations
- 🟦 Retrieval Augmented Generation (RAG)
- 🟦 Clustering

### coming soon

- 🟦 Images / multimodal
- 🟦 Image-to-image search
- 🟦 Image-to-text search
- 🟦 Image-to-image recommendations

## Getting started

We are still under development, but you can try our API by following the instructions below.

1. Clone the project

```bash
git clone https://github.com/squaredev-io/embeddings-engine.git
cd embeddings-engine
```

2. Create a virtual environment adn activate it

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies

```bash
make install
```

4. Run the database

```bash
make db
```

5. Run the server

```bash
make run
```

6. Open your browser and go to `http://localhost:8000/docs`
