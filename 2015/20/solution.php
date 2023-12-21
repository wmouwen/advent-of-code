<?php

ini_set('memory_limit', '1G');

$input = intval(fgets(STDIN));

$houses = [];

for ($elf = 1; $elf <= intval($input / 10); $elf++) {
    for ($nr = $elf; $nr <= intval($input/10); $nr += $elf) {
        $houses[$nr] = ($houses[$nr] ?? 0) + 10 * $elf;
    }
}

for ($nr = 1; $nr <= intval($input/10); $nr++) {
    if ($houses[$nr] > $input) {
        fwrite(STDOUT, $nr . PHP_EOL);
        break;
    }
}

$houses = [];

for ($elf = 1; $elf <= intval($input / 10); $elf++) {
    for ($nr = $elf; $nr <= intval($input/10) && $nr <= 50 * $elf; $nr += $elf) {
        $houses[$nr] = ($houses[$nr] ?? 0) + 11 * $elf;
    }
}

for ($nr = 1; $nr <= intval($input/10); $nr++) {
    if ($houses[$nr] > $input) {
        fwrite(STDOUT, $nr . PHP_EOL);
        break;
    }
}
