start:
	@echo Starting FastAPI server...
	@uvicorn main:app --reload

test:
	@echo Running tests...
	@pytest -s --log-cli-level=DEBUG --capture=tee-sys