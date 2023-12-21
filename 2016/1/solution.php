<?php

$x   = 0;
$y   = 0;
$dir = 0;

$visited      = [[true]];
$headquarters = null;

foreach (explode(', ', trim(fgets(STDIN))) as $instruction) {
    preg_match('/(R|L)(\d+)/', $instruction, $match);

    $dir = ($dir + ($match[1] === 'R' ? 1 : 3)) % 4;

    for ($i = intval($match[2]); $i--;) {
        $x += (2 - $dir) % 2;
        $y -= (1 - $dir) % 2;

        if (is_null($headquarters) && isset($visited[$y][$x])) {
            $headquarters = [$y, $x];
        }
        
        $visited[$y][$x] = true;
    }
}

fwrite(STDOUT, abs($x) + abs($y) . PHP_EOL);
fwrite(STDOUT, array_sum(array_map('abs', $headquarters)) . PHP_EOL);
