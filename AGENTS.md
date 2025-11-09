# Repository Guidelines

## Project Structure & Module Organization
Code lives in `src/`, split into `core/` for screening logic, `data/` for vendor adapters, and `ui/` for CLI or dashboard layers. Shared configs belong in `config/`, datasets and fixtures in `data/inputs/`, and reusable Jupyter experiments in `notebooks/`. Place fast-running unit suites in `tests/unit/` and end-to-end orchestration specs in `tests/integration/`; mirror module names so `src/data/pricing.py` pairs with `tests/unit/data/test_pricing.py`.

## Build, Test, and Development Commands
- `poetry install` — resolve dependencies and set up the managed virtual environment.
- `poetry run uvicorn src.ui.api:app --reload` — start the local API/UI shell for interactive screening.
- `poetry run pytest` — execute the entire automated suite; add `-k pattern` for focused runs.
- `poetry run ruff check src tests` and `poetry run black src tests` — lint and auto-format before every push.

## Coding Style & Naming Conventions
Follow PEP 8 with Black’s default 88-character line width, four-space indentation, and Ruff’s diagnostic set. Name modules with snake_case, exported classes with CapWords, and async coroutines with verbs such as `fetch_quotes`. Environment variables use the `SCREENER_*` prefix (e.g., `SCREENER_ALPHA_VANTAGE_KEY`).

## Testing Guidelines
Target ≥85% statement coverage on `pytest --cov=src`. Keep test names descriptive (`test_returns_sorted_candidates`) and isolate network calls with VCR cassettes stored under `tests/fixtures/vcr/`. Add a regression test whenever you fix a bug or add a new screening rule.

## Commit & Pull Request Guidelines
Use Conventional Commits (`feat:`, `fix:`, `chore:`, etc.) and keep subject lines under 72 characters. Every PR should include: a summary of changes, linked issue IDs, screenshots or CLI captures for user-visible updates, and confirmation that `pytest`, `ruff`, and `black` were run locally. Request at least one reviewer for logic changes touching `src/core/`.

## Security & Configuration Tips
Store API secrets in `.env` (never commit) and load them through `pydantic` settings models. When adding new data vendors, document required scopes in `docs/integrations.md` and gate usage behind feature flags defined in `config/features.yaml`.
