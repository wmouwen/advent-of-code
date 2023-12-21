<?php

$changes = [];
while (preg_match('/(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)./', fgets(STDIN), $matches)) {
    list(, $person, $gain_or_lose, $units, $neighbour) = $matches;
    $changes[$person][$neighbour] = ($gain_or_lose === 'gain' ? 1 : -1) * intval($units);
}

function max_happiness(array &$changes, array $remaining, array $seating): int
{
    if (empty($remaining)) {
        $happiness = 0;
        for ($i = 0; $i < count($seating); $i++) {
            $happiness += $changes[$seating[$i]][$seating[($i + 1) % count($seating)]] ?? 0;
            $happiness += $changes[$seating[($i + 1) % count($seating)]][$seating[$i]] ?? 0;
        }

        return $happiness;
    }

    $max = PHP_INT_MIN;
    foreach ($remaining as $next) {
        $max = max($max, max_happiness($changes, array_diff($remaining, [$next]), array_merge($seating, [$next])));
    }

    return $max;
}

$remaining = array_keys($changes);
$seating   = [array_pop($remaining)];
fwrite(STDOUT, max_happiness($changes, $remaining, $seating) . PHP_EOL);
fwrite(STDOUT, max_happiness($changes, array_merge($remaining, ['Self']), $seating) . PHP_EOL);