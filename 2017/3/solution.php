<?php

$part_one = 0;
$part_two = 0;
$input    = intval(fgets(STDIN));
$grid     = [[1]];

$x = $dy = 1;
$y = $dx = 0;

for ($i = 2; $i < $input; $i++) {
    $sum = 0;
    for ($rx = -1; $rx <= 1; $rx++) {
        for ($ry = -1; $ry <= 1; $ry++) {
            if (isset($grid[$x + $rx]) && isset($grid[$x + $rx][$y + $ry])) {
                $sum += $grid[$x + $rx][$y + $ry];
            }
        }
    }

    $part_two     = $part_two === 0 && $sum > $input ? $sum : $part_two;
    $grid[$x][$y] = $sum;
    $x            += $dx;
    $y            += $dy;

    $new_dx = ($dx === 0 ? -$dy : 0);
    $new_dy = ($dy === 0 ? $dx : 0);
    if (!isset($grid[$x + $new_dx]) || !isset($grid[$x + $new_dx][$y + $new_dy])) {
        $dx = $new_dx;
        $dy = $new_dy;
    }
}

fwrite(STDOUT, abs($x) + abs($y) . PHP_EOL);
fwrite(STDOUT, $part_two . PHP_EOL);