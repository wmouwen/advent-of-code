<?php

ini_set('memory_limit', '1G');

$elves = intval(fgets(STDIN));

$circle = new Ds\Deque(range(1, $elves));

while ($circle->count() > 1) {
    $circle->rotate(1);
    $circle->shift();
}

fwrite(STDOUT, $circle->first() . PHP_EOL);

$circle = new Ds\Deque(range(1, $elves));

$circle->rotate(intval($circle->count() / 2));

while ($circle->count() > 1) {
    $circle->shift();
    $circle->rotate($circle->count() % 2 === 1 ? 0 : 1);
}

fwrite(STDOUT, $circle->first() . PHP_EOL);
