<?php

// TODO: INCORRECT RESULTS

function battle(
    int $boss_hp, int $boss_damage, bool $hard_mode = false,
    int $hit_points = 100, int $mana_left = 500,
    int $mana_spent = 0, bool $player_turn = true,
    int $shield = 0, int $poison = 0, int $recharge = 0,
    int &$result = PHP_INT_MAX
): int
{
    if ($hard_mode && $player_turn) {
        $hit_points--;
    }

    if ($hit_points <= 0) {
        return $result;
    }

    if ($shield > 0) {
        $shield--;
    }

    if ($poison > 0) {
        $poison--;
        $boss_hp -= 3;
    }

    if ($recharge > 0) {
        $recharge--;
        $mana_left += 101;
    }

    if ($boss_hp <= 0) {
        return $mana_spent;
    }

    if ($player_turn) {
        // Magic Missile
        $cost = 53;
        if ($mana_left >= $cost && $mana_spent + $cost < $result) {
            $result = min($result, battle(
                $boss_hp - 4, $boss_damage, $hard_mode,
                $hit_points, $mana_left - $cost,
                $mana_spent + $cost, !$player_turn,
                $shield, $poison, $recharge,
                $result
            ));
        }

        // Drain
        $cost = 73;
        if ($mana_left >= $cost && $mana_spent + $cost < $result) {
            $result = min($result, battle(
                $boss_hp - 2, $boss_damage, $hard_mode,
                $hit_points + 2, $mana_left - $cost,
                $mana_spent + $cost, !$player_turn,
                $shield, $poison, $recharge,
                $result
            ));
        }

        // Shield
        $cost = 113;
        if ($mana_left >= $cost && !$shield && $mana_spent + $cost < $result) {
            $result = min($result, battle(
                $boss_hp, $boss_damage, $hard_mode,
                $hit_points, $mana_left - $cost,
                $mana_spent + $cost, !$player_turn,
                6, $poison, $recharge,
                $result
            ));
        }

        // Poison
        $cost = 173;
        if ($mana_left >= $cost && !$poison && $mana_spent + $cost < $result) {
            $result = min($result, battle(
                $boss_hp, $boss_damage, $hard_mode,
                $hit_points, $mana_left - $cost,
                $mana_spent + $cost, !$player_turn,
                $shield, 6, $recharge,
                $result
            ));
        }

        // Recharge
        $cost = 229;
        if ($mana_left >= $cost && !$recharge && $mana_spent + $cost < $result) {
            $result = min($result, battle(
                $boss_hp, $boss_damage, $hard_mode,
                $hit_points, $mana_left - $cost,
                $mana_spent + $cost, !$player_turn,
                $shield, $poison, 5,
                $result
            ));
        }

    } elseif ($hit_points >= 0) {
        // Boss attack
        $result = min($result, battle(
            $boss_hp, $boss_damage, $hard_mode,
            $hit_points - $boss_damage + ($shield ? 7 : 0), $mana_left,
            $mana_spent, !$player_turn,
            $shield, $poison, $recharge,
            $result
        ));
    }

    return $result;
}

$boss_hp     = 0;
$boss_damage = 0;

while (preg_match('/^([\w\s]+): (\d+)$/', fgets(STDIN), $stat)) {
    switch ($stat[1]) {
        case 'Hit Points':
            $boss_hp = intval($stat[2]);
            break;
        case 'Damage':
            $boss_damage = intval($stat[2]);
            break;
    }
}

fwrite(STDOUT, battle($boss_hp, $boss_damage) . PHP_EOL);
fwrite(STDOUT, battle($boss_hp, $boss_damage, true) . PHP_EOL);