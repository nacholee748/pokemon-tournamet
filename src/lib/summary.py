from typing import Sequence, Dict

from lib.battle import Pokemon
from lib.reporting import Reporter
import pandas as pd
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
        return rounds['ability'].value_counts().index[0]

    @property
    def strongest_type(self) -> str:
        """The type that ranked better overall. """
        winners = self._reporter.read_winner_files()
        return winners['type'].value_counts().index[0]

    @property
    def strongest_generation(self) -> str:
        """
        The generation that was most common in later stages of the
        tournament.
        """
        import pandas as pd
        winners = self._reporter.read_winner_files()
        defeated = self._reporter.read_defeated_files()
        competitors = pd.concat([winners,defeated],ignore_index=True)
        stage = competitors['stage'].values.max()
        if stage > 3:
            stage = stage - 3
        
        gen_by_stage = competitors.groupby(['stage','generation'])['type'].count().reset_index()
        return gen_by_stage[gen_by_stage['stage']>=stage]['generation'].value_counts().index[0]

    @property
    def max_rounds_in_tournament(self) -> int:
        """The number of rounds """
        rounds = self._reporter.read_rounds_files()
        return len(rounds)

    @property
    def most_endurance(self) -> str:
        """Pokemon that resisted the most number of attacks in the tournament."""
        rounds = self._reporter.read_rounds_files()
        return rounds.groupby('defendant')['damage'].mean().reset_index().sort_values('damage',ascending=False).values[0][0]

    @property
    def participants_per_type(self) -> Dict[str, int]:
        winners = self._reporter.read_winner_files()
        defeated = self._reporter.read_defeated_files()
        competitors = pd.concat([winners,defeated],ignore_index=True)
        return competitors['type'].value_counts().to_dict()

    @property
    def in_top_fifty_per_type(self) -> Dict[str, int]:
        winners = self._reporter.read_winner_files()
        winners = winners.sort_values('type',ascending=False)[:50]
        
        return winners['type'].value_counts().to_dict() 

    @property
    def in_top_fifty_per_generation(self) -> Dict[str, int]:
        """A mapping from generation to position"""
        winners = self._reporter.read_winner_files()
        winners = winners.sort_values('stage',ascending=False)[:50]
        
        return winners['generation'].value_counts().to_dict()        



    