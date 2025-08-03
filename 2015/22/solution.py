import re
import sys
from enum import Enum
from typing import NamedTuple


class Player(NamedTuple):
    hit_points: int = 50
    mana: int = 500
    mana_used: int = 0


class Boss(NamedTuple):
    hit_points: int
    damage: int


class Effect(Enum):
    MAGIC_MISSILE = 'magic_missile'
    DRAIN = 'drain'
    SHIELD = 'shield'
    POISON = 'poison'
    RECHARGE = 'recharge'


class ActiveEffect(NamedTuple):
    effect: Effect
    turns: int


def read_input() -> Boss:
    hit_points = damage = None

    for line in sys.stdin:
        match = re.match(
            r'(?P<type>Hit Points|Damage): (?P<quantity>\d+)', line.strip()
        )
        if match['type'] == 'Hit Points':
            hit_points = int(match['quantity'])
        if match['type'] == 'Damage':
            damage = int(match['quantity'])

    if hit_points is None or damage is None:
        raise Exception('Invalid input file')

    return Boss(hit_points=hit_points, damage=damage)


def apply_effects(
    player: Player, boss: Boss, effects: list[ActiveEffect]
) -> (Player, Boss, list[ActiveEffect]):
    remaining_effects = []

    for active_effect in effects:
        if active_effect.effect == Effect.POISON:
            boss = boss._replace(hit_points=boss.hit_points - 3)

        if active_effect.effect == Effect.RECHARGE:
            player = player._replace(mana=player.mana + 101)

        if active_effect.turns > 1:
            remaining_effects.append(
                active_effect._replace(turns=active_effect.turns - 1)
            )

    return player, boss, remaining_effects


def player_turn(
    player: Player,
    boss: Boss,
    hard_mode: bool,
    effects: list[ActiveEffect] = [],
    best_so_far: int = sys.maxsize,
):
    if hard_mode:
        player = player._replace(hit_points=player.hit_points - 1)
        if player.hit_points <= 0:
            return None

    # Effects
    (player, boss, effects) = apply_effects(player, boss, effects)

    # Check win condition
    if boss.hit_points <= 0:
        return player.mana_used

    # Check loss condition
    if player.mana < 53:
        return None

    # Player turn
    if player.mana >= 53 and player.mana_used + 53 < best_so_far:
        score = player_attack(
            Effect.MAGIC_MISSILE, player, boss, hard_mode, effects, best_so_far
        )
        if score is not None and score < best_so_far:
            best_so_far = score

    if player.mana >= 73 and player.mana_used + 73 < best_so_far:
        score = player_attack(
            Effect.DRAIN, player, boss, hard_mode, effects, best_so_far
        )
        if score is not None and score < best_so_far:
            best_so_far = score

    if (
        player.mana >= 113
        and player.mana_used + 113 < best_so_far
        and not len(list(filter(lambda x: x.effect == Effect.SHIELD, effects)))
    ):
        score = player_attack(
            Effect.SHIELD, player, boss, hard_mode, effects, best_so_far
        )
        if score is not None and score < best_so_far:
            best_so_far = score

    if (
        player.mana >= 173
        and player.mana_used + 173 < best_so_far
        and not len(list(filter(lambda x: x.effect == Effect.POISON, effects)))
    ):
        score = player_attack(
            Effect.POISON, player, boss, hard_mode, effects, best_so_far
        )
        if score is not None and score < best_so_far:
            best_so_far = score

    if (
        player.mana >= 229
        and player.mana_used + 229 < best_so_far
        and not len(list(filter(lambda x: x.effect == Effect.RECHARGE, effects)))
    ):
        score = player_attack(
            Effect.RECHARGE, player, boss, hard_mode, effects, best_so_far
        )
        if score is not None and score < best_so_far:
            best_so_far = score

    return best_so_far


def player_attack(
    attack: Effect,
    player: Player,
    boss: Boss,
    hard_mode: bool,
    effects: list[ActiveEffect] = [],
    best_so_far: int = sys.maxsize,
):
    if attack == Effect.MAGIC_MISSILE:
        player = player._replace(mana=player.mana - 53, mana_used=player.mana_used + 53)
        boss = boss._replace(hit_points=boss.hit_points - 4)

    elif attack == Effect.DRAIN:
        player = player._replace(
            mana=player.mana - 73,
            mana_used=player.mana_used + 73,
            hit_points=player.hit_points + 2,
        )
        boss = boss._replace(hit_points=boss.hit_points - 2)

    elif attack == Effect.SHIELD:
        player = player._replace(
            mana=player.mana - 113, mana_used=player.mana_used + 113
        )
        effects = effects + [ActiveEffect(effect=Effect.SHIELD, turns=6)]

    elif attack == Effect.POISON:
        player = player._replace(
            mana=player.mana - 173, mana_used=player.mana_used + 173
        )
        effects = effects + [ActiveEffect(effect=Effect.POISON, turns=6)]

    elif attack == Effect.RECHARGE:
        player = player._replace(
            mana=player.mana - 229, mana_used=player.mana_used + 229
        )
        effects = effects + [ActiveEffect(effect=Effect.RECHARGE, turns=5)]

    return boss_turn(player, boss, hard_mode, effects, best_so_far)


def boss_turn(
    player: Player,
    boss: Boss,
    hard_mode: bool,
    effects: list[ActiveEffect] = [],
    best_so_far: int = sys.maxsize,
):
    # Check win condition
    if boss.hit_points <= 0:
        return player.mana_used

    shield = 7 if len(list(filter(lambda x: x.effect == Effect.SHIELD, effects))) else 0

    # Effects
    (player, boss, effects) = apply_effects(player, boss, effects)

    # Check win condition
    if boss.hit_points <= 0:
        return player.mana_used

    # Boss turn
    player = player._replace(
        hit_points=player.hit_points - max(boss.damage - shield, 1)
    )

    # Check loss condition
    if player.hit_points <= 0:
        return None

    return player_turn(player, boss, hard_mode, effects, best_so_far)


boss = read_input()
print(player_turn(player=Player(), boss=boss, hard_mode=False))
print(player_turn(player=Player(), boss=boss, hard_mode=True))
