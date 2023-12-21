<?php

function find_passage(array $discs): ?int
{
    $first = array_pop($discs);

    for ($timing = $first['positions'] - $first['offset'] - $first['distance']; ; $timing += $first['positions']) {
        foreach ($discs as &$disc) {
            if (($timing + $disc['distance'] + $disc['offset']) % $disc['positions']) {
                continue 2;
            }
        }

        return $timing;
    }

    return null;
}

$discs = [];

while (preg_match('/Disc \#(\d+) has (\d+) positions; at time=0, it is at position (\d+)./', fgets(STDIN), $disc)) {
    $discs[] = [
        'distance'  => intval($disc[1]),
        'positions' => intval($disc[2]),
        'offset'    => intval($disc[3])
    ];
}

fwrite(STDOUT, find_passage($discs) . PHP_EOL);

$discs[] = [
    'distance'  => 1 + max(array_map(function ($disc) {
            return $disc['distance'];
        }, $discs)),
    'positions' => 11,
    'offset'    => 0
];

fwrite(STDOUT, find_passage($discs) . PHP_EOL);
