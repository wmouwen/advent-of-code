<?php

$valid_one = $valid_two = 0;

while ($phrase = trim(fgets(STDIN))) {
    $words     = explode(' ', $phrase);
    $valid_one += count($words) == count(array_unique($words)) ? 1 : 0;

    $words = array_map(function ($word) {
        $word = str_split($word);
        sort($word);

        return implode($word);
    }, $words);

    $valid_two += count($words) == count(array_unique($words)) ? 1 : 0;
}

fwrite(STDOUT, $valid_one . PHP_EOL);
fwrite(STDOUT, $valid_two . PHP_EOL);