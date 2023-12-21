<?php

$memory = array_map('intval', explode("\t", trim(fgets(STDIN))));

$visited = new Ds\Map;

$steps = 0;

for ($steps = 1; true; $steps++) {
    $blocks = max($memory);
    $index = array_search($blocks, $memory);

    for ($memory[$index] = 0; $blocks > 0; $blocks--) {
        $index++;
        $memory[$index % count($memory)]++;
    }

    if ($visited->hasKey($memory)) {
        fwrite(STDOUT, $steps . PHP_EOL);
        fwrite(STDOUT, ($steps - $visited->get($memory)) . PHP_EOL);
        break;
    }

    $visited->put($memory, $steps);
}
