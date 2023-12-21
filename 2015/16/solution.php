<?php

const COMPOUNDS = [
    'children'    => 3,
    'cats'        => 7,
    'samoyeds'    => 2,
    'pomeranians' => 3,
    'akitas'      => 0,
    'vizslas'     => 0,
    'goldfish'    => 5,
    'trees'       => 3,
    'cars'        => 2,
    'perfumes'    => 1
];

function compare(string $name, int $test, bool $corrected = false): bool
{
    if ($corrected) {
        if (in_array($name, ['cats', 'trees'])) {
            return COMPOUNDS[$name] < $test;
        }
        if (in_array($name, ['goldfish', 'pomeranians'])) {
            return COMPOUNDS[$name] > $test;
        }
    }

    return COMPOUNDS[$name] === $test;
}

$sue_one = $sue_two = null;
while (preg_match('/Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)/', fgets(STDIN), $matches)) {
    if (compare($matches[2], $matches[3])
        && compare($matches[4], $matches[5])
        && compare($matches[6], $matches[7])) {
        $sue_one = $matches[1];
    }
    if (compare($matches[2], $matches[3], true)
        && compare($matches[4], $matches[5], true)
        && compare($matches[6], $matches[7], true)) {
        $sue_two = $matches[1];
    }
}

fwrite(STDOUT, $sue_one . PHP_EOL);
fwrite(STDOUT, $sue_two . PHP_EOL);