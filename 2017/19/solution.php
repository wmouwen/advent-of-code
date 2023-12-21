<?php

$grid = [];
while ($line = fgets(STDIN)) {
    $grid[] = str_split(rtrim($line, PHP_EOL));
}

$letters = [];
$steps   = 0;

for ($x = array_search('|', $grid[0]), $y = 0, $dx = 0, $dy = 1; ; $x += $dx, $y += $dy, $steps++) {
    switch ($grid[$y][$x] ?? ' ') {
        case '|':
        case '-':
            break;

        case ' ':
            break 2;

        case '+':
            if ($dx === 0) {
                $dx = ($grid[$y][$x - 1] ?? ' ') === ' ' ? 1 : -1;
                $dy = 0;
            } else {
                $dx = 0;
                $dy = ($grid[$y - 1][$x] ?? ' ') === ' ' ? 1 : -1;
            }
            break;

        default:
            $letters[] = $grid[$y][$x];
            break;
    }
}

fwrite(STDOUT, implode($letters) . PHP_EOL . $steps . PHP_EOL);