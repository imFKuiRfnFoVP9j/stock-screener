"""Sample stock universe used by the CLI demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class Stock:
    """Minimal representation of a stock needed for the demo screeners."""

    symbol: str
    name: str
    exchange: str
    market_cap_millions: float
    eps_growth_5y: float
    pe_ratio: float
    peg_ratio: float
    debt_to_equity: float
    industry: str


def load_sample_universe() -> List[Stock]:
    """Return a curated list of stocks that loosely match the screenshot."""

    return [
        Stock(
            symbol="ACLR",
            name="Accelera Pharma",
            exchange="NYSE",
            market_cap_millions=1550,
            eps_growth_5y=36.8,
            pe_ratio=21.3,
            peg_ratio=0.58,
            debt_to_equity=12.5,
            industry="Biotechnology",
        ),
        Stock(
            symbol="AFBI",
            name="Affinity Bancshares",
            exchange="NASDAQ",
            market_cap_millions=480,
            eps_growth_5y=12.4,
            pe_ratio=13.5,
            peg_ratio=0.95,
            debt_to_equity=58.2,
            industry="Banks",
        ),
        Stock(
            symbol="AGCO",
            name="AGCO Corporation",
            exchange="NYSE",
            market_cap_millions=9800,
            eps_growth_5y=18.1,
            pe_ratio=14.2,
            peg_ratio=0.78,
            debt_to_equity=45.6,
            industry="Farm & Heavy Machinery",
        ),
        Stock(
            symbol="AGM",
            name="Federal Agricultural Mtg",
            exchange="NYSE",
            market_cap_millions=1500,
            eps_growth_5y=15.6,
            pe_ratio=9.3,
            peg_ratio=0.62,
            debt_to_equity=210.4,
            industry="Credit Services",
        ),
        Stock(
            symbol="AMAL",
            name="Amalgamated Financial",
            exchange="NASDAQ",
            market_cap_millions=1110,
            eps_growth_5y=9.5,
            pe_ratio=9.9,
            peg_ratio=1.04,
            debt_to_equity=58.8,
            industry="Banks",
        ),
        Stock(
            symbol="AMRK",
            name="A-Mark Precious Metals",
            exchange="NASDAQ",
            market_cap_millions=930,
            eps_growth_5y=27.4,
            pe_ratio=7.4,
            peg_ratio=0.43,
            debt_to_equity=57.9,
            industry="Capital Markets",
        ),
        Stock(
            symbol="ATKR",
            name="Atkore Inc",
            exchange="NYSE",
            market_cap_millions=6350,
            eps_growth_5y=42.7,
            pe_ratio=8.2,
            peg_ratio=0.36,
            debt_to_equity=74.5,
            industry="Electrical Components",
        ),
        Stock(
            symbol="AX",
            name="Axos Financial",
            exchange="NYSE",
            market_cap_millions=2500,
            eps_growth_5y=19.1,
            pe_ratio=10.8,
            peg_ratio=0.57,
            debt_to_equity=62.4,
            industry="Banks",
        ),
    ]


def filter_by_exchange(stocks: Iterable[Stock], exchanges: Iterable[str]) -> List[Stock]:
    """Return stocks that trade on one of the desired exchanges."""

    allowed = {exchange.upper() for exchange in exchanges}
    return [stock for stock in stocks if stock.exchange.upper() in allowed]
