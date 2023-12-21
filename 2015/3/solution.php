<?php

$x              = [0, 0];
$y              = [0, 0];
$santa          = 0;
$visited_single = [[true]];
$visited_double = [[true]];

foreach (str_split(trim(fgets(STDIN))) as $move) {
    $santa = 1 - $santa;

    switch ($move) {
        case '^':
            $y[$santa]++;
            break;
        case 'v':
            $y[$santa]--;
            break;
        case '>':
            $x[$santa]++;
            break;
        case '<':
            $x[$santa]--;
            break;
    }
    
    $visited_single[array_sum($y)][array_sum($x)] = true;
    $visited_double[$y[$santa]][$x[$santa]]       = true;
}

fwrite(STDOUT, array_sum(array_map('count', $visited_single)) . PHP_EOL);
fwrite(STDOUT, array_sum(array_map('count', $visited_double)) . PHP_EOL);
