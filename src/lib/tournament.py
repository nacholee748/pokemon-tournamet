from msilib.schema import SelfReg
import random
from secrets import randbits
from typing import List, Sequence, Tuple

from joblib import Parallel, delayed # type: ignore

from lib.battle import BattleSummary, Pokemon, simulate_battle


class Tournament:
    """A class to simulate a tournament between pokemons.

    Args:
        participants: the pokemons that will participate in the tournament.
        num_arenas: the available arenas to run battles simoultaneously.

    """

    def __init__(
        self, participants: Sequence[Pokemon], num_arenas: int, random_seed: int = 0
    ) -> None:
        self._paticipants = participants
        self._num_arenas = num_arenas
        self._next_matches = _create_matches(participants)
        random.seed(random_seed)

    def run_stage(self) -> List[BattleSummary]:
        """Runs all the battles defined in the current set of matches.

        After running this method, the property `current_matches` gets
        updated.

        This method returns the summary of each battle run during the stage.
        """
        battle_summary = []

        for _ in range(self._num_arenas):
            battle_summary.append(BattleSummary(self.next_matches(self._paticipants)))
        
        return battle_summary

    @property
    def next_matches(self) -> List[Tuple[Pokemon, Pokemon]]:
        return self._next_matches


def _create_matches(participants: Sequence[Pokemon])-> List[Tuple[Pokemon, Pokemon]]:
    """Takes a sequence of Pokémons and matches them randomly.

    If the sequence is not even then one participant will be matched with
    itself. No matter the input, this should happen at most once. If there

    `random_seed` is used for reproducible results.
    """
    participants = random.sample(participants,len(participants))
    participants_next_match = []

    if len(participants)%2:
        last_poke = participants.pop()
        participants_next_match.append((last_poke,last_poke))
    
    for i in range(0,len(participants),2):
        participants_next_match.append((participants[i],participants[i+1]))

    return participants_next_match


##########################3
# _create_matches([Pokemon(name = "pok1",
#                 generation =  "gen",
#                 type = "c",
#                 abilities = ("1","2"),
#                 health_points = 1.2,
#                 attack = 1,
#                 defense = 2,
#                 speed =  3),
#                 Pokemon(name = "pok2",
#                 generation =  "gen",
#                 type = "c",
#                 abilities = ("1","2"),
#                 health_points = 1.2,
#                 attack = 1,
#                 defense = 2,
#                 speed =  3),
#                 Pokemon(name = "pok3",
#                 generation =  "gen",
#                 type = "c",
#                 abilities = ("1","2"),
#                 health_points = 1.2,
#                 attack = 1,
#                 defense = 2,
#                 speed =  3),
#                 Pokemon(name = "pok4",
#                 generation =  "gen",
#                 type = "c",
#                 abilities = ("1","2"),
#                 health_points = 1.2,
#                 attack = 1,
#                 defense = 2,
#                 speed =  3),
#                 Pokemon(name = "pok5",
#                 generation =  "gen",
#                 type = "c",
#                 abilities = ("1","2"),
#                 health_points = 1.2,
#                 attack = 1,
#                 defense = 2,
#                 speed =  3),
#                 Pokemon(name = "pok2",
#                 generation =  "gen",
#                 type = "c",
#                 abilities = ("1","2"),
#                 health_points = 1.2,
#                 attack = 1,
#                 defense = 2,
#                 speed =  3)])