<?php

$input = "";
while ($line = fgets(STDIN)) {
    $input .= $line;
}

preg_match_all('/-?\d+/', $input, $matches);
fwrite(STDOUT, array_sum($matches[0]) . PHP_EOL);

function sum_without_red($element): int
{
    switch (gettype($element)) {
        case 'integer':
            return $element;
        case 'array':
            return array_sum(array_map(__FUNCTION__, $element));
        case 'object':
            return in_array('red', (array)$element, true) ? 0 : array_sum(array_map(__FUNCTION__, (array)$element));
        default:
            return 0;
    }
}

fwrite(STDOUT, sum_without_red(json_decode($input)) . PHP_EOL);