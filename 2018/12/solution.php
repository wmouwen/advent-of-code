<?php

preg_match('/^initial state:\s(.*?)$/', trim(fgets(STDIN)), $input);
$state = str_split($input[1]);

// Catch blank line.
fgets(STDIN);

$rules = new Ds\Map;
while (preg_match('/^(.*?)\s=>\s(.*?)$/', trim(fgets(STDIN)), $input)) {
    $rules->put(str_split($input[1]), $input[2]);
}

function evolve(array &$state, Ds\Map &$rules)
{
    $oldKeys = array_keys($state);
    $new = [];

    for ($x = min($oldKeys) - 2; $x <= max($oldKeys) + 2; $x++) {
        $key = [];
        for ($dx = -2; $dx <= 2; $dx++) {
            $key[] = $state[$x + $dx] ?? '.';
        }
        $new[$x] = $rules->get($key);
    }

    return $new;
}

function result(array &$state): int
{
    $sum = 0;

    foreach ($state as $key => $value) {
        if ($value === '#') {
            $sum += $key;
        }
    }

    return $sum;

}

for ($i = 0; $i < 20; $i++) {
    $state = evolve($state, $rules);
}

fwrite(STDOUT, result($state) . PHP_EOL);

$previous = $current = 0;
for ($i = 0; $i < 280; $i++) {
    $state = evolve($state, $rules);
    $previous = $current;
    $current = result($state);
}

$result = $current + (50000000000 - 300) * ($current - $previous);

fwrite(STDOUT, $result . PHP_EOL);
