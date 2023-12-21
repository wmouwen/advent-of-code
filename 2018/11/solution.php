<?php

const GRID_SIZE = 300;

$input = intval(fgets(STDIN));
$partials = [];

for ($y = 1; $y <= GRID_SIZE; $y++) {
    for ($x = 1; $x <= GRID_SIZE; $x++) {
        $power = (intval((($x + 10) * $y + $input) * ($x + 10) / 100) % 10) - 5;

        $partials[$y][$x] = $power
            + ($partials[$y - 1][$x] ?? 0)
            + ($partials[$y][$x - 1] ?? 0)
            - ($partials[$y - 1][$x - 1] ?? 0);
    }
}

function bestPowerLocation(array &$partial, int $minSize, int $maxSize = null): string
{
    $bestPower = PHP_INT_MIN;
    $bestX = null;
    $bestY = null;
    $bestSize = null;

    for ($size = $minSize; $size <= ($maxSize ?? $minSize); $size++) {
        for ($y = $size; $y <= GRID_SIZE; $y++) {
            for ($x = $size; $x <= GRID_SIZE; $x++) {
                $power = $partial[$y][$x]
                    - ($partial[$y - $size][$x] ?? 0)
                    - ($partial[$y][$x - $size] ?? 0)
                    + ($partial[$y - $size][$x - $size] ?? 0);

                if ($power > $bestPower) {
                    $bestPower = $power;
                    $bestX = $x - $size + 1;
                    $bestY = $y - $size + 1;
                    $bestSize = $size;
                }
            }
        }
    }

    return $maxSize === null
        ? sprintf('%d,%d', $bestX, $bestY)
        : sprintf('%d,%d,%d', $bestX, $bestY, $bestSize);
}

fwrite(STDOUT, bestPowerLocation($partials, 3) . PHP_EOL);
fwrite(STDOUT, bestPowerLocation($partials, 1, GRID_SIZE) . PHP_EOL);
