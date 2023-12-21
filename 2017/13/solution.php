<?php

while ($firewall = trim(fgets(STDIN))) {
    list($depth, $range) = explode(': ', $firewall);
    $severity = ($severity ?? 0) + ($depth % (2 * ($layers[$depth] = $range) - 2) ? 0 : $depth * $range);
}
fwrite(STDOUT, $severity . PHP_EOL);

for ($delay = 0; ; $delay++) {
    foreach ($layers as $depth => $range) {
        if (!(($depth + $delay) % (2 * $range - 2))) {
            continue 2;
        }
    }
    break;
}
fwrite(STDOUT, $delay . PHP_EOL);