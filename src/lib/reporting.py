import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple, Protocol
import os
import pandas as pd

from lib.battle import BattleSummary, Pokemon, one_battle


class WithName(Protocol):
    name: str

class Reporter:
    """Persists the results matches into permanent storage. """
    def __init__(self, dir: Path) -> None:
        self._filepath = dir
        self._report: Dict[str, str] = {}
        self._num_stages = 0
        _reset_folder_poke_data(dir)

    def update(
        self, *, stage: int, results: Sequence[BattleSummary]
    ) -> None:
        """
        Updtes the internal registry of matches, as well as the num_stages
        property.
        """
        df_winner, df_defeated, df_rounds  = [], [], []
        for item in results:
            df_winner.append({'stage':stage,'name':item.winner.name,'generation':item.winner.generation, 'type':item.winner.type, 'abilities':item.winner.abilities, 'health_points':item.winner.health_points, 'attack':item.winner.attack, 'defense':item.winner.defense, 'speed':item.winner.speed})
            df_defeated.append({'stage':stage,'name':item.defeated.name,'generation':item.defeated.generation, 'type':item.defeated.type, 'abilities':item.defeated.abilities, 'health_points':item.defeated.health_points, 'attack':item.defeated.attack, 'defense':item.defeated.defense, 'speed':item.defeated.speed})
            
            if len(item.rounds) > 0:
                for round in item.rounds:
                    for item_round in item.rounds[round]:
                        df_rounds.append({'stage':stage,'attacker':item_round.attacker,'defendant':item_round.defendant, 'damage':item_round.damage, 'ability':item_round.ability})
        
        df_winner = pd.DataFrame(df_winner)
        df_defeated = pd.DataFrame(df_defeated)
        df_rounds = pd.DataFrame(df_rounds)

        winner_path = os.path.join(self._filepath,"poke-data","winner.csv")
        df_winner.to_csv(winner_path, mode='a', header=not os.path.exists(winner_path))

        defeated_path = os.path.join(self._filepath,"poke-data","defeated.csv")
        df_defeated.to_csv(defeated_path, mode='a', header=not os.path.exists(defeated_path))

        rounds_path = os.path.join(self._filepath,"poke-data","rounds.csv")
        df_rounds.to_csv(rounds_path, mode='a', header=not os.path.exists(rounds_path))

        pass

    def review_battle(self, p1: str, p2: str) -> str:
        """
        *Quickly* return the result of a particular match defined by the
        provided parameters.

        Raise a ValueError if the provided participants have not had a match.
        """
        one_battle()
        return "Pokèmon"

    def review_stage(self, stage: int) -> List[Tuple[str, str]]:
        """Returns the battles at a particular stage. """
        rounds = self.read_rounds_files()        
        return (list(rounds[rounds['stage']==stage][(['attacker','defendant'])]))

    @property
    def num_stages(self):
        return self._num_stages
        
    def read_winner_files(self)->pd.DataFrame:
        winner_path = os.path.join(self._filepath,"poke-data","winner.csv")
        winner = pd.read_csv(winner_path)
        return winner

    def read_defeated_files(self)->pd.DataFrame:
        defeated_path = os.path.join(self._filepath,"poke-data","defeated.csv")
        defeated = pd.read_csv(defeated_path)
        return defeated

    def read_rounds_files(self)->pd.DataFrame:
        rounds_path = os.path.join(self._filepath,"poke-data","rounds.csv")
        rounds = pd.read_csv(rounds_path)
        return rounds

def _reset_folder_poke_data(current_path: Path):
    files = ['winner','defeated','rounds']
    for file in files:
        filePath = os.path.join(current_path,"poke-data",f"{file}.csv")
        if os.path.exists(filePath):
            os.remove(filePath)




