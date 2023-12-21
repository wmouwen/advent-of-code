<?php

ini_set('memory_limit', '4G');

/** @var string[] $input */
preg_match('/^(\d+) players; last marble is worth (\d+) points$/', trim(fgets(STDIN)), $input);

/** @var int $max_marble */
$max_marble = intval($input[2]);

/** @var int[] $scores */
$scores = array_fill(0, intval($input[1]), 0);

/** @var Ds\Deque $deque */
$deque = new Ds\Deque([0]);

for ($i = 1; $i <= 100 * $max_marble; $i++) {
    if ($i % 23 === 0) {
        $deque->rotate(-7);
        $scores[$i % count($scores)] += $i + $deque->pop();
        $deque->rotate(1);
    } else {
        $deque->rotate(1);
        $deque->push($i);
    }

    if ($i === $max_marble) {
        fwrite(STDOUT, max($scores) . PHP_EOL);
    }
}

fwrite(STDOUT, max($scores) . PHP_EOL);
