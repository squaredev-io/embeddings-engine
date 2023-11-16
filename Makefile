run:
	@echo Starting FastAPI server...
	@uvicorn embeddings-engine.main:app --reload

test:
	@echo Running tests...
	@pytest -s --log-cli-level=DEBUG --capture=tee-sys


db:
	@echo Starting database...
	@docker run -d --name pgvector -v ./postgresql:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=postgres ankane/pgvector