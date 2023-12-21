<?php

$escaped = $unescaped = 0;

while ($string = trim(fgets(STDIN))) {
    $characters = array_count_values(str_split($string));
    $escaped    += 2 + ($characters['"'] ?? 0) + ($characters['\\'] ?? 0);
    $unescaped  += 2 + strlen($string) - strlen(str_replace(['\\"', '\\\\'], '-', preg_replace('/\\\\x([0-9a-f]{2})/', '-', $string)));
}

fwrite(STDOUT, $unescaped . PHP_EOL);
fwrite(STDOUT, $escaped . PHP_EOL);