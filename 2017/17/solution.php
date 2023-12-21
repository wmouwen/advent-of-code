<?php

const PART_ONE_ITERATIONS = 2017;
const PART_TWO_ITERATIONS = 50000000;

$speed     = intval(fgets(STDIN));
$memory    = [0];
$position  = 0;
$iteration = 1;

for (; $iteration <= PART_ONE_ITERATIONS; $iteration++) {
    $position = (($position + $speed) % $iteration) + 1;
    array_splice($memory, $position, 0, $iteration);
}

fwrite(STDOUT, $memory[(array_search(PART_ONE_ITERATIONS, $memory) + 1) % count($memory)] . PHP_EOL);

for (; $iteration <= PART_TWO_ITERATIONS; $iteration++) {
    $position = (($position + $speed) % $iteration) + 1;
    if ($position == 1) {
        $memory[1] = $iteration;
    }
}

fwrite(STDOUT, $memory[1] . PHP_EOL);
