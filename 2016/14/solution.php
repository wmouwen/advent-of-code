<?php

$salt = trim(fgets(STDIN));

$keys     = [];
$triplets = [];

for ($i = 0; $i < ($keys[63] ?? $i) + 1000; $i++) {
    $md5 = md5($salt . $i);

    foreach ($triplets as $t => list($index, $char)) {
        if (strpos($md5, $char . $char . $char . $char . $char) !== false) {
            $keys[] = $index;
            unset($triplets[$t]);
        }
        if ($i - $index >= 1000) {
            unset($triplets[$t]);
        }
    }

    if (preg_match('/(\w)\1\1/', $md5, $match)) {
        $triplets[] = [$i, $match[1]];
    }
}

fwrite(STDOUT, $keys[63] . PHP_EOL);

$keys     = [];
$triplets = [];

for ($i = 0; $i < ($keys[63] ?? $i) + 1000; $i++) {
    $md5 = md5($salt . $i);
    for ($s = 0; $s < 2016; $s++) {
        $md5 = md5($md5);
    }

    foreach ($triplets as $t => list($index, $char)) {
        if (strpos($md5, $char . $char . $char . $char . $char) !== false) {
            $keys[] = $index;
            unset($triplets[$t]);
        }
        if ($i - $index >= 1000) {
            unset($triplets[$t]);
        }
    }

    if (preg_match('/(\w)\1\1/', $md5, $match)) {
        $triplets[] = [$i, $match[1]];
    }
}

fwrite(STDOUT, $keys[63] . PHP_EOL);