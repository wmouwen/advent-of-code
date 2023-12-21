<?php

function decompressed_length(string $string, bool $recursive = true): int
{
    $length = 0;

    for ($position = 0; $position < strlen($string); $position++) {
        if (preg_match('/^\((\d+)x(\d+)\)/', substr($string, $position), $match)) {
            list($marker, $characters, $repetition) = $match;
            $substring = substr($string, $position + strlen($marker), $characters);
            $length    += ($recursive ? decompressed_length($substring) : $characters) * $repetition;
            $position  += strlen($marker) + $characters - 1;
        } else {
            $length++;
        }
    }

    return $length;
}

$string = trim(fgets(STDIN));
fwrite(STDOUT, decompressed_length($string, false) . PHP_EOL);
fwrite(STDOUT, decompressed_length($string) . PHP_EOL);