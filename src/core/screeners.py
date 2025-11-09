"""Stock screener implementations inspired by famous investors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from rich.text import Text

from src.data.sample_data import Stock


@dataclass(frozen=True)
class ScreeningCriterion:
    """Represents a single rule within a screening template."""

    description: str

    def format(self) -> Text:
        text = Text(self.description)
        text.stylize("bold")
        return text


@dataclass(frozen=True)
class Screen:
    """A named collection of screening rules with helper metadata."""

    name: str
    criteria: Sequence[ScreeningCriterion]

    def apply(self, stocks: Iterable[Stock]) -> List[Stock]:
        """Return stocks that satisfy all of the screen's criteria."""

        filtered = list(stocks)
        for criterion in self.criteria:
            if hasattr(criterion, "predicate"):
                filtered = [stock for stock in filtered if criterion.predicate(stock)]
        return filtered


class PredicateCriterion(ScreeningCriterion):
    """Criterion that knows how to filter the dataset."""

    def __init__(self, description: str, predicate):
        super().__init__(description)
        self.predicate = predicate


def peter_lynch_screen() -> Screen:
    """Return a Peter Lynch inspired growth-at-reasonable-price screen."""

    return Screen(
        name="Peter Lynch Screen",
        criteria=[
            ScreeningCriterion("Exchange: NYSE, NASDAQ"),
            PredicateCriterion("Market Cap in Millions is Less Than 5000", lambda s: s.market_cap_millions < 5000),
            PredicateCriterion("EPS, 5-Year Growth, % is Greater Than 10", lambda s: s.eps_growth_5y > 10),
            PredicateCriterion("PEG Ratio is Less Than 1.5", lambda s: s.peg_ratio < 1.5),
            PredicateCriterion("P / E is Less Than 25", lambda s: s.pe_ratio < 25),
            PredicateCriterion(
                "Debt / Equity is Less Than 60",
                lambda s: s.debt_to_equity < 60,
            ),
        ],
    )


def james_os_shaughnessy_screen() -> Screen:
    """Return a value-oriented screen similar to O'Shaughnessy."""

    return Screen(
        name="James O'Shaughnessy Screen",
        criteria=[
            ScreeningCriterion("Exchange: NYSE"),
            PredicateCriterion("Market Cap in Millions is Greater Than 1000", lambda s: s.market_cap_millions > 1000),
            PredicateCriterion("P / E is Less Than 20", lambda s: s.pe_ratio < 20),
            PredicateCriterion("PEG Ratio is Less Than 1", lambda s: s.peg_ratio < 1),
            PredicateCriterion("Debt / Equity is Less Than 80", lambda s: s.debt_to_equity < 80),
        ],
    )
