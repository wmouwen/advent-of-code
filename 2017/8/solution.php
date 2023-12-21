<?php

$result    = 0;
$part_two  = 0;
$registers = [];

while ($row = trim(fgets(STDIN))) {
    list($reg_work, $action, $delta, , $reg_test, $comperator, $comp_value) = explode(' ', $row);

    eval('$result = ' . ($registers[$reg_test] ?? 0) . ' ' . $comperator . ' ' . $comp_value . ';');

    $registers[$reg_work] = ($registers[$reg_work] ?? 0) + intval($result) * ($action == 'inc' ? 1 : -1) * $delta;

    $part_two = max($part_two, max($registers));
}

fwrite(STDOUT, max($registers) . PHP_EOL);
fwrite(STDOUT, $part_two . PHP_EOL);