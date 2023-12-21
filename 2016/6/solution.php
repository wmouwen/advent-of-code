<?php

$letters = [];
while ($noise = trim(fgets(STDIN))) {
    for ($i = 0; $i < strlen($noise); $i++) {
        $letters[$i][$noise[$i]] = ($letters[$i][$noise[$i]] ?? 0) + 1;
    }
}

fwrite(STDOUT, implode(array_map(function ($letter) {
        arsort($letter);
        return array_keys($letter)[0];
    }, $letters)) . PHP_EOL);

fwrite(STDOUT, implode(array_map(function ($letter) {
        asort($letter);
        return array_keys($letter)[0];
    }, $letters)) . PHP_EOL);