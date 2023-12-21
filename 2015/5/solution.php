<?php

$nice_one = $nice_two = 0;

while ($string = trim(fgets(STDIN))) {
    if (preg_match('/[aeiou]\w*?[aeiou]\w*?[aeiou]/', $string)
        && preg_match('/(\w)\1/', $string)
        && !preg_match('/(ab|cd|pq|xy)/', $string)) {
        $nice_one++;
    }

    if (preg_match('/(\w\w)\w*?\1/', $string)
        && preg_match('/(\w)\w\1/', $string)) {
        $nice_two++;
    }
}

fwrite(STDOUT, $nice_one . PHP_EOL);
fwrite(STDOUT, $nice_two . PHP_EOL);