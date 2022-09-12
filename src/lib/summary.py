from typing import Sequence, Dict

from lib.battle import Pokemon
from lib.reporting import Reporter

class Summary:
    def __init__(self, participants: Sequence[Pokemon], reporter: Reporter) -> None:
        self._paticipants = participants
        self._reporter = reporter

    @property
    def num_paticipants(self) -> int:
        return len(self._paticipants)
        

    @property
    def champion(self) -> str:
        winners = self._reporter.read_winner_files()
        return winners[winners['stage'] == winners['stage'].max()]['name'].values[-1]

    @property
    def most_common_ability_used_in_battle(self) -> str:
        rounds = self._reporter.read_rounds_files()
        return rounds.groupby(['ability'])['ability'].count().sort_values(ascending=False).index[0]

    @property
    def strongest_type(self) -> str:
        """The type that ranked better overall. """
        # rounds = self._reporter.read_rounds_files()
        # a = rounds.groupby(['damage'])['attacker'].agg('max')
        return "Pokèmon"

    @property
    def strongest_generation(self) -> str:
        """
        The generation that was most common in later stages of the
        tournament.
        """
        return "Pokèmon"

    @property
    def max_rounds_in_tournament(self) -> int:
        """The number of rounds """
        return 3

    @property
    def most_endurance(self) -> str:
        """Pokemon that resisted the most number of attacks in the tournament."""
        return "Bulbasaur"

    @property
    def participants_per_type(self) -> Dict[str, int]:
        return {"Type1": 1, "Type2": 2}

    @property
    def in_top_fifty_per_type(self) -> Dict[str, int]:
        return {"Type1": 1, "Type2": 2}

    @property
    def in_top_fifty_per_generation(self) -> Dict[str, int]:
        """A mapping from generation to position"""
        return {"Gen1": 1, "Gen2": 2}


    