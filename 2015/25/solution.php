<?php

preg_match_all('/\d+/', fgets(STDIN), $matches);
list($row, $col) = $matches[0];
$find = ($col + 1) * $col / 2 + ($row <= 1 ? 0 : ((($col + $row - 2) + $col) * ($row - 1) / 2));
$num  = 20151125;

for ($i = 1; $i < $find; $i++) {
    $num = ($num * 252533) % 33554393;
}

fwrite(STDOUT, $num . PHP_EOL);
