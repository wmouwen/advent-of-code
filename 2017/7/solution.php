<?php

$weights = $parents = $children = [];

while ($row = trim(fgets(STDIN))) {
    $args               = explode(' ', $row);
    $weights[$args[0]]  = intval(trim($args[1], '()'));
    $children[$args[0]] = [];

    for ($i = 3; $i < count($args); $i++) {
        $parents[rtrim($args[$i], ',')] = $args[0];
        $children[$args[0]][]           = rtrim($args[$i], ',');
    }
}

$part_one = reset($parents);
while (isset($parents[$part_one])) {
    $part_one = $parents[$part_one];
}
fwrite(STDOUT, $part_one . PHP_EOL);

function recursive_weight($node)
{
    global $children, $weights;

    if (!count($children[$node])) {
        return $weights[$node];
    }

    $subweights = [];
    foreach ($children[$node] as $child) {
        $subweights[$child] = recursive_weight($child);
    }

    if (count($count_values = array_count_values($subweights)) > 1) {
        $misweighed = array_search(array_search(1, $count_values), $subweights);
        fwrite(STDOUT, ($weights[$misweighed] + array_search(count($subweights) - 1, $count_values) - $subweights[$misweighed]) . PHP_EOL);
        die();
    }

    return array_sum($subweights) + $weights[$node];
}

recursive_weight($part_one);