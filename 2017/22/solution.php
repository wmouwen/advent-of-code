<?php

$lines = [];
while ($line = trim(fgets(STDIN))) {
    $lines[] = str_split($line);
}

$grid = [];
foreach ($lines as $line) {
    $grid[] = array_map(function ($cell) {
        return $cell == '#' ? 1 : 0;
    }, $line);
}

$y   = intval(count($grid) / 2);
$x   = intval(count($grid[$y]) / 2);
$dir = 0;

$infections = 0;

for ($burst = 10000; $burst; $burst--) {
    $grid[$y][$x] = $grid[$y][$x] ?? 0;

    switch ($grid[$y][$x]) {
        case 0:
            $dir = ($dir + 3) % 4;
            $infections++;
            break;
        case 1:
            $dir = ($dir + 1) % 4;
            break;
    }

    $grid[$y][$x] = ($grid[$y][$x] + 1) % 2;

    switch ($dir) {
        case 0:
            $y--;
            break;
        case 1:
            $x++;
            break;
        case 2:
            $y++;
            break;
        case 3:
            $x--;
            break;
    }
}

fwrite(STDOUT, $infections . PHP_EOL);

$grid = [];
foreach ($lines as $line) {
    $grid[] = array_map(function ($cell) {
        return $cell == '#' ? 2 : 0;
    }, $line);
}

$y   = intval(count($grid) / 2);
$x   = intval(count($grid[$y]) / 2);
$dir = 0;

$infections = 0;

for ($burst = 10000000; $burst; $burst--) {
    $grid[$y][$x] = $grid[$y][$x] ?? 0;

    switch ($grid[$y][$x]) {
        case 0:
            $dir = ($dir + 3) % 4;
            break;
        case 1:
            $infections++;
            break;
        case 2:
            $dir = ($dir + 1) % 4;
            break;
        case 3:
            $dir = ($dir + 2) % 4;
            break;
    }

    $grid[$y][$x] = ($grid[$y][$x] + 1) % 4;

    switch ($dir) {
        case 0:
            $y--;
            break;
        case 1:
            $x++;
            break;
        case 2:
            $y++;
            break;
        case 3:
            $x--;
            break;
    }
}

fwrite(STDOUT, $infections . PHP_EOL);