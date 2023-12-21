<?php

/** @var int[][] $fabric */
$fabric = [];

/** @var array[] $claims */
$claims = [];

/** @var string $box */
while (preg_match('/^#(\d+)\s@\s(\d+),(\d+):\s(\d+)x(\d+)$/', trim(fgets(STDIN)), $input)) {
    // Store the claim.
    $claim = [
        'x' => intval($input[2]),
        'y' => intval($input[3]),
        'width' => intval($input[4]),
        'height' => intval($input[5]),
    ];

    $claims[intval($input[1])] = $claim;

    // Increment amount of claims for each coordinate.
    for ($dy = 0; $dy < $claim['height']; $dy++) {
        for ($dx = 0; $dx < $claim['width']; $dx++) {
            $fabric[$claim['y'] + $dy][$claim['x'] + $dx] = ($fabric[$claim['y'] + $dy][$claim['x'] + $dx] ?? 0) + 1;
        }
    }
}

// Find amount of coordinates with more than one claim.
$overlapping = array_reduce($fabric, function ($carry, $row) {
    return $carry + array_reduce($row, function ($carry, $field) {
            return $carry + ($field > 1 ? 1 : 0);
        }, 0);
}, 0);

fwrite(STDOUT, $overlapping . PHP_EOL);

// Find first claim which doesn't overlap with any other claim.
foreach ($claims as $id => $claim) {
    for ($dy = 0; $dy < $claim['height']; $dy++) {
        for ($dx = 0; $dx < $claim['width']; $dx++) {
            if ($fabric[$claim['y'] + $dy][$claim['x'] + $dx] > 1) {
                continue 3;
            }
        }
    }

    fwrite(STDOUT, $id . PHP_EOL);
    break;
}
