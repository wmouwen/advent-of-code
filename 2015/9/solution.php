<?php

$distances = [];
while (preg_match('/(\w+) to (\w+) = (\d+)/', fgets(STDIN), $matches)) {
    list(, $a, $b, $distance) = $matches;
    $distances[$a][$b] = $distances[$b][$a] = intval($distance);
}

function tsp(array &$distances, array $remaining, string $location = null, int $travelled = 0, array &$records = [PHP_INT_MAX, PHP_INT_MIN]): array
{
    if (empty($remaining)) {
        $records = [min($records[0], $travelled), max($records[1], $travelled)];
    } else {
        foreach ($remaining as $next) {
            tsp($distances, array_diff($remaining, [$next]), $next, $travelled + ($distances[$location][$next] ?? 0), $records);
        }
    }

    return $records;
}

$records = tsp($distances, array_keys($distances));
fwrite(STDOUT, $records[0] . PHP_EOL);
fwrite(STDOUT, $records[1] . PHP_EOL);