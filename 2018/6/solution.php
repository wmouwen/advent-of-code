<?php

/** @var array[] $coordinates List of coordinate pairs [x, y]. */
$coordinates = [];

// Grid corners.
$minx = $miny = PHP_INT_MAX;
$maxx = $maxy = PHP_INT_MIN;

while ($row = trim(fgets(STDIN))) {
    [$x, $y] = array_map('intval', explode(',', $row));

    // Determine the size of the grid.
    $minx = min($minx, $x);
    $miny = min($miny, $y);
    $maxx = max($maxx, $x);
    $maxy = max($maxy, $y);

    $coordinates[] = [$x, $y];
}

/** @var int[][] $distances Distances to closest coordinate. */
$distances = [];

/** @var int[][] $closest ID number of closest coordinate, or -1 in case of a tie. */
$closest = [];

/** @var int[][] $sums Sum of manhattan distances to all coordinates. */
$sums = [];

/** @var int[] $areas Size of the area each coordinate covers. */
$areas = array_fill(-1, count($coordinates) + 1, 0);

/** @var int[] $infinite List of ID's for coordinates with infinite region. */
$infinite = [
    -1,
];

/** @var int $center Number of coordinates within a specified combined distance to all coordinates. */
$center = 0;

// Fill $distances, $closest and $sums.
for ($y = $miny; $y <= $maxy; $y++) {
    for ($x = $minx; $x <= $maxx; $x++) {
        $distances[$y][$x] = PHP_INT_MAX;
        $area = -1;
        $sums[$y][$x] = 0;

        foreach ($coordinates as $id => $coordinate) {
            $manhattan = abs($x - $coordinate[0]) + abs($y - $coordinate[1]);
            $sums[$y][$x] += $manhattan;

            if ($manhattan < $distances[$y][$x]) {
                $distances[$y][$x] = $manhattan;
                $area = $id;
            } elseif ($manhattan === $distances[$y][$x]) {
                $area = -1;
            }
        }

        $closest[$y][$x] = $area;
        $areas[$area]++;

        if ($x === $minx || $x === $maxx || $y === $miny || $y === $maxy) {
            $infinite[] = $area;
        }

        if ($sums[$y][$x] < 10000) {
            $center++;
        }
    }
}

// Exclude ties as an area.
foreach (array_unique($infinite) as $area) {
    unset($areas[$area]);
}

fwrite(STDOUT, max($areas) . PHP_EOL);
fwrite(STDOUT, $center . PHP_EOL);
