<?php

const FINISH     = [31, 39];
const DIRECTIONS = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0]
];

function is_a_wall(int $x, int $y, int &$addition): bool
{
    if ($x < 0 || $y < 0) {
        return true;
    }

    return (substr_count(decbin($x * $x + 3 * $x + 2 * $x * $y + $y + $y * $y + $addition), 1) & 1) === 1;
}

$distances = [];
$addition  = intval(trim(fgets(STDIN)));
$todo      = [[1, 1]];

for ($distance = 0; ($distance <= 50 || !isset($distances[FINISH[1]][FINISH[0]])) && !empty($todo); $distance++) {
    $next = [];
    foreach ($todo as list($x, $y)) {
        $distances[$y][$x] = $distance;
        foreach (DIRECTIONS as list($dx, $dy)) {
            if (!isset($distances[$y + $dy][$x + $dx]) && !is_a_wall($x + $dx, $y + $dy, $addition)) {
                $next[] = [$x + $dx, $y + $dy];
            }
        }
    }
    $todo = $next;
}

fwrite(STDOUT, ($distances[FINISH[1]][FINISH[0]] ?? -1) . PHP_EOL);
fwrite(STDOUT, array_sum(array_map(function ($row) {
        return array_sum(array_map(function ($cell) {
            return $cell <= 50 ? 1 : 0;
        }, $row));
    }, $distances)) . PHP_EOL);