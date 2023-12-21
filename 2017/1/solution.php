<?php

$input = trim(fgets(STDIN));

for ($part_one = $part_two = $i = 0; $i < strlen($input); $i++) {
    $part_one += ($input[$i] == $input[($i + 1) % strlen($input)]) ? $input[$i] : 0;
    $part_two += ($input[$i] == $input[($i + (strlen($input) / 2)) % strlen($input)]) ? $input[$i] : 0;
}

fwrite(STDOUT, $part_one . PHP_EOL);
fwrite(STDOUT, $part_two . PHP_EOL);