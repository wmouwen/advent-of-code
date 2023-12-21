<?php

$garbage = $ignore = false;
$depth   = $score = $garbage_count = 0;

foreach (str_split(trim(fgets(STDIN))) as $char) {

    // Ignore exclamation marks and the following character
    if ($ignore) {
        $ignore = false;
        continue;
    }
    if ($char == '!') {
        $ignore = true;
        continue;
    }

    // Exclude garbage
    if ($char == '>') {
        $garbage = false;
        continue;
    }
    if ($garbage) {
        $garbage_count++;
        continue;
    }
    if ($char == '<') {
        $garbage = true;
        continue;
    }

    // Track depth
    if ($char == '{') {
        $depth++;
    }
    if ($char == '}') {
        $score += $depth;
        $depth--;
    }
}

fwrite(STDOUT, $score . PHP_EOL);
fwrite(STDOUT, $garbage_count . PHP_EOL);