<?php

const TYPE_LUMBERYARD = '#';
const TYPE_OPEN = '.';
const TYPE_WOODED = '|';

$area = [];

while ($row = trim(fgets(STDIN))) {
    $area[] = str_split($row);
}

function step(array $old): array
{
    $new = [];

    for ($y = 0; $y < count($old); $y++) {
        for ($x = 0; $x < count($old[$y]); $x++) {
            $lumberyards = 0;
            $woodedAcres = 0;

            for ($dy = -1; $dy <= 1; $dy++) {
                for ($dx = -1; $dx <= 1; $dx++) {
                    if ($dy === 0 && $dx === 0) {
                        continue;
                    }

                    switch ($old[$y + $dy][$x + $dx] ?? null) {
                        case TYPE_LUMBERYARD:
                            $lumberyards++;
                            break;

                        case TYPE_WOODED:
                            $woodedAcres++;
                            break;
                    }
                }
            }

            switch ($old[$y][$x]) {
                case TYPE_WOODED:
                    $new[$y][$x] = ($lumberyards >= 3) ? TYPE_LUMBERYARD : TYPE_WOODED;
                    break;

                case TYPE_LUMBERYARD:
                    $new[$y][$x] = ($lumberyards >= 1 && $woodedAcres >= 1) ? TYPE_LUMBERYARD : TYPE_OPEN;
                    break;

                case TYPE_OPEN:
                    $new[$y][$x] = ($woodedAcres >= 3) ? TYPE_WOODED : TYPE_OPEN;
                    break;
            }

        }
    }

    return $new;
}

for ($tick = 1; $tick <= 10; $tick++) {
    $area = step($area);
}

$lumberyards = 0;
$woodedAcres = 0;

foreach (array_map('array_count_values', $area) as $rowValues) {
    $lumberyards += $rowValues[TYPE_LUMBERYARD] ?? 0;
    $woodedAcres += $rowValues[TYPE_WOODED] ?? 0;
}

fwrite(STDOUT, ($lumberyards * $woodedAcres) . PHP_EOL);

// TODO Improve me by looking for cycles.

for ($tick = 11; $tick <= 1000000000; $tick++) {
    $area = step($area);

    $lumberyards = 0;
    $woodedAcres = 0;

    foreach (array_map('array_count_values', $area) as $rowValues) {
        $lumberyards += $rowValues[TYPE_LUMBERYARD] ?? 0;
        $woodedAcres += $rowValues[TYPE_WOODED] ?? 0;
    }
}

$lumberyards = 0;
$woodedAcres = 0;

foreach (array_map('array_count_values', $area) as $rowValues) {
    $lumberyards += $rowValues[TYPE_LUMBERYARD] ?? 0;
    $woodedAcres += $rowValues[TYPE_WOODED] ?? 0;
}

fwrite(STDOUT, ($lumberyards * $woodedAcres) . PHP_EOL);
