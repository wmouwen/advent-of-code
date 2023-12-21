<?php

$input = [];
while (is_numeric($row = trim(fgets(STDIN)))) {
    $input[] = intval($row);
}

for ($instructions = $input, $cycles = $loc = 0; 0 <= $loc && $loc < count($instructions); $cycles++) {
    $loc += $instructions[$loc]++;
}
fwrite(STDOUT, $cycles . PHP_EOL);

for ($instructions = $input, $cycles = $loc = 0; 0 <= $loc && $loc < count($instructions); $cycles++) {
    $goto               = $loc + $instructions[$loc];
    $instructions[$loc] += $instructions[$loc] < 3 ? 1 : -1;
    $loc                = $goto;
}
fwrite(STDOUT, $cycles . PHP_EOL);