<?php

$input = trim(fgets(STDIN));

$counts = array_count_values(str_split($input));

fwrite(STDOUT, $counts['('] - $counts[')'] . PHP_EOL);

for ($elevator = $floor = 0; $floor !== -1; $elevator++) {
    $floor += $input[$elevator] === '(' ? 1 : -1;
}

fwrite(STDOUT, $elevator . PHP_EOL);
