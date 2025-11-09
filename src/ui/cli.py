"""Console interface that mimics the MarketInOut screenshot layout."""

from __future__ import annotations

from typing import Iterable, List

from rich.console import Console
from rich.table import Table

from src.core.screeners import james_os_shaughnessy_screen, peter_lynch_screen
from src.data.sample_data import Stock, filter_by_exchange, load_sample_universe


def _render_criteria(console: Console, screen_name: str, criteria: Iterable[str]) -> None:
    console.print(f"[bold cyan]{screen_name}[/bold cyan]")
    for description in criteria:
        console.print(f"  • {description}")


def _build_results_table(stocks: List[Stock]) -> Table:
    table = Table(title="Overview", show_lines=False)
    table.add_column("Symbol", justify="left", style="bold")
    table.add_column("Name", justify="left")
    table.add_column("Exchange", justify="left")
    table.add_column("Market Cap ($M)", justify="right")
    table.add_column("EPS 5Y %", justify="right")
    table.add_column("P/E", justify="right")
    table.add_column("PEG", justify="right")
    table.add_column("Debt/Equity", justify="right")
    table.add_column("Industry", justify="left")

    for stock in stocks:
        table.add_row(
            stock.symbol,
            stock.name,
            stock.exchange,
            f"{stock.market_cap_millions:,.0f}",
            f"{stock.eps_growth_5y:.1f}",
            f"{stock.pe_ratio:.1f}",
            f"{stock.peg_ratio:.2f}",
            f"{stock.debt_to_equity:.1f}",
            stock.industry,
        )
    return table


def run_cli() -> None:
    """Entry point used by ``python -m src.ui.cli``."""

    console = Console()
    universe = load_sample_universe()

    peter_screen = peter_lynch_screen()
    james_screen = james_os_shaughnessy_screen()

    console.rule("Stock Screener Demo")

    _render_criteria(console, peter_screen.name, [c.description for c in peter_screen.criteria])
    console.print()
    _render_criteria(console, james_screen.name, [c.description for c in james_screen.criteria])

    console.print("\n[bold underline]Overview[/bold underline]")

    exchanges = ["NYSE", "NASDAQ"]
    filtered = filter_by_exchange(universe, exchanges)

    peter_matches = peter_screen.apply(filtered)
    james_matches = james_screen.apply(filtered)

    combined = {stock.symbol: stock for stock in peter_matches + james_matches}
    ordered = sorted(combined.values(), key=lambda stock: stock.symbol)

    console.print(_build_results_table(ordered))
    console.print("\n[i]Use this demo as a starting point for real market data integrations.[/i]")


if __name__ == "__main__":
    run_cli()
