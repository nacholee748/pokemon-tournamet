import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple, Protocol

from lib.battle import BattleSummary, Pokemon

class WithName(Protocol):
    name: str


class Reporter:
    """Persists the results matches into permanent storage. """
    def __init__(self, dir: Path) -> None:
        self._filepath = dir / "report.json"
        self._report: Dict[str, str] = {}
        self._num_stages = 0

    def update(
        self, *, stage: int, results: Sequence[BattleSummary]
    ) -> None:
        """
        Updtes the internal registry of matches, as well as the num_stages
        property.
        """
        pass

    def review_battle(self, p1: str, p2: str) -> str:
        """
        *Quickly* return the result of a particular match defined by the
        provided parameters.

        Raise a ValueError if the provided participants have not had a match.
        """
        return "Pokèmon"

    def review_stage(self, stage: int) -> List[Tuple[str, str]]:
        """Returns the battles at a particular stage. """
        return [("Pokèmon", "Pokèmon")]


    @property
    def num_stages(self):
        return self._num_stages