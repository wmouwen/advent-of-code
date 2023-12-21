<?php

const DIRECTION = [
    'n'  => [1, -1, 0],
    'ne' => [0, -1, 1],
    'se' => [-1, 0, 1],
    's'  => [-1, 1, 0],
    'sw' => [0, 1, -1],
    'nw' => [1, 0, -1]
];

$x = $y = $z = $max = 0;

foreach (explode(',', trim(fgets(STDIN))) as $step) {
    $max = max(
        $max,
        abs($x += DIRECTION[$step][0]),
        abs($y += DIRECTION[$step][1]),
        abs($z += DIRECTION[$step][2])
    );
}

fwrite(STDOUT, max(abs($x), abs($y), abs($z)) . PHP_EOL);
fwrite(STDOUT, $max . PHP_EOL);