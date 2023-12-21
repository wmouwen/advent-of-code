<?php

$sequence = trim(fgets(STDIN));

for ($i = 1; $i <= 50; $i++) {
    $sequence = preg_replace_callback('/(\d)\1*/', function ($match) {
        return strlen($match[0]) . $match[1];
    }, $sequence);

    if ($i === 40) {
        fwrite(STDOUT, strlen($sequence) . PHP_EOL);
    }
}

fwrite(STDOUT, strlen($sequence) . PHP_EOL);