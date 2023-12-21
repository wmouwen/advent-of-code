<?php

const FACTOR_A = 16807;
const FACTOR_B = 48271;

function generate(int &$input, int $factor, int $divisor = 1): int
{
    do {
        $input = ($input * $factor) % 0x7FFFFFFF;
    } while ($input % $divisor !== 0);

    return $input;
}

$start = [];
while (preg_match('/Generator (A|B) starts with (\d+)/', fgets(STDIN), $match)) {
    $start[ord($match[1]) - 65] = intval($match[2]);
}

$count = 0;
for (list($a, $b) = $start, $i = 40000000; $i--;) {
    if ((generate($a, FACTOR_A) & 0xFFFF) === (generate($b, FACTOR_B) & 0xFFFF)) {
        $count++;
    }
}
fwrite(STDOUT, $count . PHP_EOL);

$count = 0;
for (list($a, $b) = $start, $i = 5000000; $i--;) {
    if ((generate($a, FACTOR_A, 4) & 0xFFFF) === (generate($b, FACTOR_B, 8) & 0xFFFF)) {
        $count++;
    }
}
fwrite(STDOUT, $count . PHP_EOL);