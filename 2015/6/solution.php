<?php

$boolean_lights = [[]];
$digital_lights = [[]];

while (preg_match('/(toggle|turn (off|on)) (\d+),(\d+) through (\d+),(\d+)/', fgets(STDIN), $matches)) {
    list(, $instruction, $set_to, $x_low, $y_low, $x_high, $y_high) = $matches;

    for ($y = $y_low; $y <= $y_high; $y++) {
        for ($x = $x_low; $x <= $x_high; $x++) {
            if ($instruction === 'toggle') {
                $boolean_lights[$y][$x] = !($boolean_lights[$y][$x] ?? false);
                $digital_lights[$y][$x] = ($digital_lights[$y][$x] ?? 0) + 2;
            } elseif ($set_to === 'on') {
                $boolean_lights[$y][$x] = true;
                $digital_lights[$y][$x] = ($digital_lights[$y][$x] ?? 0) + 1;
            } else {
                $boolean_lights[$y][$x] = false;
                $digital_lights[$y][$x] = max(0, ($digital_lights[$y][$x] ?? 0) - 1);
            }
        }
    }
}

fwrite(STDOUT, array_sum(array_map('array_sum', $boolean_lights)) . PHP_EOL);
fwrite(STDOUT, array_sum(array_map('array_sum', $digital_lights)) . PHP_EOL);