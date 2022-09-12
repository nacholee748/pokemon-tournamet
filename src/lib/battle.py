import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

from lib.pokemon import Pokemon

@dataclass
class BattleRound:
    attacker: str
    defendant: str
    damage: float
    ability: str

@dataclass
class BattleSummary:
    winner: Pokemon
    defeated: Pokemon
    rounds: List[BattleRound]


def simulate_battle(p1: Pokemon, p2: Pokemon, random_seed: int = 0) -> BattleSummary:
    """This function simulates a single battle between two Pokémons.

    A battle consists of several rounds, at each round there is only one Pokémon
    doing the attack, while the other is defending. The role at each turn
    is defined randomly and each participant has a random chance of being
    selected as the attacker, weigthed by the amount abilities of the
    participant over the total number of abilities of both participants. For
    example, if `p1` has 2 abilities, while `p2` has only one, then `p1` is
    expected to be selected as the attacker 66.66% of the time.

    Since a battle is a random process, we will repeat each battle a thousand
    times and pick the winner as the most common winner in all battles, as well
    as picking the least number of rounds in which the winner won.

    Each battle comes to an end whenever the health points of any of the
    Pokémons reaches 0 or there are 100 rounds. At each turn of the battle,
    the health points of the attacker remain the same, while the ones for the
    defendant are computed as:

        damage = attacker.attack * random.betavariate(1, 5)
        HP_t+1 = HP_t - damage (Health points of the defendant at time t)


    This function is provided a random_seed value, so that the battle always
    yields the same results.
    """
    if p1.name == p2.name:
        return BattleSummary(winner=p1,defeated=p2,rounds=[])

    random.seed(random_seed)
    winner_count: Dict[str,int]  = {p1.name:0,p2.name:0}
    winner_rounds: Dict[str,list]  = {p1.name:[],p2.name:[]}

    for _ in range(1000):
        result = one_battle(p1,p2)
        winner_count[result.winner.name] += 1

        if winner_rounds[result.winner.name]:
            if len(result.rounds) < len(winner_rounds[result.winner.name]):
                winner_rounds[result.winner.name] = result.rounds
        else:
            winner_rounds[result.winner.name] = result.rounds

    winner_name = sorted(winner_count.items(), key=lambda x: x[1])[0][0]
    if winner_name == p1.name:
        defeated =p2
        winner = p1
    else:
        defeated =p1
        winner = p2

    summary = BattleSummary(winner=winner,defeated=defeated,rounds=winner_rounds)
    
    return summary

def one_battle(p1: Pokemon,p2: Pokemon) -> BattleSummary:
    rounds = []
    probability_of_p1_begin_attacker = len(p1.abilities)/(len(p1.abilities)+len(p2.abilities))
    health_points = {p1.name: p1.health_points,p2.name: p2.health_points}

    while len(rounds)<=100 and (health_points[p1.name] > 0 and health_points[p2.name] > 0):
        if random.random() <= probability_of_p1_begin_attacker:
            attacker = p1
            defendant = p2
        else:
            attacker = p2
            defendant = p1

        damage = attacker.attack * random.betavariate(1,5)
        health_points[defendant.name] -= damage

        rounds.append(
            BattleRound(
                attacker=attacker.name,
                defendant=defendant.name,
                damage=damage,
                ability=random.choice(attacker.abilities)
            )
        )

        defeated_name=sorted(health_points.items(), key = lambda x: x[1])[0][0]
        if defeated_name == p1.name:
            defeated = p1
            winner = p2
        else:
            defeated = p2
            winner = p1
        
        summary = BattleSummary(winner=winner, defeated=defeated, rounds=rounds)

        return summary
