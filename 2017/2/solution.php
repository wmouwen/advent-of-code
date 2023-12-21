<?php

$part_one = $part_two = 0;

while (preg_match_all('/\d+/', fgets(STDIN), $matches)) {
    $numbers = array_map('intval', $matches[0]);
    rsort($numbers);

    $part_one += $numbers[0] - $numbers[count($numbers) - 1];

    for ($n = 0; $n + 1 < count($numbers); $n++) {
        for ($d = $n + 1; $d < count($numbers); $d++) {
            if (($numbers[$n] % $numbers[$d]) == 0) {
                $part_two += $numbers[$n] / $numbers[$d];
                break 2;
            }
        }
    }
}

fwrite(STDOUT, $part_one . PHP_EOL);
fwrite(STDOUT, $part_two . PHP_EOL);