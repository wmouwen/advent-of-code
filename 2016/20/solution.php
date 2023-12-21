<?php

$blacklist = [];
while (preg_match('/(\d+)-(\d+)/', fgets(STDIN), $range)) {
    $blacklist[] = $range;
}

$valid  = 0;
$lowest = null;

for ($i = 0; $i <= 0xFFFFFFFF; $i++) {
    foreach ($blacklist as $range) {
        if ($range[1] <= $i && $i <= $range[2]) {
            $i = $range[2];
            continue 2;
        }
    }

    $valid++;

    if (is_null($lowest)) {
        $lowest = $i;
        fwrite(STDOUT, $lowest . PHP_EOL);
    }
}

fwrite(STDOUT, $valid . PHP_EOL);