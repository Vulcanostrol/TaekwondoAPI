from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple, Generator

from tournament import models


@dataclass(frozen=True)
class CompetitionClass:
    name: str
    description: str
    level: int


BELT_TO_GRADE_MAPPING: Dict[str, CompetitionClass] = {}

A_CLASS = CompetitionClass(
    name="A-Class",
    description="1st Dan and up",
    level=4,
)
BELT_TO_GRADE_MAPPING.update({
    "1D": A_CLASS,
    "2D": A_CLASS,
    "3D": A_CLASS,
    "4D": A_CLASS,
    "5D": A_CLASS,
})

B_CLASS = CompetitionClass(
    name="B-Class",
    description="blue to red-black",
    level=3,
)
BELT_TO_GRADE_MAPPING.update({
    "BL": B_CLASS,
    "BR": B_CLASS,
    "RE": B_CLASS,
    "RB": B_CLASS,
})

C_CLASS = CompetitionClass(
    name="D-Class",
    description="Yellow to green-blue",
    level=2,
)
BELT_TO_GRADE_MAPPING.update({
    "YE": C_CLASS,
    "YG": C_CLASS,
    "GR": C_CLASS,
    "GB": C_CLASS,
})

D_CLASS = CompetitionClass(
    name="D-Class",
    description="White to white-yellow",
    level=1,
)
BELT_TO_GRADE_MAPPING.update({
    "WH": D_CLASS,
    "WY": D_CLASS,
})


AGE_GROUPS: Dict[str, List[Tuple[int, int]]] = {
    models.Pool.PoolType.Solo: [
        (0, 8), (9, 11), (12, 14), (15, 17), (18, 30), (31, 40), (41, 50), (51, 60), (61, 65), (66, 100),
    ],
    models.Pool.PoolType.Pair: [
        (0, 11), (12, 14), (15, 17), (18, 30), (31, 100),
    ],
    models.Pool.PoolType.Team: [
        (0, 11), (12, 14), (15, 17), (18, 30), (31, 100),
    ],
    models.Pool.PoolType.Para: [
        (0, 17), (18, 100),
    ],
}


def belt_grade_to_class(belt_grade: str) -> CompetitionClass:
    if belt_grade not in BELT_TO_GRADE_MAPPING:
        raise KeyError(f"Belt grade {belt_grade} not one of: {[grade[0] for grade in models.Participant.BELT_GRADES]}.")
    return BELT_TO_GRADE_MAPPING[belt_grade]


ClassPoolsType = Dict[str, Dict[str, models.Pool]]
def make_class_pools(tournament: models.Tournament) -> ClassPoolsType:
    pool_type_solo = models.Pool.PoolType.Solo
    pool_type_pair = models.Pool.PoolType.Pair
    pair_pool = models.Pool(tournament=tournament, pool_type=pool_type_pair)
    pool_type_team = models.Pool.PoolType.Team
    return {
        pool_type_solo: {
            "F": models.Pool(tournament=tournament, pool_type=pool_type_solo),
            "M": models.Pool(tournament=tournament, pool_type=pool_type_solo),
        },
        pool_type_pair: {
            "F": pair_pool,
            "M": pair_pool,
        },
        pool_type_team: {
            "F": models.Pool(tournament=tournament, pool_type=pool_type_team),
            "M": models.Pool(tournament=tournament, pool_type=pool_type_team),
        }
    }


TournamentPoolsType = Dict[CompetitionClass, ClassPoolsType]
def make_tournament_pools(tournament: models.Tournament) -> TournamentPoolsType:
    return {
        D_CLASS: make_class_pools(tournament),
        C_CLASS: make_class_pools(tournament),
        B_CLASS: make_class_pools(tournament),
        A_CLASS: make_class_pools(tournament),
    }


def tournament_pools_walker(pools: TournamentPoolsType) -> Generator[models.Pool, None, None]:
    for class_pools in pools.values():
        for team_type_pool in class_pools.values():
            for sex_pool in team_type_pool.values():
                yield sex_pool
