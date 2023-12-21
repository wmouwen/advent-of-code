<?php

$input = array_map('intval', explode('-', fgets(STDIN)));
$partOne = 0;
$partTwo = 0;

foreach (range ($input[0], $input[1]) as $i) {
    if (!preg_match('/^0*1*2*3*4*5*6*7*8*9*$/', $i)) {
        continue;
    }

    if (preg_match_all('/(\d)\1+/', $i, $matches, PREG_SET_ORDER)) {
        $partOne++;

        foreach ($matches as $match) {
            if (strlen(strval($match[0])) === 2) {
                $partTwo++;
                break;
            }
        }
    }
}

fwrite(STDOUT, $partOne . PHP_EOL);
fwrite(STDOUT, $partTwo . PHP_EOL);
