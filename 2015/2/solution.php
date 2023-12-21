<?php

$surface = $ribbon = 0;

while ($input = trim(fgets(STDIN))) {
    list($x, $y, $z) = array_map('intval', explode('x', $input));
    list($a, $b, $c) = [$x * $y, $x * $z, $y * $z];

    $surface += 2 * ($a + $b + $c) + min($a, $b, $c);
    $ribbon  += ($x * $y * $z) + 2 * ($x + $y + $z - max($x, $y, $z));
}

fwrite(STDOUT, $surface . PHP_EOL);
fwrite(STDOUT, $ribbon . PHP_EOL);