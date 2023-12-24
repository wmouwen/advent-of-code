<?php

$memory = array_map('intval', explode("\t", trim(fgets(STDIN))));

$visited = [];

$steps = 0;

for ($steps = 1; true; $steps++) {
    $blocks = max($memory);
    $index = array_search($blocks, $memory);

    for ($memory[$index] = 0; $blocks > 0; $blocks--) {
        $index++;
        $memory[$index % count($memory)]++;
    }

    $hash = md5(serialize($memory));

    if (array_key_exists($hash, $visited)) {
        fwrite(STDOUT, $steps . PHP_EOL);
        fwrite(STDOUT, ($steps - $visited[$hash]) . PHP_EOL);
        break;
    }

    $visited[$hash] = $steps;
}
