"""FastAPI application that renders the stock screener demo in the browser."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, TypedDict

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.core.screeners import Screen, james_os_shaughnessy_screen, peter_lynch_screen
from src.data.sample_data import Stock, filter_by_exchange, load_sample_universe

app = FastAPI(title="Stock Screener Demo")

_templates_dir = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(_templates_dir))


class ScreenContext(TypedDict):
    screen: Screen
    matches: List[Stock]


class ScreenerContext(TypedDict):
    peter: ScreenContext
    james: ScreenContext
    combined: List[Stock]


def _load_screen_results() -> ScreenerContext:
    """Return the unique set of stocks that pass either screen."""

    universe = load_sample_universe()
    exchanges = ["NYSE", "NASDAQ"]
    filtered = filter_by_exchange(universe, exchanges)

    peter_screen = peter_lynch_screen()
    james_screen = james_os_shaughnessy_screen()

    peter_matches = peter_screen.apply(filtered)
    james_matches = james_screen.apply(filtered)

    combined = {stock.symbol: stock for stock in peter_matches + james_matches}
    ordered = sorted(combined.values(), key=lambda stock: stock.symbol)

    return {
        "peter": {
            "screen": peter_screen,
            "matches": peter_matches,
        },
        "james": {
            "screen": james_screen,
            "matches": james_matches,
        },
        "combined": ordered,
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Render the browser-based demo."""

    context = _load_screen_results()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "screens": [
                {
                    "title": context["peter"]["screen"].name,
                    "criteria": [c.description for c in context["peter"]["screen"].criteria],
                    "match_count": len(context["peter"]["matches"]),
                },
                {
                    "title": context["james"]["screen"].name,
                    "criteria": [c.description for c in context["james"]["screen"].criteria],
                    "match_count": len(context["james"]["matches"]),
                },
            ],
            "stocks": context["combined"],
        },
    )


@app.get("/api/results")
async def api_results() -> Dict[str, Any]:
    """Return the raw screening payload for programmatic clients."""

    context = _load_screen_results()

    return {
        "screens": {
            "peter": {
                "name": context["peter"]["screen"].name,
                "criteria": [c.description for c in context["peter"]["screen"].criteria],
                "matches": [stock.symbol for stock in context["peter"]["matches"]],
            },
            "james": {
                "name": context["james"]["screen"].name,
                "criteria": [c.description for c in context["james"]["screen"].criteria],
                "matches": [stock.symbol for stock in context["james"]["matches"]],
            },
        },
        "combined": [
            {
                "symbol": stock.symbol,
                "name": stock.name,
                "exchange": stock.exchange,
                "market_cap_millions": stock.market_cap_millions,
                "eps_growth_5y": stock.eps_growth_5y,
                "pe_ratio": stock.pe_ratio,
                "peg_ratio": stock.peg_ratio,
                "debt_to_equity": stock.debt_to_equity,
                "industry": stock.industry,
            }
            for stock in context["combined"]
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.ui.api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
