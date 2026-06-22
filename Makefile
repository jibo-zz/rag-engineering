run-podman-compose:
	uv sync
	podman machine start 2>/dev/null || true
	podman compose -f docker-compose.yml up --build

clean-notebook-output:
	uv run jupyter nbconvert --clear-output --inplace notebooks/*/*.ipynb

run-evals-retriever:
	uv sync
	PYTHONPATH=${PWD}/apps/api:${PWD}/apps/api/src:$$PYTHONPATH:${PWD} uv run --env-file .env python -m evals.eval_retriever