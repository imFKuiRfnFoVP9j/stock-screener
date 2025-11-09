# Stock Screener Demo

This repository contains a simple stock screener inspired by the MarketInOut layout shown in the prompt. It now ships with both a Rich-powered CLI and a browser experience so you can explore the sample screens interactively before wiring in live market data.

## Getting Started

```bash
poetry install

# Launch the FastAPI app at http://127.0.0.1:8000
poetry run uvicorn src.ui.api:app --reload

# Or run directly with the Python module entry point
python -m src.ui.api

# Or run the original console walkthrough
poetry run python -m src.ui.cli
```

Both interfaces showcase the Peter Lynch and James O'Shaughnessy templates along with the combined list of matching stocks from the bundled sample universe.

## Project Structure

- `src/data/` – sample dataset and lightweight helpers.
- `src/core/` – reusable screening rules.
- `src/ui/` – console user interface powered by [Rich](https://rich.readthedocs.io/) and a FastAPI-powered web demo.

## Next Steps

Replace the sample dataset with live market data, add persistence for custom screens, or expose the logic via a web dashboard.
