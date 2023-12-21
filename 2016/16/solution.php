<?php

$input = trim(fgets(STDIN));

$state     = $input;
$disk_size = 272;

while (strlen($state) < $disk_size) {
    $state .= '0' . strtr(strrev($state), '01', '10');
}

$checksum = substr($state, 0, $disk_size);
do {
    $new = '';
    for ($i = 0; $i < strlen($checksum); $i += 2) {
        $new .= $checksum[$i] === $checksum[$i + 1] ? '1' : 0;
    }
    $checksum = $new;
} while ((strlen($checksum) & 1) === 0);

fwrite(STDOUT, $checksum . PHP_EOL);

$state     = $input;
$disk_size = 35651584;

while (strlen($state) < $disk_size) {
    $state .= '0' . strtr(strrev($state), '01', '10');
}

$checksum = substr($state, 0, $disk_size);
do {
    $new = '';
    for ($i = 0; $i < strlen($checksum); $i += 2) {
        $new .= $checksum[$i] === $checksum[$i + 1] ? '1' : 0;
    }
    $checksum = $new;
} while ((strlen($checksum) & 1) === 0);

fwrite(STDOUT, $checksum . PHP_EOL);