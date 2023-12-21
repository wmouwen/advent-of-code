<?php

$containers = [];
while ($container = intval(fgets(STDIN))) {
    $containers[] = $container;
}

function combinations(array &$elements, int $depth = 0, int $remaining = 150): int
{
    if ($depth === count($elements) || $remaining < 0) {
        return $remaining === 0 ? 1 : 0;
    }

    return combinations($elements, $depth + 1, $remaining)
        + combinations($elements, $depth + 1, $remaining - $elements[$depth]);
}

function small_combinations(array &$elements, int $depth = 0, int $remaining = 150, int $used = 0): ?array
{
    $result = [PHP_INT_MAX, 0];

    if ($depth === count($elements) || $remaining < 0) {
        return $remaining === 0 ? [$used, 1] : $result;
    }

    foreach ([
                 small_combinations($elements, $depth + 1, $remaining, $used),
                 small_combinations($elements, $depth + 1, $remaining - $elements[$depth], $used + 1)
             ] as $try) {
        if ($try[0] < $result[0]) {
            $result = $try;
        } elseif ($try[0] == $result[0]) {
            $result[1] += $try[1];
        }
    }

    return $result;
}

fwrite(STDOUT, combinations($containers) . PHP_EOL);
fwrite(STDOUT, small_combinations($containers)[1] . PHP_EOL);